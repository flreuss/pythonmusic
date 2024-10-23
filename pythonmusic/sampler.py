from typing import override

from pythonmusic.play import Player
from pythonmusic.io import MidiMessage

__all__ = ["AudioSample", "AudioSampler", "SamplePlayer"]


# An individual sound file that is loaded and stored inside the audio sampler
class AudioSample:
    pass


# A sampler that stores audio samples and plays them back as required by
# a note's pitch, duration, etc.
class AudioSampler:
    def __init__(self):
        # self._storage =
        pass

    def __del__(self):
        pass

    # ==== EVENTS ====
    def note_on(self, channel: int, note: int, velocity: int):
        raise NotImplemented()

    def note_off(self, channel: int, note: int, velocity: int):
        raise NotImplemented()

    def set_cc(self, channel: int, control: int, value: int):
        raise NotImplemented()

    def cc(self, channel: int, control: int) -> int:
        raise NotImplemented()

    def select_patch(self, channel: int, patch: int):
        raise NotImplemented()

    def patch(self, channel: int) -> int:
        raise NotImplemented()


# A player implementation the audio sampler
class SamplePlayer(Player):
    def __init__(self, audio_sampler: AudioSampler) -> None:
        super().__init__()

        self.audio_sampler = audio_sampler

    def _note_on(self, message: MidiMessage):
        channel = message["channel"]
        pitch = message["note"]
        velocity = message["velocity"]
        self.audio_sampler.note_on(channel, pitch, velocity)

    def _note_off(self, message: MidiMessage):
        channel = message["channel"]
        pitch = message["note"]
        self.audio_sampler.note_off(channel, pitch)

    def _control_change(self, message: MidiMessage):
        channel = message["channel"]
        control = message["control"]
        value = message["value"]
        self.audio_sampler.set_cc(channel, control, value)

    def _program_change(self, message: MidiMessage):
        channel = message["channel"]
        patch = message["program"]
        self.audio_sampler.set_instrument(channel, patch)

    def _pitchwheel(self, message: MidiMessage):
        channel = message["channel"]
        pitch = message["pitch"]
        self.audio_sampler.set_pitchbend(channel, pitch)

    @override
    def play_message(self, message: MidiMessage):
        """
        Plays the given midi message.

        Args:
            message (MidiMessage): A MidiMessage
        """
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

    @override
    def set_instrument(self, channel: int, instrument: int):
        patch, bank = instrument_get_patch_bank(instrument)
        self.audio_sampler.set_instrument(channel, patch, bank)

    @override
    def send_cc(self, channel: int, control: int, value: int):
        self.audio_sampler.set_control_change(channel, control, value)
