from typing import override

from .player import Player

from pythonmusic.sample import AudioSampler
from pythonmusic.io import MidiMessage
from pythonmusic.constants import NOTE_OFF, NOTE_ON


__all__ = ["SamplePlayer"]


# A player implementation the audio sampler
class SamplePlayer(Player):
    """
    A player implementation for the AudioSampler.

    .. important:: Only supports note on and off events. All other midi messages
        are ignored.

    Args:
        audio_sampler (AudioSampler): An audio sampler
    """

    def __init__(self, audio_sampler: AudioSampler) -> None:
        super().__init__()

        self.audio_sampler = audio_sampler

    def _note_on(self, message: MidiMessage):
        pitch = message["note"]
        velocity = message["velocity"]
        self.audio_sampler.note_on(pitch, velocity)

    def _note_off(self, message: MidiMessage):
        pitch = message["note"]
        self.audio_sampler.note_off(pitch)

    @override
    def play_message(self, message: MidiMessage):
        """
        Plays the given midi message.

        Args:
            message (MidiMessage): A MidiMessage
        """
        message_type = message.type
        if message_type == NOTE_ON:
            self._note_on(message)
        elif message_type == NOTE_OFF:
            self._note_off(message)
