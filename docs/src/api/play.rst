Playback
========

PythonMusic splits playback into two areas: *targets* implement functionality that responds to received (music) signals, *players*
convert music structures from this library to messages and use targets to play them back.

.. code-block:: python

   from pythonmusic import *

   target: Target = SfTarget("path/to/file.sf2")
   player = Player(target)  # takes any target


Targets
-------

All targets inherit from the :obj:`Target <pythonmusic.play.Target>` class. It is their responsibility to respond to incoming midi
messages or notifications (see methods). This can be in form of creating sound, such as the :obj:`SfTarget <pythonmusic.play.SfTarget>`, or
something else (see ``PrintTarget`` below).

By design, any target should work in place of any other target.

Reference
.........

.. autoclass:: pythonmusic.play.Target
   :no-index:
   :members:
   :undoc-members:
   :show-inheritance:

Creating a new Target
.....................

To create a new target, inherit from the :obj:`Target <pythonmusic.play.Target>` class. Override notification handler functions 
(:meth:`note_on <pythonmusic.play.Target.note_on>`, :meth:`note_off <pythonmusic.play.Target.note_off>`, ...) to replace existing 
functionality. To implement new handlers, override the :meth:`midi_message <pythonmusic.play.Target.midi_message>` method. See its
documentation for more information.

.. code-block:: python

    class PrintTarget(Target):
        @override
        def note_off(self, channel: int, key: int, velocity: int):
            print(f"NoteOff(channel: {channel}, key: {key}, velocity: {velocity})")

        @override
        def note_on(self, channel: int, key: int, velocity: int):
            print(f"NoteOn(channel: {channel}, key: {key}, velocity: {velocity})")

        @override
        def control_change(self, channel: int, control: int, value: int):
            print(f"CC(channel: {channel}, control: {control}, value: {value})")

        @override
        def program_change(self, channel: int, program: int):
            print(f"Changing instrument on channel {channel} to {program}")

        @override
        def midi_message(self, message: Message) -> bool:
            if super().midi_message(self, message):
                return True
            
            match message.type():
                ...



Included Targets
................

This library comes with a few pre-implemented targets.

.. autoclass:: pythonmusic.play.EmptyTarget
   :no-index:
   :members:
   :undoc-members:
   :show-inheritance:

.. autoclass:: pythonmusic.play.SfTarget
   :no-index:
   :members:
   :undoc-members:
   :show-inheritance:

.. autoclass:: pythonmusic.play.MidiOutTarget
   :no-index:
   :members:
   :undoc-members:
   :show-inheritance:

.. autoclass:: pythonmusic.play.SamplerTarget
   :no-index:
   :members:
   :undoc-members:
   :show-inheritance:

.. autoclass:: pythonmusic.play.SynthesizerTarget
   :no-index:
   :members:
   :undoc-members:
   :show-inheritance:


Players
-------

Players handle conversion of :obj:`notes <pythonmusic.music.Note>`, :obj:`chords <pythonmusic.music.Chord>`,
:obj:`phrases <pythonmusic.music.Phrase>`, :obj:`parts <pythonmusic.music.Part>`, and :obj:`scores <pythonmusic.music.Score>` to
:obj:`messages <pythonmusic.io.MidiMessage>` and use a provided target to play them back.

Reference
.........

.. autoclass:: pythonmusic.play.Player
   :no-index:
   :members:
   :undoc-members:
   :show-inheritance:


Callbacks
.........

All play methods, such as :meth:`play_note() <pythonmusic.play.Player.play_note>` accept a callback. This allows manipulation of each
:obj:`note <pythonmusic.music.Note>` that is about to be played. The callback receives the note, its channel, and a boolean that
indicates whether the note is part of a chord. The note may be shortened, though its duration in playback won't change. The
callback must return the note that will be played.

.. code-block:: python

    from pythonmusic import *

    def my_callback(note: Note, channel: int, is_chord: bool) -> Note:
        # mutes all notes on channel 1, pitch all other notes by +3
        if channel == 1:
            return note.as_rest()

        note.pitch += 3

        return note

    player.play_score(score, callback=my_callback)


Included Players
................

A few players that wrap targets are included for convenience.

.. autoclass:: pythonmusic.play.SfPlayer
   :no-index:
   :members:
   :undoc-members:
   :show-inheritance:

.. autoclass:: pythonmusic.play.MidiOutPlayer
   :no-index:
   :members:
   :undoc-members:
   :show-inheritance:

.. autoclass:: pythonmusic.play.MidiInPlayer
   :no-index:
   :members:
   :undoc-members:
   :show-inheritance:

.. autoclass:: pythonmusic.play.SynthesizerPlayer
   :no-index:
   :members:
   :undoc-members:
   :show-inheritance:
