Phrase Elements
===============

:obj:`Phrase elements <pythonmusic.music.PhraseElement>` are :obj:`notes <pythonmusic.music.Note>` and 
:obj:`chords <pythonmusic.music.Chord>`. They can be added to :obj:`phrases <pythonmusic.music.Phrase>` to create melodies and rhythms.

.. autoclass:: pythonmusic.music.PhraseElement
   :no-index:
   :members:
   :undoc-members:
   :show-inheritance:

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


Articulations
.............

Articulations can be added to notes to change their length, velocity, or general playback behaviour. To add an articulation to a Note,
either pass a list of articulations to the notes initialiser, or use the :meth:`add_articulation <pythonmusic.music.Note.add_articulation>`
method.

.. code-block:: python

   note_a = Note(C4, EN, [LEGATO])

   note_b = Note(C4, EN)
   note_b.add_articulation(LEGATO)

   assert note_a == note_b

For a list of articulations, see the defined :mod:`articulation constants <pythonmusic.constants.articulations>`.


Reference
.........

.. autoclass:: pythonmusic.music.Note
   :no-index:
   :members:
   :undoc-members:
   :show-inheritance:


Chord
-----

While :obj:`phrases <pythonmusic.music.phrase>` store phrase elements horizontally, chords are used to store them vertically. Use a 
:obj:`chord <pythonmusic.music.Chord>` to create groups of notes that are played at the same time.

Chords are constructed similarly to phrases in that you pass a list of notes to the constructor.

.. code-block:: python

   >>> from pythonmusic import *
   >>> chord = Chord([Note(C4, EN), Note(G5, EN), ...])

A chord can also be constructed from a base note and intervals, or lists defining the chord's notes by their parts.

.. code-block:: python

   >>> from pythonmusic import *
   >>> chord_a = Chord.from_root(C4, MAJOR, QN, MF)
   >>> chord_b = Chord.from_lists([C4, E4, G4], [QN, QN, QN], [MF, MF, MF])
   >>> assert chord_a == chord_b  # both chords are identical


Reference
.........

.. autoclass:: pythonmusic.music.Chord
   :no-index:
   :members:
   :undoc-members:
   :show-inheritance:


A Collection of Notes
.....................

Like :obj:`phrases <pythonmusic.music.Phrase>`, chords inherit from :obj:`NoteCollection <pythonmusic.music.NoteCollection>` and share
a few common methods.


.. autoclass:: pythonmusic.music.NoteCollection
   :no-index:
   :members:
   :undoc-members:
   :show-inheritance:

For more information, see the :doc:`Music reference page <../reference/music>`.
