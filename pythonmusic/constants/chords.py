"""
Defines pitch offset constants for chotds.
"""

from .intervals import *

MAJOR: list[int] = [UNISON, MAJOR_THIRD, FIFTH]
"""Chord constant that defines offsets over a root note for a major chord."""
MINOR: list[int] = [UNISON, MINOR_THIRD, FIFTH]
"""Chord constant that defines offsets over a root note for a major chord."""

# given that notation usually uses m7 for minor 7 and M7 for major seven, which
# is not "possible" with python constants, MAJOR7 refers to the minor, and
# MAJORM7 refers to the major quality.
MAJOR7: list[int] = MAJOR + [MINOR_SEVENTH]
"""
Chord constant that defines offsets over a root note for a major minor 7 chord.
"""
MAJORM7: list[int] = MAJOR + [MAJOR_SEVENTH]
"""
Chord constant that defines offsets over a root note for a major major 7 chord.
"""
MINOR7: list[int] = MINOR + [MINOR_SEVENTH]
"""
Chord constant that defines offsets over a root note for a minor minor 7 chord.
"""
MINORM7: list[int] = MINOR + [MAJOR_SEVENTH]
"""
Chord constant that defines offsets over a root note for a minor major 7 chord.
"""
AUGMENTED: list[int] = [UNISON, MAJOR_THIRD, MINOR_SIXTH]
"""
Chord constant that defines offsets over a root note for a augmented chord.
"""
DIMINISHED: list[int] = [UNISON, MINOR_THIRD, TRITONE]
"""
Chord constant that defines offsets over a root note for a diminished chord.
"""
HALF_DIMINISHED: list[int] = DIMINISHED + [MINOR_SEVENTH]
"""
Chord constant that defines offsets over a root note for a half-diminished chord.
"""
SUS2: list[int] = [UNISON, MAJOR_SECOND, FIFTH]
"""
Chord constant that defines offsets over a root note for a suspended 2 chord.
"""
SUS4: list[int] = [UNISON, FOURTH, FIFTH]
"""
Chord constant that defines offsets over a root note for a suspended 4 chord.
"""
