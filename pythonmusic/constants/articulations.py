"""
Defines articulations constants for notes.
"""


def _articulation(offset: int) -> int:
    """Returns the articulation mask for the given offset."""
    return 0x1 << offset


STACCATO: int = _articulation(0)
"""Articulation constant for staccato."""
STACCATISSIMO: int = _articulation(1)
"""Articulation constant for staccatissimo."""
MARCATO: int = _articulation(2)
"""Articulations constant for marcato."""
ACCENT: int = _articulation(3)
"""Articulation constant for accented notes."""
TENUTO: int = _articulation(4)
"""Articulation constant for tenuto."""
LEGATO: int = _articulation(5)
"""Articulation constant for legato."""


# compounds
PORTATO: int = LEGATO | STACCATO
"""Articualtion constant for portato"""
