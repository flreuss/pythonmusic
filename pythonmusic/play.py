from collections.abc import Callable
from abc import ABC, abstractmethod
from time import sleep
from typing import Optional, TypeVar, override, cast
from queue import PriorityQueue, Empty
from dataclasses import dataclass
from threading import Thread, Event
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


# ======== Code Play ========
# support for up to
_CODE_MULTIPLYER = 100_000


def _encode_timing(time: float) -> int:
    return int(time * _CODE_MULTIPLYER)


def _decode_timing(coded: int) -> float:
    return float(coded) / _CODE_MULTIPLYER


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
        self._queue: PriorityQueue[MidiMessage] = PriorityQueue(maxsize=0)
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

    @property
    def player(self) -> Player:
        return self._player

    @staticmethod
    def _loop(queue: PriorityQueue[MidiMessage], player: Player, abort: Event):
        while not abort.is_set():
            try:
                # I don't see another way to check if a message should be played
                # we cant store this in, lets say, `next_message` because another
                # message may be added that precedes the stored message
                item = queue.get(False, timeout=None)
                trigger = _decode_timing(item[0])
                if trigger >= time():
                    player.play_message(item[1])
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
            item = PriorityItem((coded, message))

            # add to queue
            self._queue.put(item, block=True, timeout=1)

    def send_message(self, message: MidiMessage):
        """Remember to set time"""
        timing = message.time + time()
        coded = _encode_timing(timing)
        self._queue.put(PriorityItem((coded, message)))


class CodePlayer:
    """ """

    def __init__(
        self,
        player: Optional[Player],
        on_note: Callable[
            [Optional[AsyncPlayer], Note, int, Optional[int], Optional[int]], None
        ],
    ):
        self.on_note = on_note
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
        ir = score_to_ir(score)
        nodes: list[tuple[int, IrNode]] = []  # channel_nr, node
        for channel in ir.channels:
            channel_nr = channel.channel
            for node in channel.nodes:
                nodes.append((channel_nr, node))

        self._play_nodes(nodes, score.tempo)

    def _play_nodes(self, nodes: list[tuple[int, IrNode]], tempo: float):
        if len(nodes) == 0:
            return

        # init optional player
        player: Optional[AsyncPlayer] = None
        if self._player is not None:
            player = AsyncPlayer(self._player, tempo)

        # setup memory for instruments and panning for all 16 channels
        instruments: list[Optional[int]] = [None] * 16
        pannings: list[Optional[int]] = [None] * 16

        # main loop
        current: tuple[int, IrNode]
        next: tuple[int, IrNode] = nodes.pop()
        Ty = IrNode.Type

        try:
            while next is not None:
                current = next
                channel, node = current

                instrument = instruments[channel]
                panning = pannings[channel]

                match node.type:
                    case Ty.NOTE | Ty.REST:
                        note_node = cast(IrNote, node.payload)
                        note = Note(
                            note_node.note, note_node.duration, note_node.velocity
                        )

                        self.on_note(player, note, channel, instrument, panning)

                    case Ty.CC:
                        if player:
                            cc_node = cast(IrControlChange, node.payload)
                            message = MidiMessage(
                                CONTROL_CHANGE,
                                control=cc_node.control,
                                value=cc_node.value,
                            )

                            player.send_message(message)

                    case Ty.PROGRAM:
                        if player:
                            program_node = cast(IrProgramChange, node.payload)
                            program_message = MidiMessage(
                                PROGRAM_CHANGE,
                                channel=channel,
                                program=program_node.program,
                            )
                            bank_message = MidiMessage(
                                CONTROL_CHANGE,
                                channel=channel,
                                control=BANK_CHANGE,
                                value=program_node.bank,
                            )

                            # time is 0 to play immediately (or as close as possible)
                            player.send_message(program_message)
                            player.send_message(bank_message)

        except KeyboardInterrupt:
            pass
