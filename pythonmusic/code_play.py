# TODO: move into play

from dataclasses import dataclass, field
from heapq import heappop, heappush
from typing import Callable
from typing import Optional, cast
from time import time, sleep

from pythonmusic.util import instrument_get_patch_bank, make_instrument
from pythonmusic.play import Player
from pythonmusic.constants import (
    ACOUSTIC_GRAND_PIANO,
    PAN_CENTER,
    MODERATO,
    CHANNEL_PAN,
    PROGRAM_CHANGE,
    NOTE_ON,
    NOTE_OFF,
    BANK_CHANGE,
    CONTROL_CHANGE,
)
from pythonmusic.music import Note, Chord, Phrase, Part, Score, PhraseElement
from pythonmusic.io import MidiMessage
from pythonmusic.io.ir import (
    IrNote,
    IrControlChange,
    IrProgramChange,
    pe_to_ir,
    score_to_ir,
    IrNode,
)
from pythonmusic.io.ir.midi import irnodes_to_midi

__all__ = ["ProxyPlayer", "CodePlayer"]


CODE_MULTIPLYER = 100_000


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
        self, note: Note, channel: int, instrument: int, panning: int, tempo: float
    ) -> list[MidiMessage]:
        proxy = ProxyPlayer(tempo)
        self.on_note(proxy, note, channel, instrument, panning)
        return irnodes_to_midi(proxy._buffer, tempo, channel)

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

        if message_type in [NOTE_ON, NOTE_OFF]:
            print(f"{message_type} for {message["note"]}")

        # CONTINUE: Note off event come exponentioally (?) quicker after note on

        if self._player is not None:
            self._player.play_message(message)
