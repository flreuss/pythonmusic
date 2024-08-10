"""
Defines midi message type constants.

The values follow [mido's format](https://mido.readthedocs.io/en/latest/message_types.html)
"""

NOTE_OFF: str = "note_off"
"""
MIDI message constant that defines a note_off message.
"""

NOTE_ON: str = "note_on"
"""
MIDI message constant that defines a note_on message.
"""

POLYTOUCH: str = "polytouch"
"""
MIDI message constant that defines a polytouch message.
"""

CONTROL_CHANGE: str = "control_change"
"""
MIDI message constant that defines a control_change message.
"""

PROGRAM_CHANGE: str = "program_change"
"""
MIDI message constant that defines a program_change message.

Usually this refers to an instrument change.
"""

AFTERTOUCH: str = "aftertouch"
"""
MIDI message constant that defines an aftertouch message.
"""

PITCHWHEEL: str = "pitchwheel"
"""
MIDI message constant that defines a pitchwheel message.
"""

SYSEX: str = "sysex"
"""
MIDI message constant that defines a sysex (system exclusive) message.
"""

QUARTER_FRAME: str = "quarter_frame"
"""
MIDI message constant that defines a quarter_frame message.
"""

SONGPOS: str = "songpos"
"""
MIDI message constant that defines a songpos (song position pointer) message.
"""

SONG_SELECT: str = "song_select"
"""
MIDI message constant that defines a song_select message.
"""

TUNE_REQUEST: str = "tune_request"
"""
MIDI message constant that defines a tune_request message.
"""

CLOCK: str = "clock"
"""
MIDI message constant that defines a clock message.
"""

START: str = "start"
"""
MIDI message constant that defines a start message.
"""

CONTINUE: str = "continue"
"""
MIDI message constant that defines a continue message.
"""

STOP: str = "stop"
"""
MIDI message constant that defines a stop message.
"""

ACTIVE_SENSING: str = "active_sensing"
"""
MIDI message constant that defines an active_sensing message.
"""

RESET: str = "reset"
"""
MIDI message constant that defines a reset message.
"""
