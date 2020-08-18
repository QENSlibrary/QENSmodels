#!/usr/bin/env python
# coding: utf-8

# Imported required libraries
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

# Resolution
# Wavelength 5 Angstrom
with h5py.File(path_to_data + 'V_273K_5A.hdf', 'r') as f:
    res_5A = np.transpose(f['entry1']['data1']['DATA'][:])

# Force resolution function to have unit area
# Wavelength 5 Angstrom
for i in range(len(q_5A)):
    area = simps(res_5A[:, i], hw_5A)
    res_5A[:, i] /= area

# Fit range -1 to +1 meV
idx_5A = np.where(np.logical_and(hw_5A > -1.0, hw_5A < 1.0))


# Fitting model
def model_convol(x, q, scale=1, center=0, hwhm=1, radius=1, DR=1, resolution=None):
    model = QENSmodels.lorentzian(x,
                                  scale,
                                  center,
                                  hwhm) 
    model += QENSmodels.sqwIsotropicRotationalDiffusion(x,
                                                        q,
                                                        scale,
                                                        center,
                                                        radius,
                                                        DR)
    return np.convolve(model, resolution / resolution.sum(), mode='same')


print(f"""At 5 Angstroms, the names and units of `w` (`x`axis) and `q` are: 
{str(unit_w5A[0], 'utf-8')} and {str(unit_q5A[0], 'utf-8')}, respectively.""")


# Fit
M = []

for i in range(len(q_5A)):

    x = hw_5A[idx_5A]
    data = sqw_5A[idx_5A, i]
    error = err_5A[idx_5A, i]
    resol = res_5A[idx_5A, i]

    # Select only valid data (error = -1 for Q, w points not accessible)
    valid = np.where(error > 0.0)
    x = x[valid[1]]
    data = data[valid]
    error = error[valid]
    resol = resol[valid]

    # model
    Mq = bmp.Curve(model_convol, x, data, error, q=q_5A[i], scale=15,
                   center=0.0, hwhm=0.1, radius=1.1, DR=1., resolution=resol)

    # Fitted parameters
    Mq.scale.range(0, 1e2)
    Mq.center.range(-0.1, 0.1)
    Mq.hwhm.range(0., 1)
    Mq.radius.range(0.9, 1.1)
    Mq.DR.range(0.01, 5)

    # Q-independent parameters
    if i == 0:
        Qhwhm = Mq.hwhm
        QR = Mq.radius
        QDR = Mq.DR
    else:
        Mq.hwhm = Qhwhm
        Mq.radius = QR
        Mq.DR = QDR

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

