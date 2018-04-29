from __future__ import print_function

import h5py
import numpy as np
import matplotlib.pyplot as plt
from bumps.names import *
from scipy.integrate import simps

import qens_models 

'''

Example of fit to model generated data corresponding to a 
Brownian Translational diffusion model with self-diffusion 
coefficient = 0.145 AA^2*meV.

The model is convoluted with a Gaussian resolution function 
of FWHM = 0.1 meV, centered randomly in the range [-0.01, +0.01] meV.

Finally the data are sampled randomly from a Poisson distribution.

The data do not have a background. Trying to fit the background 
makes the Levenberg-Marquardt algorithm to fail! With other 
algorithms the result is not so bad, but it is always worse
than keeping the background fixed at zero.

Usage examples (on Windows) and results: 

   python -m bumps.cli bumps_BrownianDiff_fit.py --fit=lm --store=QENS 
   
      Uses standard Levenberg-Marquardt optimizer
      chisq = [0.40, 0.65, 0.94, 1.20, 1.27, 1.01, 1.09, 1.10, 1.09, 1.17]
      center = [0.010, -0.010, -0.010, 0, 0, 0.010, 0.008, 0.010, 0, 0]
      scale = [111, 155, 229, 333, 484, 677, 905, 1176, 1475, 1824]
      overall chisq = 1.0
      D = 0.144

   python -m bumps.cli bumps_BrownianDiff_fit.py --fit=amoeba --store=QENS 
   
      Uses Nelder-Mead Simplex optimizer
      chisq = [0.52, 1.75, 1.04, 1.41, 1.44, 1.22, 1.39, 1.79, 1.11, 1.23]
      center = [0.010, 0.010, 0.003, 0.004, 0, 0, 0.009, 0.012, -0.003, -0.012]
      scale = [104, 161, 231, 321, 502, 700, 940, 1118, 1481, 1833]
      overall chisq = 1.3
      D = 0.146

   python -m bumps.cli bumps_BrownianDiff_fit.py --fit=newton --store=QENS 
   
      Uses Quasi-Newton BFGS optimizer
      chisq = [1418, 1140, 663, 329, 136, 40, 5.1, 7.0, 32, 74]
      center = [0.015, 0.001, -0.025, 0, 0, -0.003, 0.001, 0.001, 0, 0]
      scale = [1000, 1000, 1000, 1000, 1000, 1000, 1000, 1000, 1000, 1000]
      overall chisq = 387
      D = 0.131
 
   python -m bumps.cli bumps_BrownianDiff_fit.py --fit=de --store=QENS 
   
      Uses Differential Evolution optimizer
      chisq = [0.40, 0.65, 0.94, 1.20, 1.27, 1.01, 1.09, 1.10, 1.09, 1.16]
      center = [0.010, -0.010, -0.011, 0, 0, 0.011, 0.008, 0.011, 0.001, 0.011]
      scale = [111, 155, 229, 333, 484, 676, 905, 1176, 1475, 1824]
      overall chisq = 1.0
      D = 0.144
 
   python -m bumps.cli bumps_BrownianDiff_fit.py --fit=dream --store=QENS 
   
      Uses DREAM (Markov chain) optimizer
      chisq = [2.3, 6.8, 2.5, 5.5, 1.4, 6.2, 1.7, 8.2, 11, 2.1]
      center = [0.017, 0, -0.005, 0.006, -0.001, -0.011, -0.005, 0.005, 0.019, -0.006]
      scale = [91, 94, 265, 407, 481, 555, 887, 978, 1204, 1850]
      overall chisq = 4.8
      D = 0.136

'''

# Read sample

f = h5py.File('BrownianDiff_Sample.hdf', 'r')
hw = f['entry1']['data1']['X'][:]
q = f['entry1']['data1']['Y'][:]
sqw = np.transpose(f['entry1']['data1']['DATA'][:])
err = np.transpose(f['entry1']['data1']['errors'][:])
f.close()

# Read resolution

f = h5py.File('BrownianDiff_Resol.hdf', 'r')
res = np.transpose(f['entry1']['data1']['DATA'][:])
f.close()

# Force resolution function to have unit area

for i in range(len(q)):
    area = simps(res[:,i], hw)
    res[:,i] /= area    

# Fit

M = []

for i in range(len(q)):
    
    # Model = Brownian Translational Diffusion    
    Mq = Curve(qens_models.sqwBrownianTranslationalDiffusion, hw, sqw[:,i], 
               err[:,i], q=q[i], scale=1000, center=0.0, D=0.1, background=0, 
               resolution=res[:,i])
               
    Mq.scale.range(0, 1e5)
    Mq.center.range(-0.1,0.1)
    Mq.D.range(0,1)
    #Mq.background.range(0,10)

    # Q-independent parameters
    if i == 0:
        QD = Mq.D
    else:
        Mq.D = QD
        
    M.append(Mq)

problem = FitProblem(M)