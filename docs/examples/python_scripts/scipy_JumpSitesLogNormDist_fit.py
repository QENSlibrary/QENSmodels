#!/usr/bin/env python
# coding: utf-8

from __future__ import print_function
import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit


# import model from QENS library
import QENSmodels


# Units of parameters for selected QENS model and experimental data

dict_physical_units = {'scale': "unit_of_signal.ps",
                       'center': "1/ps",
                       'radius': 'Angstrom',
                       'resTime': 'ps'}


# Creation of reference data
nb_points = 100
xx = np.linspace(-10, 10, nb_points)
added_noise = 0.02 * np.random.normal(0, 1, nb_points)
sqw_jump_sites_noisy = QENSmodels.sqwJumpSitesLogNormDist(xx,
                                                          q=0.89,
                                                          scale=1,
                                                          center=0.3,
                                                          Nsites=5,
                                                          radius=2,
                                                          resTime=0.45,
                                                          sigma=0.25) * (1 + 2 * added_noise) 
sqw_jump_sites_noisy += added_noise

fig0, ax0 = plt.subplots()
ax0.plot(xx, sqw_jump_sites_noisy, label='reference data')
ax0.set_xlabel('x')
ax0.grid()
ax0.legend();


# From https://docs.scipy.org/doc/scipy/reference/generated/scipy.optimize.curve_fit.html
# perform fit with initial guesses scale=0.95, center=0.2, radius=2, resTime=0.45, sigma=0.25
# Nsites=5 and q =0.89 are fixed

def func_to_fit(xx, scale, center, radius, resTime, sigma):
    return QENSmodels.sqwJumpSitesLogNormDist(xx, 0.89, scale, center, 5, radius, resTime, sigma)


fig0, ax0 = plt.subplots()
ax0.plot(xx, sqw_jump_sites_noisy, 'b-', label='reference data')
ax0.plot(xx, QENSmodels.sqwJumpSitesLogNormDist(xx,
                                                0.89,
                                                scale=0.95,
                                                center=0.2,
                                                Nsites=5,
                                                radius=2,
                                                resTime=0.45,
                                                sigma=0.25),
         'r-',
         label='model with initial guesses')
ax0.set_xlabel('x')
ax0.grid()
ax0.legend(bbox_to_anchor=(0.6, 1), loc=2, borderaxespad=0.);


success_fit = True

try:
    popt, pcov = curve_fit(func_to_fit, xx, sqw_jump_sites_noisy,
                           p0=[0.95, 0.2, 2, 0.45, 0.25],
                           bounds=((0.1, -2, 0.1, 0.1, 0.1), (5., 2., 5., 11., 1.)))
except RuntimeError:
    success_fit = False
    print("Error - curve_fit failed")


# Calculation of the errors on the refined parameters:
if success_fit:
    perr = np.sqrt(np.diag(pcov))
    print('Values of refined parameters:')
    print('scale:', popt[0], '+/-', perr[0], dict_physical_units['scale'])
    print('center :', popt[1], '+/-', perr[1], dict_physical_units['center'])
    print('radius', popt[2], '+/-', perr[2], dict_physical_units['radius'])
    print('resTime', popt[3], '+/-', perr[3], dict_physical_units['resTime'])
    print('sigma', popt[4], '+/-', perr[4])


# Comparison of reference data with fitting result
if success_fit:
    fig1, ax1 = plt.subplots()
    ax1.plot(xx,
             sqw_jump_sites_noisy,
             'b-',
             label='reference data')
    ax1.plot(xx,
             func_to_fit(xx, *popt),
             'g--',
             label='fit: %5.3f, %5.3f, %5.3f, %5.3f, %5.3f' % tuple(popt))
    ax1.legend(bbox_to_anchor=(0., 1.15),
               loc='upper left',
               borderaxespad=0.)
    ax1.set_xlabel('x')
    ax1.grid();



plt.show()

