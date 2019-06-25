This folder contains tools to extract information from the QENS models or to
help users converting units

* ``Convert_units.ipynb``

  This notebook gives a few references and tips to convert physical units
  in order to be able to use the QENS models if the experimental data are expressed in
  different units.

* ``Explore_model.ipynb``

  This notebook displays the characteristics of
  a selected model of the QENS library: the peak half-width half-maximum
  (\ *hwhm*\ ), the elastic incoherent structure factor (\ *eisf*\ ) and the
  quasielastic incoherent structure factor (\ *qisf*\ ).

* ``Test_models.ipynb``

  This notebook displays *S(omega,q)* in linear and log scale for a selected
  model from the QENS library. This model can be convoluted with a Gaussian
  instrument profile .

* ``run_tests.sh``

  This script runs unittests and doctests through the models in ``QENSmodels``.

Note that in order to open the Jupyter notebooks, you'll need `jupyter`, `numpy`,
`matplotlib`, and `panel` + `pandas` (for interactive plots).

To run the Jupyter notebooks, you can, for example, create an anaconda
environment:


* download and install Anaconda / Miniconda (a mini version of Anaconda
  that saves you disk space) on Windows, OSX and Linux.

* after installing, to ensure that your packages are up to date,
  run the following command in a terminal:

  .. code-block:: console

     conda update conda

* create a new environment (called ``mynewenv`` in the following example),
  which will contain the required packages

  .. code-block:: console

     conda create --name mynewenv python numpy matplotlib jupyter
     conda activate mynewenv
     conda install -c pyviz panel

* to access the notebooks,
  - activate your conda environment. For example, if the environment was created using the above commands, simply
  type `conda activate mynewenv` in a terminal.
  -  move to the folder where the notebook you want to open is located,
  -  type ``jupyter notebook``
  - click on the notebook you want to open.
