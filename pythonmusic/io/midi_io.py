from os.path import abspath as _abspath

from mido import (
    MidiFile as _MidiFile,
    MidiTrack as _MidiTrack,
    MetaMessage as _MetaMessage,
    bpm2tempo as _bpm2tempo,
    second2tick as _second2tick,
)

from pythonmusic.music import Score, Part
from pythonmusic.io.ir import part_to_ir as _part_to_ir
from pythonmusic.io.ir.midi import irchannel_to_midi as _irchannel_to_midi


def export_score(score: Score, path: str):
    # FIXME: doesn't expand ~ to (on linux) /home/{user}/

    # convert path to absolute
    path = _abspath(path)

    # create mido objects
    file = _MidiFile()

    # mido uses only uses the lower component for calculating midi ticks
    # setting this to `4` will ensure this align with this library
    tempo = _bpm2tempo(score.tempo, (4, 4))

    for index, part in enumerate(score.parts):
        # create track
        track = _MidiTrack()

        # if we are on the first part, add the tempo message
        if index == 0:
            track.append(_MetaMessage("set_tempo", tempo=tempo))
            track.append(_MetaMessage("time_signature", numerator=4, denominator=4))

        # add channel and instrument track info
        channel_prefix = _MetaMessage("channel_prefix", channel=part.channel)
        track.append(channel_prefix)
        track.append(_MetaMessage("track_name", name=f"track {index}"))
        track.append(channel_prefix)
        track.append(
            _MetaMessage("instrument_name", name=part.title or f"instrument {index}")
        )

        # convert part to nodes and then midi messages
        nodes = _part_to_ir(part)
        messages = _irchannel_to_midi(nodes, score.tempo)

        # add messages to track
        for message in messages:
            tick = _second2tick(message.time, file.ticks_per_beat, tempo)
            raw_message = message.raw().copy(time=100 * (index + 1))
            track.append(raw_message)

        track.append(_MetaMessage("end_of_track"))

        file.tracks.append(track)

    file.save(filename=path)
