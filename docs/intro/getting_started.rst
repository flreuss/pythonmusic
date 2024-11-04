Getting Started
===============

Creating a Project
------------------

PythonMusic is a normal Python library that can be added to your projects.

.. note:: All instructions below that need to be run in the terminal assume that the ``python`` command is available. If this command is not found, try using ``python3`` instead.

.. important:: The instructions below may not work while the project's repository is not public. Instead, download the repo as a zip and install locally.

Choose one of the installation steps below. For beginners, using PyCharm is recommended.


In PyCharm
..........

Download and install PyCharm (Community) from the official `download page <https://www.jetbrains.com/pycharm/download/>`_.

Create a new project. Make sure that "Project venv" and a Python version ``>=3.11`` are selected in the dialogue.

To add PythonMusic to your project, open the Python Packages toolbar in the lower left corner.

CONTINUE HERE


In Visual Studio Code
.....................

Open VS Code inside a new folder, or if already present, your existing project. Install the Python extension from the Extensions Marketplace (left sidebar). 

Creating the Environment
~~~~~~~~~~~~~~~~~~~~~~~~

Click on "View" in the menu bar at the top of the window and select "Open Command Pallete". Search for "Python: Create Environment", select "Venv", and confirm your Python version. This should create a 
``.venv`` directory in your project folder. 

Next, open a terminal from "Terminal" in the menu bar and select "New Terminal". Continue from the :ref:`"Activate the Environment" <from_vs_activate>` below.


In the Terminal
...............

Creating the Environment
~~~~~~~~~~~~~~~~~~~~~~~~

In the terminal, we need to create the virtual environment manually. Starting in Python ``3.4``, this can be done using the *venv* module. The command below will create a new environment.

.. code-block:: bash

   python -m venv venv

.. _from_vs_activate:

Activate the Environment
~~~~~~~~~~~~~~~~~~~~~~~~

Activating the environment differs depending on your operating system.


Linux and macOS
***************

On Linux and macOS, the *source* command is used to activate the environment. The script to do so can be found in ``./venv/bin/activate``.

.. code-block::

   source venv/bin/activate


Windows
*******

On Windows, activate the environment by running the activate script. Which script to run depends on the type of console you are using.

.. code-block:: powershell

   # in powershell
   venv\Scripts\Activate.ps1

   # in command prompt (cmd.exe)
   venv\Scripts\activate.bat


Adding PythonMusic
~~~~~~~~~~~~~~~~~~

In your activated environment, install PythonMusic with pip.

.. code-block:: bash

   pip install git+https://gitup.uni-potsdam.de/music-with-pc/pythonmusic


Importing PythonMusic
---------------------

In your ``main.py``, import PythonMusic. This can be done as a ``*``-import which imports all definitions, 
or by importing symbols directly:

.. code-block:: python

   from pythonmusic import *
   # or
   from pythonmusic import Score, Part, Phase, Note, ...


A small Melody
--------------

Below we create a small melody and play it back though a :obj:`SynthPlayer <pythonmusic.synth.SynthPlayer>`.
As an alternative, this example also shows how to use the :obj:`MidiPlayer <pythonmusic.play.MidiPlayer>`
below, if you don't want to use the synth.

First, we import the ``pythonmusic`` module. We also define a path constant to a SoundFont2 library, which
we will need later. 

.. code-block:: python

    from pythonmusic import *

    SF2_PATH = "./resources/gm.sf2"

SoundFont2 libraries can be found online. For a good start, have a look at a
`Default Windows MIDI SoundFont <https://musical-artifacts.com/artifacts/713>`_. For more information on
the synth player, see the :doc:`Players <../objects/players>` page. 

Now we can define a list of notes that make up our melody. In their basic form, notes are defined by their
pitch, the first parameter, and their duration, the second parameter. Various constants are provided for
pitches and durations.

Pitches are defined by their root note (for instance, ``A``) and their octave (for instance, ``4``). If a
note has a ♭ or a ♯, the root note is folled by a ``F`` (flat) or ``S`` (sharp), respectively. See 
:mod:`pitch constants <pythonmusic.constants.pitches>` for a list of available pitches.

Durations are defined by their name (for instance, ``WHOLE_NOTE``), though abbreviations such as ``WN`` are
provided. They can be preceded by modifiers (for instance, ``D`` for double). For a complete list of 
defined durations, see :mod:`duration constants <pythonmusic.constants.durations>`.

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

The list of notes can then be added to a :obj:`Phrase <pythonmusic.music.phrase>`.

.. code-block:: python

    phrase = Phrase(notes)

Next, we create a part, assign a title and an instrument, and add our phrase.

.. code-block:: python

   part = Part("A Druid", FLUTE)
   part.add_phrase(phrase)

Finally, we create a score from our part.

.. code-block:: python

   score = Score("Op. 60 No. 1")
   score.tempo = 96  # tempo in bpm
   score.add_part(part)

To playback the score, we create a ``SynthPlayer`` object. For this we need pass the path constant we defined in the
beginning to tell the player which SoundFont2 library to load.

.. code-block:: python

   player = SynthPlayer(SF2_PATH)
   player.play_score(score)

Alternatively, we can also stream our score to a MIDI keyboard or other MIDI receiver, such as a DAW. For this,
create a :obj:`MidiPlayer <pythonmusic.play.MidiPlayer>` object, and pass the name of the MIDI receiver.

.. code-block:: python

    RECEIVER = "SomeCompany Digital Piano"
    player = MidiPlayer(RECEIVER)
    player.play_score(score)

To dynamically choose a port name, use the :meth:`get_midi_receivers <pythonmusic.io.get_midi_receivers()>`
function.

.. code-block:: python

   receiver = get_midi_receivers()[0]  # get the first receiver
   player = MidiPlayer(receiver)
   player.play_score(score)

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

This leaves us with the example ``spring.py`` from PythonMusic's examples. More example scores can be found
in the project's `example directory <https://gitup.uni-potsdam.de/music-with-pc/pythonmusic/-/tree/main/examples>`_.
For code snippets and a starter template, have a look at the :doc:`Examples <./examples>` section.

.. code-block:: python

    from pythonmusic import *

    # Defines the path to a SoundFont2 file. Change as needed.
    SF2_PATH = "./resources/gm.sf2"

    # A list of notes that represent the melody.
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

    # A phrase that contains the notes.
    phrase = Phrase(notes)

    # A part represents an instrument in a score.
    part = Part("A Druid", FLUTE)
    part.add_phrase(phrase)

    # A score represents a piece of music.
    score = Score("Op. 60 No. 1")
    score.tempo = 96  # in bpm where a beat is a quarter
    score.add_part(part)


    # === Using the SynthPlayer ===
    # If FluidSynth was not found on your system, the Synth and SynthPlayer classes
    # will not be available.
    try:
        player = SynthPlayer(SF2_PATH)
        player.play_score(score)
    except NameError:
        print("FluidSynth was not detected. Skipping")

    # === Using a MIDI Keyboard ===
    # Find midi devices connected to your system
    receivers = get_midi_receivers()
    if len(receivers) > 0:
        # get the first receiver
        receiver = receivers[0]

        player = MidiPlayer(receiver)
        player.play_score(score)
    else:
        print("No midi devices found")
