from __future__ import print_function

import sys
import numpy as np
import matplotlib.pyplot as plt

import qens_models

# Vector of Q and omega values
q = np.arange(0.25, 2.1, 0.25)
omega = np.arange(-2, 2.01, 0.01)

# Parameters
scale = 1.0
center = 0.0
background = 0.0

if len(sys.argv) == 1:
    print ("")
    print ("Use: python explore_models.py MODEL_NAME [sigma]")
    print ("")
    print ("Available model names: ")
    print ("   BrownianTranslationalDiffusion")
    print ("   JumpTranslationalDiffusion")
    print ("   IsotropicRotationalDiffusion")
    print ("   WaterTeixeira")
    print ("")
    print ("If sigma is given, a gaussian resolution function with")
    print ("standard deviation = sigma is convolved with the model.")
    print ("")
    sys.exit()

# Resolution    
if len(sys.argv) == 3:
   sigma = float(sys.argv[2])
   resol = np.exp(-omega**2/(2*sigma**2)) / (sigma*np.sqrt(2*np.pi))
else:
   resol = None

if sys.argv[1] == 'BrownianTranslationalDiffusion':

    print ("")
    print ("Brownian Translational Diffusion model:")
    D = float(raw_input("Value of self-diffusion coefficient (in A^2*meV)? "))
    print ("")
    sqw = qens_models.sqwBrownianTranslationalDiffusion(omega, q, scale, center,
           D, background, resolution=resol)

elif sys.argv[1] == 'JumpTranslationalDiffusion':

    print ("")
    print ("Jump Translational Diffusion model:")
    D = float(raw_input("Value of self-diffusion coefficient (in A^2*meV)? "))
    resTime = float(raw_input("Residence time between jumps (in meV^-1)? "))
    print ("")
    sqw = qens_models.sqwJumpTranslationalDiffusion(omega, q, scale, center,
           D, background, resTime, resolution=resol)
           
elif sys.argv[1] == 'IsotropicRotationalDiffusion':

    print ("")
    print ("Isotropic Rotational Diffusion model:")
    R = float(raw_input("Radius of sphere (in A)? "))
    DR = float(raw_input("Value of rotational diffusion coefficient (in meV)? "))
    print ("")
    sqw = qens_models.sqwIsotropicRotationalDiffusion(omega, q, scale, center,
           R, DR, background, resolution=resol)

elif sys.argv[1] == 'WaterTeixeira':

    print ("")
    print ("Teixeira's model for water:")
    D = float(raw_input("Value of self-diffusion coefficient (in A^2*meV)? "))
    resTime = float(raw_input("Residence time between jumps (in meV^-1)? "))
    R = float(raw_input("Radius of sphere (in A)? "))
    DR = float(raw_input("Value of rotational diffusion coefficient (in meV)? "))
    print ("")
    sqw = qens_models.sqwWaterTeixeira(omega, q, scale, center,
           D, resTime, R, DR, background, resolution=resol)

else:

    print ("")
    print ("Model not known!")
    print ("")
    print ("Available model names: ")
    print ("   BrownianTranslationalDiffusion")
    print ("   JumpTranslationalDiffusion")
    print ("   IsotropicRotationalDiffusion")
    print ("   WaterTeixeira")
    print ("")
    sys.exit()
    
# Plot
fig = plt.figure(1)

ax1 = fig.add_subplot(121)
for i in range(q.size):
    integral = np.trapz(sqw[i,:], omega)
    print ("Integral S(Q=",q[i],",w) = ", integral)
    ax1.plot(omega, sqw[i,:], label=str(q[i]))
ax1.grid(True)
ax1.set_xlabel('Omega')
ax1.set_ylabel('S(Q,w)')
ax1.set_yscale('log')

ax2 = fig.add_subplot(122)
for i in range(q.size):
    ax2.plot(omega, sqw[i,:], label=str(q[i]))
ax2.grid(True)
ax2.set_xlabel('Omega')
ax2.set_ylabel('S(Q,w)')

plt.legend()
plt.show()   
