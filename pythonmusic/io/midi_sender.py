from typing import Self

from mido import open_output as _open_output  # type: ignore [reportAttributeAccessIssue]
from mido.backends.rtmidi import Output as RtOutput

from .midi_message import MidiMessage


class MidiSender:
    """
    An object that can be used to send midi messages to midi input ports.
    """

    def __init__(self, name: str) -> None:
        self.name: str | None = name
        self._port: RtOutput = _open_output(name, virtual=True)

    def __del__(self):
        self.port.close()

    def _assert_open_port(self):
        """
        Panics if this sender's port is not open.

        The `port` property is public. Closing the output manually will trigger
        a segfault if it's accessed later. This method should prevent that.
        """
        if self._port.closed:
            raise IOError(f'Port for "{self.name}" is already closed')

    @property
    def port(self) -> RtOutput:
        self._assert_open_port()
        return self._port

    @classmethod
    def attach(cls, output_name: str) -> Self:
        """
        Attaches to the given output.

        The `output_name` parameter must refer to a valid, open midi port.
        Use `MidiSender.get_outputs()` to retrieve a list of open ports.
        """
        port = _open_output(output_name, virtual=False)
        if not port:
            raise ConnectionError(f'Cannot attach to given output "{output_name}"')

        new = cls.__new__(cls)
        new.name = None
        new._port = port

        return new

    def send_message(self, msg: MidiMessage):
        """
        Sends the given midi message to this sender's output.
        """
        self.port.send(msg.raw())

    def reset(self):
        """
        Sends note off and reset controller on all channels.

        Ideally, this method resets the attached midi receiver to its default
        state.
        """
        self.port.reset()

    def force_note_off(self):
        """
        Instructs the attached receiver to abort all notes. This does not reset
        controller values.
        """
        self.port.panic()
