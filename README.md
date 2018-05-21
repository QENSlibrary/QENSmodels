# Introduction

*QENSlibrary* is a repository containing models (mathematical functions) that
could be used to fit Quasi Elastic Neutron Scattering (QENS) data.

This project has received funding from the European Union’s Horizon
2020 research and innovation programme under grant agreement No 654000.

# Installation

Support Python 2.7 and 3.6


## Requirements

Python modules:
- [numpy](http://www.numpy.org/)

Note that additional modules are required to run the examples. Details can be
found in the README file of the *examples* folder.

## How to install?

- Download or clone the repository which can be found at the following [link](https://github.com/QENSlibrary/QENSmodels)

- To **install the package** to the Python user install directory for your platform, type the following
command in a terminal

```
pip install --user full_path/to/QENSmodels_folder
```
See [the documentation on pip install](https://pip.pypa.io/en/stable/reference/pip_install/#editable-installs) for additional information. Run `pip show QENSmodels` to display details about the installed package.

To **test the installation**, type the following command in a terminal

```
python -c "import QENSmodels"
```

To **uninstall** the library, type

```
pip uninstall QENSmodels
```

## How to build documentation?

In a terminal, move to the *docs* folder and type

   `make html`

This command will generate html files in the subfolder *_build/html*.

# Documentation
The developers' documentation is built using `Sphinx`. The required packages can be
installed using the following commands:

```
pip install sphinx
pip install sphinx-rtd-theme
pip install sphinxcontrib-napoleon
```

Other ways of installing `Sphinx` at be found at
http://www.sphinx-doc.org/en/stable/install.html#


## License

Redistribution of the software is permitted under the terms of the [General Public License version 3 or higher](https://www.gnu.org/licenses/gpl-3.0.en.html).

## How to use?

```python
import QENSmodels
value = QENSmodels.lorentzian(1, 1, 1, 1)

```
or copy and paste the script related to the Lorentzian function.

The scripts can be found in the [git repository](https://github.com/QENSlibrary/QENSmodels)

## How to cite?

**add list of authors**,<br>
"QENS models, version 1",<br>
https://github.com/QENSlibrary/QENSmodels (2018).

## Need help / report a problem / found a bug

Bugs and feature requests are collected at https://github.com/QENSlibrary/QENSmodels/issues.

Add link to websites, email addresses...


# TODO

- complete README.md files
- add tests
- add instructions in installation / setup.py for models and documentation
