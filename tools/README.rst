.. role:: raw-html-m2r(raw)
   :format: html


This folder contains tools to extract information from the QENS models


* 
  ``Explore_model.ipynb``\ :raw-html-m2r:`<br>`
  This notebook displays the characteristics of 
  a selected model of the QENS library: the peak half-width half-maximum 
  (\ *hwhm*\ ), the elastic incoherent structure factor (\ *eisf*\ ) and the 
  quasielastic incoherent structure factor (\ *qisf*\ ).

* 
  ``Test_models.ipynb``\ :raw-html-m2r:`<br>`
  This notebook displays *S(omega,q)* in linear and log scale for a selected 
  model from the QENS library. This model can be convoluted with a Gaussian 
  instrument profile .

* 
  ``run_tests.sh``\ :raw-html-m2r:`<br>`
  This script runs unittests and doctests through the models in ``QENSmodels``.

Note that in order to open the Jupyter notebooks, you'll need jupyter, numpy, 
matplotlib, and ipywidgets (for interactive plots).

To run the jupyter notebooks, you can, for example, create an anaconda 
environment:


* 
  download and install Anaconda / Miniconda (a mini version of Anaconda 
  that saves you disk space) on Windows, OSX and Linux.

* 
  after installing, to ensure that your packages are up to date, 
  run the following command in a terminal:

  .. code-block::

     conda update conda

* 
  create a new environment (called ``mynewenv`` in the following example), 
  which will contain the required packages

  .. code-block::

     conda create --name mynewenv python numpy matplotlib jupyter

* 
  to access the notebooks, open a terminal, move to the folder where the 
  notebook you want to open is located, type ``jupyter notebook``\ , and click on 
  the notebook you want to open.
