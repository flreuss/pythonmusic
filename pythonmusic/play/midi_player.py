from pythonmusic.io import MidiSender, MidiMessage
from pythonmusic.music import Note, Phrase, Part, Score


class MidiPlayer:
    def __init__(self, target: str) -> None:
        self.target: str = target

        try:
            self.sender = MidiSender(target)
        except OSError as error:
            print("Unable to create sender. Is your port correct?")
            raise error

    def play_note(self, note: Note):
        pass
