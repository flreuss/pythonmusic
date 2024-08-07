"""
Defines some of midi's control change values.

The constants below define the type of control change that a message contains.

These are not message types. See `messages.py` for that.

See [Wikipedia](https://en.wikipedia.org/wiki/General_MIDI)
"""

BANK_CHANGE: int = 0
"""
MIDI CC constant for bank changes.

Accepts values in range from 0 to 127.
"""

MOD_WHEEL: int = 1
"""
MIDI CC constant for mod wheel.

Accepts values in range from 0 to 127.
"""

CHANNEL_VOLUME: int = 7
"""
MIDI CC constant for channel volumne.

Accepts values in range form 0 to 127.
"""

CHANNEL_PAN: int = 10
"""
MIDI CC constant for channel panning.

Accepts values in range from 0 to 127 where 64 is centre. See `panning.py`.
"""

EXPRESSION: int = 11
"""
MIDI CC constant for expression.

Accepts values in range from 0 to 127.
"""

SUSTAIN_PEDAL: int = 64
"""
MIDI CC constant for the sustain pedal.

Accepts values in range from 0 to 127. Many controllers understand this value as
a switch where a value ≤63 is treaded as off, and ≥64 as on.
"""

SOSTENUTO_PEDAL: int = 66
"""
MIDI CC constant for the sostenuto pedal.

This pedal is similar to the normal sustain pedal, except in that it only 
sustains notes that were already pressed when the sostenuto pedal is used.

Accepts values in range from 0 to 127. Many controllers understand this value as
a switch where a value ≤63 is treaded as off, and ≥64 as on.
"""

SOFT_PEDAL: int = 67
"""
MIDI CC constant for the soft pedal.

Accepts values in range from 0 to 127. Many controllers understand this value as
a switch where a value ≤63 is treaded as off, and ≥64 as on.
"""

RESET: int = 121
"""
MIDI CC constant for resetting all controllers to their defalt values.

A value of 0 is expected.
"""

ALL_NOTES_OFF: int = 123
"""
MIDI CC constant for muting all sounding notes.

A value of 0 is ecpected.
"""
