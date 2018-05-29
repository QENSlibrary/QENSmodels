from __future__ import print_function

import h5py
import numpy as np
import matplotlib.pyplot as plt
from bumps.names import *
from scipy.integrate import simps

import qens_models 

'''

Example of fit of two sets of water data measured at IN5 (ILL)
using two different wavelengths.
Reference: J. Qvist, H. Schober and B. Halle, J. Chem. Phys. 134, 144508 (2011)

Usage example: 

   python -m bumps.cli bumps_waterIN5_fit1.py --fit=dream --samples=1e5 --burn=1e3 --store=QENS1 
 
'''

# Data
path_to_data = '../examples/data/'

f = h5py.File(path_to_data + 'H2O_293K_5A.hdf', 'r')
hw_5A = f['entry1']['data1']['X'][:]
q_5A = f['entry1']['data1']['Y'][:]
sqw_5A = np.transpose(f['entry1']['data1']['DATA'][:])
err_5A = np.transpose(f['entry1']['data1']['errors'][:])
f.close()

f = h5py.File(path_to_data +'H2O_293K_8A.hdf', 'r')
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
    area = simps(res_5A[:,i], hw_5A)
    res_5A[:,i] /= area    

for i in range(len(q_8A)):
    area = simps(res_8A[:,i], hw_8A)
    res_8A[:,i] /= area    

# Fit range -1 to +1 meV
idx_5A = np.where(np.logical_and(hw_5A > -1.0, hw_5A < 1.0))
idx_8A = np.where(np.logical_and(hw_8A > -1.0, hw_8A < 1.0))


# Fit

M = []

for i in range(len(q_5A)):

    x = hw_5A[idx_5A]
    data = sqw_5A[idx_5A, i]
    error = err_5A[idx_5A, i]
    resol = res_5A[idx_5A,i]
        
    # Select only valid data (error = -1 for Q, w points not accessible)
    valid = np.where(error > 0.0)
    x = x[valid[1]]
    data = data[valid]
    error = error[valid]
    resol = resol[valid]
    
    # Teixeira model
    Mq = Curve(qens_models.sqwDeltaTwoLorentz, x, data, error, q=q_5A[i],
               scale=20, center=0.0, A0=0.0, A1=0.9, hwhm1=0.05, hwhm2=0.3, 
               resolution=resol)
    
    # Fitted parameters    
    Mq.scale.range(1.e-12, 20)
    Mq.center.range(-0.1, 0.1)
    Mq.A0.range(0, 0.05)
    Mq.A1.range(0, 1)
    Mq.hwhm1.range(0, 0.5)
    Mq.hwhm2.range(0, 3)
    Mq.background.range(0, 1)
    
    # Q-independent parameters
    if i == 0:
        QA0 = Mq.A0
    else:
        Mq.A0 = QA0
        
    M.append(Mq)

for i in range(len(q_8A)):

    x = hw_8A[idx_8A]
    data = sqw_8A[idx_8A, i]
    error = err_8A[idx_8A, i]
    resol = res_8A[idx_8A,i]
        
    # Select only valid data (error = -1 for Q, w points not accessible)
    valid = np.where(error > 0.0)
    x = x[valid[1]]
    data = data[valid]
    error = error[valid]
    resol = resol[valid]
    
    # Teixeira model    
    Mq = Curve(qens_models.sqwDeltaTwoLorentz, x, data, error, q=q_8A[i],
               scale=35, center=0.0, A0=0.0, A1=0.9, hwhm1=0.05, hwhm2=0.3, 
               resolution=resol)

    # Fitted parameters    
    Mq.scale.range(0.1, 40)
    Mq.center.range(-0.1, 0.1)
    Mq.A0.range(0, 0.05)
    Mq.A1.range(0, 1)
    Mq.hwhm1.range(0, 0.5)
    Mq.hwhm2.range(0, 3)
    Mq.background.range(0, 1)
    
    # Q-independent parameters
    if i == 0:
        QA0 = Mq.A0
    else:
        Mq.A0 = QA0

    M.append(Mq)

problem = FitProblem(M)
