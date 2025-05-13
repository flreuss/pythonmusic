Players
=======

Players are objects used to playback 
:obj:`notes <pythonmusic.music.Note>`,
:obj:`chords <pythonmusic.music.Chord>`,
:obj:`phrases <pythonmusic.music.Phrase>`,
:obj:`parts <pythonmusic.music.Part>`,
:obj:`scores <pythonmusic.music.Score>`, and 
:obj:`messages <pythonmusic.io.MidiMessage>`.
PythonMusic provides two player implementations by default. 


Message Callbacks
-----------------

All players feature functions to play musical objects. These functions allow for callbacks that react to certain stages 
of the playback.

To add a callback to a playback define a function or lambda-expression and pass it as a parameter.

.. code-block:: python

    from pythonmusic import *

    SF2_PATH = "./resources/gm.sf2"
    player = SynthPlayer(SF2_PATH)


    def my_on_start(messages: list[MidiMessage]):
        print("Starting playback")
        print(f"playing {len(messages)} messages")


    def my_on_message(message: MidiMessage, time: float):
        print(f"Playing message at {time}: {message}")


    phrase = Phrase([Note(C4, EN), Note(D4, EN), Note(E4, EN)])
    player.play_phrase(
        phrase,
        ADAGIO,
        0,
        on_start=my_on_start,
        on_message=my_on_message,
        on_end=lambda finished: print(f"did finish? {finished}"),
    )

More information on available methods can be found at the bottom of this document, or in :obj:`Player <pythonmusic.play.Player>`.


MidiPlayer
----------

The :obj:`MidiPlayer <pythonmusic.play.MidiPlayer>` can be used to play scores and other objects on MIDI capable devices.

To create a midi player, you need the name of an open midi input (receiver) port. These ports can be retrieved using the 
:meth:`get_midi_receivers <pythonmusic.io.get_midi_receivers>` function.

.. code-block:: python

    from pythonmusic import *

    receivers = get_midi_receivers()


The receivers name can then be used to create the midi player.

.. code-block:: python

   receiver = receivers[0]  # get the first receiver
   player = MidiPlayer(receiver)

If you know the name of the midi receiver, you can simply pass that as a string to the midi player constructor.

.. important:: On some systems, the name a MIDI port is listed as may differ from its declared name. 
  On Linux, for instance, a device labled ``SomeCompany Digital Piano`` may be listed as ``SomeCompany Digital
  Piano: SomeCompany Digital Piano MIDI 1 28:0``. In this case, the system's name needs to be retrieved.

  .. code-block:: python
    
    RECEIVER_NAME = "SomeCompany Digital Piano"

    # This function searches for a closely-named open port
    receiver = find_midi_receiver(RECEIVER)

    # check if any port was found
    if receiver is None:
        raise IOError("receiver not found")

    player = MidiPlayer(receiver)
    player.play_score(score)


When using a :obj:`MidiPlayer <pythonmusic.play.MidiPlayer>`, you may want to add a small delay after your
playback finishes. A note may still continue to play (fade out, or similar) on the synthesizer even after 
the note-off event has been sent. If Python terminates before the sound finishes, you may experience a cut 
off on your midi receiver. 

.. code-block:: python

   from pythonmusic import *
   from time import sleep

   ...

   player = MidiPlayer("Some Piano")
   player.play_score(score)
   sleep(1)

Reference
.........

.. autoclass:: pythonmusic.play.MidiPlayer
   :no-index:
   :members:
   :undoc-members:
   :show-inheritance:


SynthPlayer
-----------

A player implementation for the :obj:`Synth <pythonmusic.synth.Synth>` synthesizer.

The synth player requires a SoundFont2 compatible instrument library. These libraries can be found online. For a working example,
have a look at a `Default Windows MIDI SoundFont <https://musical-artifacts.com/artifacts/713>`_.

To create a synth player, pass the path to a SoundFont2 library to the initialiser.

.. code-block:: python

    from pythonmusic import *

    SF2_PATH = "./resources/gm.sf2"
    player = SynthPlayer(SF2_PATH)

.. note::

    If you create a :obj:`SynthPlayer <pythonmusic.synth.SynthPlayer>` (or a :obj:`Synth <pythonmusic.synth.Synth>`), no instrument is 
    selected by default. You need to manually select an instrument for each channel.

    .. code-block:: python

       player.set_instrument(channel=0, instrument=VIOLIN)

    Use one of the provided :mod:`instrument constants <pythonmusic.constants.instruments>`.


Not all features of MIDI may be availble with this player. Some features may be further restricted depending on the selected
SoundFont2 library.

.. note:: Depending on your playform, you may see a lot of messages when initialising this object.
  FluidSynth may report any invalid instruments found in the selected SF2 library. The library will propably still work.
  Some sound drivers (i.e. ALSA) may try to find some outputs that are not availble. If you hear sound, you should be fine.

Reference
.........

.. autoclass:: pythonmusic.synth.SynthPlayer
   :no-index:
   :members:
   :undoc-members:
   :show-inheritance:


The Abstract Player Class
-------------------------

Both :obj:`SynthPlayer <pythonmusic.synth.SynthPlayer>` and :obj:`MidiPlayer <pythonmusic.play.MidiPlayer>` inherit from the 
:obj:`Player <pythonmusic.play.Player>` abstract class. This class enables you to write your own player implementation. To do so, 
subclass the :obj:`Player <pythonmusic.play.Player>` object and implement the :meth:`play_message() <pythonmusic.play.Player.play_message>`
method.

.. code-block:: python

    from typing import override
    from pythonmusic import *


    class MyPlayer(Player):
        @override
        def play_message(self, message: MidiMessage):
            print(f"Received MIDI Message: {message}")


    player = MyPlayer()
    player.play_phrase(Phrase([Note(C4, EN), Note(E4, QN)]), ADAGIO)


Optionally, you can also override the :meth:`set_instrument <pythonmusic.play.Player.set_instrument>` and 
:meth:`send_cc <pythonmusic.play.Player.send_cc>` methods to add more functionality.

Reference
.........

.. autoclass:: pythonmusic.play.Player
   :no-index:
   :members:
   :undoc-members:
   :show-inheritance:


CodePlayer
----------

The :obj:`CodePlayer <pythonmusic.play.CodePlayer>` is a different kind of player. It allows you to specify a playback function 
that reacts to a note event as opposed to :obj:`MidiMessages <pythonmusic.io.MidiMessage>` for normal players.

When creating a new :obj:`CodePlayer <pythonmusic.play.CodePlayer>` object, you can optionally pass an already initialised 
:obj:`Player <pythonmusic.play.Player>` (sub-) class to enable playback with that player during your callback. The callback 
needs to be defined with certain parameters. See below.

.. code-block:: python

    from pythonmusic import *


    def my_callback(
        proxy: ProxyPlayer,
        note: Note,
        channel: int,
        instrument: int,
        panning: int,
    ):
        print(f"{note} on channel {channel}, instrument {instrument}, panning {panning}")
        proxy.play_note(note)


    receiver = find_midi_receiver("Digital Piano")
    if receiver is None:
        print("Device not found")
        exit(1)

    midi_player = MidiPlayer(receiver)
    code_player = CodePlayer(midi_player, my_callback)


If you don't want to use an internal player, pass an explicit ``None`` instead of the player.

.. code-block:: python

   code_player = CodePlayer(None, my_callback)
   

Inside your callback, you can can update a channel's instrument or panning by passing a value to the 
corresponding parameter of the :meth:`play_code() <pythonmusic.play.ProxyPlayer.play_node>` method. 
These changes will be saved during the playback, but generally revert back to default values when a 
new play-session starts. 
You can also reroute a note to a different channel. This will update the instrument and panning
of that channel, instead.

.. important:: You can access other players from within your callback. However, keep in mind that normal players will block the 
   thread during playback and wait for a given note to finish.
   This means that you would not be able to playback multiple notes at the same time. Use the provided
   :obj:`ProxyPlayer <pythonmusic.play.ProxyPlayer>`, instead.

   .. code-block:: python

      synth = SynthPlayer("./resources/gm.sf2")

      def my_callback(
        proxy: ProxyPlayer, 
        note: Note, 
        channel: int, 
        instrument: int,
        panning: int
      ):
        # do this
        proxy.play_note(note)
        # not this
        synth.play_note(note)

      player = CodePlayer(synth, my_callback)
      player.play_score(...)


Reference
.........

.. autoclass:: pythonmusic.play.CodePlayer
   :no-index:
   :members:
   :undoc-members:
   :show-inheritance:

ProxyPlayer
...........

A proxy player is an object that stores note events you pass to it during your callback. Generally, you do not need
to create this class yourself, an instance will be passed to your playback function.

.. autoclass:: pythonmusic.play.ProxyPlayer
   :no-index:
   :members:
   :undoc-members:
   :show-inheritance:


SamplePlayer
------------

The :obj:`SamplePlayer <pythonmusic.play.SamplePlayer>` is a player implementation around a
:obj:`AudioSampler <pythonmusic.sample.AudioSampler>`. For more information see the 
:doc:`Sample <../objects/sample>` section.

.. autoclass:: pythonmusic.play.SamplePlayer
   :no-index:
   :members:
   :undoc-members:
   :show-inheritance:
