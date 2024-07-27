from typing import cast as _cast
from mido import open_output as _open_output, get_output_names as _get_output_names


class MidiSender:
    def __init__(self) -> None:
        self.port = _open_output("")

    def __del__(self):
        self.port.close()

    @staticmethod
    def get_names() -> list[str]:
        return _get_output_names()
