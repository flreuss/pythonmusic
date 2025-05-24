Getting Started
===============

Importing PythonMusic
---------------------

Create a new Python file and import PythonMusic. This can be done as a wildcard (``*``) import which imports 
all definitions, or by specifying symbols directly:

.. code-block:: python

   from pythonmusic import *
   # or
   from pythonmusic import Note, Chord, C4, EF4, QN, MF

   note = Note(C4, QN, MF)
   chord = Chord([note, Note(EF4, QN, MF)])

You can import PythonMusic as a module, in which case you need to prefix all of this library's 
types and functions with the module name.

.. code-block:: python

   import pythonmusic as pm

   note = pm.Note(pm.C4, pm.QN, pm.MF)
   chord = pm.Chord([note, pm.Note(pm.EF4, pm.QN, pm.MF)])

.. note::
   There is some discussion on wildcard imports in Python. While this can lead to import issues 
   and should generally avoided, this documentation uses them for simplicity.


Installing a SoundFont
----------------------

SoundFonts are libraries that contain a single or multiple instruments and are used by this libary's
`SfTarget <pythonmusic.play.SfTarget>` to play back your projects. More on that in the example below.

You can find SoundFonts online. For a good starting point, have a look at 
`Default Windows MIDI SoundFont <https://musical-artifacts.com/artifacts/713>`_. 
Once downloaded, save the `.sf2` or `.sf3` file in a location accessable by your project. For instance,
create a directory called `sound_fonts` in your project and save it there.


A small Melody
--------------

Below we create a small melody and play it, using an :obj:`SfTarget <pythonmusic.play.SfTarget>`.

First, we ipmort the ``pythonmusic`` module. We also define a path constant to a SoundFont library, which 
we will need later.

.. code-block:: python

   from pythonmusic import *

   SF_PATH = "sound_fonts/FluidR3_GM2-2.sf2"


Next, we define a list of notes that make up our melody. In their basic form, notes are defined by their
pitch and duration. Optionally, you can also set the velocity (volume) and articulation. Various
:mod:`constants <pythonmusi.constants>` are provided.

Pitches are defined by their root note (for instance, ``A``) and their octave (for instance, ``4``). If a
note has a ♭ or a ♯, the root note is folled by a ``F`` (flat) or ``S`` (sharp), respectively. See 
:mod:`pitch constants <pythonmusic.constants.pitches>` for a list of available pitches.

Durations are defined by their name (for instance, 
:obj:`WHOLE_NOTE <pythonmusic.constants.durations.WHOLE_NOTE>`), though abbreviations such as 
:obj:`WH <pythonmusic.constants.durations.WN>` are provided. They can be preceded by modifiers (for 
instance, ``D`` for double). For a complete list of defined durations, see 
:mod:`duration constants <pythonmusic.constants.durations>`.

.. code-block:: python

    notes = [
        Note(A4, QN),
        Note(CS5, DHN),
        Note(D5, QN),
        Note(E5, WN + QN),
        Note(E5, QN),
        Note(CS5, QN),
        Note(E5, QN),
        Note(A5, DHN),
        Note(E5, QN),
        Note(CS5, QN),
        Note(D5, QN),
        Note(FS5, DQN),
        Note(E5, EN),
        Note(E5, HN),
        Note(CS5, HN),
    ]

The list of notes is then added to a :obj:`Phrase <pythonmusic.music.phrase>`.
:obj:`Parts <pythonmusic.music.Part>` group phrases into a voice. They usually represent a single
instrument. Parts are assigned a name and instrument. For a full list of supported instruments,
see :mod:`instruments <pythonmusic.constants.instruments>`.

.. code-block:: python

    phrase = Phrase(notes)
    part = Part(0, "A Druid", FLUTE)
    part.add_phrase(phrase)

Finally, we create a :obj:`score <pythonmusic.music.Score>` and add our part. Scores group multiple
parts into a single score.

.. code-block:: python

   score = Score("Op. 60 No. 1")
   score.tempo = 96  # tempo in bpm
   score.add_part(part)

In order to play back the score, we create an :obj:`SfPlayer <pythonmusic.play.SfTarget>` and a
:obj:`Player <pythonmusic.play.Player>`. Players convert our score and Parts, Phrases, etc. into
messages that a :obj:`Target <pythonmusic.play.Target>` can interpret and convert to sound. This
library provides various targets for playback. You can easily implement your own targets.
For more information on targets, see the :doc:`Playback <../api/play>` section.

.. code-block:: python

   target = SfTarget(SF_PATH)  # <-- our path from earlier
   player = Player(target)


.. note::
   PythonMusic also provides :obj:`players <../api/play>` that setup their target
   automatically. In this example, you can replace the target/player setup by creating a 
   :obj:`SfPlayer <pythonmusic.play.SfPlayer>`.

   .. code-block:: python

      # target = SfTarget(SF_PATH)
      # player = Player(target)

      player = SfPlayer(SF_PATH)


Play the score with the :meth:`play_score() <pythonmusic.play.Player.play_score>` method.

.. code-block:: python

   player.play_score(score)


For the full code, see the ``spring.py`` example song in ``examples/songs/``.

Playback on an External Device
..............................

You can also play your scores on external devices. Make sure that your midi keyboard or digital
piano is connected to your computer. You can check on available inputs and outputs with
:meth:`midi_inputs() <pythonmusic.midi.midi_inputs>` and :meth:`midi_outputs() <pythonmusic.midi.midi_outputs>`. 
In the example below, we use the 
:meth:`output_user_prompt() <pythonmusic.midi.output_user_prompt>`, which prompts the user to
choose one of the available midi receivers. The chosen midi device is then used to create a
:obj:`MidiOutTarget <pythonmusic.play.MidiOutTarget>`, which as a target, can be used to create
a player.

.. code-block:: python

    port = input_user_prompt()
    if port is None:
        print("no port found")
        exit(1)

    target = MidiOutTarget(port)
    player = Player(target)
    # player = MidiOutPlayer(port)

    player.play_score(score)
