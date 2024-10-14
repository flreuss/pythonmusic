from typing import Callable
from abc import ABC, abstractmethod
from time import sleep
from typing import Optional, override, cast
from time import time

from pythonmusic.constants import (
    ACOUSTIC_GRAND_PIANO,
    PAN_CENTER,
    MODERATO,
    CONTROL_CHANGE,
    PROGRAM_CHANGE,
    ADAGIO,
    NOTE_ON,
    NOTE_OFF,
    BANK_CHANGE,
)
from pythonmusic.music import Note, Chord, Phrase, Part, Score, PhraseElement
from pythonmusic.io import MidiMessage, MidiSender
from pythonmusic.io.ir import (
    IrNote,
    IrControlChange,
    IrProgramChange,
    pe_to_ir,
    phrase_to_ir,
    part_to_ir,
    score_to_ir,
    IrNode,
    make_panning_node,
    make_instrument_node,
)
from pythonmusic.io.ir.midi import irnodes_to_midi, irchannel_to_midi, irfile_to_midi
from pythonmusic.util import instrument_get_patch_bank

__all__ = ["Player", "MidiPlayer"]


def _calculate_start_time(beat: int, tempo: float) -> float:
    """
    Calculates the time offset of a beat (in quarter notes) in the given tempo.
    """
    return float(60 * beat) / tempo


class Player(ABC):
    """
    An abstract class that is used to implement player objects.
    """

    def __init__(self) -> None:
        pass

    def play_note(
        self,
        note: Note,
        on_start: Callable[[list[MidiMessage]], None] | None = None,
        on_message: Callable[[MidiMessage, float], None] | None = None,
        on_end: Callable[[bool], None] | None = None,
    ):
        """
        Plays a single note on the attached midi target.

        Args:
            note (Note): A note
            on_start (Callable[[list[MidiMessage]], None] | None): A callback that is called before playback starts
            on_message (Callable[[MidiMessage, float], None] | None): A callback that is called for every message, before it plays
            on_end (Callable[[bool], None] | None): A callback that is called after the last note played.
                If the playback finishes normally, the passed bool will be ``True``. If the playback loop receives a ``KeyboardInterrupt``
                before then, the passed boolean is ``False``.
        """
        self._play_pe(note, ADAGIO, 0, on_start, on_message, on_end)

    def play_chord(
        self,
        chord: Chord,
        on_start: Callable[[list[MidiMessage]], None] | None = None,
        on_message: Callable[[MidiMessage, float], None] | None = None,
        on_end: Callable[[bool], None] | None = None,
    ):
        """
        Plays a chord on the attached midi target.

        Args:
            chord (Chord): A chord
            on_start (Callable[[list[MidiMessage]], None] | None): A callback that is called before playback starts
            on_message (Callable[[MidiMessage, float], None] | None): A callback that is called for every message, before it plays
            on_end (Callable[[bool], None] | None): A callback that is called after the last note played.
                If the playback finishes normally, the passed bool will be ``True``. If the playback loop receives a ``KeyboardInterrupt``
                before then, the passed boolean is ``False``.
        """
        self._play_pe(chord, ADAGIO, 0, on_start, on_message, on_end)

    def play_phrase(
        self,
        phrase: Phrase,
        tempo: float = ADAGIO,
        channel: int = 0,
        on_start: Callable[[list[MidiMessage]], None] | None = None,
        on_message: Callable[[MidiMessage, float], None] | None = None,
        on_end: Callable[[bool], None] | None = None,
    ):
        """
        Plays a phrase on the attached midi target.

        Args:
            phrase (Phrase): A phrase
            tempo (float): The playback tempo in bpm
            channel (int): The channel to play on
            on_start (Callable[[list[MidiMessage]], None] | None): A callback that is called before playback starts
            on_message (Callable[[MidiMessage, float], None] | None): A callback that is called for every message, before it plays
            on_end (Callable[[bool], None] | None): A callback that is called after the last note played.
                If the playback finishes normally, the passed bool will be ``True``. If the playback loop receives a ``KeyboardInterrupt``
                before then, the passed boolean is ``False``.
        """
        ir = phrase_to_ir(phrase, start_time=0.0)
        messages = irnodes_to_midi(ir, tempo, channel)
        self._play_messages(messages, 0.0, on_start, on_message, on_end)

    def play_part(
        self,
        part: Part,
        tempo: float = ADAGIO,
        start_beat: int = 0,
        on_start: Callable[[list[MidiMessage]], None] | None = None,
        on_message: Callable[[MidiMessage, float], None] | None = None,
        on_end: Callable[[bool], None] | None = None,
    ):
        """
        Plays a part on the attached midi target.

        Args:
            part (Part): A part
            tempo (float): The playback tempo in bpm
            on_start (Callable[[list[MidiMessage]], None] | None): A callback that is called before playback starts
            on_message (Callable[[MidiMessage, float], None] | None): A callback that is called for every message, before it plays
            on_end (Callable[[bool], None] | None): A callback that is called after the last note played.
                If the playback finishes normally, the passed bool will be ``True``. If the playback loop receives a ``KeyboardInterrupt``
                before then, the passed boolean is ``False``.
        """
        ir = part_to_ir(part)
        messages = irchannel_to_midi(ir, tempo)
        self._play_messages(
            messages,
            _calculate_start_time(start_beat, tempo),
            on_start,
            on_message,
            on_end,
        )

    def play_score(
        self,
        score: Score,
        start_beat: int = 0,
        on_start: Callable[[list[MidiMessage]], None] | None = None,
        on_message: Callable[[MidiMessage, float], None] | None = None,
        on_end: Callable[[bool], None] | None = None,
    ):
        """
        Plays a score on the attached midi target.

        Args:
            score (Score): A score
            on_start (Callable[[list[MidiMessage]], None] | None): A callback that is called before playback starts
            on_message (Callable[[MidiMessage, float], None] | None): A callback that is called for every message, before it plays
            on_end (Callable[[bool], None] | None): A callback that is called after the last note played.
                If the playback finishes normally, the passed bool will be ``True``. If the playback loop receives a ``KeyboardInterrupt``
                before then, the passed boolean is ``False``.
        """
        ir = score_to_ir(score)
        messages = irfile_to_midi(ir)
        self._play_messages(
            messages,
            _calculate_start_time(start_beat, score.tempo),
            on_start,
            on_message,
            on_end,
        )

    def _play_pe(
        self,
        pe: PhraseElement,
        tempo: float,
        channel: int,
        on_start: Callable[[list[MidiMessage]], None] | None,
        on_message: Callable[[MidiMessage, float], None] | None,
        on_end: Callable[[bool], None] | None,
    ):
        ir = pe_to_ir(pe, start_time=0.0)
        messages = irnodes_to_midi(ir, tempo, channel)
        self._play_messages(messages, 0.0, on_start, on_message, on_end)

    @abstractmethod
    def play_message(self, message: MidiMessage): ...

    def set_instrument(self, channel: int, instrument: int):
        """
        A method that should update the instrument for the player.

        By default, this does nothing.

        Args:
            channel (int): The channel for which to change the instrument for
            instrument (int): The new instrument
        """
        # keep the type checker happy
        _ = channel
        _ = instrument

    def _play_messages(
        self,
        messages: list[MidiMessage],
        start_at: float,
        on_start: Callable[[list[MidiMessage]], None] | None,
        on_message: Callable[[MidiMessage, float], None] | None,
        on_end: Callable[[bool], None] | None,
    ):
        # return if no messages given
        if len(messages) == 0:
            return

        # sort in descending order for fast pop, making this, essentially, a
        # stack
        messages.sort(key=lambda message: message.time, reverse=True)

        # remove messages that occur before start time
        start_time: float = start_at

        index = len(messages) - 1
        while index < len(messages) and index >= 0:
            message = messages[index]

            # if message starts before the start time and is a 0x09 or 0x08
            # event, pop from stack
            if message.time < start_time:
                # this conditional needs to be split to allow for optimisation
                # below (not checking ever message)
                message_type = message.type
                if message_type == NOTE_ON or message_type == NOTE_OFF:
                    del messages[index]
                else:
                    index -= 1
            else:
                break

        # return if no messages left
        if len(messages) == 0:
            return

        if on_start:
            on_start(messages)

        current: MidiMessage
        next: MidiMessage = messages.pop()  # we at least one

        try:
            while True:
                current = next

                if on_message:
                    on_message(current, start_time)

                self.play_message(current)

                if len(messages) > 0:
                    next = messages.pop()
                    start_time += current.time
                    # protect against negative sleep time
                    # this should not happen, but float imprecision may cause this maybe
                    sleep_time = max(0, next.time - current.time)
                    sleep(sleep_time)
                else:
                    break

            if on_end:
                on_end(True)
        except KeyboardInterrupt:
            if on_end:
                on_end(False)


class MidiPlayer(Player):
    """
    An implementation of a player that attaches to a midi receiver and plays
    Note, Chords, Phrases etc.

    Args:
        target (str): The output port to attach to
    """

    def __init__(self, target: str) -> None:
        super().__init__()
        self.target: str = target
        self.sender: MidiSender = MidiPlayer._attach_to_receiver(target)

    @staticmethod
    def _attach_to_receiver(name: str) -> MidiSender:
        try:
            return MidiSender.attach(name)
        except OSError as error:
            print("Unable to create sender. Is your port correct?")
            raise error

    @override
    def play_message(self, message: MidiMessage):
        """
        Plays the given midi message.

        Args:
            message (MidiMessage): A MidiMessage
        """
        self.sender.send_message(message)

    @override
    def set_instrument(self, channel: int, instrument: int):
        """
        Updates the selected instrument for a given channel.

        Sends both a program and bank change to the attached midi receiver.

        .. note:: Depends on the ``play_message()`` method.

        Args:
            channel (int): A channel for which to change the instrument for
            instrument (int): The id of the new instrument
        """
        patch, bank = instrument_get_patch_bank(instrument)
        program_change = MidiMessage(PROGRAM_CHANGE, channel=channel, program=patch)
        bank_change = MidiMessage(
            CONTROL_CHANGE, channel=channel, control=BANK_CHANGE, value=bank
        )

        self.play_message(program_change)
        self.play_message(bank_change)
