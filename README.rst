===========
Description
===========

.. image:: https://readthedocs.org/projects/qensmodels/badge/?version=latest
   :target: https://qensmodels.readthedocs.io/?badge=latest
   :alt: Documentation Status

Introduction
============


*QENSlibrary* is a repository containing models (mathematical functions) written in `Python <https://www.python.org/>`_.
These models can be used to fit Quasi Elastic Neutron Scattering (QENS) data.
This project has received funding from the European Union’s Horizon
2020 research and innovation programme under grant agreement No 654000.

Installation
============

Requirements
------------

Python modules to use the models:


* `numpy <http://www.numpy.org/>`_

Python modules to test the models (for contributors):


* `flake8 <http://flake8.pycqa.org/en/latest/>`_ 
* `unittest <https://docs.python.org/3/library/unittest.html>`_
* `doctest <https://docs.python.org/3.7/library/doctest.html>`_

Additional modules are required to run the examples. Details can be
found in the README file of the *examples* folder.

How to install?
---------------

Note:
^^^^^

If you want to use a virtual environment, please go to `this link <https://docs.conda.io/projects/conda/en/latest/user-guide/getting-started.html>`_
for instructions. 

The steps to follow are:  


* Download or clone the repository which can be found at the following `link <https://github.com/QENSlibrary/QENSmodels>`_

* To **install the package** to the Python user install directory for your platform, type the following
  command in a terminal  

  .. code-block:: console

     pip install --user full_path/to/QENSmodels_folder

See `the documentation on pip install <https://pip.pypa.io/en/stable/reference/pip_install/#editable-installs>`_ for 
additional information. Run ``pip show QENSmodels`` to display details about the installed package.

To **test the installation**\ , type the following command in a terminal

.. code-block:: console

   python -c "import QENSmodels"

To **uninstall** the library, type

.. code-block:: console

   pip uninstall QENSmodels

Documentation
=============

The documentation is available at https://qensmodels.readthedocs.io .

.. The documentation is built using ``Sphinx``. The required packages can be installed using the following commands:

.. .. code-block:: console

..    pip install sphinx
..    pip install sphinx-rtd-theme
..    pip install sphinxcontrib-napoleon

.. Other ways of installing ``Sphinx`` at be found at http://www.sphinx-doc.org/en/master/usage/installation.html

.. How to build documentation?
.. ---------------------------

.. In a terminal, move to the *docs* folder and type

.. .. code-block:: console

..    make html

.. This command will generate html files in the subfolder *_build/html*.

Tests
=====

The script to run the tests is located in the ``tools`` folder. 
These tests require the installation of ``doctest`` and ``unittest``.

In a terminal, move to the ``tools`` directory and run

.. code-block:: console

   ./run_tests.sh

License
-------

Redistribution of the software is permitted under the terms of the 
`General Public License version 3 or higher <https://www.gnu.org/licenses/gpl-3.0.en.html>`_.


How to use?
-----------

.. code-block:: python

   import QENSmodels
   value = QENSmodels.lorentzian(1, 1, 1, 1)

or copy and paste the script related to the Lorentzian function.

The scripts can be found in the 
`git repository <https://github.com/QENSlibrary/QENSmodels>`_

Jupyter notebooks using some of the QENS models are located in the *examples*
folder. The name of the notebook indicates which fitting engine and QENS model 
are used. Additional tools might have to be installed in order to use a 
particular notebook.

Physical units
^^^^^^^^^^^^^^

Please note that the following units are used for the QENS models

.. list-table::
   :header-rows: 1

   * - Type of parameter
     - Unit
   * - Time
     - picosecond
   * - Length
     - Angstrom
   * - Momentum transfer
     - 1/Angstrom


How to cite?
------------

If you found this package useful, please don't forget to acknowledge its use in your publications 
as suggested below and reference this website: https://github.com/QENSlibrary/QENSmodels. 

Please also consider letting us know by sending us the reference to your work. 
This will help us to ensure the long term support and development of the software.


   This work benefited from the use of the QENSmodels library, which contains code developed with funding from the 
   European Union’s Horizon 2020 research and innovation programme under grant agreement No 654000. 



How to contribute?
------------------

If you are interested in contributing to this project, please refer to the `CONTRIBUTING document <https://github.com/QENSlibrary/QENSmodels/blob/master/CONTRIBUTING.rst>`_

Need help / found a bug
-----------------------

Bugs and feature requests are collected at https://github.com/QENSlibrary/QENSmodels/issues.

If you are reporting a bug, please include:


* Your operating system name and version.
* Any details about your local setup that might be helpful in troubleshooting.
* Detailed steps to reproduce the bug.
