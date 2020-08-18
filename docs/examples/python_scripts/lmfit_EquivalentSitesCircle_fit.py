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
dict_physical_units = {'omega': "1/ps",
                       'q': "1/Angstrom",
                       'scale': "unit_of_signal/ps",
                       'center': "1/ps",
                       'radius': "Angstrom",
                       'resTime': "ps"}


nb_points = 200
xx = np.linspace(-5, 5, nb_points)
added_noise = 0.1 * np.random.normal(0, 1, nb_points)

equiv_sites_circle_noisy = QENSmodels.sqwEquivalentSitesCircle(xx,
                                                               q=1.,
                                                               scale=1.3,
                                                               center=0.3,
                                                               Nsites=5,
                                                               radius=4.,
                                                               resTime=3.) * (1 + added_noise)

equiv_sites_circle_noisy += 0.1 * added_noise


gmodel = Model(QENSmodels.sqwEquivalentSitesCircle)

print('Names of parameters:', gmodel.param_names)
print('Independent variable(s):', gmodel.independent_vars)

ini_values = {'scale': 1.22, 'center': 0.2, 'Nsites': 5, 'radius': 3.1, 'resTime': 0.33}

# Define boundaries for parameters to be refined
gmodel.set_param_hint('scale', min=0)
gmodel.set_param_hint('center', min=-5, max=5)
gmodel.set_param_hint('radius', min=0)
gmodel.set_param_hint('resTime', min=0)

# Fix some of the parameters
gmodel.set_param_hint('q', vary=False)
gmodel.set_param_hint('Nsites', vary=False)

# Fit
result = gmodel.fit(equiv_sites_circle_noisy, w=xx, q=1.,
                    scale=ini_values['scale'],
                    center=ini_values['center'],
                    Nsites=ini_values['Nsites'],
                    radius=ini_values['radius'],
                    resTime=ini_values['resTime'])


# Plots - Initial model and reference data
fig0, ax0 = plt.subplots()
ax0.plot(xx, equiv_sites_circle_noisy, 'b.-', label='reference data')
ax0.plot(xx, result.init_fit, 'k--', label='model with initial guesses')
ax0.set(xlabel='x', title='Initial model and reference data')
ax0.grid()
ax0.legend();


# display result
print('Result of fit:\n', result.fit_report())


# plot fitting result using lmfit functionality
result.plot()


# plot fitting resulting using matplotlib.pyplot
fig1, ax1 = plt.subplots()
ax1.plot(xx, equiv_sites_circle_noisy, 'b-', label='reference data')
ax1.plot(xx, result.best_fit, 'r', label='fitting result')
ax1.legend()
ax1.set(xlabel='x', title='Fit result and reference data')
ax1.grid();


for item in ['resTime', 'radius', 'center', 'scale']:
    print(item,
          result.params[item].value, '+/-', result.params[item].stderr, dict_physical_units[item])



plt.show()

