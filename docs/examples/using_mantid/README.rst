QENS models and Mantid
######################

Introduction
============

The instructions below describe the procedure to use the QENS models in Mantid Workbench.
They were tested with Mantid Workbench version 6.3.0.

Installation
============

The first step in all cases is to install Mantid Workbench following the instructions on the
`official page <https://download.mantidproject.org/>`__.


Then you can run the following lines in the scripting window of Mantid workbench

.. code-block:: python

    import subprocess
    path_to_QENS_lib = "path_to_QENSmodels"
    # install phase
    subprocess.Popen("python -m pip install -U --no-deps "+path_to_QENS_lib ,
                      shell=True,
                      stdout=subprocess.PIPE,
                      stderr=subprocess.PIPE,
                      stdin=subprocess.PIPE).communicate()

where "path_to_QENSmodels" is the path where the library is located on your computer.

If you want to use the version available in the git repository instead, please use

.. code-block:: python

    import subprocess
    subprocess.Popen("python -m pip install -U --no-deps git+https://github.com/QENSlibrary/QENSmodels.git@main",
                      shell=True,
                      stdout=subprocess.PIPE,
                      stderr=subprocess.PIPE,
                      stdin=subprocess.PIPE).communicate()

After running one of these code snippets, you might have to close MantidWorkbench to be able to
import the library.

Test the installation
----------------------

After following one of the above methods, you should just be able to use import the QENSmodels
library within Mantid. For example, to test the installation, in the editor of MantidWorkbench
simply type

.. code-block:: python

    import QENSmodels


Example
=======

The Python script `mantid_BrownianDiff_fit.py` can be used as an example to be loaded in Mantid
Workbench for fitting data to functions from the QENSmodels library.

Uninstall QENSmodels from Mantid Workbench
==========================================

If you want to remove the library from your Python installation in Mantid, simply type the following lines in the
scripting window of Mantid workbench

.. code-block:: python

    import subprocess
    print(subprocess.Popen("python -m pip uninstall --yes QENSmodels",
                       shell=True,
                       stdout=subprocess.PIPE,
                       stderr=subprocess.PIPE,
                       stdin=subprocess.PIPE).communicate())


and then restart the workbench.
