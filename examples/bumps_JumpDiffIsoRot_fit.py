from __future__ import print_function

import h5py
import numpy as np
import matplotlib.pyplot as plt
from bumps.names import *
from scipy.integrate import simps

import qens_models 

'''

Example of fit to model generated data corresponding to a 
combination of a jump translational diffusion with an
isotropic rotational diffusion. 
Parameters used: D = 0.145 AA^2*meV, Residence time = 1 meV^-1,
                 Radius = 1.10 AA and D_rot = 0.125 meV.
                 
The model is convoluted with a Gaussian resolution function 
of FWHM = 0.1 meV, centered randomly in the range [-0.01, +0.01] meV.

Finally the data are sampled randomly from a Poisson distribution.

No background.

Usage examples (on Windows) and results:

   python -m bumps.cli bumps_JumpDiffIsoRot_fit.py --fit=lm --store=QENS 
   
      Uses standard Levenberg-Marquardt optimizer
      overal chisq = 1.1
      D = 0.142
      Residence time = 0.73 
      R = 1.03
      D_rot = 0.125

   python -m bumps.cli bumps_JumpDiffIsoRot_fit.py --fit=amoeba --store=QENS 
   
      Uses Nelder-Mead Simplex optimizer
      overal chisq = 1.13
      D = 0.143
      Residence time = 0.74
      R = 0.95
      D_rot = 0.157

   python -m bumps.cli bumps_JumpDiffIsoRot_fit.py --fit=newton --store=QENS 
   
      Uses Quasi-Newton BFGS optimizer
      overal chisq = 138
      D = 0.089
      Residence time = 0.51 
      R = 0.99
      D_rot = 0
 
   python -m bumps.cli bumps_JumpDiffIsoRot_fit.py --fit=de --store=QENS 
   
      Uses Differential Evolution optimizer
      overal chisq = 1.10
      D = 0.081
      Residence time = 1.19 
      R = 2.32
      D_rot = 0.037
 
   python -m bumps.cli bumps_JumpDiffIsoRot_fit.py --fit=dream --store=QENS 
   
      Uses DREAM (Markov chain) optimizer
      overal chisq = 5.3
      D = 0.104
      Residence time = 0.57
      R = 0.93
      D_rot = 0.270
 
   python -m bumps.cli bumps_JumpDiffIsoRot_fit.py --fit=dream --samples=1e5 --burn=1e3 --store=QENS 
   
      Uses DREAM (Markov chain) optimizer
      overal chisq = 1.11
      D = 0.154
      Residence time = 0.57 
      R = 0.82
      D_rot = 0.168

'''

# Read sample

f = h5py.File('JumpDiffIsoRot_Sample.hdf', 'r')
hw = f['entry1']['data1']['X'][:]
q = f['entry1']['data1']['Y'][:]
sqw = np.transpose(f['entry1']['data1']['DATA'][:])
err = np.transpose(f['entry1']['data1']['errors'][:])
f.close()

# Read resolution

f = h5py.File('JumpDiffIsoRot_Resol.hdf', 'r')
res = np.transpose(f['entry1']['data1']['DATA'][:])
f.close()

# Force resolution function to have unit area

for i in range(len(q)):
    area = simps(res[:,i], hw)
    res[:,i] /= area    

# Fit

M = []
#I0 = np.array([111, 155, 229, 333, 484, 677, 905, 1176, 1475, 1824])

for i in range(len(q)):
    
    # Model    
    Mq = Curve(qens_models.sqwWaterTeixeira, hw, sqw[:,i], 
               err[:,i], q=q[i], scale=100., center=0.0, D=0.1,
               resTime=0.5, radius=1., DR=0.1,
               background=0, resolution=res[:,i])
               
    Mq.scale.range(0, 1e5)
    Mq.center.range(-0.1,0.1)
    Mq.D.range(0,1)
    Mq.resTime.range(0,5)
    Mq.radius.range(0,3)
    Mq.DR.range(0,2)
    #Mq.background.range(0,10)

    # Q-independent parameters
    if i == 0:
        QD = Mq.D
        QT = Mq.resTime
        QR = Mq.radius
        QDR = Mq.DR
    else:
        Mq.D = QD
        Mq.resTime = QT
        Mq.radius = QR
        Mq.DR = QDR
        
    M.append(Mq)

problem = FitProblem(M)