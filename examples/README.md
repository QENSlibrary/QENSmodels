This folder contains different jupyter notebooks showing how to use models of
the QENS library.

Note that in order to open and run these examples, you need [jupyter](http://jupyter.org/),
[scipy](https://www.scipy.org/),
[matplotlib](https://matplotlib.org/),
[ipywidgets](https://ipywidgets.readthedocs.io/en/latest/),
[lmfit](https://lmfit.github.io/lmfit-py/) (optional),
[bumps](https://github.com/bumps/bumps) (optional),
[h5py](https://www.h5py.org/) (for some of the examples).


To access the notebooks, type `jupyter notebook` in a terminal and click on
 the notebook you want to open.

In addition to the notebooks, this `example` folder also contains some
reference datafiles:

- **Example 1**: the Nexus files are parts of the ISIS sample datasets of [Mantid](http://download.mantidproject.org/). For this example, ASCII data files contain a subset of the original workspaces and are organised as follow:
  - `data_2lorentzians.dat` extracted from `irs26176_graphite002_red.nxs`
   (workspace index = 0)
  - `irf_iris.dat` extracted from `irs26173_graphite002_res.nxs`
  (instrument resolution file of IRIS)

- **Example 2** (**ADD REFERENCE OF PUBLICATION**):
  - `H2O_293K_5A.hdf`, `H2O_293K_8A.hdf`: Water measured at 293K for 2
  wavelengths (5 and 8 &#8491;)
  - `V_273K_5A.hdf`, `V_273K_8A.hdf`: Vanadium measured at 273K for 2
  wavelengths (5 and 8 &#8491;)


**todo**: add instructions to install anaconda environment to use jupyter
notebook and have all required libraries installed.
