# Contributing

## Introduction

First of all, thank you for considering contributing to the QENS models' 
library. Contributions are welcome from the community.   
This document describes some guidelines that are intended to help to communicate 
with the developers' team, so that it can address your issue, assess your 
changes and help you finalize your pull requests.

## Ground rules

If you have direct contributions you would like to be considered for 
incorporation into the project you can fork this repository and submit a pull 
request for review.


Contributors feeling unsure or inexperienced about contributing to an open-source 
repository are referred to [this tutorial](https://github.com/firstcontributions/first-contributions).

**Working on your first Pull Request?** You can learn how from this *free* 
series 
[How to Contribute to an Open Source Project on GitHub](https://egghead.io/series/how-to-contribute-to-an-open-source-project-on-github) 


People interested can contribute to the project in different ways:
1. adding QENS models
2. adding new examples of fitting using some of the QENS models and the 
  fitting engine of their choice 
  
### New QENS models

- Contributed models should be written in `Python` (compatibility with 
  `Python 3.x` is preferred).
- For each new model, a Python script should be provided alongside some 
 documentation and tests.
- Once ready, you need to upload the `Python` source code files to the 
  [git repository](https://github.com/QENSlibrary/QENSmodels) by submitting a 
  pull request.


#### Python script
- It should be placed in the `QENS models` folder. The associated `Python` 
  script for the tests should be placed in the `tests` folder. 
- The [`doctest`](https://docs.python.org/2/library/doctest.html) module has 
  to be imported (*i.e.* paste `import doctest` in your 
  `Python` script. Please refer to the existing models 
  for help).
- Each function should have a docstring specifying its name, parameters, a 
  short description and some examples. These examples will be used when 
  running `doctest`. Please refer to the existing models 
  for help. A more general template for docstring can be found 
  [here](https://sphinxcontrib-napoleon.readthedocs.io/en/latest/example_numpy.html). 
- And before submitting your pull request, check that your script, tests and 
  built of the documentation run on your machine. Please also run ``flake8`` 
  to check your code matches the project style (by running, for example, 
  `flake8 new_python_script.py`).

#### Documentation

- For the QENS models' library, the documentation is built using 
  [`Sphinx`](http://www.sphinx-doc.org/en/master/).
- The related files are located in the `docs` folder.
- In addition, as mentioned in the previous section, each model should contain 
  a self-contained description. 


### New examples
    
- Contributed examples should use [![jupyter](https://img.shields.io/badge/-jupyter-%236091f2.svg)][labels-jupyter] notebooks (preferred) or `Python` 
  scripts.
- Please add a maximum of information about the case being described: 
    * physical model
    * reference to publication (if any)
    * steps leading to the final results 
      (reduction, convolution of different models, normalization...)
    * choice of minimizer and link to its documentation
- If additional reference datasets are required, they can be stored in 
the `/examples/data` folder. But the preferred option is to generate these 
reference data on the fly in the notebook or script without creating any 
permanent external file.
- If additional `Python` modules are used in the new notebook or script, 
please add them to the list of requirements in the 
[README](./examples/README.md) file located in the `examples` directory.
       

## Other issues
- [![question](https://img.shields.io/badge/-question-%23d876e3.svg)][labels-question] 
  or [![Enhancement](https://img.shields.io/badge/-enhancement-%23a2eeef.svg)][labels-enhancement] related to the library can be asked on the issues page. 
- Before creating a new issue, please take a moment to search and make sure a 
  similar issue does not already exist. If one does exist, you add a comment to 
  it; most simply even with just a :+1: to show your support for that issue.
- If you find any bugs, please report them by submitted a new issue labelled 
  as [![bug](https://img.shields.io/badge/-bug-%23d73a4a.svg)][labels-bug]. 
  The more details you can provide the better. If you know how to fix the bug, 
   please open an issue first and then submit a pull request.
- [![good-first-issue](https://img.shields.io/badge/-good%20first%20issue-%237057ff.svg)][labels-firstissue] 
    
    *These issues are particularly appropriate if it is your first 
    contribution.*
    If you're not sure about how to go about contributing, these are good 
    places to start. You'll be mentored through the process by the maintainers 
    team. If you're a seasoned contributor, please select a different issue to 
    work from and keep these available for the newer and potentially more 
    anxious team members.
- [![help-wanted](https://img.shields.io/badge/-help%20wanted-%23008672.svg)][labels-helpwanted] 
    contain a task that you can contribute to. We especially 
    encourage you to do so if you feel you can help.


[qens-issues-labels]: https://github.com/QENSlibrary/QENSmodels/labels
[labels-bug]: https://github.com/QENSlibrary/QENSmodels/labels/bug
[labels-helpwanted]: https://github.com/QENSlibrary/QENSmodels/labels/help%20wanted
[labels-question]: https://github.com/QENSlibrary/QENSmodels/labels/question
[labels-enhancement]: https://github.com/QENSlibrary/QENSmodels/labels/enhancement
[labels-jupyter]: https://github.com/QENSlibrary/QENSmodels/labels/jupyter
[labels-firstissue]: https://github.com/QENSlibrary/QENSmodels/labels/good%20first%20issue

[markdown]: https://daringfireball.net/projects/markdown
[github]: https://github.com
