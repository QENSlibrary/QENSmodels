This folder contains tools to extract information from the QENS models

- `Explore_model.ipynb`   
  This notebook displays the characteristics of 
  a selected model of the QENS library: the peak half-width half-maximum 
  (*hwhm*), the elastic incoherent structure factor (*eisf*) and the 
  quasielastic incoherent structure factor (*qisf*).

- `Test_models.ipynb`  
  This notebook displays *S(omega,q)* in linear and log scale for a selected 
  model from the QENS library. This model can be convoluted with a Gaussian 
  instrument profile .

- `run_tests.sh`  
  This script runs unittests and doctests through the models in `QENSmodels`.