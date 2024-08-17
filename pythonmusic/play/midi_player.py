from time import sleep

from pythonmusic.music import Note, Chord, Phrase, Part, Score, PhraseElement
from pythonmusic.constants.tempo import ADAGIO as _ADAGIO
from pythonmusic.io import MidiSender, MidiMessage
from pythonmusic.io.ir import pe_to_ir, phrase_to_ir, part_to_ir, score_to_ir
from pythonmusic.io.ir.midi import irnodes_to_midi, irchannel_to_midi, irfile_to_midi


class MidiPlayer:
    def __init__(self, target: str) -> None:
        self.target: str = target
        self.sender: MidiSender = MidiPlayer._attach_to_sender(target)

    @staticmethod
    def _attach_to_sender(name: str) -> MidiSender:
        try:
            return MidiSender(name)
        except OSError as error:
            print("Unable to create sender. Is your port correct?")
            raise error

    def play_note(self, note: Note):
        """Plays a single note on the attached midi target."""
        self._play_pe(note)

    def play_chard(self, chord: Chord):
        """Plays a chord on the attached midi target."""
        self._play_pe(chord)

    def play_phrase(self, phrase: Phrase, tempo: float = _ADAGIO, channel: int = 0):
        """Plays a phrase on the attached midi target."""
        ir = phrase_to_ir(phrase, start_time=0.0)
        messages = irnodes_to_midi(ir, tempo, channel)
        self._play_messages(messages)

    def play_part(self, part: Part, tempo: float = _ADAGIO):
        """Plays a part on the attached midi target."""
        ir = part_to_ir(part)
        messages = irchannel_to_midi(ir, tempo)
        self._play_messages(messages)

    def play_score(self, score: Score):
        """Plays a score on the attached midi target."""
        ir = score_to_ir(score)
        messages = irfile_to_midi(ir)
        self._play_messages(messages)

    def _play_pe(self, pe: PhraseElement, tempo: float = _ADAGIO, channel: int = 0):
        ir = pe_to_ir(pe, start_time=0.0)
        messages = irnodes_to_midi(ir, tempo, channel)
        self._play_messages(messages)

    def _play_messages(self, messages: list[MidiMessage]):
        if len(messages) == 0:
            return

        # TODO: do proper sorting here, check for faster algorithms
        messages.sort(
            key=lambda message: message.time, reverse=True
        )  # sorts in decending order for fast pop

        # for message in messages:
        #     print(message)
        #
        # exit()

        start_time: float = 0.0
        current: MidiMessage
        next: MidiMessage | None = messages.pop()  # we at least one

        while next is not None:
            current = next
            self.sender.send_message(current)

            if len(messages) > 0:
                next = messages.pop()
                start_time += current.time
                sleep(next.time - current.time)
            else:
                next = None
