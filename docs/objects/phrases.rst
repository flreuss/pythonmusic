Phrases
=======

Phrases group :obj:`notes <pythonmusic.music.Note>` and :obj:`chords <pythonmusic.music.Chord>` 
(:obj:`PhraseElement <pythonmusic.music.PhraseElement>`) to melodies. Unlike chords, phrases are oriented horizontally.

To add notes to a phrase, either pass a list of notes to the initialiser, or add them later.

.. code-block:: python

   phrase = Phrase([Note(C4, EN), Note(C5, EN)])

   phrase = Phrase()
   phrase.add_note(Note(C4, EN))

Reference
---------

.. autoclass:: pythonmusic.music.Phrase
   :no-index:
   :members:
   :undoc-members:
   :show-inheritance:

A Collection of Notes
---------------------

Like chords, phrases inherit from :obj:`NoteCollection <pythonmusic.music.NoteCollection>` and share a few common methods. See the 
reference below for more information.


.. autoclass:: pythonmusic.music.NoteCollection
   :no-index:
   :members:
   :undoc-members:
   :show-inheritance:
