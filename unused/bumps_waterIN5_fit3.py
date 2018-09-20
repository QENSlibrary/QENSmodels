from __future__ import print_function

import h5py
import numpy as np
import os
import matplotlib.pyplot as plt
from bumps.names import *
from scipy.integrate import simps

import QENSmodels

'''

Example of fit of two sets of water data measured at IN5 (ILL)
using two different wavelengths.
Reference: J. Qvist, H. Schober and B. Halle, J. Chem. Phys. 134, 144508 (2011)

The fitting model is the sum of sqwBrownianTranslationalDiffusion 
and sqwIsotropicRotationalDiffusion convoluted by the resolution function

Usage example: 

   python -m bumps.cli bumps_waterIN5_fit3.py --fit=lm --store=QENS3 

'''
# Path to where the data for the examples are (/QENSmodels/examples/data)
path_to_data = os.path.join(os.getcwd(), 'data/')

# Data

f = h5py.File(path_to_data + 'H2O_293K_5A.hdf', 'r')
hw_5A = f['entry1']['data1']['X'][:]
q_5A = f['entry1']['data1']['Y'][:]
sqw_5A = np.transpose(f['entry1']['data1']['DATA'][:])
err_5A = np.transpose(f['entry1']['data1']['errors'][:])
f.close()

f = h5py.File(path_to_data + 'H2O_293K_8A.hdf', 'r')
hw_8A = f['entry1']['data1']['X'][:]
q_8A = f['entry1']['data1']['Y'][:]
sqw_8A = np.transpose(f['entry1']['data1']['DATA'][:])
err_8A = np.transpose(f['entry1']['data1']['errors'][:])
f.close()

# Resolution

f = h5py.File(path_to_data + 'V_273K_5A.hdf', 'r')
res_5A = np.transpose(f['entry1']['data1']['DATA'][:])
f.close()

f = h5py.File(path_to_data + 'V_273K_8A.hdf', 'r')
res_8A = np.transpose(f['entry1']['data1']['DATA'][:])
f.close()

# Force resolution function to have unit area

for i in range(len(q_5A)):
    area = simps(res_5A[:, i], hw_5A)
    res_5A[:, i] /= area

for i in range(len(q_8A)):
    area = simps(res_8A[:, i], hw_8A)
    res_8A[:, i] /= area

# Fit range -1 to +1 meV
idx_5A = np.where(np.logical_and(hw_5A > -1.0, hw_5A < 1.0))
idx_8A = np.where(np.logical_and(hw_8A > -1.0, hw_8A < 1.0))

# Fit

M = []


def composite_model(w, q, scale=1., center=0., D=1., radius=1., DR=1.,
                    resolution=None):
    model = QENSmodels.sqwBrownianTranslationalDiffusion(w, q, scale, center, D)\
           + QENSmodels.sqwIsotropicRotationalDiffusion(w, q, scale, center, radius, DR)
    return np.convolve(model, resolution/resolution.sum(), mode='same')


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

    # Teixeira model

    Mq = Curve(composite_model, x, data, error, q=q_5A[i], scale=20,
               center=0.0, D=0.1, radius=0.98, DR=0.5, resolution=resol)

    # Fitted parameters
    Mq.scale.range(0, 1e2)
    Mq.center.range(-0.1, 0.1)
    Mq.D.range(0., 1)
    Mq.radius.range(0.9, 1.1)
    Mq.DR.range(0, 5)

    # Q-independent parameters
    if i == 0:
        QD = Mq.D
        QR = Mq.radius
        QDR = Mq.DR
    else:
        Mq.D = QD
        Mq.radius = QR
        Mq.DR = QDR

    M.append(Mq)

for i in range(len(q_8A)):
    x = hw_8A[idx_8A]
    data = sqw_8A[idx_8A, i]
    error = err_8A[idx_8A, i]
    resol = res_8A[idx_8A, i]

    # Select only valid data (error = -1 for Q, w points not accessible)
    valid = np.where(error > 0.0)
    x = x[valid[1]]
    data = data[valid]
    error = error[valid]
    resol = resol[valid]

    # Teixeira model
    Mq = Curve(composite_model, x, data, error, q=q_8A[i], scale=20,
               center=0.0, D=0.1, radius=0.98, DR=0.5, resolution=resol)

    # Fitted parameters
    Mq.scale.range(0, 1e2)
    Mq.center.range(-0.1, 0.1)
    Mq.D.range(0.0, 1)
    Mq.radius.range(0.9, 1.1)
    Mq.DR.range(0, 5)

    # Q-independent parameters set with 5A data
    Mq.D = QD
    Mq.radius = QR
    Mq.DR = QDR

    M.append(Mq)

problem = FitProblem(M)
