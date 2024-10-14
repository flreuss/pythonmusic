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

    def __init__(self, tempo: float, instruments: list[int], pannings: list[int]):
        self._buffer: list[MidiMessage] = []
        self._tempo = tempo
        self._instruments: list[int] = instruments
        self._pannings: list[int] = pannings

    def __len__(self) -> int:
        return self._buffer.__len__()

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

    def has_messages(self) -> bool:
        """
        Returns `True` if the proxy has buffered messages.
        """
        return self._buffer.__len__() != 0

    def _pop_message(self) -> Optional[MidiMessage]:
        """
        Pops the top-most (latest) Midi Message of the internal buffer.

        Returns:
            Optional[MidiMessage]: Latest message, or `None` if empty
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
        if instrument is not None and instrument != self._instruments[channel]:
            patch, bank = instrument_get_patch_bank(instrument)
            nodes.append(
                IrNode(timing, IrNode.Type.PROGRAM, IrProgramChange(patch, bank))
            )

        # make panning node
        if panning is not None and panning != self._pannings[channel]:
            nodes.append(
                IrNode(timing, IrNode.Type.CC, IrControlChange(CHANNEL_PAN, panning))
            )

        # make note nodes
        nodes += pe_to_ir(note, timing)

        # convert to midi messages
        self._buffer += irnodes_to_midi(nodes, self._tempo, channel)
        print(self._buffer)


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
        # timing = time()
        ir = score_to_ir(score)
        nodes: list[tuple[int, IrNode]] = []  # channel_nr, node
        for channel in ir.channels:
            channel_nr = channel.channel
            for node in channel.nodes:
                # node.time += timing
                nodes.append((channel_nr, node))

        # FIXME: first few notes may be sent without a selected instrument

        self._play_nodes(nodes, score.tempo)

    def _play_nodes(self, nodes: list[tuple[int, IrNode]], tempo: float):
        """
        Entry function to play a list of nodes with the code player.
        """
        # if no nodes, return early
        if len(nodes) == 0:
            return

        # init memory for instruments and pannings on all 16 channels
        instruments: list[int] = [0] * 16  # zero represents no instrument selected
        pannings: list[int] = [PAN_CENTER] * 16

        # init proxy player
        proxy = ProxyPlayer(tempo, instruments, pannings)

        # prepare a queue and stack for messages and nodes
        messages: list[MidiMessage] = []  # heapsort queue
        nodes.sort(key=lambda item: item[1].time, reverse=True)  # stack

        # store current time to calculate offset
        start_time = time()

        try:
            while len(nodes) > 0:
                # save current time
                timing = time() - start_time

                # check for nodes that need to be handled
                channel, node = nodes[len(nodes) - 1]
                if timing >= node.time:
                    # if node is ready, handle node and pop off the stack
                    self._handle_node(
                        proxy, channel, node, tempo, instruments, pannings
                    )
                    nodes.pop()

                # for each message in the proxy player, push message onto the
                # heap
                while True:
                    message = proxy._pop_message()
                    if message is None:
                        break

                    # insert message into heap
                    heappush(messages, message)

                    # ensures that proxy is empty after this loop

                # check for messages that need to be dispatched
                # heap-sorted property: heap[0] is smallest/next element
                if len(messages) != 0 and messages[0].time >= timing:
                    message = heappop(messages)
                    self._handle_message(message, channel, instruments, pannings)

                sleep(0.001)  # arbitrary sleep

        except KeyboardInterrupt:
            pass

    def _handle_node(
        self,
        proxy: ProxyPlayer,
        channel: int,
        node: IrNode,
        tempo: float,
        instruments: list[int],
        pannings: list[int],
    ) -> list[MidiMessage]:
        """
        Handles a node event. If the event is a NOTE, the users callback is
        executed and the proxy player read.
        """
        # if node type is not a NOTE, handle internally and return
        if node.type != IrNode.Type.NOTE:
            messages = irnodes_to_midi([node], tempo, channel)
            for m in messages:
                t = m.type
                if t == "control_change":
                    print(f"CC: {m["value"]}")
                else:
                    print(f"PC: {m["program"]}")
            return messages

        # else, prepare and use callback
        note_node = cast(IrNote, node.payload)
        instrument = instruments[channel]
        panning = pannings[channel]
        note = Note(note_node.note, note_node.duration, note_node.velocity)

        self.on_note(proxy, note, channel, instrument, panning)

        return []

    def _handle_message(
        self,
        message: MidiMessage,
        channel: int,
        instruments: list[int],
        pannings: list[int],
    ):
        """
        Handles a midi message event and updates instrument and panning values.
        """
        # update instrument (patch)
        if message.type == PROGRAM_CHANGE:
            print(f"MSG: Program Change to {message["program"]}")
            _, bank = instrument_get_patch_bank(instruments[channel])
            new_patch = message["program"]
            instruments[channel] = make_instrument(new_patch, bank)
            exit(123)

        # update panning or instrument (bank)
        elif message.type == CONTROL_CHANGE:
            control = message["control"]

            # update bank in instrument
            if control == BANK_CHANGE:
                print(f"MSG: Bank Change to {message["value"]}")
                patch, _ = instrument_get_patch_bank(instruments[channel])
                new_bank = message["value"]
                instruments[channel] = make_instrument(patch, new_bank)

            # update channel pan
            elif control == CHANNEL_PAN:
                print(f"MSG: Channel Pan to {message["value"]}")
                pannings[channel] = message["value"]

        # if a player was provided during init, send message along
        # this should guarantee identical instrument (patch+bank) and pan
        #   settings in player and scope
        if self._player:
            self._player.play_message(message)
