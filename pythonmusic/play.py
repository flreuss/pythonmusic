from typing import Callable
from dataclasses import dataclass
from heapq import heappop, heappush
from abc import ABC, abstractmethod
from time import sleep
from typing import Optional, override, cast, Callable
from time import time, sleep

from pythonmusic.constants import (
    ACOUSTIC_GRAND_PIANO,
    PAN_CENTER,
    MODERATO,
    CONTROL_CHANGE,
    CHANNEL_PAN,
    PROGRAM_CHANGE,
    ADAGIO,
    NOTE_ON,
    NOTE_OFF,
    BANK_CHANGE,
)
from pythonmusic.music import Note, Chord, Phrase, Part, Score, PhraseElement
from pythonmusic.io import MidiMessage, MidiSender
from pythonmusic.io.ir import (
    IrControlChange,
    IrProgramChange,
    pe_to_ir,
    phrase_to_ir,
    part_to_ir,
    score_to_ir,
    IrNode,
)
from pythonmusic.io.ir.midi import irnodes_to_midi, irchannel_to_midi, irfile_to_midi
from pythonmusic.util import instrument_get_patch_bank, make_instrument

__all__ = ["Player", "MidiPlayer", "ProxyPlayer", "CodePlayer"]


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

    @override
    def send_cc(self, channel: int, control: int, value: int):
        """
        Send a control change message to the attached midi receiver.

        .. note:: Depends on the ``play_message()`` method.

        Args:
            channel (int): The channel for which to update the cc value
            control (int): The control id to update
            value (int): The control value to update with
        """
        self.play_message(
            MidiMessage(CONTROL_CHANGE, channel=channel, control=control, value=value)
        )


# TODO: doc strings
# CONTINUE: docs for below and players.rst
class ProxyPlayer:
    """
    A player class that can be used to play notes inside a code player.

    Args:
        tempo (float): A playback tempo
    """

    def __init__(self, tempo: float):
        self._buffer: list[IrNode] = []
        self._tempo = tempo

    def tempo(self) -> float:
        """
        Returns the players tempo.
        """
        return self._tempo

    def is_empty(self) -> bool:
        """
        Returns `True` if there are no notes in the proxy's buffer.

        Returns:
            bool: `True` if no notes in internal buffer
        """
        return self._buffer.__len__() == 0

    def _pop_node(self) -> Optional[IrNode]:
        """
        Pops the top-most (latest) IrNode of the internal buffer.

        Returns:
            Optional[IrNode]: Latest node, or `None` if empty
        """
        if len(self._buffer) == 0:
            return None
        else:
            return self._buffer.pop()

    def _clear(self):
        """
        Removes all buffered midi messages.
        """
        self._buffer = []

    def play_note(
        self,
        note: Note,
        channel: int = 0,
        instrument: Optional[int] = None,
        panning: Optional[int] = PAN_CENTER,
    ):
        """
        Registers a note event with the player.

        Args:
            note (Note): A note to play
            instrument (Optional[int]): If set, updates the instrument on the channel
            channel (int): A channel to play the note on and change instrument and panning on, if given. Defaults to channel 0
            panning (Optional[int]): If set, updates the panning on the channel
        """
        nodes: list[IrNode] = []
        START_TIME = 0.0

        # make instrument node
        if instrument is not None and instrument:
            patch, bank = instrument_get_patch_bank(instrument)
            nodes.append(
                IrNode(START_TIME, IrNode.Type.PROGRAM, IrProgramChange(patch, bank))
            )

        # make panning node
        if panning is not None:
            nodes.append(
                IrNode(
                    START_TIME, IrNode.Type.CC, IrControlChange(CHANNEL_PAN, panning)
                )
            )

        # make note nodes
        nodes += pe_to_ir(note, START_TIME)

        self._buffer += nodes


@dataclass
class _Channel:
    instrument: int
    panning: int
    notes: list[tuple[float, Note]]  # flat, (reversed) stack

    def __len__(self) -> int:
        return self.notes.__len__()

    def next(self) -> Optional[tuple[float, Note]]:
        """
        Returns the next node of the channel.

        .. important:: Does not remove. Uses ``pop()`` instead.

        Returns:
            IrNode: The next node in the channel
        """
        length = len(self)
        if length == 0:
            return None
        return self.notes[length - 1]

    def pop(self) -> Optional[tuple[float, Note]]:
        """
        Pop the next node of the internal stack and returns it.

        Returns:
            IrNode: The next node in the channel
        """
        if len(self) == 0:
            return None
        else:
            return self.notes.pop()

    def is_empty(self) -> bool:
        """
        Returns `True` if no notes are left in the channel.

        Returns:
            bool: If no notes are left in the channel
        """
        return len(self) == 0


class CodePlayer:
    """ """

    def __init__(
        self,
        player: Optional[Player],
        on_note: Callable[
            [ProxyPlayer, Note, int, int, int], None
        ],  # channel, instrument, panning
    ):
        self.on_note = on_note
        self._player = player

    def has_player(self) -> bool:
        """Returns `True` if a player has been registered."""
        return self._player is not None

    def player(self) -> Optional[Player]:
        """Returns the registered player."""
        return self._player

    def update_player(self, player: Optional[Player]):
        """Updates the internal player."""
        self._player = player

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
        channels: list[Optional[_Channel]] = [None] * 16

        for part in score.parts:
            notes: list[tuple[float, Note]] = part.linearise()
            notes = list(
                map(
                    lambda element: (element[0] * (60 / score.tempo), element[1]), notes
                )
            )

            # if another part uses the same channel, this simply adds the
            # already existing notes to the new channel so no notes a dropped
            # however, this also means that only the last part can set
            # instrument and panning
            other_channel = channels[part.channel]
            if other_channel is not None:
                notes += other_channel.notes

            notes.sort(key=lambda element: element[0], reverse=True)  # stack

            channels[part.channel] = _Channel(part.instrument, part.panning, notes)

        self._play_channels(channels, score.tempo)

    def _play_channels(self, channels: list[Optional[_Channel]], tempo: float):
        start_time = time()

        # if we have a player
        if self._player is not None:
            # for each channel
            for channel_nr, channel in enumerate(channels):
                # that exists (counted for channel_nr)
                if channel is not None:
                    self._player.set_instrument(channel_nr, channel.instrument)
                    self._player.send_cc(channel_nr, CHANNEL_PAN, channel.panning)

        # NOTE: If this library is ever updated to allow for tempo changes (or
        # other meta and cc changes), add them here
        messages: list[MidiMessage] = []  # heap sorted

        # calculate number of channels that have notes
        counter = 16 - (channels.count(None))

        # repeat while all channels still have messages
        while counter != 0:
            delta_time = time() - start_time  # seconds since start

            # check channels for notes that need to be played
            for channel_nr, channel in enumerate(channels):
                if channel is not None:
                    if not channel.is_empty():
                        last_note = cast(tuple[float, Note], channel.next())
                        if last_note[0] <= delta_time:
                            for message in self._handle_note(
                                last_note[1],
                                channel_nr,
                                channel.instrument,
                                channel.panning,
                                tempo,
                                delta_time,
                            ):
                                heappush(messages, message)
                            channel.pop()
                        else:
                            pass  # wait until note needs to be sent
                else:
                    channels[channel_nr] = None
                    counter -= 1

            # check messages that need to be sent
            #   the heap invariant guarantees that element 0 is the next message
            #   --> we do not need to check other messages, only ever the first
            while messages and messages[0].time <= delta_time:
                self._handle_message(channels, heappop(messages))

            sleep(0.001)

    def _handle_note(
        self,
        note: Note,
        channel: int,
        instrument: int,
        panning: int,
        tempo: float,
        current_time: float,
    ) -> list[MidiMessage]:
        proxy = ProxyPlayer(tempo)
        self.on_note(proxy, note, channel, instrument, panning)
        return irnodes_to_midi(proxy._buffer, tempo, channel, current_time)

    def _handle_message(self, channels: list[Optional[_Channel]], message: MidiMessage):
        message_type = message.type

        # if message type is a program change, update channel instrument
        if message_type == PROGRAM_CHANGE:
            channel_nr = message["channel"]
            channel = channels[channel_nr]

            _, bank = instrument_get_patch_bank(channel.instrument)
            program = message["program"]
            channel.instrument = make_instrument(program, bank)

        # if control change, handle if bank or panning change
        elif message_type == CONTROL_CHANGE:
            channel_nr = message["channel"]
            channel = channels[channel_nr]
            control = message["control"]

            # update bank change
            if control == BANK_CHANGE:
                patch, _ = instrument_get_patch_bank(channel.instrument)
                bank = message["value"]
                channel.instrument = make_instrument(patch, bank)

            # update panning change
            elif control == CHANNEL_PAN:
                channel.panning = message["value"]

        # if a player exists, play the message
        if self._player is not None:
            self._player.play_message(message)
