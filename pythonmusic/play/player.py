from copy import copy
from dataclasses import dataclass, field
from functools import reduce
from heapq import heapify, heappop, heappush
from time import sleep, time
from typing import Callable, Optional, cast

from pythonmusic.constants import (
    AUDIO_STREAM_DEFAULT_BUFFER_SIZE,
    AUDIO_STREAM_DEFAULT_SAMPLE_RATE,
    PPQ,
)
from pythonmusic.constants.tempo import ADAGIO
from pythonmusic.midi.convert import initial_part_messages, pe_to_midi
from pythonmusic.midi.io import MidiIn
from pythonmusic.midi.message import Message
from pythonmusic.music import Chord, Note, Part, Phrase, PhraseElement, Score
from pythonmusic.play.sampler import SamplerTarget
from pythonmusic.play.synthesizer import Oscillator, SynthesizerTarget
from pythonmusic.util import beats_to_ticks, bpm_to_mpqn

from .target import MidiOutTarget, SfTarget, Target

__all__ = [
    "Player",
    "Player",
    "SfPlayer",
    "SynthesizerPlayer",
    "MidiOutPlayer",
    "MidiInPlayer",
]


@dataclass(order=True)
class PlaybackElement:
    note: Note = field(compare=False)
    start_time: int
    channel: int = field(compare=False)
    in_chord: bool = field(compare=False)


class Player:
    """
    A class that enables playback of midi messages on targets.

    Players handle the conversion, timing, and sending of midi messages to
    targets.

    All players accept a callback in their play methods that is called for each
    note that is about to be played. The callback receives the note, its
    channel, and a boolean that indicates whether the note is part of a chord.
    The note may be shortened, though its duration in playback won't change. The
    callback returns the note that will be played.

    .. code-block:: python

        from pythonmusic import *

        def my_callback(note: Note, channel: int, is_chord: bool) -> Note:
            # mutes all notes on channel 1, pitch all other notes by +3
            if channel == 1:
                return note.as_rest()

            note.pitch += 3

            return note

        player.play_score(score, callback=my_callback)

    Args:
        target (Target): A target
    """

    def __init__(self, target: Target):
        self._target = target

    def target(self) -> Target:
        """Returns the internal target."""
        return self._target

    def play_message(self, message: Message):
        """
        Plays the given midi message on the registered target.

        Args:
            message(Message): A midi message
        """
        self._target.midi_message(message)

    def set_instrument(self, channel: int, instrument: int):
        """
        Updates the players instrument on the given channel.

        Only instruments defined in @@@ should be used here.

        Args:
            channel(int): The channel for which to change the instrument
            instrument(int): A valid instrument to change to
        """
        self._target.set_instrument(channel, instrument)

    def play_phrase_element(
        self,
        pe: PhraseElement,
        channel: int,
        tempo: float = ADAGIO,
        callback: Optional[Callable[[Note, int, bool], Note]] = None,
    ):
        """
        Plays a phrase element on the given channel.

        Phrase elements are notes and chords. You can use this function to play
        both. Individual methods for each exist with `play_note()` and
        `play_chord()`.

        Args:
            note(PhraseElement): A phrase element
            channel(int): The channel to play on
            tempo(float): The tempo in BPM
            callback (Optional[Callable[[Note, int, bool], Note]]): Callback for
                each note
        """
        self.play_phrase(Phrase([pe]), channel, tempo, callback)

    def play_note(
        self,
        note: Note,
        channel: int,
        tempo: float = ADAGIO,
        callback: Optional[Callable[[Note, int, bool], Note]] = None,
    ):
        """
        Plays a note on the given channel.

        Args:
            note(Note): A note
            channel(int): The channel to play on
            tempo(float): The tempo in BPM
            callback (Optional[Callable[[Note, int, bool], Note]]): Callback for
                each note
        """
        self.play_phrase_element(note, channel, tempo, callback)

    def play_chord(
        self,
        chord: Chord,
        channel: int,
        tempo: float = ADAGIO,
        callback: Optional[Callable[[Note, int, bool], Note]] = None,
    ):
        """
        Plays a chord on the given channel.

        Args:
            note(Chord): A chord
            channel(int): The channel to play on
            tempo(float): The tempo in BPM
            callback (Optional[Callable[[Note, int, bool], Note]]): Callback for
                each note
        """
        self.play_phrase_element(chord, channel, tempo, callback)

    def play_phrase(
        self,
        phrase: Phrase,
        channel: int,
        tempo: float = ADAGIO,
        callback: Optional[Callable[[Note, int, bool], Note]] = None,
    ):
        """
        Plays a phrase on the given channel.

        Args:
            phrase(Phrase): A phrase
            channel(int): The channel to play on
            tempo(float):  Tempo in BPM
            callback (Optional[Callable[[Note, int, bool], Note]]): Callback for
                each note
        """
        self.play_part(Part(None, phrases=[phrase], channel=channel), tempo, callback)

    def play_part(
        self,
        part: Part,
        tempo: float = ADAGIO,
        callback: Optional[Callable[[Note, int, bool], Note]] = None,
        start_at: float = 0.0,
    ):
        """
        Plays a part on the given channel.

        Args:
            part(Part): A part
            tempo(float): Tempo in BPM
            callback (Optional[Callable[[Note, int, bool], Note]]): Callback for
                each note
            start_at(float): The beat to start on
        """
        self.play_score(Score(None, [part], tempo), callback, start_at)

    def play_score(
        self,
        score: Score,
        callback: Optional[Callable[[Note, int, bool], Note]] = None,
        start_at: float = 0.0,
    ):
        """
        Plays a score on the given channel.

        Args:
            score(Score): A score
            callback (Optional[Callable[[Note, int, bool], Note]]): Callback for
                each note
            start_at(float): The beat to start on
        """
        self._play_elements(
            sorted(
                reduce(
                    lambda prev, next: prev + list(next),
                    map(
                        lambda part: filter(
                            lambda element: element.start_time >= start_at,
                            self._prepare_part(part),
                        ),
                        score.parts,
                    ),
                    [],
                ),
                reverse=True,
            ),
            reduce(
                lambda prev, next: prev + list(next),
                map(lambda part: initial_part_messages(part), score.parts),
                [],
            ),
            score.tempo,
            callback,
        )

    @staticmethod
    def _prepare_part(part: Part) -> list[PlaybackElement]:
        def _convert_pe(
            pe: PhraseElement, start_time: int, is_chord: bool
        ) -> tuple[list[PlaybackElement], int]:
            # returns: list of items and duration of pe
            #   if note, len(list) == 1

            if isinstance(pe, Note):
                note: Note = cast(Note, pe)
                duration = beats_to_ticks(note.duration, PPQ)
                return (
                    [PlaybackElement(note, start_time, part.channel, is_chord)],
                    duration,
                )

            if isinstance(pe, Chord):
                chord: Chord = cast(Chord, pe)
                duration = beats_to_ticks(chord.duration, PPQ)

                return (
                    reduce(  # combine items into single list
                        lambda prev, next: prev + next,
                        map(  # for each note in chord.flatten()), make item
                            # here we only care about the item, not the duration,
                            # as this is calculated above
                            lambda note: _convert_pe(note, start_time, True)[0],
                            chord.flatten(),
                        ),
                        [],
                    ),
                    duration,
                )

            raise TypeError("Unknown PhraseElement")

        output: list[PlaybackElement] = []

        for start_time, phrase in part.phrases_with_start_times():
            accumulator: int = beats_to_ticks(start_time, PPQ)
            for pe in phrase:
                items, note_duration = _convert_pe(pe, accumulator, False)
                output += items
                accumulator += note_duration

        return output

    def _play_elements(
        self,
        playback_elements: list[PlaybackElement],
        initial_messages: list[Message],
        tempo: float,
        callback: Optional[Callable[[Note, int, bool], Note]],
    ):
        if len(playback_elements) == 0:
            return

        # messages
        messages = initial_messages
        heapify(messages)

        seconds_per_tick = float(bpm_to_mpqn(tempo)) / float(PPQ) / 1000.0 / 1000.0
        accumulator: float = 0.0
        current_tick: int = 0
        has_advanced: bool = True

        last_t = time()
        while len(messages) > 0 or len(playback_elements) > 0:
            # timing
            now = time()
            accumulator += now - last_t
            last_t = now

            # if accumulator > than single tick length, trigger
            if accumulator > seconds_per_tick:
                advances = int(accumulator // seconds_per_tick)
                accumulator %= seconds_per_tick

                current_tick += advances
                has_advanced = True

            if has_advanced:
                has_advanced = False

                # check pe
                if (
                    playback_elements
                    and playback_elements[-1].start_time <= current_tick
                ):
                    next_pe = playback_elements.pop()

                    if not next_pe.note.is_rest():
                        note = copy(next_pe.note)
                        note = (
                            callback(note, next_pe.channel, next_pe.in_chord)
                            if callback
                            else note
                        )

                        note_messages, _ = pe_to_midi(
                            note, next_pe.channel, next_pe.start_time
                        )

                        # note on / off
                        if len(note_messages) == 2:
                            note_on = note_messages[0]
                            note_off = note_messages[1]
                            note_off.time += next_pe.start_time

                            heappush(messages, note_on)
                            heappush(messages, note_off)

                        # rest
                        elif len(note_messages) == 0:
                            pass

                        else:
                            raise ValueError("Invalid conversion")

                # check message
                if len(messages) > 0:
                    # heap property
                    if messages[0].time <= current_tick:
                        self.play_message(heappop(messages))

            # sleep minim amount possible (will be up to system) to prevent
            # 100% CPU util
            sleep(0.00001)


class SfPlayer(Player):
    """
    A player implementation for the sound font target.

    For more information, see :obj:`SfTarget <pythonmusic.play.SfTarget>`.

    Sound fonts differ in their base volume. If your playback is too loud or too
    quiet, you can adjust the font's base level with the `gain` parameter. All
    values between `-3` (quieter) and `3` (louder) are valid.

    Args:
        sound_font(str): Path to a sound font file
        gain(int): Gain from `-3` to `3`
    """

    def __init__(self, sound_font: str, gain: int = 0):
        target = SfTarget(sound_font, gain)
        super().__init__(target)


class SamplePlayer(Player):
    """
    A player implementation for the sampler target.

    For more information, see :obj:`SamplerTarget <pythonmusic.play.SamplerTarget>`.

    Args:
        sample_rate (int): The sample rate per second
        buffer_size (int): The buffer size
    """

    def __init__(
        self,
        sample_rate: int = AUDIO_STREAM_DEFAULT_SAMPLE_RATE,
        buffer_size: int = AUDIO_STREAM_DEFAULT_BUFFER_SIZE,
    ):
        self._sampler = SamplerTarget(buffer_size, sample_rate)
        super().__init__(self._sampler)


class MidiOutPlayer(Player):
    """
    A player implementation for the midi out target.

    For more information, see :obj:`MidiOut <pythonmusic.midi.MidiOut>`.
    """

    def __init__(self, name: str, virtual: bool):
        target = MidiOutTarget(name, virtual)
        super().__init__(target)

    def __del__(self):
        for channel in range(16):
            self.play_message(Message.new_all_notes_off(channel, 0))


class MidiInPlayer(Player):
    """
    A player implementation that receives input from a midi source and plays
    messages on a target.

    For more information, see :obj:`MidiIn <pythonmusic.midi.MidiIn>`.

    .. important::
        This player runs in the background and is not blocking. You may need to
        add a mechanism for keeping the thread alive

        .. code-block:: python

            player = MidiInPlayer(target, name, virtual)
            while True:
                sleep(1)

    Args:
        target(Target): A target to play messages on
        name(str): The name of the port to host or attach to
        virtual(bool): If `True`, creates a virtual port, otherwise attaches to
            an existing port
    """

    def __init__(self, target: Target, name: str, virtual: bool):
        super().__init__(target)
        self._port = MidiIn(name, virtual)
        self._port.set_callback(None, self.play_message)

    def port(self) -> MidiIn:
        """
        Returns the internal midi port.
        """
        return self._port


class SynthesizerPlayer(Player):
    """
    A player implementation for the synthesizer target.

    Args:
        oscillator (Oscillator): An oscillator
        attack (Optional[float]): Attack in seconds
        sustain (Optional[float]): Sustain in seconds
        decay (Optional[float]): Decay in seconds
        sample_rate(int): Sample rate per second
        buffer_size(int): Sample buffer size
    """

    def __init__(
        self,
        oscillator: Oscillator,
        attack: Optional[float] = None,
        sustain: Optional[float] = None,
        decay: Optional[float] = None,
        sample_rate: int = AUDIO_STREAM_DEFAULT_SAMPLE_RATE,
        buffer_size: int = AUDIO_STREAM_DEFAULT_BUFFER_SIZE,
    ):
        target = SynthesizerTarget(
            oscillator, attack, sustain, decay, sample_rate, buffer_size
        )
        super().__init__(target)
