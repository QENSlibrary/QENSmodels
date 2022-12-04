
.. image:: https://readthedocs.org/projects/qensmodels/badge/?version=latest
   :target: https://qensmodels.readthedocs.io/?badge=latest
   :alt: Documentation Status

.. image:: https://img.shields.io/badge/License-BSD_3--Clause-blue.svg
   :target: https://opensource.org/licenses/BSD-3-Clause
   :alt: License

.. image:: https://github.com/QENSlibrary/QENSmodels/actions/workflows/qens_ci.yml/badge.svg
   :target: https://github.com/QENSlibrary/QENSmodels/actions/workflows/qens_ci.yml
   :alt: CI Status


Introduction
============


*QENSmodels* is a repository containing `Python <https://www.python.org/>`_ models
( *i.e.*, mathematical functions) that can be used to fit Quasi Elastic Neutron
Scattering (QENS) data `S(Q, omega)`.


This project has received funding from the European Union’s
Horizon 2020 research and innovation programme under grant agreement No 654000.


Getting started
===============


To get a glimpse of what can be done with the library, click on `launch binder` below.
Please note that the notebooks can be slow to load.


.. image:: https://mybinder.org/badge_logo.svg
 :target: https://mybinder.org/v2/gh/QENSlibrary/QENSmodels/main?labpath=.%2Fdocs%2Fexamples


restructured text icon Copy rst link to clipboard

Install the QENS models
-----------------------

Currently the QENS models library has not been released on pypi. Please use the alternative
method described below to install it.

- If not already installed on your computer, download and install Python (version>=3.8),
  for example, from https://www.python.org/downloads/.
  In the following instructions, replace `python` by the path to the version of python
  you want to use.

- Create and go to, e.g., QENSmodels directory (optional)

  .. code-block:: console

      mkdir QENSmodels && cd QENSmodels


- Create a virtual environment and activate it (optional)

  - on Unix or MacOS 

    .. code-block:: console

        python -m venv .venv
        source .venv/bin/activate
  
  - on Windows
  
    .. code-block:: console
    
        python -m venv .venv
        .\.venv\Scripts\activate

  Note that the prompt of the terminal will change and contain ``(.venv)``.
  You can choose the folder name that contains your virtual environment when you create it by
  passing a name other than `.venv`. Once done working with this virtual environment, you can
  deactivate it by typing ``deactivate`` in the terminal. The prompt should go back to its initial
  version.


- Upgrade pip (optional)

  .. code-block:: console

     python -m pip install --upgrade pip

- Install the library

   - *method 1*: if you want to modify the models at a later stage

      - download or clone the repository at https://github.com/QENSlibrary/QENSmodels

      - In a terminal run

        .. code-block:: console

           python -m pip install -e full_path_to_QENSmodels_folder


   - *method 2*: if you only want to use the version of the models available in the repository

     .. code-block:: console

        python -m pip install git+https://github.com/QENSlibrary/QENSmodels.git@master


    See `the documentation on pip install <https://pip.pypa.io/en/stable/cli/pip_install/>`_
    for additional information. Run ``pip show QENSmodels`` to display details about the installed package.



To **test the installation**, type the following command in a terminal

.. code-block:: console

   python -c "import QENSmodels"




To **uninstall** the library, type

.. code-block:: console

   python -m pip uninstall QENSmodels



Documentation
-------------

The documentation is available at https://qensmodels.readthedocs.io .

Note that the Jupyter notebooks are available in the repository in the `docs/examples` folder.
But they require the installation of additional libraries. Please refer to the README file in
the same folder for instructions.


Quick example to use the models
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

   import QENSmodels
   value = QENSmodels.lorentzian(1, 1, 1, 1)



Physical units
~~~~~~~~~~~~~~
For information about unit conversion, please refer to the jupyter notebook called
`Convert_units.ipynb` in the `tools` folder.



Needing help / Reporting a bug
------------------------------

Bugs and feature requests are collected at https://github.com/QENSlibrary/QENSmodels/issues.

If you are reporting a bug, please include:


* Your operating system name and version.
* Any details about your local setup that might be helpful in troubleshooting.
* Detailed steps to reproduce the bug.



Contributing
------------

If you are interested in contributing to this project, please refer to the
`CONTRIBUTING document <https://github.com/QENSlibrary/QENSmodels/blob/master/CONTRIBUTING.rst>`_




Referring to the library
------------------------

If you found this package useful, please don't forget to acknowledge its use in your publications
as suggested below and reference this website: https://github.com/QENSlibrary/QENSmodels.

Please also consider letting us know by sending us the reference to your work.
This will help us to ensure the long term support and development of the software.


   This work benefited from the use of the QENSmodels library, which contains code developed with
   funding from the European Union's Horizon 2020 research and innovation programme under grant
   agreement No 654000.



License
-------

Redistribution of the software is permitted under the terms of the
`BSD 3-Clause license <https://opensource.org/licenses/BSD-3-Clause>`_.
