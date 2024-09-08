from typing import cast
from itertools import chain

from pythonmusic.io.ir import (
    IrNode,
    IrChannel,
    IrFile,
    IrNote,
    IrControlChange,
    IrProgramChange,
    IrTempo,
)
from pythonmusic.io.midi_message import MidiMessage
from pythonmusic.constants import (
    NOTE_ON,
    NOTE_OFF,
    CONTROL_CHANGE,
    PROGRAM_CHANGE,
    BANK_CHANGE,
)

__all__ = ["irnodes_to_midi", "irchannel_to_midi", "irfile_to_midi"]


def irnodes_to_midi(
    nodes: list[IrNode], tempo: float, channel: int
) -> list[MidiMessage]:
    """
    Converts a list of ir nodes to midi messages.

    Args:
        nodes (list[IrNode]): A list of ir nodes
        tempo (float): A tempo in bpm that will be used to create the midi
            midi message offsets
        channel (int): The midi channel on which to play the notes on

    Returns:
        list[MidiMessage]: A list of midi messages
    """
    Ty = IrNode.Type
    tempo_multiplyer = 60.0 / tempo
    output = []

    for node in nodes:
        start_time = node.time * tempo_multiplyer

        match node.type:
            case Ty.REST:
                pass
            case Ty.NOTE:
                payload = cast(IrNote, node.payload)
                end_time = start_time + (payload.duration * tempo_multiplyer)

                assert channel in range(0, 128)
                assert payload.note in range(0, 128)
                assert payload.velocity in range(0, 128)

                output += [
                    MidiMessage(
                        NOTE_ON,
                        channel=channel,
                        note=payload.note,
                        velocity=payload.velocity,
                        # TEST: Is this a compatible use of the time attribute?
                        # Event mido itself seems undecided here...
                        time=start_time,
                    ),
                    MidiMessage(
                        NOTE_OFF,
                        channel=channel,
                        note=payload.note,
                        velocity=payload.velocity,  # yes, also velocity
                        time=end_time,
                    ),
                ]
            case Ty.CC:
                payload = cast(IrControlChange, node.payload)
                output.append(
                    MidiMessage(
                        CONTROL_CHANGE,
                        channel=channel,
                        control=payload.control,
                        value=payload.value,
                        time=start_time,
                    )
                )
            case Ty.PROGRAM:
                payload = cast(IrProgramChange, node.payload)
                output += [
                    MidiMessage(
                        PROGRAM_CHANGE,
                        channel=channel,
                        program=payload.program,
                        time=start_time,
                    ),
                    MidiMessage(
                        CONTROL_CHANGE,
                        channel=channel,
                        control=BANK_CHANGE,
                        value=payload.bank,
                        time=start_time,
                    ),
                ]
            case Ty.META:
                # NOTE: if other METAs are supported, change here
                # TODO: Add support for meta messages
                pass

    return output


def irchannel_to_midi(channel: IrChannel, tempo: float) -> list[MidiMessage]:
    """
    Converts an ir channel to a list of midi messages.

    Args:
        channel (IrChannel): An ir channel to convert
        tempo (float): A tempo in bpm that will be used to calculate the midi
            message timing offsets

    Returns:
        list[MidiMessage]: A list of midi messages
    """
    return irnodes_to_midi(channel.nodes, tempo, channel.channel)


def irfile_to_midi(file: IrFile) -> list[MidiMessage]:
    """
    Converts an ir file to a list of midi messages.

    Args:
        file (IrFile): An ir file

    Returns:
        list[MidiMessage]: A list of midi messages
    """
    payload = file.channels[0].nodes[0].payload
    assert type(payload) == IrTempo
    tempo = cast(IrTempo, payload)

    return list(
        chain(
            *map(lambda channel: irchannel_to_midi(channel, tempo.value), file.channels)
        )
    )
