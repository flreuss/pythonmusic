__all__ = ["FFFF", "FFF", "FF", "F", "MF", "MP", "P", "PP", "PPP", "PPPP", "MUTE"]

# FFF is *not* 127, so even FFF can still be accented


FFFF: int = 127
"""Defines maximum possible dynamic."""

FFF: int = 112
"""Defines dynamic constant for *forte fortissimo*."""

FF: int = 96
"""Defines dynamic constant for *fortissimo*."""

F: int = 80
"""Defines dynamic constant for *forte*."""

MF: int = 64
"""Defines dynamic constant for *mezzoforte*."""

MP: int = 53
"""Defines dynamic constant for *mezzopiano*."""

P: int = 42
"""Defines dynamic constant for *piano*."""

PP: int = 31
"""Defines dynamic constant for *pianissimo*."""

PPP: int = 20
"""Defines dynamic constant for *piano pianissimo*."""

PPPP: int = 8
"""Defines minimum dynamic."""

MUTE: int = 0
"""Defines dynamic constant for muted notes."""
