"""
Defines MIDI instrument constants
"""

from pythonmusic.util import make_instrument


# Piano
# 1
ACOUSTIC_GRAND_PIANO = make_instrument(1, 0)
WIDE_ACOUSTIC_GRAND = make_instrument(1, 1)
DARK_ACOUSTIC_GRAND = make_instrument(1, 2)
# 2
BRIGHT_ACOUSTIC_PIANO = make_instrument(2, 0)
WIDE_BRIGHT_ACOUSTIC = make_instrument(2, 1)
# 3
ELECTRIC_GRAND_PIANO = make_instrument(3, 0)
WIDE_ELECTRIC_GRAND = make_instrument(3, 1)
# 4
HONKEY_TONK_PIANO = make_instrument(4, 0)
WIDE_HONKEY_TINK = make_instrument(4, 1)
# 5
RHODES_PIANO = make_instrument(5, 0)
DETUNED_ELECTRIC_PIANO_1 = make_instrument(5, 1)
ELECTRIC_PIANO_1_VARIATION = make_instrument(5, 2)
ELECTRIC_PIANO_60S = make_instrument(5, 3)
# 6
CHORUSED_ELECTRIC_PIANO = make_instrument(6, 0)
DETUNED_ELECTRIC_PIANO_2 = make_instrument(6, 1)
ELECTRIC_PIANO_2_VARIATION = make_instrument(6, 2)
ELECTRIC_PIANO_LEGEND = make_instrument(6, 3)
ELECTRIC_PIANO_PHASE = make_instrument(6, 4)
# 7
HARPSICHORD = make_instrument(7, 0)
COUPLED_HARPSICHORD = make_instrument(7, 1)
WIDE_HARPSICHORD = make_instrument(7, 2)
OPEN_HARPSICHORD = make_instrument(7, 3)
# 8
CLAVINET = make_instrument(8, 0)
PULSE_CLAVINET = make_instrument(8, 1)

# TODO: add rest
