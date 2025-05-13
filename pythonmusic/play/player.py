from typing import Optional, Callable
from abc import ABC, abstractmethod
from time import sleep

from pythonmusic.music import PhraseElement, Note, Chord, Phrase, Part, Score
from pythonmusic.io import MidiMessage
from pythonmusic.constants import ADAGIO, NOTE_ON, NOTE_OFF
from pythonmusic.io.ir import (
    phrase_to_ir,
    part_to_ir,
    score_to_ir,
    pe_to_ir,
)
from pythonmusic.io.ir.midi import irnodes_to_midi, irchannel_to_midi, irfile_to_midi

__all__ = ["Player"]


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
        on_start: Optional[Callable[[list[MidiMessage]], None]] = None,
        on_message: Optional[Callable[[MidiMessage, float], None]] = None,
        on_end: Optional[Callable[[bool], None]] = None,
    ):
        """
        Plays a single note on the attached midi target.

        Args:
            note (Note): A note
            on_start (Optional[Callable[[list[MidiMessage]], None]]): A callback that is called before playback starts
            on_message (Optional[Callable[[MidiMessage, float], None]]): A callback that is called for every message, before it plays
            on_end (Optional[Callable[[bool], None]]): A callback that is called after the last note played.
                If the playback finishes normally, the passed bool will be ``True``. If the playback loop receives a ``KeyboardInterrupt``
                before then, the passed boolean is ``False``.
        """
        self._play_pe(note, ADAGIO, 0, on_start, on_message, on_end)

    def play_chord(
        self,
        chord: Chord,
        on_start: Optional[Callable[[list[MidiMessage]], None]] = None,
        on_message: Optional[Callable[[MidiMessage, float], None]] = None,
        on_end: Optional[Callable[[bool], None]] = None,
    ):
        """
        Plays a chord on the attached midi target.

        Args:
            chord (Chord): A chord
            on_start (Optional[Callable[[list[MidiMessage]], None]]): A callback that is called before playback starts
            on_message (Optional[Callable[[MidiMessage, float], None]]): A callback that is called for every message, before it plays
            on_end (Optional[Callable[[bool], None]]): A callback that is called after the last note played.
                If the playback finishes normally, the passed bool will be ``True``. If the playback loop receives a ``KeyboardInterrupt``
                before then, the passed boolean is ``False``.
        """
        self._play_pe(chord, ADAGIO, 0, on_start, on_message, on_end)

    def play_phrase(
        self,
        phrase: Phrase,
        tempo: float = ADAGIO,
        channel: int = 0,
        on_start: Optional[Callable[[list[MidiMessage]], None]] = None,
        on_message: Optional[Callable[[MidiMessage, float], None]] = None,
        on_end: Optional[Callable[[bool], None]] = None,
    ):
        """
        Plays a phrase on the attached midi target.

        Args:
            phrase (Phrase): A phrase
            tempo (float): The playback tempo in bpm
            channel (int): The channel to play on
            on_start (Optional[Callable[[list[MidiMessage]], None]]): A callback that is called before playback starts
            on_message (Optional[Callable[[MidiMessage, float], None]]): A callback that is called for every message, before it plays
            on_end (Optional[Callable[[bool], None]]): A callback that is called after the last note played.
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
        on_start: Optional[Callable[[list[MidiMessage]], None]] = None,
        on_message: Optional[Callable[[MidiMessage, float], None]] = None,
        on_end: Optional[Callable[[bool], None]] = None,
    ):
        """
        Plays a part on the attached midi target.

        Args:
            part (Part): A part
            tempo (float): The playback tempo in bpm
            on_start (Optional[Callable[[list[MidiMessage]], None]]): A callback that is called before playback starts
            on_message (Optional[Callable[[MidiMessage, float], None]]): A callback that is called for every message, before it plays
            on_end (Optional[Callable[[bool], None]]): A callback that is called after the last note played.
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
        on_start: Optional[Callable[[list[MidiMessage]], None]] = None,
        on_message: Optional[Callable[[MidiMessage, float], None]] = None,
        on_end: Optional[Callable[[bool], None]] = None,
    ):
        """
        Plays a score on the attached midi target.

        Args:
            score (Score): A score
            on_start (Optional[Callable[[list[MidiMessage]], None]]): A callback that is called before playback starts
            on_message (Optional[Callable[[MidiMessage, float], None]]): A callback that is called for every message, before it plays
            on_end (Optional[Callable[[bool], None]]): A callback that is called after the last note played.
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
        on_start: Optional[Callable[[list[MidiMessage]], None]] = None,
        on_message: Optional[Callable[[MidiMessage, float], None]] = None,
        on_end: Optional[Callable[[bool], None]] = None,
    ):
        ir = pe_to_ir(pe, start_time=0.0)
        messages = irnodes_to_midi(ir, tempo, channel)
        self._play_messages(messages, 0.0, on_start, on_message, on_end)

    @abstractmethod
    def play_message(self, message: MidiMessage): ...

    def _play_messages(
        self,
        messages: list[MidiMessage],
        start_at: float,
        on_start: Optional[Callable[[list[MidiMessage]], None]] = None,
        on_message: Optional[Callable[[MidiMessage, float], None]] = None,
        on_end: Optional[Callable[[bool], None]] = None,
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

    def send_cc(self, channel: int, control: int, value: int):
        """
        A method that should react to a control change.

        By default, this does nothing.

        Args:
            channel (int): The channel for which to update the cc value
            control (int): The control id to update
            value (int): The control value to update with
        """
        # type checker is very happy and satisfied
        _ = channel
        _ = control
        _ = value
