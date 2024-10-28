Sample
======

Wave files can be played back using the :obj:`AudioSample <pythonmusic.sample.AudioSample>` class.
To load a sample, pass a path the file location to a sample's initialiser. The sample can then
be played back.

.. code-block:: python

   sample = AudioSample("sample.wav")
   sample.play()  # play once
   sample.loop(10)  # play 10 times

This enables you to load custom wave files to add textures and other sounds to your music. For
more information, see the documentation.

AudioSample Reference
.....................

.. autoclass:: pythonmusic.sample.AudioSample
   :no-index:
   :members:
   :undoc-members:
   :show-inheritance:


AudioSampler
............

Use the :obj:`AudioSampler <pythonmusic.sample.AudioSampler>` class to combine multiple 
:obj:`AudioSample <pythonmusic.sample.AudioSample>` instances. A sampler can connect an audio 
sample with a note pitch, which allows you to create custom instruments from sound files, or simply 
integrate multiple sound easily into your composition.

.. code-block:: python

  c4 = AudioSample("piano/c4.wav")
  d4 = AudioSample("piano/d4.wav")
  e4 = AudioSample("piano/e4.wav")

  sampler = AudioSampler()
  sampler.add_sample(c4, C4)
  sampler.add_sample(d4, D4)
  sampler.add_sample(e4, E4)

  player = SamplePlayer(sampler)
  player.play_score(score)

Reference
---------

.. autoclass:: pythonmusic.sample.AudioSampler
   :no-index:
   :members:
   :undoc-members:
   :show-inheritance:
