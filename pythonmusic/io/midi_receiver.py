from typing import Callable, Self, cast as _cast

from mido.messages import Message as _MidoMessage
from mido import open_input as _open_input  # type: ignore [reportAttributeAccessIssue]
from mido.backends.rtmidi import Input as _Input

from .midi_message import MidiMessage

MATCH_ALL = "*"
"""A callback event that matches all events"""


class MidiReceiver:
    """
    Midi reciever object.
    """

    def __init__(
        self,
        name: str,
        print_messages: bool = False,
    ) -> None:
        self.name: str | None = name
        self.port: _Input = _open_input(
            self.name, virtual=True, callback=self._handle_message
        )
        self._callbacks: dict[str, Callable[[MidiMessage], None]] = {}
        self.prints_messages_to_stdout: bool = print_messages

    def __del__(self):
        if self.prints_messages_to_stdout:
            print(f"Closing midi receiver {self.name}")
        self.port.close()

    @classmethod
    def attach(cls, input_name: str, print_messages: bool = False) -> Self:
        """
        Attaches to the given input.

        The `input_name` parameter must refer to a valid, open midi port.
        Use `MidiReceiver.get_inputs()` to retrieve a list of open ports.
        """
        port = _open_input(input_name)
        if not port:
            raise ConnectionError(f'Cannot attach to given input "{input_name}"')

        new = cls.__new__(cls)
        new.name = None
        new.port = port
        new._callbacks = {}
        new.prints_messages_to_stdout = print_messages

        # callback is set here; adding this to the initialiser clashes with the
        # `cls` property
        new.port.callback = new._handle_message

        return new

    def _handle_message(self, raw_message: _MidoMessage):
        if self.prints_messages_to_stdout:
            print(f"Midi message: {raw_message.__str__()}")

        # retrieve callbacks for event
        event = raw_message.type  # type: ignore [reportAttributeAccessIssue]
        star_callback = self._callbacks.get(MATCH_ALL)
        spec_callback = self._callbacks.get(event)

        # if any callbacks exist wrap raw message and call callbacks
        if star_callback or spec_callback:
            msg = MidiMessage.from_raw(raw_message)
            if star_callback:
                star_callback(msg)
            if spec_callback:
                spec_callback(msg)

    @property
    def callbacks(self) -> dict[str, Callable[[MidiMessage], None]]:
        return self._callbacks

    def has_callback(self, event: str) -> bool:
        return self._callbacks.get(event) is not None

    def add_callback(
        self,
        event: str,
        callback: Callable[[MidiMessage], None],
        overwrite: bool = False,
    ):
        # TODO: explain "*"
        if not overwrite and self.has_callback(event):
            raise KeyError(
                f'A callback for event "{event}" has already been registered'
            )
        self.callbacks[event] = callback

    def remove_callback(self, event: str):
        del self._callbacks[event]
