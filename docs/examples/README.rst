Introduction
^^^^^^^^^^^^

This section contains different Jupyter notebooks showing how to use models of
the QENS library. The sub-folder `using_mantid` details how to proceed if you want to use Mantid
(`link <https://github.com/QENSlibrary/QENSmodels/blob/master/docs/examples/using_mantid/README.rst>`_ ).

Note that in order to open and run these examples, you need
`jupyter <http://jupyter.org/>`_\ ,
`scipy <https://www.scipy.org/>`_\ ,
`matplotlib <https://matplotlib.org/>`_\ ,
`ipywidgets <https://ipywidgets.readthedocs.io/en/latest/>`_ (for interactive
plots),
`lmfit <https://lmfit.github.io/lmfit-py/>`_ (optional),
`bumps <https://github.com/bumps/bumps>`_ (optional),
`h5py <https://www.h5py.org/>`_ (for some of the examples).

To access the notebooks, type ``jupyter notebook`` in a terminal and click on the notebook you want
to open.


The data required to run some of the notebooks and scripts are located in the
``data`` subfolder.

Summary of the Jupyter notebooks
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

The following table summarizes some of the main features of the Jupyter notebooks in the
``examples`` folder.

+-------------------------------------------+-------------------------+--------------------+-----------------+------------+------------+
| Name "_fit.ipynb"                         | External input datafile | "Interactive plot" | Composed models | Background | Resolution |
+-------------------------------------------+-------------------------+--------------------+-----------------+------------+------------+
| bumps_BrownianDiff                        | X                       |                    |                 |            |  X         |
+-------------------------------------------+-------------------------+--------------------+-----------------+------------+------------+
| bumps_ChudleyElliotDiff                   |                         |                    |                 |            |            |
+-------------------------------------------+-------------------------+--------------------+-----------------+------------+------------+
| bumps_DeltaLorentz                        | X                       |                    |                 |            | X          |
+-------------------------------------------+-------------------------+--------------------+-----------------+------------+------------+
| bumps_IsoRot                              | X                       |                    |                 |            | X          |
+-------------------------------------------+-------------------------+--------------------+-----------------+------------+------------+
| bumps_JumpDiffIsoRot                      | X                       |                    |                 |            | X          |
+-------------------------------------------+-------------------------+--------------------+-----------------+------------+------------+
| bumps_JumpDiff                            | X                       |                    |                 |            |            |
+-------------------------------------------+-------------------------+--------------------+-----------------+------------+------------+
| bumps_waterIN5_delta_two_lorentz          | X                       |                    |                 |            |            |
+-------------------------------------------+-------------------------+--------------------+-----------------+------------+------------+
| bumps_waterIN5_lorentzian_plus_isorotdiff | X                       |                    | X               |            | X          |
+-------------------------------------------+-------------------------+--------------------+-----------------+------------+------------+
| bumps_waterIN5_water_teixeira             | X                       |                    |                 |            | X          |
+-------------------------------------------+-------------------------+--------------------+-----------------+------------+------------+
| lmfit_EquivalentSitesCircle               |                         | X                  |                 |            |            |
+-------------------------------------------+-------------------------+--------------------+-----------------+------------+------------+
| lmfit_GaussianModel3D                     |                         | X                  |                 |            |            |
+-------------------------------------------+-------------------------+--------------------+-----------------+------------+------------+
| lmfit_lorentzian_and_backgd               |                         | X                  |                 | X          |            |
+-------------------------------------------+-------------------------+--------------------+-----------------+------------+------------+
| lmfit_two_lorentzian                      | X                       |                    | X               |            | X          |
+-------------------------------------------+-------------------------+--------------------+-----------------+------------+------------+
| lmfit_waterIN5_teixeira                   | X                       |                    |                 |            | X          |
+-------------------------------------------+-------------------------+--------------------+-----------------+------------+------------+
| scipy_JumpSitesLogNormDist                |                         | X                  |                 |            |            |
+-------------------------------------------+-------------------------+--------------------+-----------------+------------+------------+
| scipy_lorentzian                          |                         | X                  |                 |            |            |
+-------------------------------------------+-------------------------+--------------------+-----------------+------------+------------+

Using the jupyter notebooks
---------------------------

Using via Anaconda
^^^^^^^^^^^^^^^^^^

You can download and install Anaconda / Miniconda (a mini version of
Anaconda that saves you disk space) on Windows, OSX and Linux.

After installing, to ensure that your packages are up to date,
run the following command in a terminal:

.. code-block:: console

   conda update conda

You can create a new environment (called ``mynewenv`` in the following example),
which will contain the required packages

.. code-block:: console

   conda create --name mynewenv python=3.7 ipywidgets h5py numpy scipy matplotlib jupyter

Note that we force the installation of version 3.7 of Python because of some
incompatibilities with one of the fitting package, `bumps`, whose version 
0.7.12 will be installed in the dedicated notebooks.

Then activate the environment and install the remaining packages

.. code-block:: console

   conda activate mynewenv

Finally, install the library

``python -m pip install path_to_QENSmodels_folder
``

where `path_to_QENSmodels_folder` is the location of the QENSmodels' folder on your computer (for
example `/Users/my_username/Desktop/QENSmodels`).

The packages for fitting, *i.e.* ``lmfit``\ , ``bumps``\ , will be installed when
running the jupyter notebooks, where they are required.

Short tutorials on Jupyter notebooks
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^


* `https://www.tutorialspoint.com/jupyter/jupyter_project_overview.htm <https://www.tutorialspoint.com/jupyter/jupyter_project_overview.htm>`_

* `tutorials from DataCamp <https://www.datacamp.com/community/tutorials/tutorial-jupyter-notebook?utm_source=adwords_ppc&utm_campaignid=898687156&utm_adgroupid=48947256715&utm_device=c&utm_keyword=&utm_matchtype=b&utm_network=g&utm_adpostion=1t1&utm_creative=229765585183&utm_targetid=dsa-473406581035&utm_loc_interest_ms=&utm_loc_physical_ms=1005010&gclid=EAIaIQobChMIpZn9hPqc4QIVzh0YCh2c1ARQEAAYASAAEgK81fD_BwE>`_

* `Jupyter notebook documentation on ReadTheDocs (pdf file) <https://buildmedia.readthedocs.org/media/pdf/jupyter-notebook/latest/jupyter-notebook.pdf>`_
