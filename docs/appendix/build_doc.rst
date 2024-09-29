Building the Documentation
==========================

This page contains instructions on how to build this documentation using `Sphinx <https://www.sphinx-doc.org/en/master/>`_. The instructions
below assume that you are on a Unix-like system with a Bash-compatible shell. You may need to alter commands for different shells and
operating systems.

Requirements
------------

Make sure that `git`, `make`, and `python3` are installed on your system. Then, clone the main repository,
navigate to the ``docs/`` directory, and install dependencies outlined in ``docs/requirements.txt`` into your virtual environment.

.. code-block:: bash

   $ cd docs/
   $ pip -r requirements.txt


Building
--------

To build the documentation run the command below inside the ``docs/`` directory.

.. code-block:: bash

   $ make html

The documentation is exported to ``docs/_build/html``.

To target other output formats, replace ``html`` with an option from Sphinx' 
`builders <https://www.sphinx-doc.org/en/master/usage/builders/index.html#builders>`_. These may have additional dependencies.
