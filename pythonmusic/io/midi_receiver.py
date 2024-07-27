from typing import cast as _cast
from mido.messages import Message as _MidoMessage
from .midi_message import Message
from mido import open_port as _open_port, get_input_names as _get_input_names


class MidiReceiver:
    def __init__(self, name: str) -> None:
        self.name: str = name
        self.port:  = mido.open_input(
            self.name, virtual=True, callback=self._handle_message_in
        )
        self.prints_messages_to_stdout: bool = False

    def __del__(self):
        self.port.close()

    def _handle_message_int(self, raw_message: _MidoMessage):
        pass
        

    def on_message(self, message: Message):
        pass

    @staticmethod
    def get_device_names() -> list[str]:
        return _cast(list[str], _get_input_names())
