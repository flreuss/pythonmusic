from abc import abstractmethod, ABC
from pathlib import Path
from typing import Mapping, Optional, Union, cast
from time import sleep
import numpy as np

from pyaudio import PyAudio, Stream, paContinue
import wave

from pythonmusic.constants.dynamics import MF
from pythonmusic.util import assert_range

# TODO: look into [pydub](https://github.com/jiaaro/pydub?tab=readme-ov-file#installation)
# not really maintained and undocumented, but easier to work with


__all__ = ["AudioSample", "AudioSampler"]

WAVE_CHUNK_SIZE: int = 1024
"""
Size of chunk in read audio file
"""


class UnsupportedAudioFormatError(Exception):
    """
    An error that is raised if :obj:`AudioSample <pythonmusic.sample.AudioSample>`
    attempts to load an unsuppoprted audio format.
    """

    pass


class _Sample(ABC):
    """
    An abstract class that defines a common interface for all audio format sample
    classes.
    """

    @abstractmethod
    def stream(self) -> Stream: ...

    @abstractmethod
    def reset(self): ...

    def is_playing(self) -> bool:
        return self.stream().is_active()

    def play(self):
        self.stream().start_stream()

    def pause(self):
        self.stream().stop_stream()

    def stop(self):
        self.stream().stop_stream()
        self.reset()

    @abstractmethod
    def volume(self) -> int: ...

    @abstractmethod
    def set_volume(self, value: int): ...

    @abstractmethod
    def signal_end(self): ...


class _WaveSample(_Sample):
    def __init__(
        self,
        port_audio: PyAudio,
        path: Path,
    ):
        self.path = Path
        self.wave_file = wave.open(str(path.absolute()), "rb")
        self.multiplyer = 1.0
        self.falloff: Optional[int] = None

        # stored to prevent unnecessary lookups
        self.bits = self.wave_file.getsampwidth() * 8
        self.frame_rate = self.wave_file.getframerate()

        self._stream = port_audio.open(
            format=port_audio.get_format_from_width(self.wave_file.getsampwidth()),
            channels=self.wave_file.getnchannels(),
            rate=self.wave_file.getframerate(),
            output=True,
            stream_callback=self.callback,
        )

        # prevent stream from starting immediately
        self._stream.stop_stream()

    def __del__(self):
        self.wave_file.close()
        self._stream.stop_stream()
        self._stream.close()

    def stream(self) -> Stream:
        return self._stream

    def callback(
        self,
        in_data: Optional[bytes],
        frame_count: int,
        time_info: Mapping[str, float],
        status: int,
    ) -> tuple[bytes, int]:
        # read data
        data = self.wave_file.readframes(frame_count)

        # determine array type (may do damage idk)
        conv_type = np.int16 if self.bits == 16 else np.int8

        # convert to np array
        np_array = np.frombuffer(data, conv_type)

        # multiply to change volume
        multiplyer = self.multiplyer
        if self.falloff is not None:
            if self.falloff <= 0:
                self.falloff = None
                self.wave_file.rewind()
                return bytes(), paContinue

            ratio = self.falloff / self.frame_rate
            multiplyer *= ratio
            self.falloff -= frame_count

        np_array = np_array * multiplyer

        # clip range to avoid over-/underflow
        np_array.clip(-32768, 32767)

        # convert back to bytes object
        data = np_array.astype(np.int16).tobytes()

        return data, paContinue

    def reset(self):
        self.wave_file.rewind()

    def volume(self) -> int:
        return round(self.multiplyer * 127.0)

    def set_volume(self, value: int):
        self.multiplyer = float(value) / 127.0

    def signal_end(self):
        # yes, this is totally random
        self.falloff = 15_000


# An individual sound file that is loaded and stored inside the audio sampler
class AudioSample:
    """
    Contains an external audio file that can be played back.

    Currently supported formates are:
    - *.wav
    """

    def __init__(self, file_path: str):
        self._path = Path(file_path)
        self._port_audio = PyAudio()
        self._sample: _Sample = self._load_audio_file()
        self._is_playing: bool = False
        self._volume: int = MF

    def __del__(self):
        # stream closes on del of sample
        self._port_audio.terminate()

    def _load_audio_file(self) -> _Sample:
        # check if file exists
        if not self._path.is_file:
            raise FileNotFoundError(f"No file found at {self._path.absolute()}")

        # check for extension
        extension = self._path.suffix
        if extension == ".wav":
            return _WaveSample(self._port_audio, self._path)
        # elif extension == "mp3": ...
        # add more extension here, when supported

        # if extension not handled, it is not supported
        raise UnsupportedAudioFormatError(
            f'Audio format with extension "{extension}" is not supported.'
        )

    def is_playing(self) -> bool:
        """
        Returns `True` if the player is currently playing.
        """
        return self._sample.is_playing()

    def play(self, block: bool = True):
        """
        Starts playback of the loaded audio file.

        .. imporant:: When using non-blocking playback, you may need to manually
            reset the audio sample. Call
            :meth:`stop() <pythonmusic.sample.AudioSample.stop>` to do so.

        Args:
            block (bool): If `True`, blocks until playback is complete
        """
        self._sample.play()

        if block:
            while self.is_playing():
                sleep(0.001)
            self.stop()

    def loop(self, count: Optional[int] = None):
        """
        Loops the loaded audio sample. If a `count` is provided, stops after
        the `count` loops.

        Blocks until playback is complete.

        Args:
            count (Optional[int]): Number of loops. If `None`, loops continuously.
        """
        # do not play if count is <= 0
        if count is not None and count <= 0:
            return

        # stop running playbacks
        if self.is_playing():
            self._sample.stop()

        if count is None:
            while True:
                self.play()
        else:
            for _ in range(count):
                self.play()

    def pause(self):
        """
        Pauses playback. Can be resumed later.

        To reset the sample, call the rewind method.
        """
        self._sample.pause()

    def falloff(self):
        """
        Stops playback of the loaded audio file. Allows for a short fall off to
        prevent cut off.

        This does not reset the sample.
        """
        self._sample.signal_end()

    def stop(self):
        """
        Stopps playback of the loaded audio file.
        """
        self.pause()
        self._sample.stop()

    def volume(self) -> int:
        """
        Returns the sample's volume in range from 0 to 127.

        Returns:
            int: The volume of the sample
        """
        return self._sample.volume()

    def set_volume(self, value: int):
        """
        Sets the sample's volume.

        .. important:: The given value must be in range from 0 to 127.

        Args:
            value(int): An int in range from 0 to 127
        """
        assert_range(value, 0, 127)
        self._sample.set_volume(value)


# A sampler that stores audio samples and plays them back as required by
# a note's pitch, duration, etc.
class AudioSampler:

    # a new PyAudio instance can be created (and terminated) for each audio
    # samler (docs, I guess)
    def __init__(self):
        self._samples: list[Optional[AudioSample]] = [None] * 128

    def add_sample(self, sample: AudioSample, notes: Union[int, list[int]]):
        """
        Registers a sample to a note pitch value or values.

        The given note pitches must be in range from 0 to 127 (included).

        Args:
            sample (AudioSample): An audio sample
            notes (int | list[int]): Either an int which represents the pitch
                value to add the sample to, or a list of ints, in which case, the
                sample will be added to all pitches
        """
        if type(notes) == int:
            self._samples[notes] = sample
        else:  # crash if wrong error
            notes = cast(list[int], notes)
            for note in notes:
                self._samples[note] = sample

    def clear_sample(self, note: int) -> Optional[AudioSample]:
        """
        Removes the audio sample from the given note pitch and returns it.

        Args:
            note (int): The note pitch to remove the sample from

        Returns:
            Optional[AudioSample]: The removed audio sample, or `None` if no
                sample was registered for the given pitch
        """
        sample = self._samples[note]
        self._samples[note] = None
        return sample

    def has_sample(self, note: int) -> bool:
        """
        Returns `True` if a sample for the given note pitch has been registered.

        Args:
            note (int): A note pitch

        Returns:
            bool: `True` if a sample has been registered for the given pitch
        """
        return self._samples[note] is not None

    def get_sample(self, note: int) -> Optional[AudioSample]:
        """
        Returns the registered AudioSample for the given pitch, if any.

        Args:
            note (int): A note pitch

        Returns:
            Optional[AudioSample]: The audio sample for the given pitch, or
                `None`, if none has been registered
        """
        return self._samples[note]

    # ==== EVENTS ====
    def note_on(self, note: int, velocity: int):
        sample = self._samples[note]
        if sample is not None:
            sample.stop()
            sample.set_volume(velocity)
            sample.play(block=False)

    def note_off(self, note: int):
        sample = self._samples[note]
        if sample is not None:
            sample.falloff()
