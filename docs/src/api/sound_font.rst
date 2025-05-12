Sound Font
==========

PythonMusic support playback via `SoundFonts <https://en.wikipedia.org/wiki/SoundFont>`_ via the 
`tinysoundfont <https://nwhitehead.github.io/tinysoundfont-pybind/index.html>`_ library.

The :obj:`SfPlayer <pythonmusic.play.SfPlayer>` :obj:`Target <pytonmusic.play.Target>` implementation can
load SoundFont2 and SoundFont3 files.

.. code-block:: python

    from pythonmusic import *

    SF_PATH = "path/to/sound_font.sf2"

    target = SfTarget(SF_PATH)
    player = Player(target)

    ...

    player.play_score(my_score)

You can adjust the base volume of the entire loaded SoundFont by changing the ``gain`` parameter.

.. important::
   When playing back :obj:`notes <pythonmusic.music.Note>`, :obj:`chords <pythonmusic.music.Chord>`, or
   :obj:`phrases <pythonmusic.music.Phrase>` the instrument must be set manually.

   .. code-block:: python

      from pythonmusic import *

      SF_PATH = "path/to/sound_font.sf2"
      CHANNEL = 2

      target = SfTarget(SF_PATH)
      target.set_instrument(CHANNEL, ACOUSTIC_BASS)

      ...

      player = Player(target)
      player.play_phrase(my_phrase, CHANNEL)

The :obj:`SfPlayer <pythonmusic.play.SfPlayer>` also provides a player implementation.

Reference
---------
.. autoclass:: pythonmusic.play.SfPlayer
   :no-index:
   :members:
   :undoc-members:
   :show-inheritance:
