"""
Defines MIDI constants for music notation dynamics.
"""

# FFF is *not* 127, so even FFF can still be accented

FFF: int = 114
"""Defines dynamic constant for *forte fortissimo*."""
FF: int = 91
"""Defines dynamic constant for *fortissimo*."""
F: int = 78
"""Defines dynamic constant for *forte*."""
MF: int = 65
"""Defines dynamic constant for *mezzoforte*."""
MP: int = 52
"""Defines dynamic constant for *mezzopiano*."""
P: int = 39
"""Defines dynamic constant for *piano*."""
PP: int = 26
"""Defines dynamic constant for *pianissimo*."""
PPP: int = 13
"""Defines dynamic constant for *piano pianissimo*."""
MUTE: int = 0
"""Defines dynamic constant for muted notes."""
