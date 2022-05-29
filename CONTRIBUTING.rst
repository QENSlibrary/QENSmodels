.. role:: raw-html-m2r(raw)
   :format: html


Contributing
============

Introduction
------------

First of all, thank you for considering contributing to the QENS models' 
library. Contributions are welcome from the community.

This document describes some guidelines that are intended to help to communicate 
with the developers' team, so that it can address your issue, assess your 
changes and help you finalize your pull requests.

Installation
------------


In order to contribute to the development of the library, in a terminal

- activate your virtual environment (see the `installation <https://github.com/QENSlibrary/QENSmodels/blob/master/README.rst>`_ )

- run:

.. code-block:: console

   python -m pip install -r requirements-dev.txt

This will install what is needed to

- build the documentation
- run the unit tests and doc tests and analyse the code
- run the examples (Jupyter notebooks)


Ground rules
------------

If you have direct contributions you would like to be considered for 
incorporation into the project you can fork this repository and submit a pull 
request for review.

Contributors feeling unsure or inexperienced about contributing to an open-source 
repository are referred to `this tutorial <https://github.com/firstcontributions/first-contributions>`_.

**Working on your first Pull Request?** You can learn how from this *free* 
series 
`How to Contribute to an Open Source Project on GitHub <https://egghead.io/courses/how-to-contribute-to-an-open-source-project-on-github>`_

People interested can contribute to the project in different ways:


#. adding QENS models
#. adding new examples of fitting using some of the QENS models and the 
   fitting engine of their choice 

New QENS models
^^^^^^^^^^^^^^^


* Contributed models should be written in ``Python 3.x``.
* For each new model, a Python script should be provided alongside some 
  documentation and tests.
* Once ready, you need to upload the ``Python`` source code files to the 
  `git repository <https://github.com/QENSlibrary/QENSmodels>`_ by submitting a 
  pull request.

Physical units
~~~~~~~~~~~~~~

For information about unit conversion, please refer to the jupyter notebook called
`Convert_units.ipynb` in the `tools` folder.

Python script
~~~~~~~~~~~~~


* It should be placed in the ``QENS models`` folder. The associated ``Python`` 
  script for the tests should be placed in the ``tests`` folder and added to
  the list in ``run_tests.sh``.
* The `doctest <https://docs.python.org/3/library/doctest.html>_` module has
  to be imported (\ *i.e.* paste ``import doctest`` in your 
  ``Python`` script. Please refer to the existing models 
  for help).
* Each function should have a docstring specifying its name, parameters, a 
  short description and some examples. These examples will be used when 
  running ``doctest``. Please refer to the existing models 
  for help. A more general template for docstring can be found 
  `here <https://sphinxcontrib-napoleon.readthedocs.io/en/latest/example_numpy.html>`_. 
* And before submitting your pull request, check that your script, tests and 
  built of the documentation run on your machine. Please also run ``flake8`` 
  to check your code matches the project style (by running, for example, 
  ``python -m flake8 new_python_script.py``\ ).


Documentation
~~~~~~~~~~~~~

* For the QENS models' library, the documentation is built using 
  `Sphinx <http://www.sphinx-doc.org/en/master/>`_.
* The related files are located in the ``docs`` folder.
* In addition, as mentioned in the previous section, each model should contain 
  a self-contained description.


**Building the documentation locally**

In a terminal, run

.. code-block:: console

  python -m sphinx path_to_docs_folder build_folder


where `build_folder` is where you want to build the documentation of the library.


Tests
~~~~~

The script to run the tests is located in the ``tools`` folder.
These tests require the installation of ``doctest`` and ``unittest``.

In a terminal, move to the ``tools`` directory and run

.. code-block:: console

   ./run_tests.sh


New examples
^^^^^^^^^^^^


* Contributed examples should use |JupyterTag| notebooks (preferred) or ``Python``
  scripts.

.. |JupyterTag| image:: https://img.shields.io/badge/-jupyter-%236091f2.svg
   :target: https://img.shields.io/badge/-jupyter-%236091f2.svg
   :alt: jupyter <https://github.com/QENSlibrary/QENSmodels/labels/jupyter>`_ 


* Please add a maximum of information about the case being described: 

  * physical model
  * reference to publication (if any)
  * steps leading to the final results 
    (reduction, convolution of different models, normalization...)
  * choice of minimizer and link to its documentation

* If additional reference datasets are required, they can be stored in 
  the ``/examples/data`` folder. But the preferred option is to generate these 
  reference data on the fly in the notebook or script without creating any 
  permanent external file.
* If additional ``Python`` modules are used in the new notebook or script, 
  please add them to the list of requirements in `requirements` files and `setup.py`.

Other issues
------------

* |QuestionTag| and |EnhancementTag| related to the library can be asked on the issues page. 

.. |QuestionTag| image:: https://img.shields.io/badge/-question-%23d876e3.svg
   :target: https://img.shields.io/badge/-question-%23d876e3.svg 
   :alt: `question <https://github.com/QENSlibrary/QENSmodels/labels/question>`_ 

.. |EnhancementTag| image:: https://img.shields.io/badge/-enhancement-%23a2eeef.svg
   :target: https://img.shields.io/badge/-enhancement-%23a2eeef.svg
   :alt: `Enhancement <https://github.com/QENSlibrary/QENSmodels/labels/enhancement>`_

* Before creating a new issue, please take a moment to search and make sure a 
  similar issue does not already exist. If one does exist, you add a comment to 
  it; most simply even with just a :+1: to show your support for that issue.
* If you find any bugs, please report them by submitted a new issue labelled 
  as |BugTag|. The more details you can provide the better. If you know how to 
  fix the bug, please open an issue first and then submit a pull request.

.. |BugTag| image:: https://img.shields.io/badge/-bug-%23d73a4a.svg
   :target: https://img.shields.io/badge/-bug-%23d73a4a.svg
   :alt: `bug <https://github.com/QENSlibrary/QENSmodels/labels/bug>`_

* |GoodFirstIssueTag| *issues are particularly appropriate if it is your first 
  contribution.*
  If you're not sure about how to go about contributing, these are good 
  places to start. You'll be mentored through the process by the maintainers 
  team. If you're a seasoned contributor, please select a different issue to 
  work from and keep these available for the newer and potentially more 
  anxious team members.
  
.. |GoodFirstIssueTag| image:: https://img.shields.io/badge/-good%20first%20issue-%237057ff.svg
   :target: https://img.shields.io/badge/-good%20first%20issue-%237057ff.svg
   :alt: `good-first-issue <https://github.com/QENSlibrary/QENSmodels/labels/good%20first%20issue>`_ 

*  |HelpTag| contains a task that you can contribute to. We especially encourage you to do so 
   if you feel you can help.

.. |HelpTag| image:: https://img.shields.io/badge/-help%20wanted-%23008672.svg
   :target: https://img.shields.io/badge/-help%20wanted-%23008672.svg
   :alt: `help-wanted <https://github.com/QENSlibrary/QENSmodels/labels/help%20wanted>`_
