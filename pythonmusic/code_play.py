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

    def _has_messages(self) -> bool:
        """
        Returns `True` if the proxy has buffered nodes.
        """
        return self._buffer.__len__() != 0

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
        timing = time()

        # make instrument node
        if instrument is not None and instrument:
            patch, bank = instrument_get_patch_bank(instrument)
            nodes.append(
                IrNode(timing, IrNode.Type.PROGRAM, IrProgramChange(patch, bank))
            )

        # make panning node
        if panning is not None:
            nodes.append(
                IrNode(timing, IrNode.Type.CC, IrControlChange(CHANNEL_PAN, panning))
            )

        # make note nodes
        nodes += pe_to_ir(note, timing)

        self._buffer += nodes


@dataclass
class _Channel:
    instrument: int
    panning: int
    nodes: list[tuple[float, Note]]  # flat, (reversed) stack

    def last(self) -> Optional[N]
    # CONTINUE: why is this Note?!


class CodePlayer:
    """ """

    def __init__(
        self,
        player: Optional[Player],
        on_note: Callable[
            [ProxyPlayer, Note, int, Optional[int], int], None
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
        proxy_player = ProxyPlayer(tempo)
        start_time = time()

        # if we have a player
        if self._player is not None:
            # for each channel
            for channel_nr, channel in enumerate(channels):
                # that exists (counted for channel_nr)
                if channel is not None:
                    self._player.set_instrument(channel_nr, channel.instrument)
                    self._player.send_cc(channel_nr, CHANNEL_PAN, channel.panning)

        messages: list[MidiMessage] = []  # heap sorted

        while True:
            delta_time = time() - start_time  # seconds since start

            for channel_nr, channel in enumerate(channels):
                if channel is not None:
                    last_node = channel.nodes[]










            sleep(0.001)
