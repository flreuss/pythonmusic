Midi
====

MIDI (Musical Instrument Digital Interface) is a standard that enables electronic musical instruments and devices to communicate by 
sending performance data, rather than audio signals. MIDI messages, which consist of simple instructions like "note on" or "note off,"
allow devices to produce or modify sounds based on these commands.

MIDI operates across 16 channels (0-15), each capable of controlling a different instrument or sound. The messages are typically 2 or 3
bytes long: the first byte identifies the type of message, and the following bytes contain additional details, like which note to play 
or how hard to press a key. Constants in the MIDI specification define note numbers, velocities, and other parameters to ensure
compatibility between different devices.

PythonMusic uses `mido <https://mido.readthedocs.io/en/stable/index.html>`_ for its MIDI communication. This document will list the
necessities for interacting with messages. For a more complete overview, see mido's documentation.

Messages
--------

The parameters that need to be passed to the initialiser of a :obj:`MidiMessage <pythonmusic.io.MidiMessage>` object differ, depending
on the type of message that you create. The table below lists the required parameters for each message type.

==============  =========================================================================
Message Type    Midi Message
==============  =========================================================================
NOTE_OFF        ``MidiMessage("NOTE_OFF", channel: int, note: int, velocity: int)``
NOTE_ON         ``MidiMessage("NOTE_ON", channel: int, note: int, velocity: int)``
POLYTOCH        ``MidiMessage("POLYTOCH", channel: int, note: int, value: int)``
CONTROL_CHANGE  ``MidiMessage("CONTROL_CHANGE", channel: int, control: int, value: int)``
PROGRAM_CHANGE  ``MidiMessage("PROGRAM_CHANGE", channel: int, program: int)``
AFTERTOUCH      ``MidiMessage("AFTERTOUCH", channel: int, value: int)``
PITCHWHEEL      ``MidiMessage("PITCHWHEEL", channel: int, pitch: int)``
SYSEX           ``MidiMessage("SYSEX", data: int)``
QUARTER_FRAME   ``MidiMessage("QUARTER_FRAME", frame_type: int, frame_value: int)``
SONGPOS         ``MidiMessage("SONGPOS", pos: int)``
SONG_SELECT     ``MidiMessage("SONG_SELECT", song: int)``
TUNE_REQUEST    ``MidiMessage("TUNE_REQUEST")``
CLOCK           ``MidiMessage("CLOCK")``
START           ``MidiMessage("START")``
CONTINUE        ``MidiMessage("CONTINUE")``
STOP            ``MidiMessage("STOP")``
ACTIVE_SENSING  ``MidiMessage("ACTIVE_SENSING")``
RESET           ``MidiMessage("RESET")``
==============  =========================================================================

The values of the parameters above need to be in bounds for their respective type.

===========  ======================
Parameter    Range           
===========  ======================
channel      0..15                 
frame_type   0..7                  
frame_value  0..15                 
control      0..127                
note         0..127                
program      0..127                
song         0..127                
value        0..127                
velocity     0..127                
data         (0..127, 0..127, ...) 
pitch        -8192..8191           
pos          0..16383              
time         any integer or float  
===========  ======================

.. note:: Channel values are 0-indexed and thus range from 0 to 15. The channel 1 is represented by 0 and the channel 16 by 15.
