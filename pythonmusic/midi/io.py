from typing import Callable, Optional

from rtmidi import MidiIn as RtMidiIn  # type: ignore
from rtmidi import MidiOut as RtMidiOut  # type: ignore

from pythonmusic.constants.messages import NOTE_OFF
from pythonmusic.midi.message import Message
from pythonmusic.util import find_pattern, find_pattern_index, user_list_prompt

__all__ = [
    "MidiIn",
    "MidiOut",
    "midi_inputs",
    "midi_outputs",
    "find_midi_input",
    "find_midi_output",
    "find_input_index",
    "find_output_index",
    "input_user_prompt",
    "output_user_prompt",
]

MIDI_CLILENT_NAME = "PythonMusic"
"""A constant that is registered with the system as midi ports' client identifyer."""


def midi_inputs() -> list[str]:
    """
    Returns a list of midi inputs on your system that can receive midi messages.

    Your operating system may impose different naming conventions for midi ports.
    If a port you have created does not show up under the direct you specified,
    try `find_input()`.
    """
    port = RtMidiOut()
    ports = port.get_ports()
    del port
    return ports


def midi_outputs() -> list[str]:
    """
    Returns a list of midi outputs on your system that can send midi messages.

    Your operating system may impose different naming conventions for midi ports.
    If a port you have created does not show up under the direct you specified,
    try `find_ouput()`.
    """
    port = RtMidiIn()
    ports = port.get_ports()
    del port
    return ports


def find_midi_input(pattern: str) -> Optional[str]:
    """
    Searches available midi inputs for the given pattern.

    This function is useful to find the system's name for a port you have
    defined, or only know a portion of.

    Args:
        pattern(str): A pattern to search for

    Returns:
        Optional[str]: The first matching midi input port, or `None` if not found
    """

    return find_pattern(pattern, midi_inputs())


def find_midi_output(pattern: str) -> Optional[str]:
    """
    Searches available midi outputs for the given pattern.

    This function is useful to find the system's name for a port you have
    defined, or only know a portion of.

    Args:
        pattern(str): A pattern to search for

    Returns:
        Optional[str]: The first matching midi output port, or `None` if not found
    """

    return find_pattern(pattern, midi_outputs())


def find_input_index(pattern: str) -> Optional[int]:
    """
    Searches available midi inputs for the given pattern and returns its port
    number.

    This function is useful to find the system's name for a port you have
    defined, or only know a portion of.

    Args:
        pattern(str): A pattern to search for

    Returns:
        Optional[str]: The index of the first matching midi input port, or `None`
            if not found
    """

    return find_pattern_index(pattern, midi_inputs())


def find_output_index(pattern: str) -> Optional[int]:
    """
    Searches available midi outputs for the given pattern.

    This function is useful to find the system's name for a port you have
    defined, or only know a portion of.

    Args:
        pattern(str): A pattern to search for

    Returns:
        Optional[str]: The index of the first matching midi output port, or `None`
            if not found
    """

    return find_pattern_index(pattern, midi_outputs())


def input_user_prompt() -> Optional[str]:
    """
    Retrieves open midi input and asks user to choose if more than one
    option is available.

    Returns:
        Optional[str]: The user's chosen port. `None` if no ports are available.
    """

    return user_list_prompt(midi_inputs())


def output_user_prompt() -> Optional[str]:
    """
    Retrieves open midi output and asks user to choose if more than one
    option is available.

    Returns:
        Optional[str]: The user's chosen output. `None` if no ports are available.
    """

    return user_list_prompt(midi_outputs())


class MidiIn:
    """
    A midi input class.

    Use this class to receive midi messages from midi output ports. Depending on
    the state of the `virtual` parameter in the initialiser, this class fulfils
    two rols:

    * If you set `virtual` to `False` (default), this class attaches to an
      existing midi output port. You need to specify the name of that output
      with the `name` parameter. Keep in mind that the system's name of midi
      devices may differ. Use `find_outputs()` to find the name of your device.

    * If `virtual` is set to `True`, this class creates a new virtual input port
      that other midi outputs can see attach to. Specify the name of the virtual
      output with the `name` parameter.

    Some midi keyboards send a zero-velocity note on instead of a note off
    message. These messages are automatially translated. To disable this, set
    `MidiIn().translate_note_off` to `False`.

    Args:
        name(str): The name of the port to host or attach to
        virtual(bool): If `True`, creates a virtual midi input port, or attaches
            to an existing output port if `False`
        translate_note_off(bool): Treat note_on with `velocity=0` as a
            note_off message
    """

    def __init__(self, name: str, virtual: bool = False):
        self._port = RtMidiIn(name=MIDI_CLILENT_NAME)
        self._name = name
        self._is_virtual = virtual
        self._callbacks: dict[int, Callable[[Message], None]] = {}
        self.translate_note_off: bool = True
        self.prints_messages = False

        assert not self._port.is_port_open()

        if virtual:
            self._port.open_virtual_port(name=name)
        else:
            port_n = find_output_index(name)
            if port_n is None:
                raise IOError("Midi device not found")
            self._port.open_port(port_n)

        # sets the callback for midi messages
        # second argument can receive any object for scope reasons, not used
        self._port.set_callback(self._callback, None)
        # disables sysex, timing, active_sense
        self._port.ignore_types()

        assert self._port.is_port_open()

    def __del__(self):
        self._port.delete()

    def is_virtual(self) -> bool:
        """
        Returns `True` if the port is virtual.
        """
        return self._is_virtual

    def port_name(self) -> str:
        """
        Returns the declared port's name.

        Depending on your platform, the actual name registered with the system
        may vary.
        """
        return self._name

    def _callback(self, input: tuple[list[int], float], _: object):
        """
        Internal handler for RtMidi callbacks.

        Calls user-registered callbacks and prints message to stdout if set.
        """
        # delta t in seconds since last received message
        bytes = bytearray(input[0])
        message = Message(bytes, 0)

        # some keybaords send a zero-velocity note on instead of note off
        # this translates
        if (
            message.type == NOTE_OFF
            and message.velocity == 0
            and self.translate_note_off
        ):
            message = Message.new_note_off(
                message.channel, message.key, 0, message.time
            )

        if self.prints_messages:
            print(message.description())

        callback = self._callbacks.get(0)
        if callback is not None:
            callback(message)

        callback = self._callbacks.get(message.type())
        if callback is not None:
            callback(message)

    def set_callback(self, event: Optional[int], callback: Callable[[Message], None]):
        """
        Registers a callback for a given message type.

        To add a callback, pass a function with a `Message` parameter and a midi
        message type:

        .. code-block:: python

            def callback(message: Message):
                ...

            midi_in.set_callback(NOTE_ON, callback)

        Keep in mind that only one callback per message type can be registered
        at the same time.

        You can also register a callback that triggers for all message types.
        This callback is separate from other callbacks and not exclusive. To set
        this callback, pass `None` as the midi event type.

        .. code-block:: python

            def callback(message: Message):
                print(message)

            midi_in.set_callback(None, callback)


        Args:
            event(Optional[int]): The midi message type, or `None` to set the
                general callback
            callback(Callable[[Message], None]): A callback
        """

        self._callbacks[event if event else 0] = callback

    def has_callback(self, event: Optional[int]) -> bool:
        """
        Returns `True` if a callback exists for the given message event. Pass
        `None` to check if the general callback is set.
        """
        return self._callbacks.get(event if event else 0) is not None

    def del_callback(self, event: Optional[int]):
        """
        Removes the callback for a given message type.
        """
        del self._callbacks[event if event else 0]

    def clear(self):
        """Removes all callbacks."""
        self._callbacks.clear()


class MidiOut:
    """
    A midi output class.

    Use this class to send midi message to midi input ports. This class has two
    modes that are set by the `virtual` parameter:

    * If `virtual` is set to `False` (default), this class attempts to attach to
      an input port with the given `name`. Keep in mind that the system's name of
      midi devices differ across platforms. Use `find_inputs()` for a list of
      available input ports.

    * If `virtual` is set to `True`, a new virtual port is creates that other
      midi inputs can attach to.  Specify the name of the new port with the
      `name` parameter.

    Args:
        name(str): The name of the port to host or attach to
        virtual(bool): If `True`, creates a virtual port, otherwise attaches to
            an existing port
    """

    def __init__(self, name: str, virtual: bool = False):
        self._port = RtMidiOut(name=MIDI_CLILENT_NAME)
        self._name = name
        self._is_virtual = virtual

        if virtual:
            self._port.open_virtual_port(name=name)
        else:
            port_n = find_input_index(name)
            if port_n is None:
                raise IOError("Midi device not found")
            self._port.open_port(port_n)

    def __del__(self):
        self._port.delete()

    def is_virtual(self) -> bool:
        """
        Returns `True` if the port is virtual.
        """
        return self._is_virtual

    def port_name(self) -> str:
        """
        Returns the declared port's name.

        Depending on your platform, the actual name registered with the system
        may vary.
        """
        return self._name

    def send_message(self, message: Message):
        """
        Sends the given message.

        The `time` parameter of messages is ignored. Messages are sent immediately.

        Args:
            message(Message): A message to send
        """

        self._port.send_message(message.raw())

    def reset(self):
        """
        Stops all playing notes and resets controller values.
        """

        def _messages() -> list[Message]:
            messages: list[Message] = []
            for channel in range(16):
                messages.append(Message.new_all_notes_off(channel))
                messages.append(Message.new_reset_controllers(channel))

            return messages

        for message in _messages():
            self.send_message(message)
