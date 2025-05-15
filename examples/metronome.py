from pythonmusic import *

global counter
counter = 0
MAX = 16


def check_counter() -> bool:
    global counter

    counter += 1

    print(f"This is beat {counter}")
    return counter < MAX


metronome = Metronome(120.0, 3, callback=check_counter)
metronome.set_velocity(MP)

metronome.start()
print("started metronome")

# metronome.start() runs the metronome's loop in a separate thread. This mean
# that Python will not exit until your callback returns false. Alternatively,
# you can use metronome.block() to block your script until the metronome
# finishes.
