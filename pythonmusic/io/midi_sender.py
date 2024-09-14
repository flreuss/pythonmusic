from typing import Self

from mido import open_output  # type: ignore [reportAttributeAccessIssue]
from mido.backends.rtmidi import Output as RtOutput

from .midi_message import MidiMessage


__all__ = ["MidiSender"]


class MidiSender:
    """
    A midi sender object.

    Use this class to create objects that can send midi messages. Midi senders
    can take on two rolls.

    * A sender that is created using its normal initialiser (``MidiSender()``)
      is virtual. This opens a midi ports that other receivers on the system can
      start listening to. Receive messages using
      :obj:`pythonmusic.io.MidiReceiver`, some DAWs, or similar. The created
      sender send messages to all attached receivers.

    * To create a non-virtual port, use the `attach` method of this class. This
      creates a sender that attaches to a specific output given as the `name`
      parameter. Messages are only send to that receiver. Depending on your use
      case, this may be necessary to attach to a source that itself does not
      select a target, such as midi keyboards.

    You can then send messages using the sender.

    Args:
        name (str): The name this sender will be displayed to the system as
    """

    def __init__(self, name: str) -> None:
        self.name: str | None = name
        self._port: RtOutput = open_output(name, virtual=True)

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
        """
        Returns the raw port this sender uses internally.
        """
        self._assert_open_port()
        return self._port

    @classmethod
    def attach(cls, output_name: str) -> Self:
        """
        Attaches to the given output.

        Args:
            output_name (str): A valid system registered midi port (receiver)
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

        Args:
            msg (MidiMessage): A message to send
        """
        self.port.send(msg.raw())

    def reset(self):
        """
        Sends note off and reset controller on all channels.

        Ideally, this method resets the attached midi receiver to its default
        state.
        """
        self.port.reset()

    def force_notes_off(self):
        """
        Instructs the attached receiver to abort all notes. This does not reset
        controller values.
        """
        self.port.panic()
