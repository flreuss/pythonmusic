from .midi_receiver import *
from .midi_sender import *
from .midi_message import *
from .midi_io import *

# does not import ir

# Module functions
from typing import cast, Optional

from mido import get_input_names  # type: ignore [reportAttributeAccessIssue]
from mido import get_output_names  # type: ignore [reportAttributeAccessIssue]s

__all__ = [
    "get_midi_receivers",
    "get_midi_senders",
    "find_midi_receiver",
    "find_midi_sender",
    "export_score",
    "MidiMessage",
    "RawMessage",
    "MidiReceiver",
    "MidiSender",
]

# reg. tests:
# these functions are not all tested directly because they rely on connected midi
# devices


def get_midi_receivers() -> list[str]:
    """
    Returns a list of available midi ports that listen for messages.

    Depending on your platform, your system may name midi ports differently.
    Even if you pass a specific name to MidiReceiver, your system may end up
    using a slightly different name. For instance, "ExampleMidiReceiver" may show
    up as "RtMidiIn Client:ExampleMidiReceiver 128:0". Use this function to
    retrieve the valid name of your receivers etc.

    Returns:
        list[str]: A list of available midi receivers
    """
    return cast(list[str], get_output_names())


def get_midi_senders() -> list[str]:
    """
    Returns a list of available midi ports that send midi messages.

    Depending on your platform, your system may name midi ports differently.
    Even if you pass a specific name to MidiSender, your system may end up
    using a slightly different name. For instance, "ExampleMidiSender" may show
    up as "RtMidiOut Client:ExampleMidiSender 128:0". Use this function to
    retrieve the valid name of your senders etc.

    Returns:
        list[str]: A list of available midi senders
    """
    return cast(list[str], get_input_names())


def _find_pattern(input: list[str], pattern: str) -> Optional[str]:
    # if list is empty, return None
    if len(input) == 0:
        return None

    # iterate over the given inputs and check if string is contained
    for s_string in input:
        if pattern in s_string:
            return s_string

    # pattern not matched in list, return None
    return None


def find_midi_receiver(name: str) -> Optional[str]:
    """
    Searches the output of `get_midi_receivers` for the first item that contains
    or equals to the given string.

    This function may be necessary to dynamically find the name of a midi
    receiver on certain platforms. Not all platforms guarantee that the
    receiver's given name is used on a system level.

    Args:
        name (str): A device name to search for

    Returns:
        Optional[str]: The prot name that contains the given name, or `None` if
            none are found
    """
    return _find_pattern(get_midi_receivers(), name)


def find_midi_sender(name: str) -> Optional[str]:
    """
    Searches the output of `get_midi_senders` for the first item that contains or
    equals to the given string.

    This function may be necessary to dynamically find the name of a midi sender
    on certain platforms. Not all platforms guarantee that the sender's given
    name is used on a system level.

    Args:
        name (str): A device name to search for

    Returns:
        Optional[str]: The port name that contains the given name, or `None` if
            none are found
    """
    return _find_pattern(get_midi_senders(), name)
