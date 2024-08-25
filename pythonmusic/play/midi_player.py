from typing import override

from pythonmusic.play.player import Player
from pythonmusic.io import MidiSender, MidiMessage


class MidiPlayer(Player):
    def __init__(self, target: str) -> None:
        super().__init__()
        self.target: str = target
        self.sender: MidiSender = MidiPlayer._attach_to_sender(target)

    @staticmethod
    def _attach_to_sender(name: str) -> MidiSender:
        try:
            return MidiSender.attach(name)
        except OSError as error:
            print("Unable to create sender. Is your port correct?")
            raise error

    @override
    def _play_message(self, message: MidiMessage):
        self.sender.send_message(message)
