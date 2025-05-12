PythonMusic
===========

.. toctree::
   :caption: Contents:
   :maxdepth: 4

.. toctree::
   :caption: Introduction
   :maxdepth: 4
   :hidden:

   self


Overview
--------

PythonMusic is a library for writing music in code. Written in pure Python, it features a simple interface for creating your compositions:

.. code-block:: python

   from pythonmusic import *

   phrase = Phrase([
       Note(C4, EN),
       Note(E4, EN),
       Note(G4, QN)
   ])
   part = Part("Piano", ACOUSTIC_GRAND_PIANO, [phrase])
   score = Score("MyScore", [part], ADAGIO)


Export your score to midi files, or send them to a midi-capable device connected to your computer.

.. code-block:: python

   export_score(score, "output/my_score.mid")
   player = MidiOutPlayer("SomeKeyboard", False)
   player.play_score(score)

This library supports playback via an integrated `SoundFont <https://en.wikipedia.org/wiki/SoundFont>`_ player.

.. code-block:: python

   ...
   player = SfPlayer("path_to_soundfont.sf2")
   player.play_score(score)


To get started, see the :doc:`Installation <intro/installation>` and :doc:`Getting Started <intro/getting_started>` sections of this document.


Requirements
------------

Requires Python ``>=3.12``. See :doc:`Installation <intro/installation>` for more information.

Source Code
-----------

Source code is available on the project's `repository <https://gitup.uni-potsdam.de/music-with-pc/pythonmusic>`_.


.. toctree::
   :caption: Start Here
   :maxdepth: 4
   :hidden:

   intro/installation
   intro/getting_started


.. toctree::
   :caption: API
   :maxdepth: 4
   :hidden:

   api/phrase_elements
   api/phrases
   api/parts
   api/scores
   api/play
   api/midi_io
   api/sound_font
   api/sampler
   api/synthesizer
   api/metronome


.. toctree::
   :caption: Reference / API
   :maxdepth: 1
   :hidden:

   reference/constants
   reference/metronome
   reference/midi
   reference/mods
   reference/music
   reference/osc
   reference/play
   reference/utility


.. toctree::
   :caption: Appendix
   :maxdepth: 4
   :hidden:

   appendix/licenses
   appendix/midi
   appendix/build_documentation
