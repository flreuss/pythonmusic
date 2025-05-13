# PythonMusic
*make music with your computer*

PythonMusic is an open-source music library written in Python that enables you to write music on your computer.

```python
from pythonmusic import *

# create a phrase from a list of notes
phrase = Phrase(
    [
        Note(C4, EN),
        Note(D4, EN),
        Note(EF4, EN),
        Note(G4, QN + EN),
        Note(F4, QN),
    ]
)

# add phrases to parts
part = Part("Flute", FLUTE, [phrase])

# assemble parts into a score
score = Score("MyScore", [part], ADAGIO)

# playback your score
SOUND_FONT2 = "./soundfont.sf2"
player = SynthPlayer(SOUND_FONT2)
player.play_score(score)

# export your score to file
export_score(score, "./output.mid")
```


## Installation
This package requires a Python version of `>=3.11`. You can check you installed Python version in the terminal.

```bash
python --version
```

Installing PythonMusic on a Unix-like system such as macOS and Linux should be as simple as installing the 
repository via pip. 

```bash
pip install git+https://gitup.uni-potsdam.de/music-with-pc/pythonmusic
```

For the full instructions and Windows dependencies, see the installation section in the documentation.


## Documentation
The documentation is available for download [here](https://www.youtube.com/watch?v=XfELJU1mRMg). To be updated.


## Dependencies and Requiremenets
PythonMusic depends on [NumPy](https://numpy.org/), [PortAudio](https://www.portaudio.com/),
and [RtMidi](https://github.com/thestk/rtmidi). Wheels may not be available for your platform or architecture. 
Optionally, [FluidSynth](https://www.fluidsynth.org/) can be installed to enable on-device playback.

See the documentation for more information and installation instructions.


## Classes
this should be internal

![Classes](docs/images/classes.png)


## Links
- [Source](https://gitup.uni-potsdam.de/music-with-pc/pythonmusic)
- [Documentation](https://gitup.uni-potsdam.de/music-with-pc/pythonmusic)
- [JythonMusic](https://jythonmusic.me)
