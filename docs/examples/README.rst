Introduction
============

This section contains different Jupyter notebooks showing how to use models of
the QENS library. The sub-folder ``using_mantid`` details how to proceed if you want to use Mantid
(`link <https://github.com/QENSlibrary/QENSmodels/blob/master/docs/examples/using_mantid/README.rst>`__).

Note that in order to open and run these examples, you need
`jupyter <http://jupyter.org/>`_\ ,
`matplotlib <https://matplotlib.org/>`_\ ,
`ipywidgets <https://ipywidgets.readthedocs.io/en/latest/>`_ (for interactive
plots),
`lmfit <https://lmfit.github.io/lmfit-py/>`_ (fitting for some of the examples),
`bumps <https://github.com/bumps/bumps>`_ (fitting for some of the examples),
`h5py <https://www.h5py.org/>`_ (loading reference data for some of the examples).


The data required to run some of the notebooks and scripts are located in the
``data`` subfolder.

Summary of the Jupyter notebooks
================================

The following table summarizes some of the main features of the Jupyter notebooks in the
``examples`` folder.

+-------------------------------------------+----------------+----------+------------+------------+
| Name "_fit.ipynb"                         | External input | Composed | Background | Resolution |
|                                           | datafile       | models   |            |            |
+-------------------------------------------+----------------+----------+------------+------------+
| bumps_BrownianDiff                        | X              |          |            | X          |
+-------------------------------------------+----------------+----------+------------+------------+
| bumps_ChudleyElliottDiff                  |                |          |            |            |
+-------------------------------------------+----------------+----------+------------+------------+
| bumps_DeltaLorentz                        | X              |          |            | X          |
+-------------------------------------------+----------------+----------+------------+------------+
| bumps_IsoRot                              | X              |          |            | X          |
+-------------------------------------------+----------------+----------+------------+------------+
| bumps_JumpDiffIsoRot                      | X              |          |            | X          |
+-------------------------------------------+----------------+----------+------------+------------+
| bumps_JumpDiff                            | X              |          |            | X          |
+-------------------------------------------+----------------+----------+------------+------------+
| bumps_waterIN5_delta_two_lorentz          | X              |          |            | X          |
+-------------------------------------------+----------------+----------+------------+------------+
| bumps_waterIN5_lorentzian_plus_isorotdiff | X              | X        |            | X          |
+-------------------------------------------+----------------+----------+------------+------------+
| bumps_waterIN5_teixeira                   | X              |          |            | X          |
+-------------------------------------------+----------------+----------+------------+------------+
| lmfit_EquivalentSitesCircle               |                |          |            |            |
+-------------------------------------------+----------------+----------+------------+------------+
| lmfit_GaussianModel3D                     |                |          |            |            |
+-------------------------------------------+----------------+----------+------------+------------+
| lmfit_lorentzian_and_backgd               |                |          | X          |            |
+-------------------------------------------+----------------+----------+------------+------------+
| lmfit_two_lorentzian                      | X              | X        |            | X          |
+-------------------------------------------+----------------+----------+------------+------------+
| lmfit_waterIN5_teixeira                   | X              |          |            | X          |
+-------------------------------------------+----------------+----------+------------+------------+
| scipy_JumpSitesLogNormDist                |                |          |            |            |
+-------------------------------------------+----------------+----------+------------+------------+
| scipy_lorentzian                          |                |          |            |            |
+-------------------------------------------+----------------+----------+------------+------------+


Using the jupyter notebooks in a virtual environment
====================================================

- If not already installed on your computer, download and install Python (version>=3.8), for example,
  from https://www.python.org/downloads/. In the following instructions, replace ``python`` by the path to
  the version of python you want to use.

- Download or clone the QENSmodels repository at https://github.com/QENSlibrary/QENSmodels

- Create virtual environment and activate it (optional)

  .. code-block:: console

      cd QENSmodels/docs
      python -m venv .venv

  To activate your virtual environment
    - on Unix or MacOS

      .. code-block:: console

         python -m venv .venv
         source .venv/bin/activate

    - on Windows

      .. code-block:: console

          python -m venv .venv
          .\.venv\Scripts\activate

- Upgrade pip (optional)

  .. code-block:: console

     python -m pip install --upgrade pip

- Install the library and the additional required packages. In a terminal run

  .. code-block:: console

     python -m pip install -e  '\path_to_QENS_library/.[examples]'


- In order to use the examples, simply type ``jupyter lab`` in a terminal.


Short tutorials on Jupyter notebooks
====================================

* `Jupyter Lab documentation <https://jupyterlab.readthedocs.io/en/stable/>`_

* `Tutorials from DataCamp <https://www.datacamp.com/community/tutorials/tutorial-jupyter-notebook?utm_source=adwords_ppc&utm_campaignid=898687156&utm_adgroupid=48947256715&utm_device=c&utm_keyword=&utm_matchtype=b&utm_network=g&utm_adpostion=1t1&utm_creative=229765585183&utm_targetid=dsa-473406581035&utm_loc_interest_ms=&utm_loc_physical_ms=1005010&gclid=EAIaIQobChMIpZn9hPqc4QIVzh0YCh2c1ARQEAAYASAAEgK81fD_BwE>`_
