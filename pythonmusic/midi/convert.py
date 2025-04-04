from functools import reduce
from math import floor

from pythonmusic.constants import PPQ
from pythonmusic.constants.articulations import (
    ACCENT,
    LEGATO,
    MARCATO,
    PORTATO,
    STACCATISSIMO,
    STACCATO,
    TENUTO,
)
from pythonmusic.constants.control_change import BANK_CHANGE, CHANNEL_PAN
from pythonmusic.constants.panning import PAN_CENTER
from pythonmusic.midi.message import Message
from pythonmusic.music import Chord, Note, Part, Phrase, PhraseElement, Score
from pythonmusic.util import beats_to_ticks, instrument_get_patch_bank

__all__ = [
    "pe_to_midi",
    "phrase_to_midi",
    "part_to_midi",
    "score_to_midi",
    "initial_part_messages",
]


def merge_messages(list_a: list[Message], list_b: list[Message]) -> list[Message]:
    """
    Merges two lists of messages recalculating their timing.
    """

    # This is a working, but terrible solution
    def _make_common_offset(l: list[Message]):
        accumulator = 0
        for index in range(len(l)):
            l[index].time += accumulator
            accumulator = l[index].time

    def _make_relative_offset(l: list[Message]):
        accumulator = 0
        for index in range(len(l)):
            l[index].time -= accumulator
            accumulator += l[index].time

    a = list_a.copy()
    b = list_b.copy()

    _make_common_offset(a)
    _make_common_offset(b)

    output = a + b
    output.sort(key=lambda m: m.time)
    _make_relative_offset(output)

    return output


def insert_message(message_list: list[Message], message: Message):
    """
    Inserts a message into the given list.

    This functionality requires a separate function (as opposed to simply
    appending), because the `time` attribute of midi messages may be, at this
    stage, negative. This can occur if the preceding note has the legato
    attribute which shifts its note off event after the note on event of the
    message to be added. This function aims to resolve this.

    `message` is mutated in this function. The `time` attribute may change. Do
    not use the original object afterwards. Create a copy, if needed.

    Args:
        message_list(list[Message]): A list of midi messages
        message(Message): A new message
    """
    # if time is positive, append
    if message.time >= 0:
        message_list.append(message)
        return

    # edge case: The first message given is empty. Should not happen *shrug*
    if len(message_list) == 0:
        message.time = 0
        message_list.append(message)
        return

    # if time is negative, resolve into previous messages
    index = len(message_list)
    while message.time < 0:
        index -= 1
        message.time += message_list[index].time

    # We only need to update the time attribute of the message to be added and
    # the message that is moved. All times are relative
    message.time = message.time
    message_list[index].time -= message.time
    message_list.insert(index, message)


def pe_to_midi(
    pe: PhraseElement,
    channel: int,
    offset: int,
) -> tuple[list[Message], int]:
    """
    Converts a phrase element to midi message.

    This function also returns the time frame the midi message should occupy in
    ticks. Due to articulations the sounding length of a note may be
    different than the note's logical length.

    Args:
        pe(PhraseElement): A note or chord
        channel(int): The channel to play on
        offset(int): Defines the inital offset in ticks of the first note. This
            sets the time parameter. If you convert a note or chord on its own,
            this value should be set to 0

    Returns:
        tuple[list[Message], int]: A tuple containing the list of converted midi
            messages and the time the messages occupy in ticks
    """

    def _note_to_midi(
        note: Note,
        channel: int,
        offset: int,
    ) -> tuple[list[Message], int]:
        # delta between note on and off is not note.duration (see below), so
        # frame describes the time these two messages should block until the
        # next message can start
        frame = beats_to_ticks(note.duration, PPQ)

        if note.is_rest():
            return ([], frame + offset)

        # Duration
        duration: float = note.duration
        if note.has_articulation(TENUTO):
            pass  # duration is unchanged, all else is ignored
        elif note.has_articulation(PORTATO):
            duration *= 0.95
        elif note.has_articulation(STACCATISSIMO):
            duration *= 0.25
        elif note.has_articulation(STACCATO):
            duration *= 0.5
        elif note.has_articulation(LEGATO):
            # FIXME: shoul be at 1.05, but this breaks midi messages
            # check why this is, algorithm for inserting may be wrong
            duration *= 1.0
        else:
            duration *= 0.90

        tick_duration = beats_to_ticks(duration, PPQ)

        # Velocity
        velocity: int = note.dynamic
        if note.has_articulation(MARCATO):
            velocity = floor(velocity * 1.50)
        elif note.has_articulation(ACCENT):
            velocity = floor(velocity * 1.25)
        else:
            pass

        # velocity is capped to 127
        velocity = min(127, velocity)

        assert frame >= 0

        return (
            [
                Message.new_note_on(channel, note.pitch, note.dynamic, offset),
                Message.new_note_off(channel, note.pitch, note.dynamic, tick_duration),
            ],
            frame,
        )

    def _chord_to_midi(
        chord: Chord,
        channel: int,
        offset: int,
    ) -> tuple[list[Message], int]:
        converted_messages: list[Message] = []
        frame: int = 0

        for note in chord.flatten():
            note_messages, note_frame = _note_to_midi(note, channel, 0)

            assert len(note_messages) & 0x1 != 0x1

            frame = max(note_frame, frame)
            converted_messages += note_messages

        # if rest or empty
        if len(converted_messages) == 0:
            return [], frame

        converted_messages.reverse()

        messages: list[Message] = []
        while len(converted_messages) > 0:
            pair = [converted_messages.pop(), converted_messages.pop()]  # on, off
            messages = merge_messages(messages, pair)

        # set offset for first note on message
        messages[0].time = offset

        assert frame >= 0
        return messages, frame

    if isinstance(pe, Note):
        return _note_to_midi(pe, channel, offset)
    if isinstance(pe, Chord):
        return _chord_to_midi(pe, channel, offset)

    raise TypeError("Unknown PhraseElement")


def phrase_to_midi(
    phrase: Phrase,
    channel: int,
    offset: int,
) -> tuple[list[Message], int]:
    """
    Converts a phrase to midi messages.

    This function also returns the time frame the midi message should occupy in
    ticks. Due to articulations the sounding length of a note may be
    different than the note's logical length.

    Args:
        phrase(Phrase): A phrase
        channel(int): The channel to play on
        offset(int): Defines the inital offset in ticks of the first note. This
            sets the time parameter. If you convert a note or chord on its own,
            this value should be set to 0

    Returns:
        tuple[list[Message], int]: A tuple containing the list of converted midi
            messages and the time the messages occupy in ticks

    """
    frame = 0
    messages: list[Message] = []

    for element in phrase.notes:
        element_messages, element_frame = pe_to_midi(element, channel, offset)
        frame += element_frame
        offset = element_frame - (
            reduce(lambda prev, message: prev + message.time, element_messages, 0)
            - element_messages[0].time
            if len(element_messages) > 0
            else 0
        )

        # messages += element_messages
        for message in element_messages:
            insert_message(messages, message)

    return messages, frame


def initial_part_messages(part) -> list[Message]:
    patch, bank = instrument_get_patch_bank(part.instrument)
    return [
        Message.new_program_change(part.channel, patch, 0),
        Message.new_control_change(part.channel, BANK_CHANGE, bank, 0),
        Message.new_control_change(part.channel, CHANNEL_PAN, PAN_CENTER, 0),
    ]


def part_to_midi(part: Part, start_at: int) -> list[Message]:
    """
    Converts a part to a track.

    This function also returns the time frame the midi message should occupy in
    ticks. Due to articulations the sounding length of a note may be
    different than the note's logical length.

    Args:
        phrase(Part): A part
        start_at(bool): Start time in ticks

    Returns:
        Track: A track containing the converted notes
    """
    note_messages: list[Message] = []

    for start_time, phrase in part.phrases_with_start_times():
        phrase_messages, _ = phrase_to_midi(
            phrase,
            part.channel,
            beats_to_ticks(start_time, PPQ),
        )
        note_messages = merge_messages(note_messages, phrase_messages)

    if start_at > 0:
        # this is slow, too bad
        note_messages.reverse()

        # prune all messages before start_at
        accumulator = 0
        while True:
            if len(note_messages) == 0:
                return []

            removed = note_messages.pop()

            if removed.time + accumulator >= start_at:
                removed.time += accumulator - start_at
                note_messages.append(removed)
                break

            accumulator += removed.time

        note_messages.reverse()

    messages = initial_part_messages(part)
    messages.extend(note_messages)
    return messages


def score_to_midi(score: Score, start_at: int) -> list[list[Message]]:
    """
    Converts a score to lists of messages.

    Args:
        score(Score): A score
        start_at(int): Tick to start on

    Returns:
        list[list[Message]]: A list of message lists that represent each part
    """
    return list(map(lambda part: part_to_midi(part, start_at), score.parts))
