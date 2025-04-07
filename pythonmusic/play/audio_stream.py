from abc import ABC, abstractmethod
from threading import Lock
from typing import Mapping, Optional

import pyaudio as pa

__all__ = ["AudioStream"]


class AudioStream(ABC):
    def __init__(self, channels: int, sample_rate: int, buffer_size: int, format: int):
        self._channels = channels
        self._sample_rate = sample_rate
        self._buffer_size = buffer_size
        self._format = format

        self._lock = Lock()
        self._pa = pa.PyAudio()
        self._stream = self._pa.open(
            format=self._format,
            channels=self._channels,
            rate=self._sample_rate,
            output=True,
            frames_per_buffer=self._buffer_size,
            stream_callback=self.stream_callback,
        )

    def __del__(self):
        # just to be save, define the order
        # 1 end stream
        self._stream.stop_stream()
        self._stream.close()
        del self._stream

        # 2 remove lock
        del self._lock

        # 3 terminate pa
        self._pa.terminate()

    def channels(self) -> int:
        """
        Returns the number of channels in the stream.
        """
        return self._channels

    def sample_rate(self) -> int:
        """
        Returns the sampler's sample rate.
        """
        return self._sample_rate

    def buffer_size(self) -> int:
        """
        Returns the audio stream's buffer size.
        """
        return self._buffer_size

    def format(self) -> int:
        """
        Returns the audio format for the pyaudio stream.
        """
        return self._format

    @abstractmethod
    def stream_callback(
        self,
        in_data: Optional[bytes],
        frame_count: int,
        time_info: Mapping[str, float],
        status: int,
    ) -> tuple[bytes, int]:
        """
        Defines the callback for the pyaudio audio stream.

        TODO: This needs some explanation
        """
