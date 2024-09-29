Midi Io
=======

PythonMusic provides various classes and functions to interact with MIDI devices and files.

This library uses `mido <https://mido.readthedocs.io/en/stable/index.html>`_ for its MIDI communication. If something is missing here,
see its documentation for more information.


Finding MIDI Ports
------------------

Use the :meth:`get_midi_receivers() <pythonmusic.io.get_midi_receivers>` and :meth:`get_midi_senders() <pythonmusic.io.get_midi_senders>` 
functions to retrieve a list of names of open MIDI receivers and senders, respectively. You can then pass one of the returned strings to
the attach methods of :obj:`MidiReceiver <pythonmusic.io.MidiReceiver>`, :obj:`MidiSender <pythonmusic.io.MidiSender>`, and the initialiser
of :obj:`MidiPlayer <pythonmusic.play.MidiPlayer>`.

*For more information on attaching to and hosting midi ports, see the sections below.*

.. code-block:: python 

    receivers = get_midi_receivers()

    if len(receivers) == 0:
        print("no open midi receivers found")
        exit(1)

    sender = MidiSender.attach(receivers[0])
    player = MidiPlayer(receivers[0])


If you know the name of the MIDI port you want to send or receive messages with, you can pass that name as well.

.. code-block:: python

   sender = MidiSender.attach("My Digital Piano")

.. important:: 
     Some operating systems may not list the MIDI port under its declared name. Even if you know the name of the MIDI port, you may 
     still need to retrieve the actual name of the port by using the :meth:`find_midi_sender() <pythonmusic.io.find_midi_sender>` and 
     :meth:`find_midi_receiver() <pythonmusic.io.find_midi_receiver>` functions from the :mod:`io <pythonmusic.io>` module. These functions 
     search the available MIDI ports for a close match to the input you pass to the functions.
     
     .. code-block:: python

        # name as declared by device
        MY_DEVICE = "Pico MIDI"

        # MY_DEVICE is not listed in midi senders
        _ = get_midi_senders()  # ['Pico MIDI:Pico MIDI MIDI 1 32:0', 'Moland Digital Piano:Moland Digital Piano MIDI 1 28:0']

        sender = find_midi_sender(MY_DEVICE)  # 'Pico MIDI:Pico MIDI MIDI 1 32:0'

     During testing, this was only necessary on Linux, as macOS and Windows reported the correct MIDI port names.


Reference
.........

.. autoclass:: pythonmusic.io.get_midi_senders
   :no-index:
   :members:
   :undoc-members:
   :show-inheritance:

.. autoclass:: pythonmusic.io.get_midi_receivers
   :no-index:
   :members:
   :undoc-members:
   :show-inheritance:

.. autoclass:: pythonmusic.io.find_midi_sender
   :no-index:
   :members:
   :undoc-members:
   :show-inheritance:

.. autoclass:: pythonmusic.io.find_midi_receiver
   :no-index:
   :members:
   :undoc-members:
   :show-inheritance:


Creating Ports
--------------

PythonMusic provides two classes that handle MIDI port communication: the :obj:`MidiSender <pythonmusic.io.MidiSender>` and the :obj:`MidiReceiver <pythonmusic.io.MidiReceiver>`.
Both can be either in a host (or virtual), or a attached (non-virtual) configuration.

A :obj:`MidiSender <pythonmusic.io.MidiSender>` is used to send :obj:`MIDI messages <pythonmusic.io.MidiMessage>` to other MIDI input ports. Use this class if you want to play
MIDI messages through a DAW, digital piano, or similar.

A :obj:`MidiReceiver <pythonmusic.io.MidiReceiver>` is used to receive :obj:`MIDI messages <pythonmusic.io.MidiMessage>` from MIDI output ports. Use this class if you want to 
receive messages from, for instance, a MIDI keyboard, digital piano, or DAW.

Hosting a Port
..............

Hosting a MIDI port means that other ports and applications can connect to the port. To create a MIDI port host, use the default initialiser
of :obj:`MidiReceiver <pythonmusic.io.MidiReceiver>`, :obj:`MidiSender <pythonmusic.io.MidiSender>` to create a new instance.

.. code-block:: python

    receiver = MidiReceiver("MyReceiverPort")
    sender = MidiSender("MySenderPort")

The system now lists both of these ports as open and other applications, such as DAWs, should be able to see them. See the documentation for both classes on how to interact
with attaching clients.


Attaching to a Port
...................

To attach to another MIDI ports means sending or receiving messages with that port exclusively. This may also be necessary if the other port cannot choose its target port on 
its own, for instance, MIDI keyboards, or digital pianos. To attach to a host, use the *attach()* methods available on :meth:`MidiSender <pythonmusic.io.MidiSender.attach>`
and :meth:`MidiReceiver <pythonmusic.io.MidiReceiver.attach>`.

.. code-block:: python

    sender = MidiSender.attach("MyMidiReceiver")
    receiver = MidiReceiver.attach("MyMidiSender")

See the documentation for both classes on how to interact with the attached host.

.. important:: Keep in mind that even if you know the name of the host you intend to attach to, some operating systems do not list MIDI ports as they are declared. See the section
    for finding MIDI ports above.


Reference
.........

.. autoclass:: pythonmusic.io.MidiReceiver
   :no-index:
   :members:
   :undoc-members:
   :show-inheritance:

.. autoclass:: pythonmusic.io.MidiSender
   :no-index:
   :members:
   :undoc-members:
   :show-inheritance:


Messages
--------

MIDI messages can be created using the :obj:`MidiMessage <pythonmusic.io.MidiMessage>` object. They can then be send via a midi senders 
:meth:`send_message() <pythonmusic.io.MidiSender.send_message>` method.

The parameters of a MIDI message vary depending on the message type. See the :doc:`midi <../appendix/midi>` page for more information.

Reference
.........

.. autoclass:: pythonmusic.io.MidiMessage
   :no-index:
   :members:
   :undoc-members:
   :show-inheritance:


Exporting
---------

PythonMusic supports exporting :obj:`scores <pythonmusic.music.Score>` as MIDI files.

Use the :meth:`export_score() <pythonmusic.io.export_score>` function and pass your score and file export path.

.. code-block:: python

    export_score(my_score, ".exports/output.mid")

.. note:: Directories on the given path must exist, and the path has to end on a file.

Reference
.........

.. autoclass:: pythonmusic.io.export_score
   :no-index:
   :members:
   :undoc-members:
   :show-inheritance:
