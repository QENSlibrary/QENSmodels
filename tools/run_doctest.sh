#!/bin/sh

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
