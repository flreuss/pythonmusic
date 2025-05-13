Building the Documentation
==========================

This page contains instructions on how to build this documentation using `Sphinx <https://www.sphinx-doc.org/en/master/>`_. The instructions
below assume that you are on a Unix-like system with a Bash-compatible shell. You may need to alter commands for different shells and
operating systems.


Requirements
------------

Make sure that `git`, `make` and `python >= 3.12` are installed on your system. Clone the
repository and install inside a virtual environment.

.. code-block:: bash

   # create environment
   python3 -m venv venv
   source venv/bin/activate

   # install library with docs dependencies
   pip install '.[docs]'

Navigate to the ``docs/`` directory in the main repository and build docs with ``make html``.

.. note:: Sphinx support building for several targets, such as tex and pdf.
