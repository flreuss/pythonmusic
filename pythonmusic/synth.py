from typing import override

from fluidsynth import Synth as _Synth

from pythonmusic.util import assert_range
from pythonmusic.io import MidiMessage
from pythonmusic.play.player import Player
from pythonmusic.constants.messages import (
    NOTE_ON,
    NOTE_OFF,
    CONTROL_CHANGE,
    PROGRAM_CHANGE,
    PITCHWHEEL,
)

# TODO: surpress ALSA messages on Linux


class Synth:
    def __init__(self, sound_font: str):
        synth = _Synth()
        synth.start()
        font_id = synth.sfload(sound_font)

        self._synth = synth
        self._font_id = font_id
        self._font_path = sound_font

    def __del__(self):
        self._synth.sfunload(self._font_id)
        self._synth.delete()

    @property
    def current_sound_font(self) -> str:
        """Returns the currently loaded sound font."""
        return self._font_path

    # Note events
    def note_on(self, channel: int, pitch: int, velocity: int):
        """Sends a note on message to the synth."""
        self._synth.noteon(channel, pitch, velocity)

    def note_off(self, channel: int, pitch: int):
        """Sends a note off message to the synth."""
        self._synth.noteoff(channel, pitch)
        self._synth.program_select

    # CC Values
    def set_control_change(self, channel: int, control: int, value: int):
        """Sets the control change value for a channel on the given `control`."""
        self._synth.cc(channel, control, value)

    def control_change(self, channel: int, control: int) -> int:
        """Returns the control change value for a channel on the given `control`."""
        return self._synth.get_cc(channel, control)

    # Pitchbend
    def set_pitchbend(self, channel: int, value: int):
        """
        Sets the pitch bend on the synth.

        This value must be in bounds of `8192` to `-8192` (4 semitones), where
        one semitone is `+/- 2048` respectively.
        """
        MAX = 8192
        assert_range(value, -MAX, MAX)

        self._synth.pitch_bend(channel, value)

    # Select instrument
    def set_instrument(self, channel: int, patch: int, bank: int):
        """
        Sets the instrument for the given channel.
        """
        # TODO: add level 2

        self._synth.program_select(channel, self._font_id, bank, patch - 1)
        # self._synth.program_change(channel, patch)

    # TODO: get instrument

    # Effects
    def set_reverb(
        self,
        size: float | None = None,
        damping: float | None = None,
        width: float | None = None,
        level: float | None = None,
    ):
        """
        Updates parameters of synth's reverb.

        `size`, `damping`, and `level` range from `0.0` to `1.0`, `width` ranges
        from `0.0` to `100.0`.
        """
        self._synth.set_reverb(
            size or -1.0, damping or -1.0, width or -1.0, level or -1.0
        )

    def reset_reverb(self):
        """Rests reverb to default values."""
        self.set_reverb(0.0, 0.0, 0.0, 0.0)

    # def set_chorus(self):
    #     self._synth.set_chorus()


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
