"""
Defines common scales by their offset from a root note.
"""

MAJOR: list[int] = [0, 2, 4, 5, 7, 9, 11]
"""Scale constant for the major scale."""

MINOR: list[int] = [0, 2, 3, 5, 7, 8, 10]
"""Scale constant for the (natrual) minor scale."""

HARMONIC_MINOR: list[int] = [0, 2, 3, 5, 7, 8, 11]
"""Scale constant for the harmonic minor scale."""

MELODIC_MINOR: list[int] = [0, 2, 3, 5, 7, 9, 11]
"""Scale constant for the melodic minor scale."""

CHROMATIC: list[int] = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11]
"""SCale constant for the chromatic scale."""

WHOLE_TONE: list[int] = [0, 2, 4, 6, 8, 10]
"""Scale constant for the whole tone scale."""

PENTATONIC: list[int] = [0, 2, 4, 7, 9]
"""Scale constant for the pentatonic scale."""

IONIAN: list[int] = MAJOR
"""
Scale constants for the ionian scale.

This is identical to the major scale.
"""

DORIAN: list[int] = [0, 2, 3, 5, 7, 9, 10]
"""Scale constant for the dorian or doric scale."""

PHRYGIAN: list[int] = [0, 1, 3, 5, 7, 8, 10]
"""Scale constant for the phrygian scale."""

LYDIAN: list[int] = [0, 2, 4, 6, 7, 9, 11]
"""Scale constant for the lydian scale."""

MIXOLYDIAN: list[int] = [0, 2, 4, 5, 7, 9, 10]
"""Scale constant for the mixolydian scale."""

AEOLIAN: list[int] = MINOR
"""
Scale constant for the aeolian scale.

This is identical to the minor scale.
"""

LOCRIAN: list[int] = [0, 1, 2, 3, 4, 6, 8, 10]
"""Scale constant for the locrian scale."""
