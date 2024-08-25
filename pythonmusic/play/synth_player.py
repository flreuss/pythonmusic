from typing import override

from pythonmusic.io import MidiMessage
from pythonmusic.synth import Synth
from pythonmusic.play.player import Player
from pythonmusic.constants.messages import (
    NOTE_ON,
    NOTE_OFF,
    CONTROL_CHANGE,
    PROGRAM_CHANGE,
    PITCHWHEEL,
)


class SynthPlayer(Player):
    def __init__(self, sound_font: str):
        super().__init__()
        self._synth = Synth(sound_font)

    def _note_on(self, message: MidiMessage):
        channel = message["channel"]
        pitch = message["note"]
        velocity = message["velocity"]
        self._synth.note_on(channel, pitch, velocity)

    def _note_off(self, message: MidiMessage):
        channel = message["channel"]
        pitch = message["note"]
        self._synth.note_off(channel, pitch)

    def _control_change(self, message: MidiMessage):
        channel = message["channel"]
        control = message["control"]
        value = message["value"]
        self._synth.set_control_change(channel, control, value)

    def _program_change(self, message: MidiMessage):
        # TODO: for midi level 2, make own format
        channel = message["channel"]
        patch = message["program"]
        bank = 0
        self._synth.set_instrument(channel, patch, bank)

    def _pitchwheel(self, message: MidiMessage):
        channel = message["channel"]
        pitch = message["pitch"]
        self._synth.set_pitchbend(channel, pitch)

    @override
    def _play_message(self, message: MidiMessage):
        # TODO: add own message type

        message_type = message.type
        if message_type == NOTE_ON:
            self._note_on(message)
        elif message_type == NOTE_OFF:
            self._note_off(message)
        elif message_type == CONTROL_CHANGE:
            self._control_change(message)
        elif message_type == PROGRAM_CHANGE:
            self._program_change(message)
        elif message_type == PITCHWHEEL:
            self._pitchwheel(message)
