
.. image:: https://readthedocs.org/projects/qensmodels/badge/?version=latest
   :target: https://qensmodels.readthedocs.io/?badge=latest
   :alt: Documentation Status
   
.. image:: https://github.com/QENSlibrary/QENSmodels/actions/workflows/qens_ci.yml/badge.svg
   :target: https://github.com/QENSlibrary/QENSmodels/actions/workflows/qens_ci.yml
   :alt: CI Status

Introduction
============


*QENSmodels* is a repository containing models (mathematical functions) written in
`Python <https://www.python.org/>`_. These models can be used to fit Quasi Elastic Neutron
Scattering (QENS) data `S(Q, omega)`. This project has received funding from the European Union’s
Horizon 2020 research and innovation programme under grant agreement No 654000.

Installation
============

Requirements
------------

*Python modules to use the models:*


* `numpy <http://www.numpy.org/>`_
* `scipy <https://www.scipy.org/>`_

The installation of these modules will be checked when installing the QENSmodels library and will
be performed if they are missing.

*Python modules to test the models (for contributors):*


* `flake8 <http://flake8.pycqa.org/en/latest/>`_ 
* `unittest <https://docs.python.org/3/library/unittest.html>`_
* `doctest <https://docs.python.org/3.7/library/doctest.html>`_

`flake8` can be installed using

.. code-block:: console

     python -m pip install flake8


Additional modules are required to run the examples. These examples show you how to run a fit with
different minimizers using some of the QENS models. Details can be found in the
`README file <https://github.com/QENSlibrary/QENSmodels/blob/master/docs/examples/README.rst>`_
of the *examples* folder or in the online documentation. How to use Mantid to fit is described in
this `document <https://github.com/QENSlibrary/QENSmodels/blob/master/docs/examples/using_mantid/README.rst>`_ .

How to install?
---------------

.. NOTE:: If you want to use a virtual environment, please go to
   `this link <https://docs.conda.io/projects/conda/en/latest/user-guide/getting-started.html>`_
    for instructions.

The steps to follow are:  


* Download or clone the repository which can be found at the following
  `link <https://github.com/QENSlibrary/QENSmodels>`_

* To **install the package**, type the following command in a terminal

  .. code-block:: console

     python -m pip install full_path_to_QENSmodels_folder


See `the documentation on pip install <https://pip.pypa.io/en/stable/reference/pip_install/#editable-installs>`_
for additional information. Run ``pip show QENSmodels`` to display details about the installed
package.

To **test the installation**\ , type the following command in a terminal

.. code-block:: console

   python -c "import QENSmodels"

To **uninstall** the library, type

.. code-block:: console

   python -m pip uninstall QENSmodels


Tests
-----

The script to run the tests is located in the ``tools`` folder.
These tests require the installation of ``doctest`` and ``unittest``.

In a terminal, move to the ``tools`` directory and run

.. code-block:: console

   ./run_tests.sh

Documentation
=============

The documentation is available at https://qensmodels.readthedocs.io .


License
-------

Redistribution of the software is permitted under the terms of the 3-Clause BSD license.


How to use the library?
-----------------------

.. code-block:: python

   import QENSmodels
   value = QENSmodels.lorentzian(1, 1, 1, 1)

or copy and paste the script related to the Lorentzian function.

The scripts of the models can be found in the
`git repository <https://github.com/QENSlibrary/QENSmodels>`_.

Jupyter notebooks showing how to use some of the QENS models are located in the *docs/examples*
folder. The name of the notebook indicates which fitting engine and QENS model 
are used. Additional tools might have to be installed in order to use a 
particular notebook. Please refer to the Please refer to the
`README file <https://github.com/QENSlibrary/QENSmodels/blob/master/docs/examples/README.rst>`_ in
the `examples` folder or to the `examples` section of the online documentation for details.

If you do not want to download neither install any component, one example can be interactively
tested online. To open it, click on `launch binder` below. Please note that the notebook can be
slow to load.

.. image:: https://mybinder.org/badge_logo.svg
   :target: https://mybinder.org/v2/gh/QENSlibrary/QENSmodels/master?filepath=examples-binder%2Fscipy_lorentzian_fit_binder_ipywidgets.ipynb

Physical units
^^^^^^^^^^^^^^
For information about unit conversion, please refer to the jupyter notebook called
`Convert_units.ipynb` in the `tools` folder.



How to cite?
------------

If you found this package useful, please don't forget to acknowledge its use in your publications 
as suggested below and reference this website: https://github.com/QENSlibrary/QENSmodels. 

Please also consider letting us know by sending us the reference to your work. 
This will help us to ensure the long term support and development of the software.


   This work benefited from the use of the QENSmodels library, which contains code developed with
   funding from the European Union’s Horizon 2020 research and innovation programme under grant
   agreement No 654000.



How to contribute?
------------------

If you are interested in contributing to this project, please refer to the
`CONTRIBUTING document <https://github.com/QENSlibrary/QENSmodels/blob/master/CONTRIBUTING.rst>`_

Need help / found a bug
-----------------------

Bugs and feature requests are collected at https://github.com/QENSlibrary/QENSmodels/issues.

If you are reporting a bug, please include:


* Your operating system name and version.
* Any details about your local setup that might be helpful in troubleshooting.
* Detailed steps to reproduce the bug.
