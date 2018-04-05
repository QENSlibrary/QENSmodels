import numpy as np
from scipy.special import jn 

def delta(x, scale, center, resolution=None):
    model = np.zeros(x.size) 
    model[np.argmin(np.abs(x))] = scale
    if resolution is not None:
        model = np.convolve(model, resolution/resolution.sum(), mode='same')
    return model

    
def lorentz(x, scale, center, hwhm, resolution=None):
    model = scale * hwhm / ((x-center)**2 + hwhm**2) / np.pi 
    if resolution is not None:
        model = np.convolve(model, resolution/resolution.sum(), mode='same')
    return model

    
def jumpDiffusion(x, scale, center, D, Q, resolution=None):
    hwhm = D*Q**2
    model = lorentz(x, scale, center, hwhm)
    if resolution is not None:
        model = np.convolve(model, resolution/resolution.sum(), mode='same')
    return model

    
def isotropicRotationalDiffusion(x, scale, center, radius, DR, Q, resolution=None):
    jl = np.zeros(10)
    hwhm = np.zeros(10)
    for i in range(10):  
        arg = Q * radius
        if arg > 0:
            jl[i] = np.sqrt(np.pi/2/arg) * jn(i+0.5, arg)
        else:
            if i == 0:
                jl[i] = 1.0
            else:            
                jl[i] = 0.0
        hwhm[i] = i * (i+1) * DR
    model = jl[0]**2 * delta(x, 1.0, center)
    for i in range(1,10):
        model += (2*i+1) * jl[i]**2 * lorentz(x, 1.0, center, hwhm[i])    
    if resolution is not None:
        model = np.convolve(model, resolution/resolution.sum(), mode='same')
    return model
            

def twoLorentz(x, scale1, center1, hwhm1, scale2, center2, hwhm2, resolution=None):
    model = lorentz(x, scale1, center1, hwhm1)
    model += lorentz(x, scale2, center2, hwhm2)    
    if resolution is not None:
        model = np.convolve(model, resolution/resolution.sum(), mode='same')
    return model

    
def waterTeixeira(x, scale, center, D, radius, DR, Q, resolution=None):
    model = jumpDiffusion(x, scale, center, D, Q)
    model += isotropicRotationalDiffusion(x, scale, center, radius, DR, Q)
    if resolution is not None:
        model = np.convolve(model, resolution/resolution.sum(), mode='same')
    return model
