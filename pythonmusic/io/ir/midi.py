from typing import cast
from itertools import chain

from pythonmusic.io.ir import (
    IrNode,
    IrChannel,
    IrFile,
    IrNote,
    IrControlChange,
    IrProgramChange,
    IrRest,
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


def irnodes_to_midi(
    nodes: list[IrNode], tempo: float, channel: int
) -> list[MidiMessage]:
    Ty = IrNode.Type
    tempo_multiplyer = 60.0 / tempo
    output = []

    for node in nodes:
        match node.type:
            case Ty.REST:
                pass
            case Ty.NOTE:
                payload = cast(IrNote, node.payload)
                start_time = node.time * tempo_multiplyer
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
                    )
                )
            case Ty.PROGRAM:
                payload = cast(IrProgramChange, node.payload)
                output += [
                    MidiMessage(
                        PROGRAM_CHANGE, channel=channel, program=payload.program
                    ),
                    MidiMessage(
                        CONTROL_CHANGE,
                        channel=channel,
                        control=BANK_CHANGE,
                        value=payload.bank,
                    ),
                ]
            case Ty.META:
                # NOTE: if other METAs are supported, change here
                # TODO: Add support for meta messages
                pass
            case _:
                raise TypeError("Unknown node type")

    return output


def irchannel_to_midi(channel: IrChannel, tempo: float) -> list[MidiMessage]:
    return irnodes_to_midi(channel.nodes, tempo, channel.channel)


def irfile_to_midi(file: IrFile) -> list[MidiMessage]:
    payload = file.channels[0].nodes[0].payload
    assert type(payload) == IrTempo
    tempo = cast(IrTempo, payload)

    return list(
        chain(
            *map(lambda channel: irchannel_to_midi(channel, tempo.value), file.channels)
        )
    )
