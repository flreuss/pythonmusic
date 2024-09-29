# PythonMusic
*make music with your computer*

PythonMusic is an open-source music library written in pure Python that enables you to write music on your computer. It is based on the [mido](https://github.com/mido/mido) library, which enables interaction with midi files.


## Installation
Before installing PythonMusic, make sure that a Python version `>=3.10` is installed on your machine. For this, open a terminal or command prompt (Windows) and type the command below.

```bash
python --version
```

If Python is not installed, download it on the [official download page](https://www.python.org/downloads/) or use your package manager to install.

Also, make sure that you have access to Python's pip package manager which is used to install most dependencies for PythonMusic.

```bash
pip --version
```


Next, it is recommended to use a virtual environment for you Python projects. If you are using an IDE, consult its documentation on how to setup an environment. In most cases this is done automatically.

In a terminal environment, use on of the may available options to setup a new virtual environment. For instance

```bash
python -m venv venv
```

With your environment created, activate it.

```bash
#!/bin/bash
source venv/bin/activate
```

Finally, install PythonMusic into your virtual environment. At the moment, the package is not available on [PyPi](https://pypi.org/), so you will need to source the package from its repository.

```bash
pip install git+https://gitup.uni-potsdam.de/music-with-pc/pythonmusic
```

> ## While in development,
> Installing this library may not work as described above because the repo is not public. Instead, you need to
> install the package from source.
>
> Either in the terminal:
> 1. clone this git repo somewhere outside your project
> 2. activate virtual environment of your project (not the PythonMusic repo)
> 3. install from source with `pip install [path to PythonMusic repo]`
>
> Or in PyCharm:
> 1. clone this git repo somewhere on your system
> 2. create a new project with venv in PyCharm ("Project venv")
>   - make sure that you create the project with a Python version `>=3.10.x`
>   - you may need to change the default selected "Python version"
> 3. then do either of the following:
>   - Option A
>     1. navigate to "Python Packages" in the side bar
>     2. click "Add Package" and then "From Disk"
>     3. select the path to the PythonMusic git repo (leave "Install as editable" unchecked)
>     4. click "OK"
>   - Option B
>     1. open a terminal inside PyCharm
>     2. make sure you are inside a venv 
>       - this is signalled by a (venv) before the prompt, or similar
>     3. install using `pip install [path to PythonMusic repo]`

This should automatically install all dependencies necessary for PythonMusic. See `pyproject.toml` for more information.


### Playback
Optionally, this package also allows you to playback your music through an integrated synthesiser. This requires manual installation of [FluidSynth](https://www.fluidsynth.org/) and a SoundFont2 compatible instrument library.

#### FluidSynth
To install FluidSynth on **Linux**, use your favourite package manager to install the `fluidsynth` package.

```bash
# Arch
pacman -S fluidsynth

# Debian / Ubuntu
apt install fluidsynth
```

On **macOS**, install a package manager such as [Homebrew](https://brew.sh/) and install `fluidsynth` via the terminal.

```bash
# macOS
brew install fluidsynth
```

No official **Windows** builds are available at the moment. If you want to use FluidSynth on Windows, you may need to [build Fluidsynth](https://github.com/FluidSynth/fluidsynth/wiki/BuildingWithCMake) from source.


#### SoundFont
Additionally, you will need to download a GM (General Midi) compatible SoundFont2 library to use FluidSynth. These  can be found readily online. Make sure to save the `*.sf2` file in a location that is accessible to your Python project.

To load a sound font, simply pass its path to a `Synth` or `SynthPlayer`.

```python
from pythonmusic import Synth, SynthPlayer

# sound font is located in myProject/resources/gm.sf2
PATH = "resources/gm.sf2"

synth = Synth(PATH)
synth_player = SynthPlayer(PATH)
```

## Getting started
TODO

## Classes
![Classes](docs/images/classes.png)


## Links
- [Source](https://gitup.uni-potsdam.de/music-with-pc/pythonmusic)
- [Documentation](https://gitup.uni-potsdam.de/music-with-pc/pythonmusic)
- [JythonMusic](https://jythonmusic.me)
