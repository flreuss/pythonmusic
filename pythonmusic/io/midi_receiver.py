from typing import Callable, Self

from mido.messages import Message as MidoMessage
from mido import open_input  # type: ignore [reportAttributeAccessIssue]
from mido.backends.rtmidi import Input as RtInput

from .midi_message import MidiMessage

__all__ = ["MidiReceiver"]

MATCH_ALL = "*"
"""A callback event that matches all events"""


class MidiReceiver:
    """
    A midi receiver object.

    Use this class to create objects that can receive midi messages. Midi
    receivers can take on two rolls.

    * A receiver that is created using its normal initialiser (``MidiReceiver()``)
      is virtual. This opens a midi port to the system under the given name and
      starts listening to incoming messages. Send messages from the dedicated
      :obj:`pythonmusic.io.MidiSender` object, DAWs, or other sources. The created
      sender may receive messages from multiple sources.

    * To create a non-virtual port, use the `attach` method of this class. This
      creates a receiver that listens to output from a specific source. Depending
      on your use case, this may be necessary to attach to a source that itself
      does not select a target, such as midi keyboards.

    You can then add callbacks to react to midi messages.

    Args:
        name (str): The name this receiver will be displayed as
        print_messages (bool): Set to `True` to print all messages into the
            console in addition to callbacks. Defaults to `False`
    """

    def __init__(
        self,
        name: str,
        print_messages: bool = False,
    ) -> None:
        self.name: str | None = name
        self._port: RtInput = open_input(
            self.name, virtual=True, callback=self._handle_message
        )
        self._callbacks: dict[str, Callable[[MidiMessage], None]] = {}
        self.prints_messages_to_stdout: bool = print_messages

    def __del__(self):
        if self.prints_messages_to_stdout:
            print(f"Closing midi receiver {self.name}")
        self.port.close()

    def _assert_open_port(self):
        """
        Panics if this receivers's port is not open.

        The `port` property is public. Closing the input manually will trigger
        a segfault if it's accessed later. This method should prevent that.
        """
        if self._port.closed:
            raise IOError(f'Port for "{self.name}" is already closed')

    @property
    def callbacks(self) -> dict[str, Callable[[MidiMessage], None]]:
        """
        All currently registered callbacks.
        """
        return self._callbacks

    @property
    def port(self) -> RtInput:
        """
        The internal port object this receiver uses.
        """
        self._assert_open_port()
        return self._port

    @classmethod
    def attach(cls, input_name: str, print_messages: bool = False) -> Self:
        """
        Attaches to the given input.

        The `input_name` parameter must refer to a valid, open midi port. You
        can check for available input by using functions defines in
        :mod:`pythonmusic.io`.
        """
        port = open_input(input_name)
        if not port:
            raise ConnectionError(f'Cannot attach to given input "{input_name}"')

        new = cls.__new__(cls)
        new.name = None
        new._port = port
        new._callbacks = {}
        new.prints_messages_to_stdout = print_messages

        # callback is set here; adding this to the initialiser clashes with the
        # `cls` property
        new.port.callback = new._handle_message

        return new

    def _handle_message(self, raw_message: MidoMessage):
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

    def has_callback(self, event: str) -> bool:
        """
        Returns `True` if a callback for the given event is registered.

        Returns:
            bool: `True` if a callback for `event` exists.
        """
        return self._callbacks.get(event) is not None

    def add_callback(
        self,
        event: str,
        callback: Callable[[MidiMessage], None],
        overwrite: bool = False,
    ):
        """
        Adds a callback for a specific event.

        Use `overwrite` to define behaviour if a callback for the given `event`
        already exists.

        The ``"*"`` event may be used to react to all incoming events.

        Example:
            >>> def my_callback(message):
            >>>     print(message.type)
            >>>
            >>> receiver = MidiReceiver("My Receiver")
            >>> receiver.add_callback("note_on", my_callback)
            >>> receiver.add_callback("*", lambda message: print(message.type))

        Args:
            event (str): The event to react to. See
                :mod:`../appendix/midi` for more information
            callback (Callable[[MidiMessage], None]): A callback function
            overwrite (bool): `True` if existing callbacks should be overwritten
                on conflict. Defaults to `False`
        """
        # TODO: explain "*"
        if not overwrite and self.has_callback(event):
            raise KeyError(
                f'A callback for event "{event}" has already been registered'
            )
        self.callbacks[event] = callback

    def remove_callback(self, event: str):
        """
        Removes the callback for the given `event`.
        """
        del self._callbacks[event]

    def clear(self):
        """
        Removes all callbacks.
        """
        self._callbacks.clear()
