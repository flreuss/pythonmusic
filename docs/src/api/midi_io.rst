Midi IO
=======

PythonMusic provides various classes and functions to interact with midi devices and files.

A midi port is represented by the library as a string. Midi devices connected to your computer are handled by the operating system,
which may impose different conventions and rules depending
on your platform. As such, the name of your device may differ depending on your platform. You can check available midi devices with
:meth:`midi_inputs() <pythonmusic.midi.midi_inputs>` for midi inputs (receivers) and :meth:`midi_outputs() <pythonmusic.midi.midi_outputs>`
for a list of midi output (senders).

.. important:: 
   Midi channels range from 1 to 16. This library is zero-indexed, so valid channels
   range from 0 to 15. Convert from midi standards by subtracting 1.

To provide a coherent API, this library uses `Rtmidi <https://www.music.mcgill.ca/~gary/rtmidi/>`_
(`python-rtmidi <https://spotlightkid.github.io/python-rtmidi/>`_) as its midi backend.


Finding Midi Ports
------------------

You can retrieve a list of available midi input/output ports with :meth:`midi_inputs() <pythonmusic.midi.midi_inputs>` and :meth:`midi_outputs() <pythonmusic.midi.midi_outputs>`. To search for a port based on a pattern, for instance, part of the devices name,
use :meth:`find_midi_input() <pythonmusic.midi.find_midi_input>` and :meth:`find_midi_output() <pythonmusic.midi.find_midi_output>`.

.. code-block:: python

   NAME = "Digital Piano"
   device_name = find_midi_input(NAME)

   if device_name is None:
     print(f"No midi port found for name: {NAME}")
     exit(1)

   device = MidiIn(device_name)
   # do something with device

For an interactive dialogue, use :meth:`input_user_prompt() <pythonmusic.midi.input_user_prompt>` and
:meth:`output_user_prompt() <pythonmusic.midi.output_user_prompt>` which prompt the user to choose a device, if more than one device is
connected.

.. autoclass:: pythonmusic.midi.midi_inputs
   :no-index:
   :members:
   :undoc-members:
   :show-inheritance:

.. autoclass:: pythonmusic.midi.midi_outputs
   :no-index:
   :members:
   :undoc-members:
   :show-inheritance:

.. autoclass:: pythonmusic.midi.find_midi_input
   :no-index:
   :members:
   :undoc-members:
   :show-inheritance:

.. autoclass:: pythonmusic.midi.find_midi_output
   :no-index:
   :members:
   :undoc-members:
   :show-inheritance:

.. autoclass:: pythonmusic.midi.input_user_prompt
   :no-index:
   :members:
   :undoc-members:
   :show-inheritance:

.. autoclass:: pythonmusic.midi.output_user_prompt
   :no-index:
   :members:
   :undoc-members:
   :show-inheritance:


Interacting with Midi Devices
-----------------------------

PythonMusic provides two classes that handle midi communication. :obj:`MidiIn <pythonmusic.midi.MidiIn>` receives midi messages from,
:obj:`MidiOut <pythonmusic.midi.MidiOut>` sends message to other midi ports and devices. Both classes can be either in virtual/host or
attach/client mode. The respective mode is selected by setting the ``virtual`` parameter in the initialiser.


Hosting a Port (Virtual)
........................

Virtual midi ports are registered as a device with the system and are visible to other midi applications.
Virtual midi ports can be retrieved with :meth:`midi_inputs() <pythonmusic.midi.midi_inputs>` or
:meth:`midi_outputs() <pythonmusic.midi.midi_outputs>`, and connected to.

.. note:: 
   Depending on your system, the name of the midi port may differ from your declared name. It is always a good idea to retrieve the
   system's port name before using the port.

     >>> from pythonmusic import MidiIn, midi_inputs
     >>> NAME = "My Virtual Midi Port"
     >>> port = MidiIn(NAME, True)
     >>> midi_inputs()
     ['PythonMusic:My Virtual Midi Port 128:0']

   When using ALSA on Linux, for instance, a port declared as "My Virtual Midi Port" may be listed as 
   "*client_id*: My Virtual Midi Port *client_number*:*port*"


Create a virtual port by setting the ``virtual`` parameter to ``True``.
To search for the OS' name of your new port, use :meth:`find_midi_input() <pythonmusic.midi.find_midi_input>` or
:meth:`find_midi_output() <pythonmusic.midi.find_midi_output>`.

.. code-block:: python
   
   NAME = "My Virtual Midi Port"

   virtual_port = MidiIn(NAME, virtual=True)
   port_name = find_midi_input(NAME)

   if port_name is None:
     print("Something went wrong")
     exit(1)

   # do something with device

Your new port is now available and visible to all midi applications on your system, such as DAWs and virtual instruments.


Attaching to a port
...................

You can attach to midi devices on your system by setting the ``virtual`` parameter to ``False`` (not setting it defaults to ``False``).

.. code-block:: python

   inputs = midi_inputs()
   outputs = midi_outputs()

   in_port = MidiIn(inputs[0], False)
   out_port = MidiOut(inputs[0])  # False can be omitted


.. autoclass:: pythonmusic.midi.MidiIn
   :no-index:
   :members:
   :undoc-members:
   :show-inheritance:

.. autoclass:: pythonmusic.midi.MidiOut
   :no-index:
   :members:
   :undoc-members:
   :show-inheritance:


File Export
-----------

:obj:`Scores <pythonmusic.music.Score>` can be exported to file using the :meth:`export_score() <pythonmusic.midi.export_score>` function.

.. code-block:: python

   score = Score("My Score")
   # populate score

   export_score(score, "export/my_score.mid")


.. autoclass:: pythonmusic.midi.export_score
   :no-index:
   :members:
   :undoc-members:
   :show-inheritance:


Messages
--------

Midi messages are used to communicate between midi devices. PythonMusic provides the 
:obj:`Message <pythonmusic.midi.Message>` class, which stores message data in byte form.

For a list of supported midi message, their properties, and data type ranges, see
the :doc:`section on midi <../appendix/midi>` in the appendix.

.. note::
   The class provides properties for accessing message parameters such as channel, key, and control value. However, not all
   message types support all these parameters and the call will throw an 
   :obj:`InvalidMessageError <pythonmusic.midi.InvalidMessageError>`
   if the type is not supported. You can check the message type with :meth:`Message.type() <pythonmusic.midi.Message.type>` and
   compare with :mod:`message constants <pythonmusic.constants.messages>`.

Messages can be constructed from byte-data using the initialiser, or the various class-methods for specific message types.


The Time attribute
..................

Messages also store the ``time`` attribute which defines the number of ticks from the previous event. 


Reference
.........

.. autoclass:: pythonmusic.midi.Message
   :no-index:
   :members:
   :undoc-members:
   :show-inheritance:
