Metronome
=========

Use the metronome to run code periodically on a beat.

To start the metronome use either the :meth:`start() <pythonmusic.metronome.Metronome.start>` method which allows your script to continue,
or :meth:`block() <pythonmusic.metronome.Metronome.block>` which blocks execution until the metronome stops playing.

.. code-block:: python

  from pythonmusic import *
  from time import sleep

  metronome = Metronome(120, 4)
  metronome.start()

  # block thread to prevent script from finishing
  while True:
    sleep(1)

Callback
--------

The metronome's initialiser accepts a callback that is called once per beat. The callback should return a boolean that indicated whether
the metronome should continue to count.

Below, an example of a metronome that counts to 8, then stops.

.. code-block:: python

    from pythonmusic import *

    MAX = 8

    global beats
    beats: int = 0

    def my_callback() -> bool:
        global beats

        beats += 1
        return beats < MAX

    metronome = Metronome(120, 4, callback=my_callback)
    metronome.block()



Metronome Volume and other Targets
----------------------------------

By default, the beats are audible via a :obj:`SynthesizerTarget <pythonmusic.play.SynthesizerTarget>`. This can be muted by 
either setting the volume to ``0``, or passing an :obj:`EmptyTarget <pythonmusic.play.EmptyTarget>` as the target.

.. code-block:: python

   from pythonmusic import *

   metronome = Metronome(120, 3)
   metronome.set_velocity(0)

   # or

   metronome = Metronome(120, 3, target=EmptyTarget())

Any target may be used for playing back the metronome's sound. You can update the on-beat and off-beat pitch (key) with
:meth:`set_on_beat <pythonmusic.metronome.Metronome.set_on_beat>` and
:meth:`set_off_beat <pythonmusic.metronome.Metronome.set_off_beat>`


Reference
---------

.. autoclass:: pythonmusic.metronome.Metronome
   :no-index:
   :members:
   :undoc-members:
   :show-inheritance:
