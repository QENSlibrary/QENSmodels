#!/usr/bin/env python
# coding: utf-8

# import python modules for plotting, fitting
from __future__ import print_function
import numpy as np
import matplotlib.pyplot as plt


# required imports from lmfit
from lmfit import Model

# import model from QENS library
import QENSmodels


# Units of parameters for selected QENS model and experimental data
dict_physical_units = {'omega': "1/ps",
                       'scale': "unit_of_signal/ps",
                       'center': "1/ps",
                       'hwhm': "1/ps"}


# Create array of reference data: noisy lorentzian with background
nb_points = 100
xx = np.linspace(-5, 5, nb_points)
added_noise = 0.02 * np.random.normal(0, 1, nb_points)
lorentzian_noisy = QENSmodels.lorentzian(xx,
                                         scale=0.89,
                                         center=-0.025,
                                         hwhm=0.45) * (1 + 5 * added_noise)
lorentzian_noisy += 0.5 * (1. + added_noise)


def flat_background(x, A0):
    """ Define flat background ot be added to fitting model"""
    return QENSmodels.background_polynomials(x, A0)


gmodel = Model(QENSmodels.lorentzian) + Model(flat_background)
print('Names of parameters:', gmodel.param_names)
print('Independent variable(s):', gmodel.independent_vars)

initial_parameters_values = [1, 0.2, 0.5, 0.33]

# Fit
result = gmodel.fit(lorentzian_noisy,
                    x=xx,
                    scale=initial_parameters_values[0],
                    center=initial_parameters_values[1],
                    hwhm=initial_parameters_values[2],
                    A0=initial_parameters_values[3])


# Plot initial model and reference data
fig0, ax0 = plt.subplots()
ax0.plot(xx, lorentzian_noisy, 'b-', label='reference data')
ax0.plot(xx, result.init_fit, 'k--', label='model with initial guesses')
ax0.set(xlabel='x', title='Initial model and reference data')
ax0.grid()
ax0.legend();


# display result
print('Result of fit:\n', result.fit_report())


# plot fitting result using lmfit functionality
result.plot()


# Plot fitting result and reference data using matplotlib.pyplot
fig1, ax1 = plt.subplots()
ax1.plot(xx, lorentzian_noisy, 'b-', label='reference data')
ax1.plot(xx, result.best_fit, 'r.', label='fitting result')
ax1.legend()
ax1.set(xlabel='x', title='Fit result and reference data')
ax1.grid();


for item in ['hwhm', 'center', 'scale']:
    print(item,
          result.params[item].value, '+/-', result.params[item].stderr, dict_physical_units[item])



plt.show()

