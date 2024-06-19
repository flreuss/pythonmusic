"""
Defines constants for note lengths.
"""


def _dotted(base: float, dots: int) -> float:
    """Returns the note unit value of a base note augmented by dots."""
    if dots < 1:
        return base
    return base * (2 - (0.5 ** float(dots)))


# Quarter Note
QUARTER_NOTE: float = 1.0
"""Defines length constant for a *quarter note* or *crotchet*."""
QN: float = QUARTER_NOTE
"""Defines length constant for a *quarter note* or *crotchet*."""
CROTCHET: float = QUARTER_NOTE
"""Defines length constant for a *quarter note* or *crotchet*."""

# Half Note
HALF_NOTE: float = QUARTER_NOTE * 2.0
"""Defines length constant for a *half note* or *minim*."""
HN: float = HALF_NOTE
"""Defines length constant for a *half note* or *minim*."""
MINIM: float = HALF_NOTE
"""Defines length constant for a *half note* or *minim*."""

# Whole Note
WHOLE_NOTE: float = QUARTER_NOTE * 4.0
"""Defines length constant for a *whole note* or *semibreve*."""
WN: float = WHOLE_NOTE
"""Defines length constant for a *whole note* or *semibreve*."""
SEMI_BREVE: float = WHOLE_NOTE
"""Defines length constant for a *whole note* or *semibreve*."""

# Double Whole Note
DOUBLE_WHILE_NOTE: float = QUARTER_NOTE * 8.0
"""Defines length constant for a *double whole* or *breve*."""
WWN: float = DOUBLE_WHILE_NOTE
"""Defines length constant for a *double whole* or *breve*."""
BREVE: float = DOUBLE_WHILE_NOTE
"""Defines length constant for a *double whole* or *breve*."""

# Eighth Note
EIGHTH_NOTE: float = QUARTER_NOTE / 2
"""Defines length constant for a *eith note* or *quaver*."""
EN: float = EIGHTH_NOTE
"""Defines length constant for a *eith note* or *quaver*."""
QUAVER: float = EIGHTH_NOTE
"""Defines length constant for a *eith note* or *quaver*."""

# Sixteenth Note
SIXTEENTH_NOTE: float = QUARTER_NOTE / 4
"""Defines length constant for a *sixteenth note* or *semiquaver*."""
SN: float = SIXTEENTH_NOTE
"""Defines length constant for a *sixteenth note* or *semiquaver*."""
SEMI_QUAVER: float = SIXTEENTH_NOTE
"""Defines length constant for a *sixteenth note* or *semiquaver*."""

# Thirtysecond Note
THIRTYSECOND_NOTE: float = QUARTER_NOTE / 8
"""Defines length constant for a *thirtysecond note* or *demisemiquaver*."""
TN: float = THIRTYSECOND_NOTE
"""Defines length constant for a *thirtysecond note* or *demisemiquaver*."""
DEMISEMI_QUAVER: float = THIRTYSECOND_NOTE
"""Defines length constant for a *thirtysecond note* or *demisemiquaver*."""


# Dotted Quarter Note
DOTTED_QUARTER_NOTE: float = _dotted(QUARTER_NOTE, 1)
"""Defines the length constant for a dotted *quarter note* or *crotchet*."""
DQN: float = DOTTED_QUARTER_NOTE
"""Defines the length constant for a dotted *quarter note* or *crotchet*."""
DOTTED_CROTCHET: float = DOTTED_QUARTER_NOTE
"""Defines the length constant for a dotted *quarter note* or *crotchet*."""

# Double Dotted Quarter Note
DOUBLE_DOTTED_QUARTER_NOTE: float = _dotted(QUARTER_NOTE, 2)
"""Defines the length constant for a double dotted *quarter note* or *crotchet*."""
DDQN: float = DOUBLE_DOTTED_QUARTER_NOTE
"""Defines the length constant for a dotted *quarter note* or *crotchet*."""
DOUBLE_DOTTED_CROTCHET: float = DOUBLE_DOTTED_QUARTER_NOTE
"""Defines the length constant for a dotted *quarter note* or *crotchet*."""

# Dotted Half Note
DOTTED_HALF_NOTE: float = _dotted(HALF_NOTE, 1)
"""Defines the length constant for a dotted *half note* or *minim*."""
DHN: float = DOTTED_HALF_NOTE
"""Defines the length constant for a dotted *half note* or *minim*."""
DOTTED_MINIM: float = DOTTED_HALF_NOTE
"""Defines the length constant for a dotted *half note* or *minim*."""

# Double Dotted Half Note
DOUBLE_DOTTED_HALF_NOTE: float = _dotted(HALF_NOTE, 2)
"""Defines the length constant for a double dotted *half note* or *minim*."""
DDHN: float = DOUBLE_DOTTED_HALF_NOTE
"""Defines the length constant for a double dotted *half note* or *minim*."""
DOUBLE_DOTTED_MINIM: float = DOUBLE_DOTTED_HALF_NOTE
"""Defines the length constant for a double dotted *half note* or *minim*."""

# Dotted While Note
DOTTED_WHOLE_NOTE: float = _dotted(WHOLE_NOTE, 1)
"""Defines the length constant for a dotted *whole note* or *semibreve*."""
DWN: float = DOTTED_WHOLE_NOTE
"""Defines the length constant for a dotted *whole note* or *semibreve*."""
DOTTED_SEMI_BREVE: float = DOTTED_WHOLE_NOTE
"""Defines the length constant for a dotted *whole note* or *semibreve*."""


# Dotted Eighth Note
DOTTED_EIGHTH_NOTE: float = _dotted(EIGHTH_NOTE, 1)
"""Defines the length constant for a dotted *eighth note* or *quaver*."""
DEN: float = DOTTED_EIGHTH_NOTE
"""Defines the length constant for a dotted *eighth note* or *quaver*."""
DOTTED_QUAVER: float = DOTTED_EIGHTH_NOTE
"""Defines the length constant for a dotted *eighth note* or *quaver*."""

# Double Dotted Eighth Note
DOUBLE_DOTTED_EIGHTH_NOTE: float = _dotted(EIGHTH_NOTE, 2)
"""Defines the length constant for a double dotted *eighth note* or *crotchet*."""
DDEN: float = DOUBLE_DOTTED_EIGHTH_NOTE
"""Defines the length constant for a double dotted *eighth note* or *crotchet*."""
DOUBLE_DOTTED_QUAVER: float = DOUBLE_DOTTED_EIGHTH_NOTE
"""Defines the length constant for a double dotted *eighth note* or *crotchet*."""


# TODO: Implement functionality and provide warning below for creating triplets.
# Using too many duration values of the following types may create a shift, as
# `3 * (1/3)` may not be guaranteed to equal `1`.

# Quarter Note Triplet
QUARTER_NOTE_TRIPLET: float = QUARTER_NOTE / 3
"""Defines the length constant for a *quarter note* triplet."""
QNT: float = QUARTER_NOTE_TRIPLET
"""Defines the length constant for a *quarter note* triplet."""
CROTCHET_TRIPLET: float = QUARTER_NOTE_TRIPLET

# Eighth Note Triplet
EIGHTH_NOTE_TRIPLET: float = EIGHTH_NOTE / 3
"""Defines the length constant for a *eighth note* triplet."""
ENT: float = EIGHTH_NOTE_TRIPLET
"""Defines the length constant for a *eighth note* triplet."""
QUAVER_TRIPLET: float = EIGHTH_NOTE_TRIPLET
"""Defines the length constant for a *eighth note* triplet."""

# Sixteenth Note Triplet
SIXTEENTH_NOTE_TRIPLET: float = SIXTEENTH_NOTE / 3
"""Defines the length constant for a *sixteenth note* triplet."""
SNT: float = SIXTEENTH_NOTE_TRIPLET
"""Defines the length constant for a *sixteenth note* triplet."""
SEMI_QUAVER_TRIPLET: float = SIXTEENTH_NOTE_TRIPLET
"""Defines the length constant for a *sixteenth note* triplet."""
