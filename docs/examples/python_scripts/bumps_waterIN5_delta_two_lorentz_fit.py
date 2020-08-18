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

# Data
# Wavelength 5 Angstrom
with h5py.File(path_to_data + 'H2O_293K_5A.hdf', 'r') as f:
    hw_5A = f['entry1']['data1']['X'][:]
    q_5A = f['entry1']['data1']['Y'][:]
    unit_w5A = f['entry1']['data1']['X'].attrs['long_name']
    unit_q5A = f['entry1']['data1']['Y'].attrs['long_name']
    sqw_5A = np.transpose(f['entry1']['data1']['DATA'][:])
    err_5A = np.transpose(f['entry1']['data1']['errors'][:])

# Wavelength 8 Angstrom
with h5py.File(path_to_data + 'H2O_293K_8A.hdf', 'r') as f:
    hw_8A = f['entry1']['data1']['X'][:]
    q_8A = f['entry1']['data1']['Y'][:]
    unit_w8A = f['entry1']['data1']['X'].attrs['long_name']
    unit_q8A = f['entry1']['data1']['Y'].attrs['long_name']
    sqw_8A = np.transpose(f['entry1']['data1']['DATA'][:])
    err_8A = np.transpose(f['entry1']['data1']['errors'][:])

# Resolution
# Wavelength 5 Angstrom
with h5py.File(path_to_data + 'V_273K_5A.hdf', 'r') as f:
    res_5A = np.transpose(f['entry1']['data1']['DATA'][:])

# Wavelength 8 Angstrom
with h5py.File(path_to_data + 'V_273K_8A.hdf', 'r') as f:
    res_8A = np.transpose(f['entry1']['data1']['DATA'][:])

# Force resolution function to have unit area
# 5 Angstrom
for i in range(len(q_5A)):
    area = simps(res_5A[:, i], hw_5A)
    res_5A[:, i] /= area

# 8 Angstrom
for i in range(len(q_8A)):
    area = simps(res_8A[:, i], hw_8A)
    res_8A[:, i] /= area

# Fit range -1 to +1 meV
idx_5A = np.where(np.logical_and(hw_5A > -1.0, hw_5A < 1.0))
idx_8A = np.where(np.logical_and(hw_8A > -1.0, hw_8A < 1.0))


def model_convol(x, q, scale=1, center=0, A0=1.0, A1=1.0, hwhm1=1.0, hwhm2=1.0, resolution=None):
    model = QENSmodels.sqwDeltaTwoLorentz(x, q, scale, center, A0, A1, hwhm1, hwhm2)
    return np.convolve(resolution / resolution.sum(), model, mode='same')


print(f"""At 5 Angstroms, the names and units of `w` ( `x`axis) and `q` are: 
{str(unit_w5A[0], 'utf-8')} and {str(unit_q5A[0], 'utf-8')}, respectively.""")

print(f"""At 8 Angstroms, the names and units of `w` ( `x`axis) and `q` are: 
{str(unit_w8A[0], 'utf-8')} and {str(unit_q8A[0], 'utf-8')}, respectively.""")


# Fit
M = []

# First dataset: wavelength=5 Angstrom
for i in range(len(q_5A)):

    x = hw_5A[idx_5A]
    data = sqw_5A[idx_5A, i]
    error = err_5A[idx_5A, i]
    resol = res_5A[idx_5A, i]

    # Select only valid data (error = -1 for Q, w points not accessible)
    valid = np.where(error > 0.0)

    x = x[valid[1]]
    if len(valid[1]) != len(x):
        print(i, "truncate to make vectors symmetric with respect to max")

    data = data[valid]
    error = error[valid]
    resol = resol[valid]

    # Teixeira model
    Mq = bmp.Curve(model_convol,
                   x,
                   data,
                   error,
                   q=q_5A[i],
                   scale=20,
                   center=0.0,
                   A0=0.0,
                   A1=0.9,
                   hwhm1=0.05,
                   hwhm2=0.3,
                   resolution=resol)

    # Fitted parameters
    Mq.scale.range(1.e-12, 20)
    Mq.center.range(-0.1, 0.1)
    Mq.A0.range(0, 0.05)
    Mq.A1.range(0, 1)
    Mq.hwhm1.range(0, 0.5)
    Mq.hwhm2.range(0, 3)

    # Q-independent parameters
    if i == 0:
        QA0 = Mq.A0
    else:
        Mq.A0 = QA0

    M.append(Mq)

# Second dataset: wavelength=8 Angstrom
for i in range(len(q_8A)):
    x = hw_8A[idx_8A]
    data = sqw_8A[idx_8A, i]
    error = err_8A[idx_8A, i]
    resol = res_8A[idx_8A, i]

    # Select only valid data (error = -1 for Q, w points not accessible)
    valid = np.where(error > 0.0)
    if len(valid[1]) != len(x):
        print(i, "truncate to make vectors symmetric with respect to max")

    x = x[valid[1]]
    data = data[valid]
    error = error[valid]
    resol = resol[valid]

    Mq = bmp.Curve(model_convol,
                   x,
                   data,
                   error,
                   q=q_8A[i],
                   scale=35,
                   center=0.0,
                   A0=0.0,
                   A1=0.9,
                   hwhm1=0.05,
                   hwhm2=0.3, 
                   resolution=resol)

    # Fitted parameters
    Mq.scale.range(0.1, 40)
    Mq.center.range(-0.1, 0.1)
    Mq.A0.range(0, 0.05)
    Mq.A1.range(0, 1)
    Mq.hwhm1.range(0, 0.5)
    Mq.hwhm2.range(0, 3)
    
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
    print(k, ":", format_uncertainty(v, dv))



plt.show()

