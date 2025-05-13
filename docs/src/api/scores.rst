Scores
======

Score represent musical pieces. Add parts to use multiple instruments at the same time.

To add parts to the score, pass them to the initialiser or add them manually.

.. code-block::

   score = Score("MyScore", [part_a], ADAGIO)
   score.add_part(part_b)

.. note:: All :obj:`parts <pythonmusic.music.Part>` contained in the score start playing at the same time. To offset the start time
    of a part, change the start time of the first phrase in the part.

You can playback scores by creating a :obj:`Player <pythonmusic.play.Player>` and passing the score to its :meth:`play_score() <pythonmusic.play.Player.play_score>` method.

.. code-block:: python

   player = SynthPlayer("path_to_sf2")
   player.play_score(score)

Reference
---------

.. autoclass:: pythonmusic.music.Score
   :no-index:
   :members:
   :undoc-members:
   :show-inheritance:
