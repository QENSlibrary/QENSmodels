#!/usr/bin/env python
# coding: utf-8

from __future__ import print_function
import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit


# import model from QENS library
import QENSmodels


# Units of parameters for selected QENS model and experimental data
dict_physical_units = {"omega": "1/ps",
                       'scale': "unit_of_signal.ps",
                       'center': "1/ps",
                       'hwhm': "1/ps"}


# Creation of reference data
nb_points = 100
xx = np.linspace(-10, 10, nb_points)
added_noise = 0.1 * np.random.normal(0, 1, nb_points)
lorentzian_noisy = QENSmodels.lorentzian(xx,
                                         scale=0.89,
                                         center=-0.025,
                                         hwhm=0.45) * (1. + added_noise)
lorentzian_noisy += 0.1 * added_noise

fig0, ax0 = plt.subplots()
ax0.plot(xx, lorentzian_noisy, label='reference data')
ax0.set_xlabel('x')
ax0.grid()
ax0.legend();


# From https://docs.scipy.org/doc/scipy/reference/generated/scipy.optimize.curve_fit.html
# perform fit with initial guesses scale=1, center=0.2 HWHM=0.5
initial_parameters_values = [1, 0.2, 0.5]

fig1, ax1 = plt.subplots()
ax1.plot(xx, lorentzian_noisy, 'b-', label='reference data')
ax1.plot(xx,
         QENSmodels.lorentzian(xx, *initial_parameters_values),
         'r-',
         label='model with initial guesses')
ax1.set_xlabel('x')
ax1.legend(bbox_to_anchor=(0., 1.15), loc='upper left', borderaxespad=0.)
ax1.grid()


popt, pcov = curve_fit(QENSmodels.lorentzian, xx, lorentzian_noisy, p0=initial_parameters_values)


# Calculation of the errors on the refined parameters:
perr = np.sqrt(np.diag(pcov))

print('Values of refined parameters:')
print('scale:', popt[0], '+/-', perr[0], dict_physical_units['scale'])
print('center :', popt[1], '+/-', perr[1], dict_physical_units['center'])
print('HWHM', popt[2], '+/-', perr[2], dict_physical_units['hwhm'])


# Comparison of reference data with fitting result
fig2, ax2 = plt.subplots()
ax2.plot(xx, lorentzian_noisy, 'b-')
ax2.plot(xx, QENSmodels.lorentzian(xx, *popt), 'g--')
ax2.legend(['reference data', 'fit: %5.3f, %5.3f, %5.3f' % tuple(popt)])
ax2.set_xlabel('x')
ax2.grid();



plt.show()

