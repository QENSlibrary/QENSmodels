#!/usr/bin/env python
# coding: utf-8

from __future__ import print_function
import numpy as np
import matplotlib.pyplot as plt


import h5py
import QENSmodels
from scipy.integrate import simps
import bumps.names as bmp
from bumps.fitters import fit
from bumps.formatnum import format_uncertainty_pm

path_to_data = '../data/'

# Read the sample
with h5py.File(path_to_data + 'BrownianDiff_Sample.hdf', 'r') as f:
    hw = f['entry1']['data1']['X'][:]
    q = f['entry1']['data1']['Y'][:]
    unit_w = f['entry1']['data1']['X'].attrs['long_name']
    unit_q = f['entry1']['data1']['Y'].attrs['long_name']
    sqw = np.transpose(f['entry1']['data1']['DATA'][:])
    err = np.transpose(f['entry1']['data1']['errors'][:])

# Read resolution
with h5py.File(path_to_data + 'BrownianDiff_Resol.hdf', 'r') as f:
    res = np.transpose(f['entry1']['data1']['DATA'][:])

# Force resolution function to have unit area
for i in range(len(q)):
    area = simps(res[:, i], hw)
    res[:, i] /= area


# Units of parameters for selected QENS model and experimental data
dict_physical_units = {'D': "meV.Angstrom^2",
                       'scale': "unit_of_signal.meV",
                       'center': "meV"}


print(f"""The names and units of `w` (`x`axis) and `q` are: 
{str(unit_w[0], 'utf-8')} and {str(unit_q[0], 'utf-8')}, respectively.""")


# Fitting model
def model_convol(x, q, scale=1, center=0, D=1, resolution=None):
    model = QENSmodels.sqwBrownianTranslationalDiffusion(x, q, scale, center, D)
    return np.convolve(model, resolution / resolution.sum(), mode='same')


# Fit
M = []

for i in range(len(q)):
    # Bumps fitting model
    Mq = bmp.Curve(model_convol,
                   hw,
                   sqw[:, i],
                   err[:, i],
                   q=q[i],
                   scale=1000,
                   center=0.0,
                   D=0.1,
                   resolution=res[:, i])
    Mq.scale.range(0, 1e5)
    Mq.center.range(-0.1, 0.1)
    Mq.D.range(0, 1)

    # Q-independent parameters
    if i == 0:
        QD = Mq.D
    else:
        Mq.D = QD
    M.append(Mq)

problem = bmp.FitProblem(M)


print(problem.summarize())


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
        print(k, ":", format_uncertainty_pm(v, dv), dict_physical_units[k])
    else:
        print(k, ":", format_uncertainty_pm(v, dv))



plt.show()

