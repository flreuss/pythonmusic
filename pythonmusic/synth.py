from fluidsynth import Synth as _Synth
from pythonmusic.util import assert_range

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
