from collections.abc import Callable
from abc import ABC, abstractmethod
from time import sleep
from typing import Optional, override
from queue import PriorityQueue, Empty
from dataclasses import dataclass
from threading import Thread, Event
from time import time

from pythonmusic.constants import ACOUSTIC_GRAND_PIANO, PAN_CENTER, MODERATO
from pythonmusic.music import Note, Chord, Phrase, Part, Score, PhraseElement
from pythonmusic.constants import ADAGIO as _ADAGIO
from pythonmusic.io import MidiMessage, MidiSender
from pythonmusic.io.ir import (
    pe_to_ir,
    phrase_to_ir,
    part_to_ir,
    score_to_ir,
    IrNode,
    make_tempo_node,
    make_panning_node,
    make_instrument_node,
)
from pythonmusic.io.ir.midi import irnodes_to_midi, irchannel_to_midi, irfile_to_midi

__all__ = ["Player", "MidiPlayer", "CodePlayer", "AsyncPlayer"]


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
        self._play_pe(note, _ADAGIO, 0, on_start, on_message, on_end)

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
        self._play_pe(chord, _ADAGIO, 0, on_start, on_message, on_end)

    def play_phrase(
        self,
        phrase: Phrase,
        tempo: float = _ADAGIO,
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
        tempo: float = _ADAGIO,
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

    def _play_messages(
        self,
        messages: list[MidiMessage],
        start_at: float,
        on_start: Callable[[list[MidiMessage]], None] | None,
        on_message: Callable[[MidiMessage, float], None] | None,
        on_end: Callable[[bool], None] | None,
    ):
        # TODO: do proper sorting here, check for faster algorithms
        messages.sort(
            key=lambda message: message.time, reverse=True
        )  # sorts in decending order for fast pop

        start_time: float = start_at
        while len(messages) > 0:
            index = len(messages) - 1
            if messages[index].time < start_time:
                del messages[index]
            else:
                break

        if len(messages) == 0:
            return

        if on_start:
            on_start(messages)

        current: MidiMessage
        next: MidiMessage | None = messages.pop()  # we at least one

        try:
            while next is not None:
                current = next

                if on_message:
                    on_message(current, start_time)

                self.play_message(current)

                if len(messages) > 0:
                    next = messages.pop()
                    start_time += current.time
                    # protect against negative sleep time
                    # this should not happen, but float imprecision may cause this
                    sleep_time = max(0, next.time - current.time)
                    sleep(sleep_time)
                else:
                    next = None

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


# ======== Code Play ========
# support for up to
_CODE_MULTIPLYER = 100_000


def _encode_timing(time: float) -> int:
    return int(time * _CODE_MULTIPLYER)


def _decode_timing(coded: int) -> float:
    return float(coded) / _CODE_MULTIPLYER


@dataclass(order=True)
class PriorityItem:
    """An item in the priority queue."""

    priority: int
    message: MidiMessage


class AsyncPlayer:
    """
    An object that sends messages to a player on another thread.

    Other players will block the main thread when playing elements.
    """

    def __init__(self, player: Player, tempo: float) -> None:
        self._player = player
        self.tempo = tempo

        # defining with maxsize 0 results in infinite queue
        # according to the docs, this queue is thread-safe
        self._queue: PriorityQueue[PriorityItem] = PriorityQueue(maxsize=0)
        # if set to true, stops the thread on the next pass
        self._abort = Event()
        self._thread = Thread(
            target=AsyncPlayer._loop, args=(self._queue, self._player, self._abort)
        )

        self._start_thread()

    def __del__(self):
        self._stop_thread()

    def _start_thread(self):
        self._thread.start()

    def _stop_thread(self):
        self._abort.set()
        self._thread.join()

    @staticmethod
    def _loop(queue: PriorityQueue[PriorityItem], player: Player, abort: Event):
        while not abort.is_set():
            try:
                # I don't see another way to check if a message should be played
                # we cant store this in, lets say, `next_message` because another
                # message may be added that precedes the stored message
                item = queue.get(False, timeout=None)
                trigger = _decode_timing(item.priority)
                if trigger >= time():
                    player.play_message(item.message)
                else:
                    queue.put(item, block=False)
            except Empty:
                continue

    def play_note(
        self,
        note: Note,
        instrument: int = ACOUSTIC_GRAND_PIANO,
        channel: int = 0,
        panning: int = PAN_CENTER,
    ):
        # first convert to ir, then midi message
        nodes: list[IrNode] = [
            make_instrument_node(instrument),
            make_panning_node(panning),
        ] + pe_to_ir(note, 0.00001)
        messages = irnodes_to_midi(nodes, self.tempo, channel)

        for message in messages:
            # calculate real time of playback
            timing = message.time + time()
            # "encode" to int (precise to 5 post decimals)
            coded = _encode_timing(timing)
            # construct item
            item = PriorityItem(coded, message)

            # add to queue
            self._queue.put(item, block=True, timeout=1)


class CodePlayer:
    """
    A player that uses a callback function to play the given material.

    Use this player to define how a :obj:`Note <pythonmusic.music.Note>` is
    played back in a callback you pass to the initialiser. The callback should
    be defined as such:

    .. code-block:: python

        def my_callback(
            player: AsyncPlayer | None,
            note: Note,
            channel: int,
            instrument: int,
            panning: int
        ):
            # do something
            pass

    To playback notes on a :obj:`Player <pythonmusic.play.Player>`
    (:obj:`MidiPlayer <pythonmusic.play.MidiPlayer>`,
    :obj:`SynthPlayer <pythonmusic.play.PynthPlayer>`, ...), create a player and
    pass it to the initialiser. This will create an
    :obj:`AsyncPlayer <pythonmusic.play.AsyncPlayer>` internally, and pass it to
    your callback.

    For more information, see the Players section in the documentation.

    Args:
        callback (Callable[[Optional[AsyncPlayer], Note, int, int, int] None]):
            A callback that is called for each note.
        player: (Optional[Player]): An optional player object. If defined, an
            AsyncPlayer will be available to the callback.
    """

    def __init__(
        self,
        callback: Callable[[Optional[AsyncPlayer], Note, int, int, int], None],
        player: Optional[Player],
    ):
        self.callback = callback
        self._player = player
        # AsyncPlayer is local to playback method call. This avoids the issue
        # where the AsyncPlayer-thread will prevent Python to exit.

    def play_note(
        self,
        note: Note,
        channel: int = 0,
        instrument: int = ACOUSTIC_GRAND_PIANO,
        panning: int = PAN_CENTER,
        tempo: float = MODERATO,
    ):
        self.play_phrase(Phrase([note]), channel, instrument, panning, tempo)

    def play_chord(
        self,
        chord: Chord,
        channel: int = 0,
        instrument: int = ACOUSTIC_GRAND_PIANO,
        panning: int = PAN_CENTER,
        tempo: float = MODERATO,
    ):
        self.play_phrase(Phrase([chord]), channel, instrument, panning, tempo)

    def play_phrase(
        self,
        phrase: Phrase,
        channel: int = 0,
        instrument: int = ACOUSTIC_GRAND_PIANO,
        panning: int = PAN_CENTER,
        tempo: float = MODERATO,
    ):
        self.play_part(Part(None, instrument, [phrase], channel, panning), tempo)

    def play_part(self, part: Part, tempo: float = MODERATO):
        self.play_score(Score(None, [part], tempo))

    def play_score(self, score: Score):
        player: Optional[AsyncPlayer]
        if self._player is not None:
            player = AsyncPlayer(self._player, score.tempo)

        # CONTINUE: convert

        ir = score_to_ir(score)
