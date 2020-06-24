QENS models and Mantid
######################

Introduction
============

Several options are possible to use QENS library and Mantid depending on your operating system.

Since Mantidplot is being replaced by Mantid Workbench, the tips and methods details in this
document have been tested using the latter only.

Installation
============

Using QENS models in Mantid Workbench
-------------------------------------

This method can be used on all operating systems.

The first step is to install Mantid Workbench following the instructions on the
`official page <https://download.mantidproject.org/>`__. Then follow the instructions below
depending on your operating system.

On Mac
~~~~~~

- Download the `get-pip.py` script from `pip's website <https://pip.pypa.io/en/stable/installing/>`__

- Save the above file to Desktop (for example).
  In a terminal run these lines to install pip and use it to install the QENSmodels library:

  .. code-block:: console

      cd ~/Desktop

      /Applications/MantidWorkbench.app/Contents/Frameworks/Python.framework/Versions/3.7/bin/python get-pip.py --user

      /Applications/MantidWorkbench.app/Contents/Frameworks/Python.framework/Versions/3.7/bin/python -m pip install path_to_QENSmodels --user

  where path_to_QENSmodels is the location of the QENSmodels' folder on your computer, for example
  `/Users/my_username/Desktop/QENSmodels`.

On Windows
~~~~~~~~~~

In a command prompt,

- `cd` into `MantidInstall\bin`

- type

  .. code-block:: console

     Scripts\pip install path_to_QENSmodels

  where path_to_QENSmodels is the location of the QENSmodels folder on your computer


On Linux
~~~~~~~~

In a terminal, type

.. code-block:: console

    python3 -m pip install path_to_QENSmodels

 where path_to_QENSmodels is the location of the QENSmodels's folder on your computer


Testing the installation
------------------------

After following one of the above methods, you should just be able to use import the QENSmodels
library within Mantid. For example, to test the installation, in the editor of MantidWorkbench
simply type

.. code-block:: python

    import QENSmodels


.. note::

   Note that this will work if you’re using Mantid version 5.0.

   These tips were heavily inspired from these webpages for
   `Mac <https://forum.mantidproject.org/t/lmfit-installation/658>`__ and for
   `Windows <https://forum.mantidproject.org/t/pandas-in-mantid-workbench/574>`__

The Python script `mantid_BrownianDiff_fit.py` can be used as an example to be loaded in Mantid
Workbench for fitting data to functions from the QENSmodels library.

