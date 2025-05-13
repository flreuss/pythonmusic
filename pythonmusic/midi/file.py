"""
Contains assorted functions and objects that enable exporting to file.
"""

import struct
from functools import reduce

from pythonmusic.constants import PPQ
from pythonmusic.music import Part, Score, instrument_get_name
from pythonmusic.util import bpm_to_mpqn

from .convert import part_to_midi
from .message import Message

__all__ = ["export_score"]

# this library only supports midi ff 1
FILE_FORMAT: int = 1


# chunks
def header_chunk(file_format: int, track_count: int, ppq: int) -> bytes:
    """Creates a header chunk."""
    type = b"MThd"
    length = struct.pack(">L", 6)
    data = (
        struct.pack(">H", file_format)
        + struct.pack(">H", track_count)
        + struct.pack(">H", ppq)
    )
    return type + length + data


def track_chunk(
    messages: list[Message],
) -> bytes:
    """Creates a track chunk"""
    type = b"MTrk"
    data = reduce(
        lambda prev, next: prev + next,
        map(lambda message: message.raw_with_time(), messages),
    )
    length = len(data)

    return type + length.to_bytes(4, "big") + data


# conversion
def part_to_messages(part: Part) -> list[Message]:
    """Converts a part to midi messages and adds meta messages."""
    meta_messages = []

    if part.title:
        meta_messages.append(Message.new_meta_track_name(part.title))

    meta_messages.append(
        Message.new_meta_instrument_name(instrument_get_name(part.instrument))
    )

    return meta_messages + part_to_midi(part, 0) + [Message.new_meta_end_of_track()]


# export
def export_score(score: Score, file_name: str):
    """
    Saves the given score as a midi file under the given path.

    Args:
        score(Score): A score to export
        file_name(str): The file name of the exported file. This should also
            contain the extention, usually `.mid`.
    """
    chunks = [
        header_chunk(FILE_FORMAT, len(score.parts) + 1, PPQ),
        track_chunk([Message.new_meta_tempo(bpm_to_mpqn(score.tempo))]),
    ]
    chunks.extend(map(lambda part: track_chunk(part_to_messages(part)), score.parts))

    data = reduce(lambda prev, next: prev + next, chunks, bytes())
    with open(file_name, "wb") as output:
        output.write(data)
