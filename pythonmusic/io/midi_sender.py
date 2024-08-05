from typing import Self, cast as _cast

from mido.messages import Message as _Midomessage
from mido import open_output as _open_output  # type: ignore [reportAttributeAccessIssue]
from mido.backends.rtmidi import Output as _Output

from .midi_message import MidiMessage


class MidiSender:
    """
    An object that can be used to send midi messages to midi input ports.
    """

    def __init__(self, name: str) -> None:
        self.name: str | None = name
        self.port: _Output = _open_output(name)

    def __del__(self):
        self.port.close()

    @classmethod
    def attach(cls, output_name: str) -> Self:
        """
        Attaches to the given output.

        The `output_name` parameter must refer to a valid, open midi port.
        Use `MidiSender.get_outputs()` to retrieve a list of open ports.
        """
        port = _open_output(output_name)
        if not port:
            raise ConnectionError(f'Cannot attach to given output "{output_name}"')

        new = cls.__new__(cls)
        new.name = None
        new.port = port

        return new

    def send_message(self, msg: MidiMessage):
        """
        Sends the given midi message to this sender's output.
        """
        self.port.send(msg.raw())
