from typing import override
from os.path import abspath, expanduser

from fluidsynth import Synth as FSynth

from pythonmusic.util import assert_range
from pythonmusic.io import MidiMessage
from pythonmusic.play import Player
from pythonmusic.constants.messages import (
    NOTE_ON,
    NOTE_OFF,
    CONTROL_CHANGE,
    PROGRAM_CHANGE,
    PITCHWHEEL,
)

__all__ = ["Synth", "SynthPlayer"]


class Synth:
    """
    A synth object that can load and play SoundFont2 libraries.

    .. note:: On Linux using ALSA, you may encounter various error messages reporting that
        some playback devices have not been found. This is normal as ALSA checks for
        multiple output sources that may not exist. As long as audio can be heard,
        you can ignore these messages.

    Args:
        sound_font (str): Path to a SoundFont2 compatible library
    """

    def __init__(self, sound_font: str):
        path = abspath(sound_font)
        path = expanduser(path)

        synth = FSynth()
        synth.start()
        font_id = synth.sfload(path)

        self._synth = synth
        self._font_id = font_id
        self._font_path = path

    def __del__(self):
        self._synth.sfunload(self._font_id)
        self._synth.delete()

    @property
    def current_sound_font(self) -> str:
        """The currently loaded sound font."""
        return self._font_path

    # Note events
    def note_on(self, channel: int, pitch: int, velocity: int):
        """
        Sends a note on message to the synth.

        Args:
            channel (int): The channel to send the message to
            pitch (int): The pitch of the note
            velocity (int): The velocity of the note
        """
        self._synth.noteon(channel, pitch, velocity)

    def note_off(self, channel: int, pitch: int):
        """
        Sends a note off message to the synth.

        Args:
            channel (int): The channel to send the message to
            pitch (int): The note's pitch
        """
        self._synth.noteoff(channel, pitch)
        self._synth.program_select

    # CC Values
    def set_control_change(self, channel: int, control: int, value: int):
        """
        Sets the control change value for a channel on the given `control`.

        Args:
            channel (int): The channel to send the message to
            control (int): Control id for the event
            value (int): The control event's value
        """
        self._synth.cc(channel, control, value)

    def control_change(self, channel: int, control: int) -> int:
        """
        Returns the control change value for a channel on the given `control`.

        Args:
            channel (int): The channel for which to check
            control (int): The control id for which to check

        Returns:
            int: Value of control on the requested channel
        """
        return self._synth.get_cc(channel, control)

    # Pitchbend
    def set_pitchbend(self, channel: int, value: int):
        """
        Sets the pitch bend on the synth.

        This value must be in bounds of `8192` to `-8192` (4 semitones), where
        one semitone is `+/- 2048` respectively.

        Args:
            channel (int): The channel to send the message to
            value (int): The value of the pitch bend in range -2048 to 2028
        """
        MAX = 8192
        assert_range(value, -MAX, MAX)

        self._synth.pitch_bend(channel, value)

    # Select instrument
    def set_instrument(self, channel: int, patch: int, bank: int):
        """
        Sets the instrument for the given channel.

        Args:
            channel (int): The channel to send the message to
            patch (int): The patch value of the instrument
            bank (int): the bank value of the instrument
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
        Updates parameters of the synth's reverb.

        `size`, `damping`, and `level` range from `0.0` to `1.0`, `width` ranges
        from `0.0` to `100.0`.

        Args:
            size (float): The size of the reverb in range from 0.0 to 1.0
            damping (float): The damping of the reverb in range from 0.0 to 1.0
            width (float): The width of the reverb in range from 0.0 to 100.0
            level (float): The level of the reverb in range from 0.0 to 1.0
        """
        self._synth.set_reverb(
            size or -1.0, damping or -1.0, width or -1.0, level or -1.0
        )

    def reset_reverb(self):
        """Rests reverb to default values."""
        self.set_reverb(0.0, 0.0, 0.0, 0.0)


class SynthPlayer(Player):
    """
    A player implementation for the :obj:`pythonmusic.synth.Synth` object.

    .. note:: On Linux using ALSA, you may encounter various error messages reporting that
        some playback devices have not been found. This is normal as ALSA checks for
        multiple output sources that may not exist. As long as audio can be heard,
        you can ignore these messages.

    Args:
        sound_font (str): Path to a SoundFont2 compatible library
    """

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
    def play_message(self, message: MidiMessage):
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
