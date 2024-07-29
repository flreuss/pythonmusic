from typing import Callable

from .midi_message import MidiMessage

from mido.messages import Message as _MidoMessage
from mido import open_input as _open_input  # type: ignore [reoportAttributeAccessIssue]
from mido.backends.rtmidi import Input as _Input


class MidiReceiver:
    """
    Midi reciever object.
    """

    def __init__(
        self,
        name: str,
        print_messages: bool = False,
    ) -> None:
        self.name: str = name
        self.port: _Input = _open_input(
            self.name, virtual=True, callback=self._handle_message
        )
        self._callbacks: dict[str, Callable[[MidiMessage], None]] = {}
        self.prints_messages_to_stdout: bool = print_messages

    def __del__(self):
        self.port.close()

    def _handle_message(self, raw_message: _MidoMessage):
        if self.prints_messages_to_stdout:
            print(f"Midi message: {raw_message.__str__()}")
        msg = MidiMessage(raw=raw_message)

    @property
    def callbacks(self) -> dict[str, Callable[[MidiMessage], None]]:
        return self.callbacks

    def has_callback_for_event(self, event: str) -> bool:
        return self._callbacks[event] is not None

    def add_callback(
        self,
        event: str,
        callback: Callable[[MidiMessage], None],
        overwrite: bool = False,
    ):
        if not overwrite and self.has_callback_for_event(event):
            raise KeyError(
                f'A callback for event "{event}" has already been registered'
            )
        self.callbacks[event] = callback

    def remove_callback(self, event: str):
        del self._callbacks[event]

    # @staticmethod
    # def get_device_names() -> list[str]:
    #     return _cast(list[str], _get_input_names())
