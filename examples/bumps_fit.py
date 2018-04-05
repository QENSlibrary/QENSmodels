from __future__ import print_function

import h5py
import numpy as np
import matplotlib.pyplot as plt
from bumps.names import *
from scipy.integrate import simps

import qens_models 

'''
Usage example: python -m bumps.cli bumps_fit.py --fit=lm --steps=1000 --store=QENS 
'''

# Data

f = h5py.File('H2O_293K_5A.hdf', 'r')
hw_5A = f['entry1']['data1']['X'][:]
q_5A = f['entry1']['data1']['Y'][:]
sqw_5A = np.transpose(f['entry1']['data1']['DATA'][:])
err_5A = np.transpose(f['entry1']['data1']['errors'][:])
f.close()

f = h5py.File('H2O_293K_8A.hdf', 'r')
hw_8A = f['entry1']['data1']['X'][:]
q_8A = f['entry1']['data1']['Y'][:]
sqw_8A = np.transpose(f['entry1']['data1']['DATA'][:])
err_8A = np.transpose(f['entry1']['data1']['errors'][:])
f.close()

# Resolution

f = h5py.File('V_273K_5A.hdf', 'r')
res_5A = np.transpose(f['entry1']['data1']['DATA'][:])
f.close()

f = h5py.File('V_273K_8A.hdf', 'r')
res_8A = np.transpose(f['entry1']['data1']['DATA'][:])
f.close()

# Force resoltion function to have unit area

for i in range(len(q_5A)):
    area = simps(res_5A[:,i], hw_5A)
    res_5A[:,i] /= area    

for i in range(len(q_8A)):
    area = simps(res_8A[:,i], hw_8A)
    res_8A[:,i] /= area    

#import pdb; pdb.set_trace()

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
        
    # Single lorentzian    
    # Mq = Curve(qens_models.lorentz, x, data, error, 
               # scale=20, center=0.0, hwhm=0.1, resolution=resol)
    # Mq.scale.range(0, 1e2)
    # Mq.center.range(-0.1,0.1)
    # Mq.hwhm.range(0,2)
    # M.append(Mq)
    
    # Two lorentzians    
    # Mq = Curve(qens_models.twoLorentz, x, data, error, 
               # scale1=10, center1=0.0, hwhm1=0.1, 
               # scale2=10, center2=0.0, hwhm2=1.0,
               # resolution=resol)
    # Mq.scale1.range(0, 1e2)
    # Mq.center1.range(-0.1,0.1)
    # Mq.hwhm1.range(0,2)
    # Mq.scale2.range(0, 1e2)
    # Mq.center2.range(-0.1,0.1)
    # Mq.hwhm2.range(0,5)
    # M.append(Mq)
    
    # Jump diffusion    
    # Mq = Curve(qens_models.jumpDiffusion, x, data, error, 
               # scale=20, center=0.0, D=0.1, Q=q_5A[i], resolution=resol)
    # Mq.scale.range(0, 1e2)
    # Mq.center.range(-0.1,0.1)
    # Mq.D.range(0,1)
    # if i == 0:
        # DDD = Mq.D
    # else:
        # Mq.D = DDD    
    # M.append(Mq)
    
    # Teixeira model    
    Mq = Curve(qens_models.waterTeixeira, x, data, error, 
               scale=20, center=0.0, D=0.1, radius=0.98, DR=0.5, Q=q_5A[i], resolution=resol)
    Mq.scale.range(0, 1e2)
    Mq.center.range(-0.1,0.1)
    Mq.D.range(0,1)
    Mq.radius.range(0.9, 1.1)
    Mq.DR.range(0,5)
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
    resol = res_8A[idx_8A,i]
        
    # Select only valid data (error = -1 for Q, w points not accessible)
    valid = np.where(error > 0.0)
    x = x[valid[1]]
    data = data[valid]
    error = error[valid]
    resol = resol[valid]
    
    # Teixeira model    
    Mq = Curve(qens_models.waterTeixeira, x, data, error, 
               scale=20, center=0.0, D=0.1, radius=0.98, DR=0.5, Q=q_8A[i], resolution=resol)
    Mq.scale.range(0, 1e2)
    Mq.center.range(-0.1,0.1)
    Mq.D.range(0,1)
    Mq.radius.range(0.9, 1.1)
    Mq.DR.range(0,5)
    # Q-independent parameters set with 5A data
    Mq.D = QD
    Mq.radius = QR
    Mq.DR = QDR        
    M.append(Mq)

    
problem = FitProblem(M)