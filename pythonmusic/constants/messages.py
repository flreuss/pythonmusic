# Channel Voice
NOTE_OFF = 0b1000
"""
A note off event.

This event is sent when a note is released or ended.
"""

NOTE_ON = 0b1001
"""
A note on event.

This event is sent when a note is pressed or should start.
"""

AFTERTOUCH = 0b1010
"""
An aftertouch event.

This event is usually sent when applying preser to a fully pressed key.

Also polyphonic key pressure.
"""

CONTROL_CHANGE = 0b1011
"""
A control change event.

This event is sent when a control change value should be changed.
"""

PROGRAM_CHANGE = 0b1100
"""
A program change event.

This event is sent when the patch number of a channel changes.

To change the instrument in terms of GM2, you may also need to update the bank
number via a bank select CC message.
"""

CHANNEL_PRESSURE = 0b1101
"""
A channel pressure event.

This is similar to aftertouch, but instead of individual pressures, should only
send the greatest aftertouch value.
"""

PITCH_WHEEL = 0b1110
"""
A pitch wheel change event.

This event is sent on change of the pitch wheel.
"""


# Channel Mode Messages
"""
A channel mode event.

This event uses the same id as control change. The associated value must be
in `120` to `127`.
"""
CHANNEL_MODE = CONTROL_CHANGE


# System Common Messages
SYSTEM_EXCLUSIVE = 0b11110000
"""
A system exclusive event.

System exclusive events are used to implement functionality that is not directly
supported by the MIDI standard.
"""

END_OF_SYSTEM_EXCLUSIVE = 0b11110111
"""
A end of exclusive event.

Indicates end of data stream of system exclusive dump.
"""

TIME_CODE_QF = 0b11110001
"""
A MIDI time code quarter fram event.
"""

SONG_POSITION = 0b11110010
"""
A song position pointer event.
"""

SONG_SELECT = 0b11110011
"""
A song select event.
"""

TUNE_REQUEST = 0b11110110
"""
A tune request event.
"""

# System Real-Time Messages
CLOCK = 0b11111000
"""
A timing clock signal.
"""

START = 0b11111010
"""
A start event.

Indicates that the current sequence should start playing. Indicates clock 
signals will follow.
"""

CONTINUE = 0b11111011
"""
A stop event.

Signalls the current sequence be stoped.
"""

STOP = 0b11111100
"""
A stop event.

Stopps the current sequence.
"""

ACTIVE_SENSING = 0b11111110
"""
An active sensing event.
"""

RESET = 0b11111111
"""
A reset event.

When sent, indicates that the receiver should return to its power-up status.

In MIDI files, acts as an escape for meta events. See `ESCAPE`.
"""

META = RESET
"""
An escape sequence indicating a meta event in a MIDI file.

Only use this in MIDI file contexts. The value is identical to `RESET` and has
different meaning if send to MIDI devices.
"""
