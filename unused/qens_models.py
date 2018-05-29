import numpy as np
from scipy.special import jn 

'''
First tests for a library of QENS models.

Models used with:

  - explore_models.py: Shows EISF and HWHM for a given model and input parameters.
  
  - test_models.py: Shows S(Q,w) for a given model and input parameters. 
  
  - bumps_MODEL_fit.py: Several examples of fitting "real" data using bumps and the
                        models here.  

To do:

 - Background and convolution with resolution should not be part of the model, 
   but I need it at the moment to use the Curve object in bumps. 
   
 - Manage loss of intensity at edges after convolution.

 - Examples with other fitting packages. 
 
 - Validation of input and output, handling of divisions by zeros, NaNs, etc.
'''

# Mathematical functions: F(x) 
# Other input parameters are single valued params, not vectors

def delta(x, scale, center):
    model = np.zeros(x.size)
    idx = np.argmin(np.abs(x - center))
    dx = 0.5 * np.abs(x[idx+1] - x[idx-1])
    model[idx] = scale / dx
    return model

def lorentz(x, scale, center, hwhm):
    if hwhm == 0:
        model = delta(x, scale, center)
    else:
        model = scale * hwhm / ((x-center)**2 + hwhm**2) / np.pi 
    return model

  
def gaussian(x, scale, center, sigma):
    if sigma == 0:
        model = delta(x, scale, center)
    else:
        model = scale * np.exp(-(x-center)**2/(2*sigma**2)) / (sigma*np.sqrt(2*np.pi))
    return model

####

# Lorentzian models: Returns hwhm, eisf, and qisf

def hwhmBrownianTranslationalDiffusion(q, D):
    eisf = np.zeros(q.size)
    qisf = np.ones(q.size)
    hwhm = D*q**2
    # Force hwhm to be numpy array, even if single value
    hwhm = np.asarray(hwhm, dtype=np.float32)
    hwhm = np.reshape(hwhm, hwhm.size)
    return hwhm, eisf, qisf

    
def hwhmJumpTranslationalDiffusion(q, D, resTime):
    eisf = np.zeros(q.size)
    qisf = np.ones(q.size)
    hwhm = D*q**2 / (1.0 + resTime*D*q**2)
    # Force hwhm to be numpy array, even if single value
    hwhm = np.asarray(hwhm, dtype=np.float32)
    hwhm = np.reshape(hwhm, hwhm.size)
    return hwhm, eisf, qisf
 
 
def hwhmIsotropicRotationalDiffusion(q, radius, DR):
    eisf = np.zeros(q.size)
    numberLorentz = 6
    qisf = np.zeros((q.size, numberLorentz))
    hwhm = np.zeros((q.size, numberLorentz))
    jl = np.zeros((q.size, numberLorentz))
    arg = q * radius
    idx = np.argwhere(arg == 0)
    for i in range(numberLorentz):  
        jl[:,i] = np.sqrt(np.pi/2/arg) * jn(i+0.5, arg) #to solve warnings for arg=0
        hwhm[:,i] = np.repeat(i * (i+1) * DR, q.size)
        if idx.size > 0:
           if i == 0:
               jl[idx,i] = 1.0
           else:
               jl[idx,i] = 0.0
    eisf = jl[:,0]**2 
    for i in range(1,numberLorentz):
        qisf[:,i] = (2*i+1) * jl[:,i]**2
    return hwhm, eisf, qisf

    
####

# S(Q,w) models: Returns I(Q,w)

def sqwDeltaLorentz(w, q, scale, center, A0, hwhm, background, resolution=None):

    # Model = A0*delta + (1-A0)*Lorentz(Gamma)

    # Input validation
    q = np.asarray(q, dtype=np.float32)
    
    # Create output array
    sqw = np.zeros((q.size, w.size))

    # Model
    if q.size > 1:
        for i in range(q.size):
            sqw[i,:] = A0[i] * delta(w, scale, center)
            sqw[i,:] += (1-A0[i]) * lorentz(w, scale, center, hwhm[i])
    else:
        sqw[0,:] = A0 * delta(w, scale, center)
        sqw[0,:] += (1-A0) * lorentz(w, scale, center, hwhm)
      
    # Convolution with resolution function (if given)
    if resolution is not None:

        # Input validation: Check if single resolution function or N spectra
        #                   Check dimensions agree with sqw   

        for i in range(q.size):
        
            if resolution.ndim == 1:
                tmp = np.convolve(sqw[i,:], resolution/resolution.sum())
            else:
                tmp = np.convolve(sqw[i,:], resolution[i,:]/resolution[i,:].sum()) 
            
            # Energy axis non necessarily symmetric --> Position model at center                
            idxMax = np.argmax(tmp)
            idxMin = np.argmin(np.abs(w-center))
            sqw[i,:] = tmp[idxMax-idxMin:idxMax-idxMin+w.size]
    
    # Add flat background
    sqw += background

    # For Bumps use (needed for final plotting)
    # Using a 'Curve' in bumps for each Q --> needs vector array
    if q.size == 1: 
         sqw = np.reshape(sqw, w.size)    
        
    return sqw
 

def sqwDeltaTwoLorentz(w, q, scale, center, A0, A1, hwhm1, hwhm2, background, resolution=None):

    # Model = A0*delta + A1*Lorentz(Gamma1) + (1-A0-A1)*Lorentz(Gamma2)

    # Input validation
    q = np.asarray(q, dtype=np.float32)
    
    # Create output array
    sqw = np.zeros((q.size, w.size))

    # Model
    if q.size > 1:
        for i in range(q.size):
            sqw[i,:] = A0[i] * delta(w, scale, center)
            sqw[i,:] += A1[i] * lorentz(w, scale, center, hwhm1[i])
            sqw[i,:] += (1-A0[i]-A1[i]) * lorentz(w, scale, center, hwhm2[i])
    else:
        sqw[0,:] = A0* delta(w, scale, center)
        sqw[0,:] += A1 * lorentz(w, scale, center, hwhm1)
        sqw[0,:] += (1-A0-A1) * lorentz(w, scale, center, hwhm2)
      
    # Convolution with resolution function (if given)
    if resolution is not None:

        # Input validation: Check if single resolution function or N spectra
        #                   Check dimensions agree with sqw

        for i in range(q.size):
            if resolution.ndim == 1:
                tmp = np.convolve(sqw[i,:], resolution/resolution.sum())
            else:
                tmp = np.convolve(sqw[i,:], resolution[i,:]/resolution[i,:].sum()) 
            
            # Energy axis non necessarily symmetric --> Position model at center                
            idxMax = np.argmax(tmp)
            idxMin = np.argmin(np.abs(w-center))
            sqw[i, :] = tmp[idxMax-idxMin: idxMax-idxMin+w.size]

    # Add flat background
    sqw += background

    # For Bumps use (needed for final plotting)
    # Using a 'Curve' in bumps for each Q --> needs vector array
    if q.size == 1: 
         sqw = np.reshape(sqw, w.size)    
        
    return sqw
       

def sqwBrownianTranslationalDiffusion(w, q, scale, center, D, background, resolution=None):

    # Model = Brownian Translational diffusion = Lorentzian of HWHM = D*Q^2
    
    # Input validation
    q = np.asarray(q, dtype=np.float32)
    
    # Create output array
    sqw = np.zeros((q.size, w.size))
        
    # Get widths, EISFs and QISFs of model
    hwhm, eisf, qisf = hwhmBrownianTranslationalDiffusion(q, D)
    
    # Model
    for i in range(q.size):
       sqw[i,:] = lorentz(w, scale, center, hwhm[i])
       
    # Convolution with resolution function (if given)
    if resolution is not None:

        # Input validation: Check if single resolution function or N spectra
        #                   Check dimensions agree with sqw   

        for i in range(q.size):
        
            if resolution.ndim == 1:
                tmp = np.convolve(sqw[i,:], resolution/resolution.sum())
            else:
                tmp = np.convolve(sqw[i,:], resolution[i,:]/resolution[i,:].sum()) 
            
            # Energy axis non necessarily symmetric --> Position model at center                
            idxMax = np.argmax(tmp)
            idxMin = np.argmin(np.abs(w-center))
            sqw[i,:] = tmp[idxMax-idxMin:idxMax-idxMin+w.size]
    
    # Add flat background
    sqw += background
    
    # For Bumps use (needed for final plotting)
    # Using a 'Curve' in bumps for each Q --> needs vector array
    if q.size == 1: 
         sqw = np.reshape(sqw, w.size)    
        
    return sqw
        

def sqwJumpTranslationalDiffusion(w, q, scale, center, D, resTime, background, resolution=None):

    # Model = Jump Translational diffusion = Lorentzian of HWHM = D*Q^2 / (1+tau*D*Q^2)
    
    # Input validation
    q = np.asarray(q, dtype=np.float32)
    
    # Create output array
    sqw = np.zeros((q.size, w.size))
        
    # Get widths, EISFs and QISFs of model
    hwhm, eisf, qisf = hwhmJumpTranslationalDiffusion(q, D, resTime)
    
    # Model
    for i in range(q.size):
       sqw[i,:] = lorentz(w, scale, center, hwhm[i])
       
    # Convolution with resolution function (if given)
    if resolution is not None:

        # Input validation: Check if single resolution function or N spectra
        #                   Check dimensions agree with sqw   

        for i in range(q.size):
        
            if resolution.ndim == 1:
                tmp = np.convolve(sqw[i,:], resolution/resolution.sum())
            else:
                tmp = np.convolve(sqw[i,:], resolution[i,:]/resolution[i,:].sum()) 
            
            # Energy axis non necessarily symmetric --> Position model at center                
            idxMax = np.argmax(tmp)
            idxMin = np.argmin(np.abs(w-center))
            sqw[i,:] = tmp[idxMax-idxMin:idxMax-idxMin+w.size]
    
    # Add flat background
    sqw += background
    
    # For Bumps use (needed for final plotting)
    # Using a 'Curve' in bumps for each Q --> needs vector array
    if q.size == 1: 
         sqw = np.reshape(sqw, w.size)    
        
    return sqw

    
def sqwIsotropicRotationalDiffusion(w, q, scale, center, radius, DR, background, resolution=None):

    # Model = Isotropic rotational diffusion = A0 + Sum of Lorentzians ...
    
    # Input validation
    q = np.asarray(q, dtype=np.float32)
    
    # Create output array
    sqw = np.zeros((q.size, w.size))
    
    # Get widths, EISFs and QISFs of model
    hwhm, eisf, qisf = hwhmIsotropicRotationalDiffusion(q, radius, DR)

    # Number of Lorentzians used to represent the infinite sum in R    
    numberLorentz = hwhm.shape[1]
    
   # Sum of Lorentzians
    for i in range(q.size):
        sqw[i,:] = eisf[i] * delta(w, scale, center)
        for j in range(1, numberLorentz):
            sqw[i,:] += qisf[i,j] * lorentz(w, scale, center, hwhm[i,j])

    # Convolution with resolution function (if given)
    if resolution is not None:

        # Input validation: Check if single resolution function or N spectra
        #                   Check dimensions agree with sqw   

        for i in range(q.size):
        
            if resolution.ndim == 1:
                tmp = np.convolve(sqw[i,:], resolution/resolution.sum())
            else:
                tmp = np.convolve(sqw[i,:], resolution[i,:]/resolution[i,:].sum()) 
            
            # Energy axis non necessarily symmetric --> Position model at center
            idxMax = np.argmax(tmp)
            idxMin = np.argmin(np.abs(w-center))
            sqw[i,:] = tmp[idxMax-idxMin:idxMax-idxMin+w.size]
    
    # Add flat background
    sqw += background

    # For Bumps use (needed for final plotting)
    # Using a 'Curve' in bumps for each Q --> needs vector array
    if q.size == 1: 
         sqw = np.reshape(sqw, w.size)    

    return sqw

    
def sqwWaterTeixeira(w, q, scale, center, D, resTime, radius, DR, background, resolution=None):

    # Model = convolution(T, R)
    #   T = Jump Translational diffusion = Lorentz(Gamma_T)
    #   R = Isotropic rotational diffusion = A0 + A1*L1 + A2*L2 + ...
    #   convolution(T,R) = A0*Lorentz(Gamma_T) + A1*Lorentz(Gamma_T+Gamma_1) + A2*Lorentz(Gamma_T+Gamma_2) + ...
    
    # Input validation
    q = np.asarray(q, dtype=np.float32)
    
    # Create output array
    sqw = np.zeros((q.size, w.size))
    
    # Get widths, EISFs and QISFs of each model
    hwhm1, eisf1, qisf1 = hwhmJumpTranslationalDiffusion(q, D, resTime)
    hwhm2, eisf2, qisf2 = hwhmIsotropicRotationalDiffusion(q, radius, DR) 

    # Number of Lorentzians used to represent the infinite sum in R    
    numberLorentz = hwhm2.shape[1]
    
    # Sum of Lorentzians giving the full model
    for i in range(q.size):
        sqw[i, :] = eisf2[i] * lorentz(w, scale, center, hwhm1[i])
        for j in range(1, numberLorentz):
            sqw[i, :] += qisf2[i, j] * lorentz(w, scale, center, hwhm1[i]+hwhm2[i,j])

    # Convolution with resolution function (if given)
    if resolution is not None:

        # Input validation: Check if single resolution function or N spectra
        #                   Check dimensions agree with sqw   

        for i in range(q.size):
        
            if resolution.ndim == 1:
                tmp = np.convolve(sqw[i,:], resolution/resolution.sum())
            else:
                tmp = np.convolve(sqw[i,:], resolution[i,:]/resolution[i,:].sum()) 
            
            # Energy axis non necessarily symmetric --> Position model at center                
            idxMax = np.argmax(tmp)
            idxMin = np.argmin(np.abs(w-center))
            # Temporal trick --> problem when all data in S(Q,w) = 0
            if idxMax < idxMin:
                pass # will just keep the initial S(Q,w) = 0
            else:    
                sqw[i,:] = tmp[idxMax-idxMin:idxMax-idxMin+w.size]
    
    # Add flat background
    sqw += background

    # For Bumps use (needed for final plotting)
    # Using a 'Curve' in bumps for each Q --> needs vector array
    if q.size == 1: 
         sqw = np.reshape(sqw, w.size)    

    return sqw
