# Introduction

*QENSlibrary* is a repository containing models (mathematical functions) that
can be used to fit Quasi Elastic Neutron Scattering (QENS) data.  
This project has received funding from the European Union’s Horizon
2020 research and innovation programme under grant agreement No 654000.

# Installation
Support [Python](https://www.python.org/downloads/) 2.7 and 3.6

## Requirements

Python modules to use the models:
- [numpy](http://www.numpy.org/)  

Additional modules are required to run the examples. Details can be
found in the README file of the *examples* folder.

## How to install?

### Note: 
If you want to use a virtual environment, please go to [this link](https://conda.io/docs/user-guide/getting-started.html)
for instructions. 

The steps to follow are:  
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

# Documentation
The documentation is built using `Sphinx`. The required packages can be
installed using the following commands:

```
pip install sphinx
pip install sphinx-rtd-theme
pip install sphinxcontrib-napoleon
pip install m2r
```

Other ways of installing `Sphinx` at be found at
http://www.sphinx-doc.org/en/stable/install.html#


## How to build documentation?

In a terminal, move to the *docs* folder and type

   `make html`

This command will generate html files in the subfolder *_build/html*.

# Tests
The script to run the doctests is located in the `tools` folder.  
In a terminal, move to the `tools` directory and run
```
./run_doctest.sh
```

## License

Redistribution of the software is permitted under the terms of the 
[General Public License version 3 or higher](https://www.gnu.org/licenses/gpl-3.0.en.html).

## How to use?

```python
import QENSmodels
value = QENSmodels.lorentzian(1, 1, 1, 1)

```
or copy and paste the script related to the Lorentzian function.  
The scripts can be found in the 
[git repository](https://github.com/QENSlibrary/QENSmodels)

Jupyter notebooks using some of the QENS models are located in the `examples` 
folder. The name of the notebook indicates which fitting engine and QENS model 
are used. Additional tools might have to be installed in order to use a 
particular notebook.

## How to cite?

**add list of authors**<br>
"QENS models, version 1",<br>
https://github.com/QENSlibrary/QENSmodels (2018).

## Need help / found a bug

Bugs and feature requests are collected at 
https://github.com/QENSlibrary/QENSmodels/issues.

If you are reporting a bug, please include:

- Your operating system name and version.
- Any details about your local setup that might be helpful in troubleshooting.
- Detailed steps to reproduce the bug.
