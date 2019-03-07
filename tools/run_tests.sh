#!/usr/bin/env bash
cd ../tests/

# TO RUN UNITTEST
python -m unittest -v test_background_polynomials
python -m unittest -v test_brownian_translational_diffusion
python -m unittest -v test_delta
python -m unittest -v test_delta_lorentz
python -m unittest -v test_delta_two_lorentz
python -m unittest -v test_gaussian
python -m unittest -v test_isotropic_rotational_diffusion
python -m unittest -v test_jump_translational_diffusion
python -m unittest -v test_lorentzian
python -m unittest -v test_water_teixeira

# TO RUN DOCTEST
# list of models in QENSmodels folder
MODELS_DIRECTORY="../QENSmodels/"
cd $MODELS_DIRECTORY
FILES=`ls [^_]*.py`

for file in $FILES
do
  echo '****************'
  echo 'Test' $file
  python -m doctest $file -v

done
