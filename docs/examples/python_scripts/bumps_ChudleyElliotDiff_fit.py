#!/usr/bin/env python
# coding: utf-8

# Imported required libraries
from __future__ import print_function
import numpy as np
import matplotlib.pyplot as plt


import bumps.names as bmp
from bumps.fitters import fit


import QENSmodels


nb_points = 500
xx = np.linspace(-4, 4, nb_points)
q = np.linspace(0.2, 2, 10)
added_noise = 0.1 * np.random.normal(0, 1, nb_points)
chudley_elliot_noisy = QENSmodels.sqwChudleyElliotDiffusion(xx,
                                                            q,
                                                            scale=1.,
                                                            center=0.,
                                                            D=0.23,
                                                            L=1.) * (1. + added_noise) 
chudley_elliot_noisy += 0.1 * added_noise


# Units of parameters for selected QENS model and experimental data
dict_physical_units = {'omega': "1/ps",
                       'q': "1/Angstrom",
                       'D': "ps.Angstrom^2",
                       'L': "Angstrom",
                       'scale': "unit_of_signal/ps",
                       'center': "1/ps"}


M = []
for i in range(len(q)):
    # Bumps fitting model
    Mq = bmp.Curve(QENSmodels.sqwChudleyElliotDiffusion,
                   xx,
                   chudley_elliot_noisy[i],
                   q[i],
                   scale=1,
                   center=0,
                   D=0.2,
                   L=0.7)

    Mq.scale.range(0.1, 1e5)
    Mq.center.range(-0.1, 0.1)
    Mq.D.range(0.1, 1)
    Mq.L.range(0.1, 3)

    # Q-independent parameters
    if i == 0:
        QD = Mq.D
        QL = Mq.L
    else:
        Mq.D = QD
        Mq.L = QL

    M.append(Mq)

problem = bmp.FitProblem(M)


# Preview of the settings
print('Initial chisq', problem.chisq_str())


problem.plot()


result = fit(problem,
             method='lm',
             steps=100,
             verbose=True)


problem.plot()


# Print chi**2 and parameters' values after fit
print("final chisq", problem.chisq_str())

for k, v, dv in zip(problem.labels(), result.x, result.dx):
    if k in dict_physical_units.keys():
        print(k, ":", v, dv, dict_physical_units[k])
    else:
        print(k, ":", v, dv)



plt.show()

