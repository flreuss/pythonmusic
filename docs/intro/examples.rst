Examples
========

A collection of code snippets for PythonMusic.


Input / Output
--------------

Receive messages from a midi sender, and print them into the terminal.

.. code-block:: python

    from pythonmusic import *
    from time import sleep

    RECEIVER_NAME = "MyKeyboard"  # change name

    receiver = find_midi_receiver(RECEIVER_NAME)
    if receiver is None:
        raise IOError(f'No open midi port found for "{SENDER_NAME}"')

    receiver = MidiReceiver.attach(sender, True)

    while True:
        # keep thread busy
        sleep(1)

Send messages to a midi receiver.

.. code-block:: python

    from pythonmusic import *
    from time import sleep

    RECEIVER_NAME = "MyKeyboard"  # change name

    receiver = find_midi_receiver(RECEIVER_NAME)
    if receiver is None:
        raise IOError(f'No open midi port found for "{RECEIVER_NAME}"')

    sender = MidiSender.attach(receiver)

    duration = QN * 0.9
    notes = [C4, EF4, G4, C5]
    try:
        while True:
            for i in range(len(notes)):
                pitch = notes[i]
                on = MidiMessage(NOTE_ON, note=pitch, velocity=MF)
                off = MidiMessage(NOTE_OFF, note=pitch, velocity=MF)

                sender.send_message(on)
                sleep(duration)
                sender.send_message(off)
                sleep(QN - duration)

    except KeyboardInterrupt:
        # stopps playing notes
        sender.force_notes_off()


Players
-------

Implement a custom player that can playback scores and other musical objects.

.. code-block:: python

    from typing import override
    from pythonmusic import *


    class MyPlayer(Player):
        @override
        def play_message(self, message: MidiMessage):
            print(f"Received MIDI Message: {message}")


    player = MyPlayer()
    player.play_phrase(Phrase([Note(C4, EN), Note(E4, QN)]), ADAGIO)
