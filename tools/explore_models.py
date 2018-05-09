from __future__ import print_function

import sys
import numpy as np
import matplotlib.pyplot as plt

import QENSmodels

# Vector of Q values
q = np.arange(0.0, 10, 0.1)

if len(sys.argv) == 1:
    print ("")
    print ("Use: python explore_models.py MODEL_NAME")
    print ("")
    print ("Available model names: ")
    print ("   BrownianTranslationalDiffusion")
    print ("   JumpTranslationalDiffusion")
    print ("   IsotropicRotationalDiffusion")
    print ("")
    sys.exit()

if sys.argv[1] == 'BrownianTranslationalDiffusion':

    print ("")
    print ("Brownian Translational Diffusion model:")
    D = float(raw_input("Value of self-diffusion coefficient (in A^2*meV)? "))
    print ("")
    hwhm, eisf, qisf = QENSmodels.hwhmBrownianTranslationalDiffusion(q, D)

elif sys.argv[1] == 'JumpTranslationalDiffusion':

    print ("")
    print ("Jump Translational Diffusion model:")
    D = float(raw_input("Value of self-diffusion coefficient (in A^2*meV)? "))
    resTime = float(raw_input("Residence time between jumps (in meV^-1)? "))
    print ("")
    hwhm, eisf, qisf = QENSmodels.hwhmJumpTranslationalDiffusion(q, D, resTime)

elif sys.argv[1] == 'IsotropicRotationalDiffusion':

    print ("")
    print ("Isotropic Rotational Diffusion model:")
    R = float(raw_input("Radius of sphere? "))
    DR = float(raw_input("Value of rotational diffusion coefficient (in meV)? "))
    print ("")
    hwhm, eisf, qisf = QENSmodels.hwhmIsotropicRotationalDiffusion(q, R, DR)

else:

    print ("")
    print ("Model not known!")
    print ("")
    print ("Available model names: ")
    print ("   BrownianTranslationalDiffusion")
    print ("   JumpTranslationalDiffusion")
    print ("   IsotropicRotationalDiffusion")
    print ("")
    sys.exit()
    
# Plot
fig = plt.figure(1)

ax1 = fig.add_subplot(131)
ax1.plot(q, eisf, 'ro', linestyle='--')
ax1.grid(True)
ax1.set_xlim((0,10))
ax1.set_ylim((0,1.1))
ax1.set_xlabel('Q/AA-1')
ax1.set_ylabel('EISF(Q)')
ax1.set_title('Elastic component')

ax2 = fig.add_subplot(132)
ax2.plot(q, hwhm, linestyle='-', marker='o')
ax2.grid(True)
ax2.set_xlim((0,10))
ax2.set_xlabel('Q/AA-1')
ax2.set_ylabel('HWHM(Q)')
ax2.set_title('Widths')

ax3 = fig.add_subplot(133)
ax3.plot(q, qisf, linestyle='-')
ax3.grid(True)
ax3.set_xlim((0,10))
ax3.set_ylim((0,1.1))
ax3.set_xlabel('Q/AA-1')
ax3.set_ylabel('QISF(Q)')
ax3.set_title('Quasi components')

plt.show()   
