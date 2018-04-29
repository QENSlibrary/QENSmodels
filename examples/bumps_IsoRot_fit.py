from __future__ import print_function

import h5py
import numpy as np
import matplotlib.pyplot as plt
from bumps.names import *
from scipy.integrate import simps

import qens_models 

'''

Example of fit to model generated data corresponding to a 
isotropic rotational diffusion model. 
Parameters used: Radius = 1.10 AA and D_rot = 0.125 meV.

The model is convoluted with a Gaussian resolution function 
of FWHM = 0.1 meV, centered randomly in the range [-0.01, +0.01] meV.

Finally the data are sampled randomly from a Poisson distribution.

No background.

Usage examples (on Windows) and results: 

   python -m bumps.cli bumps_IsoRot_fit.py --fit=lm --store=QENS 
   
      Uses standard Levenberg-Marquardt optimizer
      overal chisq = 1.14
      R = 1.08
      D_rot = 0.120 

   python -m bumps.cli bumps_IsoRot_fit.py --fit=amoeba --store=QENS 
   
      Uses Nelder-Mead Simplex optimizer
      overal chisq = 3.9
      R = 0.95 
      D_rot = 0.222

   python -m bumps.cli bumps_IsoRot_fit.py --fit=newton --store=QENS 
   
      Uses Quasi-Newton BFGS optimizer
      overal chisq = 711
      R = 1.55
      D_rot = 2.00
 
   python -m bumps.cli bumps_IsoRot_fit.py --fit=de --store=QENS 
   
      Uses Differential Evolution optimizer
      overal chisq = 27.2
      R = 2.50
      D_rot = 2.00
 
   python -m bumps.cli bumps_IsoRot_fit.py --fit=dream --store=QENS 
   
      Uses DREAM (Markov chain) optimizer
      overal chisq = 7.3
      R = 1.05
      D_rot = 0.126 

'''

# Read sample

f = h5py.File('IsoRot_Sample.hdf', 'r')
hw = f['entry1']['data1']['X'][:]
q = f['entry1']['data1']['Y'][:]
sqw = np.transpose(f['entry1']['data1']['DATA'][:])
err = np.transpose(f['entry1']['data1']['errors'][:])
f.close()

# Read resolution

f = h5py.File('IsoRot_Resol.hdf', 'r')
res = np.transpose(f['entry1']['data1']['DATA'][:])
f.close()

# Force resolution function to have unit area

for i in range(len(q)):
    area = simps(res[:,i], hw)
    res[:,i] /= area    

# Fit

M = []

for i in range(len(q)):
    
    # Model    
    Mq = Curve(qens_models.sqwIsotropicRotationalDiffusion, hw, sqw[:,i], 
               err[:,i], q=q[i], scale=1000, center=0.0, radius=1.0, DR=0.1,
               background=0, resolution=res[:,i])
               
    Mq.scale.range(0, 1e5)
    Mq.center.range(-0.1,0.1)
    Mq.radius.range(0,3)
    Mq.DR.range(0,2)
    #Mq.background.range(0,10)

    # Q-independent parameters
    if i == 0:
        QR = Mq.radius
        QDR = Mq.DR
    else:
        Mq.radius = QR
        Mq.DR = QDR
        
    M.append(Mq)

problem = FitProblem(M)