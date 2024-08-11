from abc import ABC, abstractmethod
from dataclasses import dataclass
from enum import Enum
from math import floor

from pythonmusic.music import PhraseElement, Note, Chord, Phrase, Part, Score
from pythonmusic.constants import CHANNEL_PAN
from pythonmusic.util import instrument_get_patch_bank, bpm_to_mspb
from pythonmusic.constants.articulations import *

# The idea behind adding an IR layer on top of midi messages is to make
# conversion between this library's types and different output formats easier.
# It also implements articulations on notes.


# ==== Payloads ====
class IrPayload(ABC):
    """
    An ABC that groups all types of payloads nodes can have.

    A payload is one abstraction above a  midi message. It retains some objects
    such as notes instead of splitting them into on/off messages.
    """

    pass


@dataclass
class IrNote(IrPayload):
    note: int
    velocity: int
    duration: float


@dataclass
class IrControlChange(IrPayload):
    __slots__ = ("control", "value")
    control: int
    value: int


@dataclass
class IrProgramChange(IrPayload):
    __slots__ = ("program", "bank")

    program: int
    # following the midi standard, bank is set as a control message
    # I group this with program change, because this library does not use bank
    # otherwise.
    # NOTE: be careful not to overwrite bank if none is set
    bank: int


# TODO: Rename to IrMeta
# It would be better to add support for midi meta messages.
# See https://www.recordingblogs.com/wiki/midi-meta-messages
@dataclass
class IrTempo(IrPayload):
    __slots__ = "value"
    value: int  # number of microseconds per beat


# ==== Objects ====
@dataclass
class IrNode:
    """An element that represents any type of event."""

    class Type(Enum):
        NOTE = 1
        CC = 2
        PROGRAM = 3
        META = 4  # only used for tempo at the moment

    __slots__ = ("time", "type", "payload")

    time: float
    type: Type
    payload: IrPayload


@dataclass
class IrChannel:
    """An element that represents a part or channel."""

    __slots__ = ("title", "channel", "nodes")

    title: str | None
    channel: int
    nodes: list[IrNode]


@dataclass
class IrFile:
    __slots__ = ("title", "channels")

    title: str | None
    channels: list[IrChannel]


# ==== Methods ====
def pe_to_ir(pe: PhraseElement, start_time: float) -> list[IrNode]:
    """
    Converts a `PhraseElement` to IR.

    `Chord`s can contain multiple notes, so this function returns an array of
    notes. If the given element is a `Note`, the array has only one member.
    Chords are flattened.

    :param pe PhraseElement: A phrase element
    :param start_time float: The start time of the phrase element
    :return: A list of nodes
    """

    def _convert_note(note: Note, start_time: float) -> IrNode:
        # Duration
        duration: float = note.duration
        if note.has_articulation(TENUTO):
            pass  # duration is unchanged, all else is ignored
        elif note.has_articulation(PORTATO):
            duration *= 0.95
        elif note.has_articulation(STACCATISSIMO):
            duration *= 0.25
        elif note.has_articulation(STACCATO):
            duration *= 0.5
        elif note.has_articulation(LEGATO):
            duration *= 1.05
        else:
            duration *= 0.90

        # Velocity
        velocity: int = note.dynamic
        if note.has_articulation(MARCATO):
            velocity = floor(velocity * 1.50)
        elif note.has_articulation(ACCENT):
            velocity = floor(velocity * 1.25)
        else:
            pass
        # velocity is capped to 127
        velocity = min(127, velocity)

        payload = IrNote(note.pitch, velocity, duration)
        return IrNode(start_time, IrNode.Type.NOTE, payload)

    def _convert_chord(chord: Chord, start_time: float) -> list[IrNode]:
        nodes = []
        for element in chord.notes:
            nodes += pe_to_ir(element, start_time)
        return nodes

    if isinstance(pe, Note):
        return [_convert_note(pe, start_time)]
    if isinstance(pe, Chord):
        return _convert_chord(pe, start_time)
    raise TypeError("Unknown PhraseElement object")


def phrase_to_ir(phrase: Phrase, start_time: float) -> list[IrNode]:
    """
    Converts a `Phrase` to IR.
    """
    output: list[IrNode] = []
    time_accumulator = start_time

    for element in phrase.notes:
        output += pe_to_ir(element, time_accumulator)
        time_accumulator += element.duration

    return output


def part_to_ir(part: Part) -> IrChannel:
    """
    Converts a `Part` to IR.

    This also adds all associated CC values as CC nodes in the beginning of the
    return list.
    """

    def instrument_node(value: int) -> IrNode:
        # TEST: No idea if this works
        patch, bank = instrument_get_patch_bank(value)
        payload = IrProgramChange(patch, bank)
        return IrNode(0.0, IrNode.Type.PROGRAM, payload)

    def panning_node(value: int) -> IrNode:
        payload = IrControlChange(CHANNEL_PAN, value)
        return IrNode(0.0, IrNode.Type.CC, payload)

    nodes: list[IrNode] = [instrument_node(part.instrument), panning_node(part.panning)]

    for start_time, phrase in part.phrases:
        nodes += phrase_to_ir(phrase, start_time)

    return IrChannel(part.title, part.channel, nodes)


def score_to_ir(score: Score) -> IrFile:
    """
    Converts a `Score` to IR.

    This also adds all associated CC values as CC nodes in the beginning of the
    """

    def tempo_node(value: float) -> IrNode:
        payload = IrTempo(bpm_to_mspb(value))
        return IrNode(0.0, IrNode.Type.META, payload)

    channels: list[IrChannel] = list(map(lambda part: part_to_ir(part), score.parts))

    tempo = tempo_node(score.tempo)
    if len(channels) == 0:
        channels = [IrChannel("Channel 0", 0, [tempo])]
    else:
        channels[0].nodes.insert(0, tempo)

    return IrFile(score.title, channels)
