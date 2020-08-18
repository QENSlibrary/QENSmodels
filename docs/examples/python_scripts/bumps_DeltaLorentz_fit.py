#!/usr/bin/env python
# coding: utf-8

from __future__ import print_function
import matplotlib.pyplot as plt


import h5py
import QENSmodels
import numpy as np
from scipy.integrate import simps
import bumps.names as bmp
from bumps.fitters import fit
from bumps.formatnum import format_uncertainty

path_to_data = '../data/'

# Read the sample
with h5py.File(path_to_data + 'DeltaBrownianDiff_Sample.hdf', 'r') as f:
    hw = f['entry1']['data1']['X'][:]
    q = f['entry1']['data1']['Y'][:]
    unit_w = f['entry1']['data1']['X'].attrs['long_name']
    unit_q = f['entry1']['data1']['Y'].attrs['long_name']
    sqw = np.transpose(f['entry1']['data1']['DATA'][:])
    err = np.transpose(f['entry1']['data1']['errors'][:])

# Read resolution
with h5py.File(path_to_data + 'DeltaBrownianDiff_Resol.hdf', 'r') as f:
    res = np.transpose(f['entry1']['data1']['DATA'][:])

# Force resolution function to have unit area
for i in range(len(q)):
    area = simps(res[:, i], hw)
    res[:, i] /= area


# Units of parameters for selected QENS model and experimental data
dict_physical_units = {'omega': "meV",
                       'q': "1/Angstrom",
                       'scale': "unit_of_signal.meV",
                       'center': "meV",
                       'hwhm': "meV"}


print(f"""The names and units of `w` (`x`axis) and `q` are: 
{str(unit_w[0], 'utf-8')} and {str(unit_q[0], 'utf-8')}, respectively.""")


# Fitting model
def model_convol(x, q, scale=1, center=0, A0=0, hwhm=1, resolution=None):
    model = QENSmodels.sqwDeltaLorentz(x, q, scale, center, A0, hwhm)
    return np.convolve(model, resolution / resolution.sum(), mode='same')


# Fit
M = []

# First dataset: wavelength=5 Angstrom
for i in range(len(q)):

    # Bumps fitting model
    Mq = bmp.Curve(model_convol,
                   hw,
                   sqw[:, i],
                   err[:, i],
                   q=q[i],
                   scale=1000,
                   center=0.0,
                   A0=0.5,
                   hwhm=0.01,
                   resolution=res[:, i])
    Mq.scale.range(0, 1e5)
    Mq.center.range(-0.1, 0.1)
    Mq.A0.range(0, 1)
    Mq.hwhm.range(0, 2)

    # Q-independent parameters
    if i == 0:
        QA0 = Mq.A0
    else:
        Mq.A0 = QA0
    M.append(Mq)

problem = bmp.FitProblem(M)


# Preview of the settings
print('Initial chisq', problem.chisq_str())


problem.plot()


result = fit(problem,
             method='lm',
             steps=100,
             verbose=True)


problem.plot()


# Print chi**2 and parameters' values after fit
print("final chisq", problem.chisq_str())
for k, v, dv in zip(problem.labels(), result.x, result.dx):
    if k in dict_physical_units.keys():
        print(k, ":", format_uncertainty(v, dv), dict_physical_units[k])
    else:
        print(k, ":", format_uncertainty(v, dv))



plt.show()

