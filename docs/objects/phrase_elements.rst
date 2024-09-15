Phrase Elements
===============

:obj:`Phrase elements <pythonmusic.music.PhraseElement>` are :obj:`notes <pythonmusic.music.Note>` and 
:obj:`chords <pythonmusic.music.Chord>`. They can be added to :obj:`phrases <pythonmusic.music.Phrase>` to create melodies and rhythms.

Note 
----
:obj:`Notes <pythonmusic.music.Note>` are the basic building blocks of PythonMusic. Use them to construct 
:obj:`phrases <pythonmusic.music.Phrase>` and :obj:`chords <pythonmusic.music.Chord>`.

.. code-block:: python

   >>> from pythonmusic import *
   >>> note = Note(C4, EN, MF, [STACCATO])

Notes are constructed from a :mod:`pitch <pythonmusic.constants.pitches>`, :mod:`duration <pythonmusic.constants.durations>`, and
:mod:`dynamic <pythonmusic.constants.dynamics>`. Optionally, you can define :mod:`articulations <pythonmusic.constants.articulations>`
to alter the length or velocity of the note.


Chord
-----
