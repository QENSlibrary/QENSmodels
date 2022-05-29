This folder contains tools to extract information from the QENS models or to
help users converting units.

* ``Convert_units.ipynb``

  This notebook gives a few references and tips to convert physical units
  of parameters used in the QENS models.

* ``Explore_model.ipynb``

  This notebook displays the characteristics of
  a selected model of the QENS library: the peak half-width half-maximum
  (\ *hwhm*\ ), the elastic incoherent structure factor (\ *eisf*\ ) and the
  quasielastic incoherent structure factor (\ *qisf*\ ).

* ``Test_models.ipynb``

  This notebook displays *S(omega,q)* in linear and log scale for a selected
  model from the QENS library. This model can be convoluted with a Gaussian
  instrument profile.

* ``run_tests.sh``

  This script runs unittests and doctests through the models in ``QENSmodels``.

Note that in order to open the Jupyter notebooks, you'll need `jupyter`, `numpy`,
`matplotlib`, and `ipywidgets` (for interactive plots).

To run the Jupyter notebooks, you can, for example, in the folder where these notebooks are located

* create a virtual environment

  .. code-block:: console

     python -m venv .venv
     source .venv/bin/activate
     python -m pip install ipywidgets jupyterlab matplotlib git+https://github.com/QENSlibrary/QENSmodels.git

 The above command assumes that the QENSmodels library is not installed in this virtual environment.
 If you had already installed the library, replace the above by
 ``python -m pip install ipywidgets jupyterlab matplotlib``.

* to access the notebooks,

  - type ``jupyter lab``
  - click on the notebook you want to open.
