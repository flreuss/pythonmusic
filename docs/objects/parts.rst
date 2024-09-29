Parts
=====

Parts represent an instrument in a :obj:`Score <pythonmusic.music.Score>`. Think of them as individual staves on sheet music.
Most instruments will only have one stave/part, whereas others may have multiple. Some instruments, while having multiple staves, 
may still be able to be represented with a single part, such as the piano or accordion. Its up to you how to split up your composition.

.. note:: Instruments are set at the beginning of the score. Make sure not to use multiple instruments on the same channel.

To create a part, call its initialiser and pass a title and instrument. Use the ``phrases`` parameter to add phrases on initialisation, 
``channel`` to set the channel of the instrument, and ``panning`` to set the panning of the part.

.. code-block:: python

    part = Part("Violin 1", 
                VIOLIN, 
                [phrase_a, phrase_b],
                0,
                PAN_CENTER)

    part.add_phrase(phrase_c)

.. important:: Keep in mind that MIDI channel 10 is reserved for percussion kit instruments. See 
   :mod:`percussion <pythonmusic.constants.percussion>` constants for more information.


Reference
---------

.. autoclass:: pythonmusic.music.Part
   :no-index:
   :members:
   :undoc-members:
   :show-inheritance:
