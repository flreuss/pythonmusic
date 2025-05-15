Mods
====

The ``mods`` module contains methods that you can use to alter melodies, phrases, etc. The module is exported as ``mods``, so to call a
method, prefix with ``mods.``:

.. code-block:: python

   from pythonmusic import *

   phrase = Phrase([Note(C4, QN), Note(EF4, QN)])
   melody = mods.repeat_phrase(phrase, 3)



.. automodule:: pythonmusic.mods
   :members:
   :undoc-members:
   :show-inheritance:
