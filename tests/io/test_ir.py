import unittest
from typing import cast
from math import floor

from pythonmusic.io.ir import (
    pe_to_ir,
    phrase_to_ir,
    part_to_ir,
    score_to_ir,
    IrNote,
    IrProgramChange,
    IrControlChange,
    IrNode,
    IrTempo,
)
from pythonmusic.music import Note, Chord, Phrase, Part, Score
from pythonmusic.constants import *
from pythonmusic.util import instrument_get_patch_bank, mspb_to_bpm


class IrEncodeTests(unittest.TestCase):
    def test_encode_note(self):
        start_time = 45.2
        note = Note(C4, QUARTER_NOTE, MF, [])
        nodes = pe_to_ir(note, start_time)

        self.assertEqual(len(nodes), 1)

        node = nodes[0]
        self.assertIsInstance(node.payload, IrNote)
        payload = cast(IrNote, node.payload)

        self.assertEqual(node.time, start_time)
        self.assertEqual(payload.note, C4)
        self.assertEqual(payload.velocity, MF)
        self.assertEqual(payload.duration, QUARTER_NOTE * 0.90)

    def test_encode_note_articulations(self):
        # durations
        payload = cast(IrNote, pe_to_ir(Note(C4, 1.0, MF, []), 0.0)[0].payload)
        self.assertEqual(payload.duration, 0.90)

        payload = cast(IrNote, pe_to_ir(Note(C4, 1.0, MF, [STACCATO]), 0.0)[0].payload)
        self.assertEqual(payload.duration, 0.50)

        payload = cast(
            IrNote,
            pe_to_ir(Note(C4, 1.0, MF, [STACCATISSIMO, STACCATO]), 0.0)[0].payload,
        )
        self.assertEqual(payload.duration, 0.25)

        payload = cast(
            IrNote, pe_to_ir(Note(C4, 1.0, MF, [TENUTO, STACCATO]), 0.0)[0].payload
        )
        self.assertEqual(payload.duration, 1.0)

        payload = cast(
            IrNote,
            pe_to_ir(Note(C4, 1.0, MF, [PORTATO, LEGATO, STACCATO]), 0.0)[0].payload,
        )
        self.assertEqual(payload.duration, 0.95)

        payload = cast(IrNote, pe_to_ir(Note(C4, 1.0, MF, [LEGATO]), 0.0)[0].payload)
        self.assertEqual(payload.duration, 1.05)

        # velocities
        payload = cast(
            IrNote, pe_to_ir(Note(C4, 1.0, MF, [MARCATO, ACCENT]), 0.0)[0].payload
        )
        self.assertEqual(payload.velocity, floor(MF * 1.50))

        payload = cast(
            IrNote,
            pe_to_ir(Note(C4, 1.0, MF, [ACCENT, STACCATO, LEGATO, PORTATO]), 0.0)[
                0
            ].payload,
        )
        self.assertEqual(payload.velocity, floor(MF * 1.25))

    def test_encode_chord(self):
        start_time = 32.45
        chord = Chord.from_root(D4, MINOR, QUARTER_NOTE, MF, None)
        nodes = pe_to_ir(chord, start_time)

        self.assertEqual(len(nodes), 3)

        for index, pe in enumerate(chord.notes):
            node = nodes[index]
            self.assertIsInstance(node.payload, IrNote)
            payload = cast(IrNote, node.payload)

            self.assertIsInstance(pe, Note)
            note = cast(Note, pe)

            self.assertEqual(node.time, start_time)
            self.assertEqual(payload.note, note.pitch)
            self.assertEqual(payload.velocity, MF)
            self.assertEqual(payload.duration, QUARTER_NOTE * 0.90)

    def test_encode_phrase(self):
        start_time = 123.45
        phrase = Phrase(
            [
                Note(REST, QN),
                Note(F4, QN, P, [STACCATO]),
                Note(EF4, QN, MP, [STACCATO]),
                Note(D4, QN, F, [STACCATO]),
                Chord.from_root(C4, MAJOR, HN, FF, None),
            ]
        )

        nodes = phrase_to_ir(phrase, start_time)
        notes = phrase.linearise()
        self.assertEqual(len(nodes), 7)
        self.assertEqual(len(notes), 7)

        for note, node in zip(notes, nodes):
            self.assertIsInstance(node.payload, IrNote)
            payload = cast(IrNote, node.payload)

            self.assertEqual(payload.note, note.pitch)

    def test_encode_part(self):
        part = Part(
            "Test Part",
            WIDE_ELECTRIC_GRAND,
            [
                Phrase(
                    [
                        Note(C4, QN),
                        Note(D4, QN),
                        Note(E4, QN),
                        Note(F4, EN),
                        Note(G4, EN),
                    ]
                ),
                Phrase(
                    [
                        Note(A4, QN),
                        Note(B4, QN),
                        Note(E5, EN),
                        Chord(
                            [
                                Note(C4, QN),
                                Note(E4, QN),
                                Note(F4, QN),
                            ]
                        ),
                        Note(C4, HN),
                    ]
                ),
                Phrase([Note(C4, QN)]),
            ],
            10,
            PAN_RIGHT,
        )

        channel = part_to_ir(part)

        self.assertEqual(channel.title, part.title)
        self.assertEqual(channel.channel, part.channel)

        nodes = channel.nodes
        self.assertEqual(len(nodes), 13 + 1 + 1)  # notes + instrument + panning

        # instrument
        instrument_node = nodes.pop(0)
        self.assertIsInstance(instrument_node.payload, IrProgramChange)
        instrument_payload = cast(IrProgramChange, instrument_node.payload)

        patch, bank = instrument_get_patch_bank(WIDE_ELECTRIC_GRAND)
        self.assertEqual(instrument_payload.program, patch)
        self.assertEqual(instrument_payload.bank, bank)

        # panning
        panning_node = nodes.pop(0)
        self.assertIsInstance(panning_node.payload, IrControlChange)
        panning_payload = cast(IrControlChange, panning_node.payload)

        self.assertEqual(panning_payload.control, CHANNEL_PAN)
        self.assertEqual(panning_payload.value, PAN_RIGHT)

        # notes
        for node in nodes:
            self.assertIsInstance(node.payload, IrNote)
            self.assertEqual(node.type, IrNode.Type.NOTE)

        notes = []
        for _, phrase in part.phrases:
            notes += phrase.linearise()

        pitches_t = list(map(lambda note: note.pitch, notes))
        pitches_d = list(map(lambda node: cast(IrNote, node.payload).note, nodes))

        self.assertEqual(pitches_t, pitches_d)

    def test_encode_score(self):
        # no parts
        score = Score("MyScore", [], 120.0)
        file = score_to_ir(score)

        self.assertEqual(len(file.channels), 1)
        self.assertIsInstance(file.channels[0].nodes[0].payload, IrTempo)
        tempo = cast(IrTempo, file.channels[0].nodes[0].payload)

        self.assertEqual(score.tempo, tempo.value)

        channel = file.channels[0]
        self.assertEqual(channel.title, "Channel 0")

        # with parts
        score = Score(
            "MySecondScore",
            [
                Part(
                    "First Part",
                    ACOUSTIC_GRAND_PIANO,
                    [
                        Phrase([Note(C4, EN), Note(C5, EN)]),
                        Phrase([Note(C4, EN), Note(C5, EN)]),
                        Phrase([Note(C4, EN), Note(C5, EN)]),
                        Phrase([Note(C4, EN), Note(C5, EN)]),
                    ],
                    0,
                ),
                Part(
                    "Second Part",
                    WIDE_HARPSICHORD,
                    [
                        Phrase([Note(C4, EN), Note(C5, EN)]),
                        Phrase([Note(C4, EN), Note(C5, EN)]),
                        Phrase([Note(C4, EN), Note(C5, EN)]),
                        Phrase([Note(C4, EN), Note(C5, EN)]),
                    ],
                    1,
                ),
                Part(
                    "Third Part",
                    VIOLIN,
                    [
                        Phrase([Note(C4, EN), Note(C5, EN)]),
                        Phrase([Note(C4, EN), Note(C5, EN)]),
                        Phrase([Note(C4, EN), Note(C5, EN)]),
                        Phrase([Note(C4, EN), Note(C5, EN)]),
                    ],
                    2,
                ),
            ],
            300.0,
        )
        file = score_to_ir(score)

        self.assertEqual(len(file.channels), 3)
        self.assertIsInstance(file.channels[0].nodes[0].payload, IrTempo)
        tempo = cast(IrTempo, file.channels[0].nodes.pop(0).payload)

        self.assertEqual(score.tempo, tempo.value)

        for index, (instrument, title) in enumerate(
            zip(
                [ACOUSTIC_GRAND_PIANO, WIDE_HARPSICHORD, VIOLIN],
                ["First Part", "Second Part", "Third Part"],
            )
        ):
            channel = file.channels[index]

            # title
            self.assertEqual(channel.title, title)

            # instrument
            instrument_node = channel.nodes.pop(0)
            self.assertIsInstance(instrument_node.payload, IrProgramChange)
            instrument_payload = cast(IrProgramChange, instrument_node.payload)

            patch, bank = instrument_get_patch_bank(instrument)
            self.assertEqual(instrument_payload.program, patch)
            self.assertEqual(instrument_payload.bank, bank)

            # panning
            panning_node = channel.nodes.pop(0)
            self.assertIsInstance(panning_node.payload, IrControlChange)
            panning_payload = cast(IrControlChange, panning_node.payload)

            self.assertEqual(panning_payload.control, CHANNEL_PAN)
            self.assertEqual(panning_payload.value, PAN_CENTER)
