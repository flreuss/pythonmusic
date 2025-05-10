Constants
=========

The ``constants`` module defines musical constants.

Articulations
------------------------------------------

Articulations are defined as a bitset where the set bit's offset identifies the type of articulations.
This means that multiple articulations can occur at the same time.

.. automodule:: pythonmusic.constants.articulations
   :members:
   :undoc-members:
   :show-inheritance:

Chords
-----------------------------------

The chord constructor :meth:`Chord.from_root <pythonmusic.music.Chord.from_root>` takes the ``intervals`` parameter which is a list of
intervals. The constants below define common chord intervals, i.e., offsets from a root note at offset 0, which can be used in this 
place.

.. automodule:: pythonmusic.constants.chords
   :members:
   :undoc-members:
   :show-inheritance:

Control Changes
--------------------------------------------

Defines control change MIDI message constants. See :doc:`midi <../appendix/midi>` for more information.

.. automodule:: pythonmusic.constants.control_change
   :members:
   :undoc-members:
   :show-inheritance:

Durations
--------------------------------------

Constants that define the duration of notes. All values are in reference to quarter notes, which are defined as ``1.0``.

.. automodule:: pythonmusic.constants.durations
   :members:
   :undoc-members:
   :show-inheritance:

Dynamics
-------------------------------------

Defines velocity constants for notes.

.. automodule:: pythonmusic.constants.dynamics
   :members:
   :undoc-members:
   :show-inheritance:

Instruments
----------------------------------------

MIDI instruments are identified by their patch id. The bank number is used in certain MIDI level 2 compatible libraries to add more
instruments on top of the original 127. 

.. important:: The constants below define instruments for both MIDI level 1 and 2. As not all midi synthesisers support level 2, you may 
    need to restrict your score to level 1. All instruments with a constant value of <=128, that is all instruments whose bank number
    is 0, are compatible with level 1 and should work on most MIDI devices.

The patch and bank ids are stored in a partitioned integer. To retrieve the individual numbers, use the 
:meth:`instrument_get_patch_bank() <pythonmusic.util.instrument_get_patch_bank>` function from the :mod:`util <pythonmusic.util>` 
sub module.
    

.. automodule:: pythonmusic.constants.instruments
   :members:
   :undoc-members:
   :show-inheritance:

Intervals
--------------------------------------

All intervals are defined as an offset of semi-tones over a root note.

.. automodule:: pythonmusic.constants.intervals
   :members:
   :undoc-members:
   :show-inheritance:

Messages
-------------------------------------

Defines midi message type constants as required my `mido <https://mido.readthedocs.io/en/stable/index.html>`_. See
:doc:`midi <../appendix/midi>` for more information.

.. automodule:: pythonmusic.constants.messages
   :members:
   :undoc-members:
   :show-inheritance:

Panning
------------------------------------

Defines panning constants.

.. automodule:: pythonmusic.constants.panning
   :members:
   :undoc-members:
   :show-inheritance:

Percussion
---------------------------------------

Defines percussion constants for MIDI channel 10. 

.. important:: These instruments refer to pitches on MIDI channel 10, not instruments. They cannot be used as instruments on 
    :obj:`parts <pythonmusic.music.Part>`.

.. automodule:: pythonmusic.constants.percussion
   :members:
   :undoc-members:
   :show-inheritance:

Pitches
------------------------------------

Defines pitch (or note in MIDI) constants.

.. automodule:: pythonmusic.constants.pitches
   :members:
   :undoc-members:
   :show-inheritance:

Scales
-----------------------------------

Scales are defines as a list of offsets over a root note.

.. automodule:: pythonmusic.constants.scales
   :members:
   :undoc-members:
   :show-inheritance:

Tempo
----------------------------------

Defines approximate values for musical tempi.

.. automodule:: pythonmusic.constants.tempo
   :members:
   :undoc-members:
   :show-inheritance:
