from collections.abc import Callable
from time import sleep

from pythonmusic.music import Note, Chord, Phrase, Part, Score, PhraseElement
from pythonmusic.constants import ADAGIO as _ADAGIO
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
            return MidiSender.attach(name)
        except OSError as error:
            print("Unable to create sender. Is your port correct?")
            raise error

    @staticmethod
    def _calculate_start_time(beat: int, tempo: float) -> float:
        print(float(60 * beat) / tempo)
        return float(60 * beat) / tempo

    def play_note(
        self,
        note: Note,
        on_start: Callable[[list[MidiMessage]], None] | None = None,
        on_message: Callable[[MidiMessage, float], None] | None = None,
        on_end: Callable[[bool], None] | None = None,
    ):
        """Plays a single note on the attached midi target."""
        self._play_pe(note, _ADAGIO, 0, on_start, on_message, on_end)

    def play_chard(
        self,
        chord: Chord,
        on_start: Callable[[list[MidiMessage]], None] | None = None,
        on_message: Callable[[MidiMessage, float], None] | None = None,
        on_end: Callable[[bool], None] | None = None,
    ):
        """Plays a chord on the attached midi target."""
        self._play_pe(chord, _ADAGIO, 0, on_start, on_message, on_end)

    def play_phrase(
        self,
        phrase: Phrase,
        tempo: float = _ADAGIO,
        channel: int = 0,
        on_start: Callable[[list[MidiMessage]], None] | None = None,
        on_message: Callable[[MidiMessage, float], None] | None = None,
        on_end: Callable[[bool], None] | None = None,
    ):
        """Plays a phrase on the attached midi target."""
        ir = phrase_to_ir(phrase, start_time=0.0)
        messages = irnodes_to_midi(ir, tempo, channel)
        self._play_messages(messages, 0.0, on_start, on_message, on_end)

    def play_part(
        self,
        part: Part,
        tempo: float = _ADAGIO,
        start_beat: int = 0,
        on_start: Callable[[list[MidiMessage]], None] | None = None,
        on_message: Callable[[MidiMessage, float], None] | None = None,
        on_end: Callable[[bool], None] | None = None,
    ):
        """Plays a part on the attached midi target."""
        ir = part_to_ir(part)
        messages = irchannel_to_midi(ir, tempo)
        self._play_messages(
            messages,
            self._calculate_start_time(start_beat, tempo),
            on_start,
            on_message,
            on_end,
        )

    def play_score(
        self,
        score: Score,
        start_beat: int = 0,
        on_start: Callable[[list[MidiMessage]], None] | None = None,
        on_message: Callable[[MidiMessage, float], None] | None = None,
        on_end: Callable[[bool], None] | None = None,
    ):
        """Plays a score on the attached midi target."""
        ir = score_to_ir(score)
        messages = irfile_to_midi(ir)
        self._play_messages(
            messages,
            self._calculate_start_time(start_beat, score.tempo),
            on_start,
            on_message,
            on_end,
        )

    def _play_pe(
        self,
        pe: PhraseElement,
        tempo: float,
        channel: int,
        on_start: Callable[[list[MidiMessage]], None] | None,
        on_message: Callable[[MidiMessage, float], None] | None,
        on_end: Callable[[bool], None] | None,
    ):
        ir = pe_to_ir(pe, start_time=0.0)
        messages = irnodes_to_midi(ir, tempo, channel)
        self._play_messages(messages, 0.0, on_start, on_message, on_end)

    def _play_messages(
        self,
        messages: list[MidiMessage],
        start_at: float,
        on_start: Callable[[list[MidiMessage]], None] | None,
        on_message: Callable[[MidiMessage, float], None] | None,
        on_end: Callable[[bool], None] | None,
    ):
        # TODO: do proper sorting here, check for faster algorithms
        messages.sort(
            key=lambda message: message.time, reverse=True
        )  # sorts in decending order for fast pop

        start_time: float = start_at
        while len(messages) > 0:
            index = len(messages) - 1
            if messages[index].time < start_time:
                del messages[index]
            else:
                break

        if len(messages) == 0:
            return

        if on_start:
            on_start(messages)

        current: MidiMessage
        next: MidiMessage | None = messages.pop()  # we at least one

        try:
            while next is not None:
                current = next

                if on_message:
                    on_message(current, start_time)

                self.sender.send_message(current)

                if len(messages) > 0:
                    next = messages.pop()
                    start_time += current.time
                    # protect against negative sleep time
                    # this should not happen, but float imprecision may cause this
                    sleep_time = max(0, next.time - current.time)
                    sleep(sleep_time)
                else:
                    next = None

            if on_end:
                on_end(True)
        except KeyboardInterrupt:
            if on_end:
                on_end(False)
