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
SF_PATH = "./soundfont.sf2"
player = SfPlayer(SF_PATH)
player.play_score(score)

# export your score to file
export_score(score, "./output.mid")
```

## Installation

This package requires Python `>=3.12`. Check your Python version in the terminal.

``` bash
python --version
```

Install PythonMusic with pip.

``` bash
pip install git+https://gitup.uni-potsdam.de/music-with-pc/pythonmusic
```

For the full installation instructions and platform-dependencies, see the documentation.

## Links

- [Source](https://gitup.uni-potsdam.de/music-with-pc/pythonmusic)
- [Documentation](https://gitup.uni-potsdam.de/music-with-pc/pythonmusic)
- [JythonMusic](https://jythonmusic.me)
