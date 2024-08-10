from typing import cast
from pythonmusic.music import Note, Chord, PhraseElement, Phrase, Part, Score
from pythonmusic.constants.messages import NOTE_ON, NOTE_OFF
from pythonmusic.io import MidiMessage

NoteDescriptor = tuple[MidiMessage, MidiMessage]
"""A tuple containing a note's start and end message."""


def phrase_element_to_messages(
    element: PhraseElement, channel: int, start_time: float
) -> list[NoteDescriptor]:
    """
    Converts a phrase element into a list of midi messages.

    If the given element is a note, the return list has only one element. Chords
    return all their contents flattened.
    """
    if isinstance(element, Note):
        # TODO: articulations
        note = cast(Note, element)
        return [
            (
                # ON
                MidiMessage(
                    NOTE_ON,
                    channel=channel,
                    note=note.pitch,
                    velocity=note.dynamic,
                    time=start_time,
                ),
                # OFF
                MidiMessage(
                    NOTE_OFF,
                    channel=channel,
                    note=note.pitch,
                    velocity=note.dynamic,
                    time=start_time + note.duration,
                ),
            )
        ]

    if isinstance(element, Chord):
        chord = cast(Chord, element)
        output: list[NoteDescriptor] = []

        # need to iterate because chord may (but should not) contain chords
        for element in chord.notes:
            output += phrase_element_to_messages(element, channel, start_time)

        return output

    raise TypeError("Unknown type")


def phrase_to_messages(
    phrase: Phrase, channel: int, start_time: float
) -> list[NoteDescriptor]:
    """
    Converts a phrase to a list of midi messages.
    """
    output: list[NoteDescriptor] = []
    time_accumulator: float = start_time
    for element in phrase.notes:
        output += phrase_element_to_messages(element, channel, time_accumulator)
        time_accumulator += element.duration

    return output


def part_to_messages(part: Part) -> list[NoteDescriptor]:
    """
    Converts a part to a list of midi messages.
    """
    output: list[NoteDescriptor] = [
        MidiMessage("instrument change", instrument=part.instrument)
    ]
    time_accumulator: float = 0
    for phrase in part.phrases:
        output += phrase_to_messages(
            phrase,
            part.channel,
        )


def score_to_messages(score: Score):
    pass
