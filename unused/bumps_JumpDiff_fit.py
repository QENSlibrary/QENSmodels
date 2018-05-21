from __future__ import print_function

import h5py
import numpy as np
import matplotlib.pyplot as plt
from bumps.names import *
from scipy.integrate import simps

import qens_models 

'''

Example of fit to model generated data corresponding to a 
Jump Translational diffusion model with self-diffusion 
coefficient = 0.145 AA^2*meV and residence time 1.0 meV^-1.

The model is convoluted with a Gaussian resolution function 
of FWHM = 0.1 meV, centered randomly in the range [-0.01, +0.01] meV.

Finally the data are sampled randomly from a Poisson distribution.

The data do not have a background. Trying to fit the background 
makes the Levenberg-Marquardt algorithm to fail! With other 
algorithms the result is not so bad, but it is always worse
than keeping the background fixed at zero.

Usage examples (on Windows) and results: 

   python -m bumps.cli bumps_JumpDiff_fit.py --fit=lm --store=QENS 
   
      Uses standard Levenberg-Marquardt optimizer
      overall chisq = 0.96
      D = 0.139 
      Residence time = 0.93 

   python -m bumps.cli bumps_JumpDiff_fit.py --fit=amoeba --store=QENS 
   
      Uses Nelder-Mead Simplex optimizer
      overall chisq = 1.09
      D = 0.136
      Residence time = 0.86 

   python -m bumps.cli bumps_JumpDiff_fit.py --fit=newton --store=QENS 
   
      Uses Quasi-Newton BFGS optimizer
      overall chisq = 391
      D = 0.083 
      Residence time = 0.50 
 
   python -m bumps.cli bumps_JumpDiff_fit.py --fit=de --store=QENS 
   
      Uses Differential Evolution optimizer
      overall chisq = 0.96
      D = 0.139 
      Residence time = 0.94 
 
   python -m bumps.cli bumps_JumpDiff_fit.py --fit=dream --store=QENS 
   
      Uses DREAM (Markov chain) optimizer
      overall chisq = 3.9
      D = 0.133 
      Residence time = 0.99
          
'''
path_to_data = './data/'

# Read sample

f = h5py.File(path_to_data + 'JumpDiff_Sample.hdf', 'r')
hw = f['entry1']['data1']['X'][:]
q = f['entry1']['data1']['Y'][:]
sqw = np.transpose(f['entry1']['data1']['DATA'][:])
err = np.transpose(f['entry1']['data1']['errors'][:])
f.close()

# Read resolution

f = h5py.File(path_to_data + 'JumpDiff_Resol.hdf', 'r')
res = np.transpose(f['entry1']['data1']['DATA'][:])
f.close()

# Force resolution function to have unit area

for i in range(len(q)):
    area = simps(res[:,i], hw)
    res[:,i] /= area    

# Fit

M = []

for i in range(len(q)):
    
    # Model = Jump Translational Diffusion    
    Mq = Curve(qens_models.sqwJumpTranslationalDiffusion, hw, sqw[:,i], 
               err[:,i], q=q[i], scale=1000, center=0.0, D=0.1, resTime=0.5,
               background=0, resolution=res[:,i])
               
    Mq.scale.range(0, 1e5)
    Mq.center.range(-0.1,0.1)
    Mq.D.range(0,1)
    Mq.resTime.range(0,5)
    #Mq.background.range(0,10)

    # Q-independent parameters
    if i == 0:
        QD = Mq.D
        QT = Mq.resTime
    else:
        Mq.D = QD
        Mq.resTime = QT
        
    M.append(Mq)

problem = FitProblem(M)