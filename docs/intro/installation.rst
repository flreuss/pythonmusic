Installation
============

Requirements
------------

This library requires a Python version ``>=3.11`` to be installed on your system. To install Python, refer to the official `Python download page <https://www.python.org/downloads/>`_, or install using your operating system's package manager.

To check the installed Python version on your system, open a terminal or command prompt and use the command below:

.. code-block:: bash

   $ python3 --version

Installing this library and its dependencies also requires Python's Pip package installer. A normal Python installation should install 
this automatically.

.. note:: If you are using an IDE, the steps to install the correct Python version may vary. Consult your IDE's documentation on how to install Python.


Additional Windows Dependencies
...............................

.. important:: This step must be completed **before** installing PythonMusic. Your installation may break without the listed 
    dependency. If you have installed ``python-rtmidi`` first, you may need to remove and reinstall it before continuing.

PythonMusic on Windows requires 
`Microsoft Build Tools for Visual Studio 2022 <https://visualstudio.microsoft.com/downloads/?q=build+tools>`_.
After downloading and running the installer, select the *Desktop development with C++* package in the workloads section (selected by
default), and click install.

.. note::
  If you have previously installed Visual Studio or the build tools itself, make sure that the *Desktop development with C++* workload is
  installed. Visual Studio can be installed instead of the build tools, which only provide VS' functionalities without the full 
  application suite.


Synth
-----

Optionally, this library supports on-device playback through `FluidSynth <https://www.fluidsynth.org/>`_ and a GM (General MIDI)
compatible SoundFont2 library.

SF2 libraries can be found online. For a good starting point, have a look at a  `Default Windows MIDI Soundfont <https://musical-artifacts.com/artifacts/713>`_.


Linux / macOS
.............

Use your favourite package manager to install FluidSynth. macOS doesn't ship with a built-in package manager, so you may want to install
`Homebrew <https://brew.sh/>`_.

.. code-block:: bash

   # Arch-based
   sudo pacman -S fluidsynth

   # Debian-based / Ubuntu
   sudo apt install fluidsynth

   # macOS with Homebrew
   brew install fluidsynth

For more information, see FluidSynth's `download page <https://github.com/FluidSynth/fluidsynth/wiki/Download>`_.


Windows
.......

.. todo:: This is bad, clunky, and dangerous. Find a better solution. Python (RtMidi, really) doesn't see FS installed via Chocolatey,
    even though it should. Passing the path to FS (Chocolatey) manyally to the C library loader, actually works. To fix this, however
    we would need to fork RtMidi or the python C loader. Not going to do that.

Download the latest Windows 10 release of FluidSynth from the  `official download page <https://github.com/FluidSynth/fluidsynth/releases>`_.
Extract the files from the zip, you will only need the contents of the ``bin\`` directory.
Drag and drop all files from the ``bin\`` directory to ``C:\Windows\System32``. This may require admin privileges.

.. note:: Windows does not ship with a built-in package manager. Alternatives such as `Chocolatey <https://chocolatey.org/>`_ exist, but 
   installing FluidSynth this way did not work during testing.

To uninstall FluidSynth, remove the DLLs you moved to ``System32``. Be careful not to remove other DLLs. This may break your system.


Creating a Project
------------------

.. warning::
   TODO: remove.
   Because this repository is not public, installing via pip as described below may not work. See the REAMDE on `gitup <https://gitup.uni-potsdam.de/music-with-pc/pythonmusic>`_.


Terminal
........

Create a new directory and initialise a virtual environment inside. Activate the environment and install the PythonMusic package.

.. code-block:: bash

   $ mkdir my_project
   $ cd my_project
   $ python3 -m venv venv
   $ source venv/bin/activate
   $ pip install git+https://gitup.uni-potsdam.de/music-with-pc/pythonmusic

IDE
...

When creating a new project, make sure to select a Python version ``>=3.11``. This may not be the default option.

Consult your IDE's documentation on how to install python packages. The repository can be found at ``git+https://gitup.uni-potsdam.de/music-with-pc/pythonmusic``.


See :doc:`Getting Started <./getting_started>` to start making music.

