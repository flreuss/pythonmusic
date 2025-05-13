Installation
============

Dependencies
------------

Python
.......

.. note:: 
   If you are using an IDE, the steps to install the correct Python version may vary. Consult your IDE's documentation on how to install Python.
   Make sure to select the correct Python version. An older version may be selected.


This library requires Python ``3.12`` or newer on your system. To install Python, refer to the official `Python download page <https://www.python.org/downloads/>`_, or install using your operating system's package manager.

You can check the installed version in the terminal with the following command:

.. code-block:: bash

   python3 --version


.. important::
   On Windows, ``python`` and ``python3`` sometimes refer to the Python app from the Microsoft Store. If you use the terminal
   and installed Python via the official installer, try using ``py`` instead of ``python3``:

   .. code-block:: powershell

      py --version

Installing this library and its dependencies also requires Python's Pip package installer. A normal Python installation should install 
this automatically.


Git
...

To clone PythonMusic and its dependencies, you need Git installed on your system. Refer to the official 
`Git download page <https://git-scm.com/downloads>`_ for installation instructions.

You can check the installed version in the terminal with the following command:

.. code-block:: bash

   git --version


Windows
.......

.. important:: The installation of PythonMusic relies on files that are installed below. If you accidentally skipped this step, you may
   need to uninstall PythonMusic and reinstall after completing the steps below.

PythonMusic on Windows requires 
`Microsoft Build Tools for Visual Studio 2022 <https://visualstudio.microsoft.com/downloads/?q=build+tools>`_.

After downloading and running the installer, select the *Desktop development with C++* package in the workloads section. To minimise the
disk space needed for installation, you can deselect all optional features in the right side bar, except the current 
version of the *MSVC build tools* and *Windows SDK*. Click on install.

.. note::
   Windows ARM is not tested and may require additional installation steps.


macOS
.....

On macOS, you need to install `PortAudio <https://www.portaudio.com/>`_ manually. For this, install the
`Homebrew <https://brew.sh/>`_ package manager. In a terminal, install the ``portaudio`` formula using:

.. code-block:: bash

   brew install portaudio


Creating a Project
------------------

PythonMusic is a normal Python library and can be installed as such.

PyCharm
.......

.. note:: If you are adding PythonMusic to an existing project, you can skip the first step. Make sure that your Python version is supported.

Create a new project make sure that a Python version ``>=3.12`` is selected. This is the minimum supported version by this library and may not be selected by default.

.. image:: ../images/pycharm_new_project.png

Once the new project has loaded, open the "Python Packages" toolbar by click on the corresponding button in the sidebar. Next, select
"Add Package" and then "From Version Control.

.. image:: ../images/pycharm_add_pm.png

In the "Install Package" dialogue, enter the PythonMusic repository URL (``https://gitup.uni-potsdam.de/music-with-pc/pythonmusic.git``).
Do not select "Install as editable (-e)". Click on "OK".

.. image:: ../images/pycharm_install_package.png

Once the process is complete, PythonMusic is installed into your 
environment and available to your project.

.. note:: If the installation fails, try cloning via SSH. For this, use ``git@gitup.uni-potsdam.de:music-with-pc/pythonmusic.git``
   instead.


VS Code
.......

Install the Python extension for VS Code from the Extension Marketplace.

.. image:: ../images/vscode_install_python.png

Open VS Code inside a new folder, or if already present, your existing project.

As a code editor, VS Code does not create a Python environment automatically. Instead, you create an environment manually by either
using the installed Python plug-in or the terminal.

The Python plug-in for VS Code can create a virtual environment for you. For this, go to the "View" menu in the menu bar, and select
"Command Palette...". Search for "Python: Create Environment".

.. image:: ../images/vscode_create_venv.png

Afterwards, select "Venv" and a compatible Python version (``>=3.11``).

Open a terminal by selecting the "New Terminal" option from the "Terminal" menu item. Continue with the instructions for a terminal
setup below. Skip creating the environment, if you have done so above.


Terminal
........

In a terminal, create a new Python virtual environment.

.. code-block:: bash

   python -m venv venv


On Linux and macOS, use the ``source`` command to load the activation script.

.. code-block:: bash

   source venv/bin/activate

On Windows, run the script for your respective prompt.

.. code-block:: powershell

   # in powershell
   venv\Scripts\Activate.ps1

   # in command prompt (cmd.exe)
   venv\Scripts\activate.bat


.. note::
   You may get an error like this:

        venv\Scripts\Activate.ps1 : File {path} cannot be loaded because running scripts is disabled on this system. For more information, see about_Execution_Policies at https:/go.microsoft.com/fwlink/?LinkID=135170.

   Sometimes, Windows Powershell blocks execution of scripts on your system. You can disable this by opening a new terminal
   with administrator access and setting the respective execution policy.

   To open a terminal with elevated privileges, open the start menu, search for "Terminal", right-click, and select
   "Run as administrator". Inside the terminal run the following command:

   .. code-block:: poweroff

      Set-ExecutionPolicy remoteSigned


   This will allow powershell to execute Python's venv activation script.

In your activated environment, install PythonMusic with pip.

.. code-block:: bash

   pip install git+https://gitup.uni-potsdam.de/music-with-pc/pythonmusic
   # or
   pip install https://gitup.uni-potsdam.de/music-with-pc/pythonmusic.git

See :doc:`Getting Started <./getting_started>` to start making music.
