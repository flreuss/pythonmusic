Phrases
=======

Phrases group :obj:`notes <pythonmusic.music.Note>` and :obj:`chords <pythonmusic.music.Chord>` 
(:obj:`PhraseElement <pythonmusic.music.PhraseElement>`) to melodies. Unlike chords, phrases are oriented horizontally.

To add notes to a phrase, either pass a list of notes to the initialiser, or add them later.

.. code-block:: python

   phrase = Phrase([Note(C4, EN), Note(C5, EN)])

   phrase = Phrase()
   phrase.add_note(Note(C4, EN))


Notes can also be added by their individual parts. The 
:meth:`add_notes_by_lists <pythonmusic.music.NoteCollection.add_notes_by_lists>` method allows you to define
lists of pitches, durations, and dynamics to add notes to a phrase.

.. code-block:: python

   phrase = Phrase()
   phrase.add_notes_by_lists([A4, B4, C5], [QN, QN, QN], [MF, MF, MF])

.. note:: 
   When adding elements by lists, you only need to define at least one element for each property. If there are,
   for instance, more pitches than durations, the last given duration is used for all remaining notes.

   .. code-block::
    
      # all notes will have duration QN and dynamic MF 
      phrase.add_notes_by_lists([A4, B4, C5, D5, E5], [QN], [MF])

   This also works for :meth:`add_chord_by_lists <pythonmusic.music.Phrase.add_chord_by_lists>` and
   :meth:`add_chords_by_lists <pythonmusic.music.Phrase.add_chords_by_lists>` described below.

Chords can also be added using a similar method, :meth:`add_chord_by_lists <pythonmusic.music.Phrase.add_chord_by_lists>`.

.. code-block:: python

   phrase = Phrase()
   phrase.add_chord_by_lists([A4, C5, E5], [QN], [MF])

To add multiple chords at the same time, you can use :meth:`add_chords_by_lists <pythonmusic.music.Phrase.add_chords_by_lists>`.
Keep in mind that while you don't need to specify dynamics and durations for all given pitches, you must still provide a non-empty
list for pitch, duration, and dynamic for each chord.

.. code-block:: python

   # adds two chords
   phrase = Phrase()
   phrase.add_chords_by_lists(
     [[A4, C5, E5], [GS4, B4, DS5]],  # must contain two lists of pitches
     [[QN], [QN]],                    # must contain two lists of dynamics
     [[MF], [MF]],                    # must contain two lists of dynamics
   )

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
