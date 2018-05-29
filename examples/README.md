This folder contains different jupyter notebooks showing how to use models of
the QENS library.

Note that in order to open and run these examples, you need [jupyter](http://jupyter.org/),
[scipy](https://www.scipy.org/),
[matplotlib](https://matplotlib.org/),
[ipywidgets](https://ipywidgets.readthedocs.io/en/latest/) (for interactive plots),
[lmfit](https://lmfit.github.io/lmfit-py/) (optional),
[bumps](https://github.com/bumps/bumps) (optional),
[h5py](https://www.h5py.org/) (for some of the examples).


To access the notebooks, type `jupyter notebook` in a terminal and click on
 the notebook you want to open.

The data required to run some of the notebooks and scripts are located in the `data` 
subfolder.


## Using the jupyter notebooks

### Using via Anaconda

You can download and install Anaconda / Miniconda (a mini version of 
Anaconda that saves you disk space)  on Windows, OSX and Linux.

After installing, to ensure that your packages are up to date, 
run the following command in a terminal:

```
conda update conda
```

You can create a new environment (called `mynewenv` in the following example), 
which will contain the required packages

```
conda create --name mynewenv python numpy scipy matplotlib jupyter
```

Note that you can specify which version of `Python`. For example, 
`conda create --name mynewenv python=3.4 numpy scipy matplotlib jupyter` 

Then activate the environment and install the remaining packages
```
source activate mynewenv
conda install -c conda-forge h5py
```
Finally, install the library
``` pip install --user path_to/QENSmodels ```

The packages for fitting, *i.e.* `lmfit`, `bumps`, will be installed when 
running the jupyter notebooks, where they are required.
