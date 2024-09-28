.. PythonMusic documentation master file, created by
   sphinx-quickstart on Sun Sep  8 13:14:04 2024.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

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

PythonMusic is a music library written in pure Python that enables you to write music in code.

.. code-block:: python

   from pythonmusic import *

   phrase = Phrase([
       Note(C4, EN),
       Note(E4, EN),
       Note(G4, QN)
   ])
   part = Part("Piano", ACOUSTIC_GRAND_PIANO)
   score = Score("MyScore", [part], ADAGIO)


Export your scores to midi files, or send them to a midi-capable device.

.. code-block:: python

   export_score(score, "output/my_score.mid")
   player = MidiPlayer("SomeKeyboard")
   player.play_score(score)


Use a :obj:`SynthPlayer <pythonmusic.synth.SynthPlayer>` and a `SoundFont2 <https://en.wikipedia.org/wiki/SoundFont>`_ compatible library to playback a score on your device.

.. code-block:: python

   ...
   player = SynthPlayer("path/to/sound_font.sf2")
   player.play_score(score)


To get started, see the :doc:`Installation <intro/installation>` and :doc:`Getting Started <intro/getting_started>` sections of this document.


Requirements
------------

Requires Python ``>=3.11``. See :doc:`Installation <intro/installation>` for more information.

Source Code
-----------

Source code is available on this project's `repository <https://gitup.uni-potsdam.de/music-with-pc/pythonmusic>`_.

.. toctree::
   :caption: Start Here
   :maxdepth: 4
   :hidden:

   intro/installation
   intro/getting_started
   intro/examples

.. toctree::
   :caption: Objects
   :maxdepth: 4
   :hidden:

   objects/phrase_elements
   objects/phrases
   objects/parts
   objects/scores
   objects/players
   objects/midi_io

.. toctree::
   :caption: Reference
   :maxdepth: 1
   :hidden:

   reference/music
   reference/constants
   reference/play
   reference/io
   reference/synth
   reference/helpers
   reference/util

.. toctree::
   :caption: Appendix
   :maxdepth: 4
   :hidden:

   appendix/midi
   appendix/licenses
   appendix/build_doc
   appendix/class_diagram
