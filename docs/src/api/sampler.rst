Sampler
=======

The sampler is a :obj:`Target <pythonmusic.play.Target>` implementation that allows you to load ``.wav`` files into your project and use them as instruments.

To create a new sampler, instantiate the class and add samples with :meth:`add_sample <pythonmusic.play.SamplerTarget.add_sample>` or 
:meth:`add_sample_for_keys <pythonmusic.play.SamplerTarget.add_sample_for_keys>`.

.. code-block:: python

    sampler = SamplerTarget()
    sampler.add_sample_for_keys("path/to/sample.wav", A4, range(A3, A6))


The library also provides a :obj:`Player <pythonmusic.play.Player>` implementation, the :obj:`SamplerPlayer <pythonmusic.play.SamplerPlayer>`.

.. note::
   By default, a sample rate of 44,100 Hz is set. You can change this in the class initialiser. All ``.wav`` files that are sampled at a different rate
   are resampled when added to the sampler.


Adding Samples
--------------

The sampler provides two methods to add samples.

The :meth:`add_sample <pythonmusic.play.SamplerTarget.add_sample>` method takes a sample and adds it to a single key. Use this method if you have a lot
of samples that you want to add to one key each. The sample is not pitched.

.. code-block:: python

    from pythonmusic import *

    SAMPLES = [
        "samples/piano_a4.wav",
        "samples/piano_bf4.wav",
        "samples/piano_b4.wav",
        "samples/piano_c4.wav",
        ...
    ]

    sampler = SamplerTarget()
    for offset, sample in enumerate(SAMPLES):
        sampler.add_sample(sample, A4 + offset)

    ...

    player = Player(sampler)
    player.play_phrase(my_phrase)


Use :meth:`add_sample_for_keys <pythonmusic.play.SamplerTarget.add_sample_for_keys>` to pitch a single sample across multiple keys.
This method takes a single sample and a range or list of keys as arguments. You also need to provide the pitch of the sample. The
sample is pitched to each defined key, which may take a few seconds.

.. code-block:: python

    from pythonmusic import *

    SAMPLE = "samples/synth_c5.wav"

    sampler = SamplerTarget()
    sampler.add_sample_for_keys(SAMPLE, C5, range(C2, C7))

    ...

    player = Player(sampler)
    player.play_score(my_score)

Both methods also accept a ``base_amp`` property, which is used to adjust the base volume of the sample, and a ``falloff`` property, which defines how long 
a sample should continue playing after the *note off* event has been received. The latter avoids a popping sound when samples end abruptly.

Reference
---------
.. autoclass:: pythonmusic.play.SamplerTarget
   :no-index:
   :members:
   :undoc-members:
   :show-inheritance:
