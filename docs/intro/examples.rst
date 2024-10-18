Examples
========

A collection of code snippets for PythonMusic.

Project Template
----------------

A simple template to get you started.

.. code-block:: python

    from pythonmusic import *

    SF2_PATH = "./resources/gm.sf2"

    TITLE = "MyScore"
    TEMPO = ADAGIO


    def make_piano_part() -> Part:
        part = Part("Piano", ACOUSTIC_GRAND_PIANO, [], 0, PAN_CENTER)

        opening_phrase = Phrase([Note(C4, QN), Chord.from_root(D4, MAJOR, QN)])
        part.add_phrase(opening_phrase)

        return part


    def make_score() -> Score:
        score = Score(TITLE, tempo=TEMPO)
        score.add_part(make_piano_part())

        return score


    if __name__ == "__main__":
        score = make_score()
        player = SynthPlayer(SF2_PATH)
        player.play_score(score)

Synth
-----

Use your computer as a synthesizer to playback input from a MIDI keyboard, or similar.

.. code-block:: python

    from pythonmusic import *
    from time import sleep

    SF2_PATH = "./resources/gm.sf2"
    SENDER = "Digital Piano"  # change name here, or ask for user input

    # init synth
    player = SynthPlayer(SF2_PATH)

    # select instrument for channel 0
    player.set_instrument(0, SQUARE_LEAD)

    # find system name of sender
    sender = find_midi_sender(SENDER)
    if sender is None:
        raise IOError(f"no device found for {SENDER}")

    # attach to sender
    receiver = MidiReceiver.attach(sender)

    # add callback
    receiver.add_callback("*", lambda message: player.play_message(message))

    # keep main thread busy
    print("Synth ready")
    while True:
        sleep(1)


Input / Output
--------------

Receive messages from a midi sender, and print them to the terminal.

.. code-block:: python

    from pythonmusic import *
    from time import sleep

    SENDER_NAME = "MyKeyboard"  # change name

    sender = find_midi_sender(SENDER_NAME)
    if receiver is None:
        raise IOError(f'No open midi port found for "{RECEIVER_NAME}"')

    receiver = MidiReceiver.attach(receiver, True)

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


Ask user to select a MIDI intput (sender).

.. code-block:: python

    from pythonmusic import *

    choice = user_sender_propt()
    print(f"Chosen MIDI sener: {choice}")


Players
-------

Implement a custom player that can playback scores and other musical objects.

.. code-block:: python

    from typing import override
    from pythonmusic import *


    class PrintPlayer(Player):
        @override
        def play_message(self, message: MidiMessage):
            print(f"Received MIDI Message: {message}")


    player = PrintPlayer()
    player.play_phrase(Phrase([Note(C4, EN), Note(E4, QN)]), ADAGIO)


Use a :obj:`CodePlayer <pythonmusic.play.CodePlayer>` to modify notes before
they are played.

.. code-block:: python

    from time import sleep
    from pythonmusic import *

    SOUNF_FONT_PATH = "../resources/gm.sf2"


    # define a callback for notes; the parameters must match as shows below
    def note_callback(
        proxy: ProxyPlayer,
        note: Note,
        channel: int,
        instrument: int,
        panning: int,
    ):
        proxy.play_note(note, channel, instrument, panning)


    # create any player or pass `None` instead
    synth = SynthPlayer(SOUNF_FONT_PATH)
    player = CodePlayer(synth, note_callback)

    # create score here
    score = Score("MyScore")
    player.play_score(score)

    # to prevent cutoff sounds on midi synthesizers, add a delay after playback
    # finishes
    sleep(1)
