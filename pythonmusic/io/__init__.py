from .midi_receiver import *
from .midi_sender import *
from .midi_message import *

# Module functions
from typing import cast as _cast
from mido import get_input_names as _get_input_names  # type: ignore [reportAttributeAccessIssue]
from mido import get_output_names as _get_output_names  # type: ignore [reportAttributeAccessIssue]s


def get_midi_receivers() -> list[str]:
    """
    Returns a list of available midi ports that listen for messages.

    Depending on your platform, your system may name midi ports differently.
    Even if you pass a specific name to MidiReceiver, your system may end up
    using a slightly different name. For instance, "ExampleMidiReceiver" may show
    up as "RtMidiIn Client:ExampleMidiReceiver 128:0". Use this function to
    retrieve the valid name of your receivers etc.
    """
    return _cast(list[str], _get_output_names())


def get_midi_senders() -> list[str]:
    """
    Returns a list of available midi ports that send midi messages.

    Depending on your platform, your system may name midi ports differently.
    Even if you pass a specific name to MidiSender, your system may end up
    using a slightly different name. For instance, "ExampleMidiSender" may show
    up as "RtMidiOut Client:ExampleMidiSender 128:0". Use this function to
    retrieve the valid name of your senders etc.
    """
    return _cast(list[str], _get_input_names())
