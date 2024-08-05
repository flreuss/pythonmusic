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
    """
    return _cast(list[str], _get_output_names())


def get_midi_senders() -> list[str]:
    """
    Returns a list of available midi ports that send midi messages.
    """
    return _cast(list[str], _get_input_names())
