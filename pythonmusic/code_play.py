# TODO: move into play

from dataclasses import dataclass, field
from heapq import heappop, heappush
from typing import Callable
from typing import Optional, override, cast
from time import time, sleep

from pythonmusic.util import instrument_get_patch_bank
from pythonmusic.play import Player
from pythonmusic.constants import (
    ACOUSTIC_GRAND_PIANO,
    PAN_CENTER,
    MODERATO,
    CHANNEL_PAN,
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
        self._buffer: list[MidiMessage] = []
        self._tempo = tempo

    def tempo(self) -> float:
        """
        Returns the players tempo.
        """
        return self._tempo

    def buffer(self) -> list[MidiMessage]:
        """
        Returns the internal buffer that stores midi messages.
        """
        return self._buffer

    def play_note(
        self,
        note: Note,
        instrument: Optional[int],
        channel: int = 0,
        panning: Optional[int] = PAN_CENTER,
    ):
        """
        Registers a note event with the player.

        The given input parameters will be converted into messages and passed to
        the :obj:`CodePlayer's <pythonmusic.play.CodePlayer>` internal player.

        Args:
            note (Note): A note to play
            instrument (Optional[int]): If set, updates the instrument on the channel
            channel (int): A channel to play the note on and change instrument and panning on, if given. Defaults to channel 0
            panning (Optional[int]): If set, updates the panning on the channel
        """
        nodes: list[IrNode] = []
        timing = time()

        # make instrument node
        if instrument is not None:
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

        # convert to midi messages
        self._buffer += irnodes_to_midi(nodes, self._tempo, channel)


@dataclass(order=True)
class _NodeItem:
    __all__ = ("priority", "channel", "node")
    priority: int
    channel: int = field(compare=False)
    node: IrNode = field(compare=False)


class CodePlayer:
    """ """

    def __init__(
        self,
        player: Optional[Player],
        on_note: Callable[[ProxyPlayer, Note, int, Optional[int], Optional[int]], None],
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
        ir = score_to_ir(score)
        nodes: list[tuple[int, IrNode]] = []  # channel_nr, node
        for channel in ir.channels:
            channel_nr = channel.channel
            for node in channel.nodes:
                nodes.append((channel_nr, node))

        self._play_nodes(nodes, score.tempo)

    def _play_nodes(self, nodes: list[tuple[int, IrNode]], tempo: float):
        """
        Entry function to play a list of nodes with the code player.
        """
        # if no nodes, return early
        if len(nodes) == 0:
            return

        # init proxy player
        proxy = ProxyPlayer(tempo)

        # init memory for instruments and pannings on all 16 channels
        # CONTINUE: where to store this? self-scope?
        instruments: list[Optional[int]] = [None] * 16
        pannings: list[Optional[int]] = [None] * 16

        # prepare a queue and stack for messages and nodes
        messages: list[MidiMessage] = []  # heapsort queue
        nodes.sort(key=lambda item: item[1].time, reverse=True)  # stack

        try:
            while len(nodes) > 0:
                # save current time
                timing = time()

                # check for nodes that need to be handled
                channel, node = nodes[len(nodes) - 1]
                if timing >= node.time:
                    # if node is ready, handle node and pop off the stack
                    self._handle_node(channel, node, tempo)
                    nodes.pop()

                # check for messages that need to be dispatched
                # heap-sorted property: heap[0] is smalles/next element
                if len(messages) != 0 and messages[0].time >= timing:
                    message = heappop(messages)
                    self._handle_message(message)

                sleep(0.001)  # arbitrary sleep

        except KeyboardInterrupt:
            pass

    def _handle_node(
        self, channel: int, node: IrNode, tempo: float
    ) -> list[MidiMessage]:
        if node.type == IrNode.Type.NOTE:
            pass
        else:
            return irnodes_to_midi(
                [node],
            )

    def _handle_message(self, message: MidiMessage):
        if self._player:
            self._player.play_message(message)

    # def _play_nodes(self, nodes: list[tuple[int, IrNode]], tempo: float):
    #     if len(nodes) == 0:
    #         return
    #
    #     # init optional player
    #     player: Optional[AsyncPlayer] = None
    #     if self._player is not None:
    #         player = AsyncPlayer(self._player, tempo)
    #
    #     # setup memory for instruments and panning for all 16 channels
    #     instruments: list[Optional[int]] = [None] * 16
    #     pannings: list[Optional[int]] = [None] * 16
    #
    #     # main loop
    #     current: tuple[int, IrNode]
    #     next: tuple[int, IrNode] | None = nodes.pop()
    #     Ty = IrNode.Type
    #
    #     try:
    #         while next is not None:
    #             current = next
    #             channel, node = current
    #
    #             if len(nodes) > 0:
    #                 next = nodes.pop()
    #             else:
    #                 next = None
    #
    #             instrument = instruments[channel]
    #             panning = pannings[channel]
    #
    #             match node.type:
    #                 case Ty.NOTE | Ty.REST:
    #                     note_node = cast(IrNote, node.payload)
    #                     note = Note(
    #                         note_node.note, note_node.duration, note_node.velocity
    #                     )
    #
    #                     self.on_note(player, note, channel, instrument, panning)
    #
    #                 case Ty.CC:
    #                     if player:
    #                         cc_node = cast(IrControlChange, node.payload)
    #                         message = MidiMessage(
    #                             CONTROL_CHANGE,
    #                             control=cc_node.control,
    #                             value=cc_node.value,
    #                         )
    #
    #                         player.send_message(message)
    #
    #                 case Ty.PROGRAM:
    #                     if player:
    #                         program_node = cast(IrProgramChange, node.payload)
    #                         program_message = MidiMessage(
    #                             PROGRAM_CHANGE,
    #                             channel=channel,
    #                             program=program_node.program,
    #                         )
    #                         bank_message = MidiMessage(
    #                             CONTROL_CHANGE,
    #                             channel=channel,
    #                             control=BANK_CHANGE,
    #                             value=program_node.bank,
    #                         )
    #
    #                         # time is 0 to play immediately (or as close as possible)
    #                         player.send_message(program_message)
    #                         player.send_message(bank_message)
    #
    #     except KeyboardInterrupt:
    #         pass
