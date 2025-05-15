"""
Use the SamplerTarget to play a score.
"""

from pythonmusic import *


def make_piano() -> Part:
    phrase = Phrase([Note(A2, QN, MF, [STACCATISSIMO])] * 16)

    part = Part(0, "piano", ACOUSTIC_GRAND_PIANO)
    part.add_phrase(phrase)
    part.add_phrase(mods.octave_phrase(phrase), 0.0)

    return part


def make_strings() -> Part:
    phrases: list[Phrase] = []

    phrase = Phrase()
    phrase.add_chord_by_lists(
        [A3, C4, E4],
        [WN],
        [MF],
    )
    phrase.add_chord_by_lists(
        [G3, B3, D4],
        [WN],
        [MF],
    )

    phrases.append(phrase)
    phrases.append(phrase)

    return Part(1, "strings", STRING_ENSEMBLE, phrases)


def make_oboe() -> Part:
    phrases: list[Phrase] = []

    notes_base = [
        Note.rest(QN),
        Note(C6, QN),
        Note(B5, QN),
        Note(A5, QN),
    ]

    notes_a = [Note(G5, dotted(QN)), Note(A5, EN), Note(B5, HN)]

    notes_b = [Note(D6, dotted(QN)), Note(B5, EN), Note(G5, HN)]

    phrase = Phrase()
    phrase.add_notes(notes_base)
    phrase.add_notes(notes_a)
    phrase.add_notes(notes_base)
    phrase.add_notes(notes_b)

    phrases.append(phrase)

    return Part(2, "oboe", OBOE, phrases)


def make_score() -> Score:
    return Score(
        "My Score",
        [
            make_piano(),
            make_strings(),
            make_oboe(),
        ],
    )
