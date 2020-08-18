#!/usr/bin/env python
# coding: utf-8

from __future__ import print_function
import numpy as np
import matplotlib.pyplot as plt


# required imports from lmfit
from lmfit import Model

# import model from QENS library
import QENSmodels


# Units of parameters for selected QENS model and experimental data
dict_physical_units = {'omega': "meV",
                       'q': "1/Angstrom",
                       'D': "meV.Angstrom^2",
                       'variance_ux': "Angstrom",
                       'scale': "unit_of_signal.meV",
                       'center': "meV"}


nb_points = 200
xx = np.linspace(-2, 2, nb_points)
added_noise = 0.1 * np.random.normal(0, 1, nb_points)

gaussian_model_3d_noisy = QENSmodels.sqwGaussianModel3D(xx,
                                                        q=.5,
                                                        scale=0.7,
                                                        center=0.3,
                                                        D=1,
                                                        variance_ux=1.2) * (1 + added_noise)
gaussian_model_3d_noisy += 0.1 * added_noise

# plot initial mode
fig0, ax0 = plt.subplots()
ax0.plot(xx, gaussian_model_3d_noisy)
ax0.grid();


gmodel = Model(QENSmodels.sqwGaussianModel3D)

print('Names of parameters:', gmodel.param_names)
print('Independent variable(s):', gmodel.independent_vars)

initial_parameters_values = [1.22, 0.25, .3, 0.33]

# Define boundaries for parameters to be refined
gmodel.set_param_hint('scale', min=0)
gmodel.set_param_hint('center', min=-5, max=5)
gmodel.set_param_hint('D', min=0)
gmodel.set_param_hint('variance_ux', min=0)

# Fix some of the parameters
gmodel.set_param_hint('q', vary=False)

# Fit
result = gmodel.fit(gaussian_model_3d_noisy,
                    w=xx,
                    q=1.,
                    scale=initial_parameters_values[0],
                    center=initial_parameters_values[1],
                    D=initial_parameters_values[2],
                    variance_ux=initial_parameters_values[3])


# Plot Initial model and reference data
fig1, ax1 = plt.subplots()
ax1.plot(xx, gaussian_model_3d_noisy, 'b-', label='reference data')
ax1.plot(xx, result.init_fit, 'k--', label='model with initial guesses')
ax1.set(xlabel='x', title='Initial model and reference data')
ax1.grid()
ax1.legend();


# display result
print('Result of fit:\n', result.fit_report())


# plot fitting results using lmfit functionality
result.plot();


# plot fitting results and reference data using matplotlib.pyplot
fig2, ax2 = plt.subplots()
ax2.plot(xx, gaussian_model_3d_noisy, 'b-', label='reference data')
ax2.plot(xx, result.best_fit, 'r.', label='fitting result')
ax2.legend()
ax2.set(xlabel='x', title='Fit result and reference data')
ax2.grid();



plt.show()

