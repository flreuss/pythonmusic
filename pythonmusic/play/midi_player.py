from typing import override

from .player import Player

from pythonmusic.constants import PROGRAM_CHANGE, CONTROL_CHANGE, BANK_CHANGE

from pythonmusic.io import MidiSender, MidiMessage
from pythonmusic.util import instrument_get_patch_bank

__all__ = ["MidiPlayer"]


class MidiPlayer(Player):
    """
    An implementation of a player that attaches to a midi receiver and plays
    Note, Chords, Phrases etc.

    Args:
        target (str): The output port to attach to
    """

    def __init__(self, target: str) -> None:
        super().__init__()
        self.target: str = target
        self.sender: MidiSender = MidiPlayer._attach_to_receiver(target)

    @staticmethod
    def _attach_to_receiver(name: str) -> MidiSender:
        try:
            return MidiSender.attach(name)
        except OSError as error:
            print("Unable to create sender. Is your port correct?")
            raise error

    @override
    def play_message(self, message: MidiMessage):
        """
        Plays the given midi message.

        Args:
            message (MidiMessage): A MidiMessage
        """
        self.sender.send_message(message)

    @override
    def set_instrument(self, channel: int, instrument: int):
        """
        Updates the selected instrument for a given channel.

        Sends both a program and bank change to the attached midi receiver.

        .. note:: Depends on the ``play_message()`` method.

        Args:
            channel (int): A channel for which to change the instrument for
            instrument (int): The id of the new instrument
        """
        patch, bank = instrument_get_patch_bank(instrument)
        program_change = MidiMessage(PROGRAM_CHANGE, channel=channel, program=patch)
        bank_change = MidiMessage(
            CONTROL_CHANGE, channel=channel, control=BANK_CHANGE, value=bank
        )

        self.play_message(program_change)
        self.play_message(bank_change)

    @override
    def send_cc(self, channel: int, control: int, value: int):
        """
        Send a control change message to the attached midi receiver.

        .. note:: Depends on the ``play_message()`` method.

        Args:
            channel (int): The channel for which to update the cc value
            control (int): The control id to update
            value (int): The control value to update with
        """
        self.play_message(
            MidiMessage(CONTROL_CHANGE, channel=channel, control=control, value=value)
        )
