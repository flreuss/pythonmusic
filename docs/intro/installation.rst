Installation
============

Requirements
------------

This library requires a Python version ``>=3.11``. If Python is not present on the system, refer to the official `Python download page <https://www.python.org/downloads/>`_, or install Python with your operating system's package manager.

.. note:: If you are using an IDE with PythonMusic, such as `PyCharm <https://www.jetbrains.com/pycharm/>`_, the steps for checking the
   Python version may not apply to you. Refer to your IDE's documentation on how to install Python. 

To check the installed Python version on your system, open a terminal or command prompt and use the command below:

.. code-block:: bash

   $ python3 --version

Your Python installation should have also installed the Pip package manager which is required for some dependencies. If Pip is present, 
the command below should print the installed version:

.. code-block:: bash

   $ pip3 --version


Additional Windows Dependencies
...............................

Some required dependencies may be missing from your Windows installation. Before installing PythonMusic, download the 
`Visual C++ Redistributable for Visual Studio 2015 <https://www.microsoft.com/en-us/download/details.aspx?id=48145>`_ from the official
websites. Install the 32-bit version and restart your PC.

.. note::
   This aims to prevent a "DLL not found error" when importing RtMidi, a dependency for Pythonmusic. If you still encounter this issue
   after installing the Visual C++ Redistributable, try installing the 64-bit version as well. It is important to install this *before*
   installing PythonMusic, as the installation may break without the Redistributable. In that case, you may need to remove PythonMusic
   from your virtual environment or system and, reinstall.


Creating a Project
------------------

.. warning::
   Because this repository is not public, installing via pip as described below may not work. See the REAMDE 



Terminal
........

Create a new directory and initialise a virtual environment inside. Activate the environment and install the PythonMusic module.

.. code-block:: bash

   $ mkdir my_project
   $ cd my_project
   $ python3 -m venv venv
   $ source venv/bin/activate
   $ pip install git+https://gitup.uni-potsdam.de/music-with-pc/pythonmusic

See :doc:`Getting Started <./getting_started>` to start making music.

IDE
...

If you are using an IDE, such as `PyCharm <https://www.jetbrains.com/pycharm/>`_, consult its documentation on how to create a new project.
Make sure to use a Python version ``>=3.11``. This may not be the option selected by default.

To add PythonMusic to your project, find the built-in package manager of your IDE. You want to supply a URL to the module, as PythonMusic 
is not available on `PyPi <https://pypi.org/>`_.

.. hint:: In PyCharm, head to the "Python Packages" in lower left corner, click "Add Packages" and then "From Version Control".
   Insert "https://gitup.uni-potsdam.de/music-with-pc/pythonmusic.git" into the text field and click on "OK".

See :doc:`Getting Started <./getting_started>` to start making music.


Synth
-----

Optionally, this library supports on-device playback through `FluidSynth <https://www.fluidsynth.org/>`_ and a compatible SoundFont2
library. These can be easily found online. For a good starting point, have a look at a 
`Default Windows MIDI Soundfont <https://musical-artifacts.com/artifacts/713>`_.

.. note::
  When searching online, make sure that the sound font is General Midi (GM) compatible. Otherwise, some instruments may not function
  properly.


Installing FluidSynth differs depending on you operating system. 

Linux / macOS
.............

Use your favourite package manager to install FluidSynth. macOS doesn't ship with a built-in package manager, so you may want to install
`Homebrew <https://brew.sh/>`_.

.. code-block:: bash

   # Debian-based / Ubuntu
   sudo apt install fluidsynth

   # Arch-based
   sudo pacman -S fluidsynth

   # macOS with Homebrew
   brew install fluidsynth

For more information, see FluidSynth's `download page <https://github.com/FluidSynth/fluidsynth/wiki/Download>`_.


Windows
.......

.. todo:: this is bad, find a better solution

Download the latest Windows (10) release of FluidSynth from the 
`official download page <https://github.com/FluidSynth/fluidsynth/releases>`_. Extract the files from the zip, and drag and drop the 
contents of the ``bin\`` folder to ``C:\Windows\System32``. This may require administrator privileges.

.. note:: Windows does not ship with a built-in package manager. Alternatives such as `Chocolatey <https://chocolatey.org/>`_ exist, but 
   installing FluidSynth this way did not work during testing.
