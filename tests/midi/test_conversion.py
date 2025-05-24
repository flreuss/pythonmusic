import unittest

from pythonmusic.constants import PPQ
from pythonmusic.constants.control_change import BANK_CHANGE, CHANNEL_PAN
from pythonmusic.constants.panning import PAN_CENTER
from pythonmusic.midi.convert import (
    merge_messages,
    part_to_midi,
    pe_to_midi,
    phrase_to_midi,
    score_to_midi,
)
from pythonmusic.midi.message import Message
from pythonmusic.music import Chord, Note, Part, Phrase, Score


class MidiConversionTests(unittest.TestCase):

    def test_merge_messages(self):
        channel = 0
        velocity = 10
        a = [
            Message.new_note_on(channel, 2, velocity, 1),  # 1
            Message.new_note_on(channel, 3, velocity, 4),  # 5
            Message.new_note_on(channel, 5, velocity, 5),  # 10
            Message.new_note_on(channel, 6, velocity, 2),  # 12
            Message.new_note_on(channel, 7, velocity, 3),  # 15
        ]

        b = [
            Message.new_note_on(channel, 1, velocity, 0),  # 0
            Message.new_note_on(channel, 4, velocity, 6),  # 6
            Message.new_note_on(channel, 8, velocity, 10),  # 16
        ]

        r = merge_messages(a, b)

        for i in range(len(r)):
            self.assertEqual(r[i].key, i + 1)

        a = [
            Message.new_note_on(channel, 1, velocity, 0),  # 0
            Message.new_note_off(channel, 1, velocity, 10),  # 10
            Message.new_note_on(channel, 2, velocity, 5),  # 15
            Message.new_note_off(channel, 2, velocity, 30),  # 45
        ]

        b = [
            Message.new_note_on(channel, 3, velocity, 5),  # 5
            Message.new_note_off(channel, 3, velocity, 12),  # 17
            Message.new_note_on(channel, 4, velocity, 10),  # 27
            Message.new_note_off(channel, 4, velocity, 5),  # 32
        ]

        er = [
            Message.new_note_on(channel, 1, velocity, 0),  # 0
            Message.new_note_on(channel, 3, velocity, 5),  # 5
            Message.new_note_off(channel, 1, velocity, 5),  # 10
            Message.new_note_on(channel, 2, velocity, 5),  # 15
            Message.new_note_off(channel, 3, velocity, 2),  # 17
            Message.new_note_on(channel, 4, velocity, 10),  # 27
            Message.new_note_off(channel, 4, velocity, 5),  # 32
            Message.new_note_off(channel, 2, velocity, 13),  # 45
        ]

        self.assertEqual(merge_messages(a, b), er)

    def test_pe_conversion(self):
        a = Note(30, 1.0, 10)

        t_on = Message.new_note_on(0, 30, 10, 0)
        t_off = Message.new_note_off(0, 30, 10, round(PPQ * 1.0 * 0.9))

        self.assertEqual(pe_to_midi(a, 0, 0), ([t_on, t_off], 960))

        b = Chord([Note(30, 1.0, 10), Note(31, 1.0, 10)])
        chord_messages, chord_frame = pe_to_midi(b, 0, 0)

        self.assertEqual(chord_frame, round(PPQ * 1.0))
        self.assertEqual(
            chord_messages,
            [
                Message.new_note_on(0, 30, 10, 0),
                Message.new_note_on(0, 31, 10, 0),
                Message.new_note_off(0, 30, 10, 86),
                Message.new_note_off(0, 31, 10, 0),
            ],
        )

        c = Note.rest(1.0)
        self.assertEqual(pe_to_midi(c, 0, 0), ([], 96))

        d = Chord(
            [
                Note.rest(3.0),
                Note(10, 2.0, 10),
                Note(12, 1.0, 10),
            ]
        )

        chord_messages, chord_frame = pe_to_midi(d, 0, 10)
        self.assertEqual(chord_frame, round(PPQ * 3.0))
        self.assertEqual(
            chord_messages,
            [
                Message.new_note_on(0, 10, 10, 10),
                Message.new_note_on(0, 12, 10, 0),
                Message.new_note_off(0, 12, 10, 86),
                Message.new_note_off(0, 10, 10, 87),
            ],
        )

    def test_phrase_conversion(self):
        phrase = Phrase(
            [
                Note(60, 1.0, 10),
                Chord(
                    [
                        Note(40, 1.0, 10),
                        Note(50, 2.0, 10),
                        Note(60, 1.0, 10),
                    ]
                ),
                Note(60, 1.0, 10),
            ]
        )

        phrase_messages, phrase_frame = phrase_to_midi(phrase, 0, 20)
        self.assertEqual(phrase_frame, round(PPQ * 4.0))
        self.assertEqual(
            phrase_messages,
            [
                Message.new_note_on(0, 60, 10, 20),
                Message.new_note_off(0, 60, 10, 864),
                Message.new_note_on(0, 40, 10, 96),
                Message.new_note_on(0, 50, 10, 0),
                Message.new_note_on(0, 60, 10, 0),
                Message.new_note_off(0, 40, 10, 864),
                Message.new_note_off(0, 60, 10, 0),
                Message.new_note_off(0, 50, 10, 864),
                Message.new_note_on(0, 60, 10, 192),
                Message.new_note_off(0, 60, 10, 864),
            ],
        )

    def test_part_conversion(self):
        part = Part(0, "A title")

        part.add_phrase(
            Phrase(
                [
                    Note(60, 1.0, 10),
                    Chord(
                        [
                            Note(40, 1.0, 10),
                            Note(50, 2.0, 10),
                            Note(60, 1.0, 10),
                        ]
                    ),
                    Note(60, 1.0, 10),
                ]
            ),
            2.0,
        )

        # part.add_phrase(Pharse())

        messages = part_to_midi(part, 0)
        self.assertEqual(
            messages,
            [
                Message.new_program_change(0, 0, 0),
                Message.new_control_change(0, BANK_CHANGE, 0, 0),
                Message.new_control_change(0, CHANNEL_PAN, PAN_CENTER, 0),
                Message.new_note_on(0, 60, 10, 1920),
                Message.new_note_off(0, 60, 10, 860),
                Message.new_note_on(0, 40, 10, 100),
                Message.new_note_on(0, 50, 10, 0),
                Message.new_note_on(0, 60, 10, 0),
                Message.new_note_off(0, 40, 10, 860),
                Message.new_note_off(0, 60, 10, 0),
                Message.new_note_off(0, 50, 10, 870),
                Message.new_note_on(0, 60, 10, 190),
                Message.new_note_off(0, 60, 10, 860),
            ],
        )

    def test_score_conversion(self):
        part_a = Part(0, "A")
        part_a.add_phrase(Phrase([Note(60, 1.0, 10), Note(61, 1.0, 10)]), 1.0)
        msg_a = [
            Message.new_note_on(0, 60, 10, 960),
            Message.new_note_off(0, 60, 10, 864),
            Message.new_note_on(0, 61, 10, 96),
            Message.new_note_off(0, 61, 10, 864),
        ]

        part_b = Part(1, "B")
        part_b.add_phrase(Phrase([Note(60, 4.0, 10), Note(70, 1.0, 10)]), 15.0)
        msg_b = [
            Message.new_note_on(1, 60, 10, 14400),
            Message.new_note_off(1, 60, 10, 3456),
            Message.new_note_on(1, 70, 10, 384),
            Message.new_note_off(1, 70, 10, 864),
        ]

        score = Score("Another title", [part_a, part_b])
        messages = score_to_midi(score, 0)

        self.assertTrue(len(messages) != 0)

        self.assertEqual(messages[0][3:], msg_a)
        self.assertEqual(messages[1][3:], msg_b)

    # FIXME: legato is disabled, fix
    # def test_convert_with_legato_simple(self):
    #     notes = legato(Note(60, 2.0, 10), Note(62, 1.0, 10), Note(63, 1.0, 10))
    #     phrase = Phrase(notes)
    #     messages = phrase_to_midi(phrase, 0, 0)[0]
    #
    #     for index, compare in enumerate([60, 62, 60, 63, 62, 63]):
    #         self.assertEqual(messages[index].key, compare)
