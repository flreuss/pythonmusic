from os.path import abspath, expanduser

from mido import (
    MidiFile,
    MidiTrack,
    MetaMessage,
    bpm2tempo,
    second2tick,
)

from pythonmusic.music import Score
from pythonmusic.io.ir import part_to_ir
from pythonmusic.io.ir.midi import irchannel_to_midi

__all__ = ["export_score"]


def export_score(score: Score, path: str):
    """
    Exports the given score to a midi file.

    The given path must end on a file. The file extension should conventionally
    be `.mid`, but this is not required.

    Example:
        Creating a simple score and exporting it to a midi file.
            >>> from pythonmusic import Score, export_score
            >>> score = Score("Some Title", [], 120.0)
            >>> export_score(score, "~/Music/my_score.mid")

    Args:
        score (Score): A score
        path (str): Path to the export midi file
    """
    # convert path to absolute
    path = expanduser(path)
    path = abspath(path)

    # create mido objects
    file = MidiFile(type=1)

    # mido uses only uses the lower component for calculating midi ticks
    # setting this to `4` will ensure this align with this library
    tempo = bpm2tempo(score.tempo, (4, 4))

    for index, part in enumerate(score.parts):
        # create track
        track = MidiTrack()

        # if we are on the first part, add the tempo message
        if index == 0:
            track.append(MetaMessage("set_tempo", tempo=tempo))
            track.append(MetaMessage("time_signature", numerator=4, denominator=4))

        # add channel and instrument track info
        channel_prefix = MetaMessage("channel_prefix", channel=part.channel)
        track.append(channel_prefix)
        track.append(MetaMessage("track_name", name=f"track {index}"))
        track.append(channel_prefix)
        track.append(
            MetaMessage("instrument_name", name=part.title or f"instrument {index}")
        )

        # convert part to nodes and then midi messages
        nodes = part_to_ir(part)
        messages = irchannel_to_midi(nodes, score.tempo)
        messages.sort(key=lambda message: message.time, reverse=False)

        # add messages to track
        last_tick = 0
        for message in messages:
            tick = second2tick(message.time, file.ticks_per_beat, tempo)
            delta_tick = tick - last_tick
            last_tick = tick

            raw_message = message.raw().copy(time=delta_tick)
            track.append(raw_message)

        track.append(MetaMessage("end_of_track"))

        file.tracks.append(track)

    file.save(filename=path)
