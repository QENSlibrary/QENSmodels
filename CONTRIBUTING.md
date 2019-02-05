# Contributing

## Introduction

First of all, thank you for considering contributing to the QENS models' 
library. Contributions are welcome from the community.   
This document describes some guidelines that are intended to help to communicate 
with the developers' team, so that it can address your issue, assess your 
changes and help you finalize your pull requests.

## Ground rules

If you have direct contributions you would like considered for incorporation 
into the project you can fork this repository and submit a pull request for review.

People interested can contribute to the project in different ways:
1. adding QENS models
2. adding new examples of fitting using some of the QENS models and the 
  fitting engine of their choice 
  
### New QENS models

- Contributed models should be written in `Python` (compatibility with 
  `Python 3.x` is preferred).
- For each new model, a Python script should be provided alongside with some 
 documentation and tests.
- Once ready, you need to upload the `Python` source code files to the 
[git repository](https://github.com/QENSlibrary/QENSmodels) by submitting a 
pull request.


Contributors feeling unsure or inexperienced about contributing to an open-source 
repository are referred to [this tutorial](https://github.com/firstcontributions/first-contributions).

**Working on your first Pull Request?** You can learn how from this *free* 
series 
[How to Contribute to an Open Source Project on GitHub](https://egghead.io/series/how-to-contribute-to-an-open-source-project-on-github) 


#### Python script
- It should be placed in the `QENS models` folder.
- The [`doctest`](https://docs.python.org/2/library/doctest.html) module has 
  to be imported (*i.e.* paste `import doctest` at the beginning of your 
  `Python` script).
- Each function should have a docstring specifying its name, parameters, a 
  short description and some examples. Please refer to the existing models 
  for help. A more general template for docstring can be found [here](https://sphinxcontrib-napoleon.readthedocs.io/en/latest/example_numpy.html). 
- And before submitting your pull request, check that your script, test and 
built of the documentation run on your machine. 

#### Documentation

- For the QENS models' library, the documentation is built using `Sphinx`.
- The related files are located in the `docs` folder.
- In addition, as mentioned in the previous section, each model should contain a 
  self-contained description. 


### New examples
    
- Contributed examples should use `Jupyter` notebooks (preferred) or `Python` scripts.
- Please add a maximum of information about the case being described: 
    * physical model
    * reference to publication (if any)
    * steps leading to the final results 
      (reduction, convolution of functions, normalization...)
- If additional reference datasets are required, they can be stored in 
the `/examples/data` folder. But the preferred option is to generate these 
reference data on the fly in the notebook or script without creating any 
permanent external file.
       

## Other issues
- Questions or requests related to the library can be asked on the issues page. 
- Before creating a new issue, please take a moment to search and make sure a 
  similar issue does not already exist. If one does exist, you add a comment to 
  it; most simply even with just a :+1: to show your support for that issue.
- If you find any bugs, please report them by submitted a new issue .
