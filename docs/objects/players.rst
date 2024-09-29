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


Callbacks
---------

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

.. note:: Depending on your playform, you may see a lot of messages when initialising this object.
  FluidSynth may report any invalid instruments found in the selected SF2 library. The library will propably still work.
  Some sound drivers (i.e. ALSA) may try to find some outputs that are not availble. If you hear sound, you should be fine.

Not all features of MIDI may be availble with this player. Some features may be further restricted depending on the selected
SoundFont2 library.

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


Reference
.........

.. autoclass:: pythonmusic.play.Player
   :no-index:
   :members:
   :undoc-members:
   :show-inheritance:
