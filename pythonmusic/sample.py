from abc import abstractmethod, ABC
from pathlib import Path
from typing import Mapping, Optional
from time import sleep

from pyaudio import PyAudio, Stream, paContinue
import wave


__all__ = ["AudioSample", "AudioSampler"]

CHUNK_SIZE: int = 1024


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


class _WaveSample(_Sample):
    def __init__(
        self,
        port_audio: PyAudio,
        path: Path,
    ):
        self.path = Path
        self.wave_file = wave.open(str(path.absolute()), "rb")
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
        data = self.wave_file.readframes(frame_count)
        return data, paContinue

    def reset(self):
        self.wave_file.rewind()


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

        To reset the sample, call the stop method.
        """
        self._sample.pause()

    def stop(self):
        """
        Stopps playback of the loaded audio file.
        """
        self.pause()
        self._sample.stop()


# A sampler that stores audio samples and plays them back as required by
# a note's pitch, duration, etc.
class AudioSampler:

    # a new PyAudio instance can be created (and terminated) for each audio
    # samler (docs, I guess)
    def __init__(self):
        self._pyaudio = PyAudio()
        # self._stream =

    def __del__(self):
        self._pyaudio.terminate()

    #     self.stream.stop_stream()
    #     self.stream.close()

    # ==== EVENTS ====
    def note_on(self, channel: int, note: int, velocity: int):
        raise NotImplemented()

    def note_off(self, channel: int, note: int):
        raise NotImplemented()

    def set_cc(self, channel: int, control: int, value: int):
        raise NotImplemented()

    def cc(self, channel: int, control: int) -> int:
        raise NotImplemented()

    def select_patch(self, channel: int, patch: int):
        raise NotImplemented()

    def patch(self, channel: int) -> int:
        raise NotImplemented()
