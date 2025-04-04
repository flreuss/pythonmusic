from time import sleep

from pythonmusic import *

# Defines the path to a SoundFont2 file. Change as needed.
SF2_PATH = "./resources/gm.sf2"

# A list of notes that represent the melody.
notes = [
    Note(A4, QN),
    Note(CS5, DHN),
    Note(D5, QN),
    Note(E5, WN + QN),
    Note(E5, QN),
    Note(CS5, QN),
    Note(E5, QN),
    Note(A5, DHN),
    Note(E5, QN),
    Note(CS5, QN),
    Note(D5, QN),
    Note(FS5, DQN),
    Note(E5, EN),
    Note(E5, HN),
    Note(CS5, HN),
]

# A phrase that contains the notes.
phrase = Phrase(notes)

# A part represents an instrument in a score.
part = Part("A Druid", FLUTE)
part.add_phrase(phrase)

# A score represents a piece of music.
score = Score("Op. 60 No. 1")
score.tempo = 96  # in bpm where a beat is a quarter
score.add_part(part)


# === Using the SfPlayer ===
# player = SfPlayer(SF2_PATH)
# player.play_score(score)

# exit(0)

# === Using a MIDI Keyboard ===
# Find midi devices connected to your system
receivers = midi_inputs()
if len(receivers) > 0:
    # get the first receiver
    receiver = receivers[0]

    player = MidiOutPlayer(receiver, False)
    # wrapping in try/except to prevent error stack on KeyboardInterrupt
    try:
        player.play_score(score)
    except KeyboardInterrupt:
        pass
else:
    print("No midi devices found")
