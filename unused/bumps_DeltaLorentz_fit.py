from __future__ import print_function

import h5py
import numpy as np
from bumps.names import *
from scipy.integrate import simps

import qens_models 

'''

Example of fit to model generated data corresponding to a 
delta representing a fraction p of fixed atoms and a
Lorentzian corresponding to a Brownian Translational
diffusion model for the remaining (1-p) atoms. 
Parameters used: p = 0.3 and D = 0.145 AA^2*meV.

The model is convoluted with a Gaussian resolution function 
of FWHM = 0.1 meV, centered randomly in the range [-0.01, +0.01] meV.

Finally the data are sampled randomly from a Poisson distribution.

No background.

The data are fitted with a general model of a delta + a
Lorentzian, so the fitted parameters are not p and D, but
p and a Q-dependent HWHM.

Usage examples (on Windows) and results: 

   python -m bumps.cli bumps_DeltaLorentz_fit.py --fit=lm --store=QENS 
   
      Uses standard Levenberg-Marquardt optimizer
      overall chisq = 0.98
      A0 = 0.30 
      HWHM = [0.005, 0.021, 0.049, 0.085, 0.137, 0.192, 0.268, 0.364, 0.449, 0.553] 
      Fitting HWHM = D*Q^2 --> D = 0.138 

   python -m bumps.cli bumps_DeltaLorentz_fit.py --fit=amoeba --store=QENS 
   
      Uses Nelder-Mead Simplex optimizer
      overall chisq = 8.5
      A0 = 0.35
      HWHM = [0.053, 0.099, 0.117, 0.165, 0.131, 0.210, 0.265, 0.230, 0.217, 0.166] 
      Fitting HWHM = D*Q^2 --> D = 0.076 

   python -m bumps.cli bumps_DeltaLorentz_fit.py --fit=newton --store=QENS 
   
      Uses Quasi-Newton BFGS optimizer
      overall chisq = 711
      A0 = 0.23
      HWHM = [0, 0.016, 0.056, 0.062, 0.091, 0.109, 0.121, 0.134, 0.138, 0.138] 
      Fitting HWHM = D*Q^2 --> D = 0.047
 
   python -m bumps.cli bumps_DeltaLorentz_fit.py --fit=de --store=QENS 
   
      Uses Differential Evolution optimizer
      overall chisq = 3.6 (but only 1st spectrum badly fitted)
      A0 = 0.31
      HWHM = [2.0, 0.022, 0.049, 0.088, 0.139, 0.195, 0.271, 0.367, 0.451, 0.566] 
      Fitting HWHM (excluding 1st point) = D*Q^2 --> D = 0.140
 
   python -m bumps.cli bumps_DeltaLorentz_fit.py --fit=dream --store=QENS 
   
      Uses DREAM (Markov chain) optimizer
      overall chisq = 26.8
      A0 = 0.52
      HWHM = [0.006, 0.010, 0.016, 0.045, 0.033, 0.124, 0.050, 0.030, 0.184, 0.067] 
      Fitting HWHM = D*Q^2 --> D = 0.032

'''
path_to_data = '../examples/data/'

# Read sample

f = h5py.File(path_to_data + 'DeltaBrownianDiff_Sample.hdf', 'r')
hw = f['entry1']['data1']['X'][:]
q = f['entry1']['data1']['Y'][:]
sqw = np.transpose(f['entry1']['data1']['DATA'][:])
err = np.transpose(f['entry1']['data1']['errors'][:])
f.close()

# Read resolution
f = h5py.File(path_to_data + 'DeltaBrownianDiff_Resol.hdf', 'r')
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
    Mq = Curve(qens_models.sqwDeltaLorentz, hw, sqw[:,i],
               err[:,i], q=q[i], scale=1000, center=0.0, A0=0.5, hwhm=0.01,
               background=0, resolution=res[:,i])

    Mq.scale.range(0, 1e5)
    Mq.center.range(-0.1, 0.1)
    Mq.A0.range(0, 1)
    Mq.hwhm.range(0, 2)
    # Mq.background.range(0, 10)

    # Q-independent parameters
    if i == 0:
        QA0 = Mq.A0
    else:
        Mq.A0 = QA0
        
    M.append(Mq)

problem = FitProblem(M)