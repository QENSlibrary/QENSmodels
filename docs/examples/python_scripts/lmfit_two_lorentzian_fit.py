#!/usr/bin/env python
# coding: utf-8

# import python modules for plotting, fitting
from __future__ import print_function
import numpy as np
import matplotlib.pyplot as plt


from lmfit import Model, CompositeModel
from scipy.interpolate import interp1d

# import model from QENS library
import QENSmodels


# Units of parameters for selected QENS model and experimental data
dict_physical_units = {'omega': "meV",
                       'q': "1/Angstrom",
                       'hwhm': "meV",
                       'scale': "unit_of_signal.meV",
                       'center': "meV"}


path_to_data = '../data/'


# Create model - 2 lorentzians convoluted with instrument resolution - 6 parameters
# Step 1 load instrument resolution data
irf_iris = np.loadtxt(path_to_data + 'irf_iris.dat')
x_irf = irf_iris[:, 0]
y_irf = irf_iris[:, 1]


# Step 2: create function for instrument resolution data
# (cubic interpolation between tabulated data points)
f = interp1d(x_irf, y_irf, kind='cubic', bounds_error=False, fill_value='extrapolate')


def irf_gate(x):
    """ Function defined from the interpolation of instrument resolution data
    Used to define fitting model and plot """
    return f(x)


# plot tabulated data and interpolated data
xx = np.linspace(-.25, .25, 500)

fig0, ax0 = plt.subplots()
ax0.plot(x_irf, y_irf, 'b.', label='tabulated data')
ax0.plot(xx, irf_gate(xx), 'g--', label='extrapolated data')
ax0.legend()
ax0.set_xlabel('Energy transfer (meV)')
ax0.set_title('Instrument resolution: plot tabulated data and interpolated data')
ax0.grid();


# Step 3: create "double lorentzian" profile
def model_2lorentzians(x, scale1, center1, hwhm1, scale2, center2, hwhm2):
    model = QENSmodels.lorentzian(x, scale1, center1, hwhm1)
    model += QENSmodels.lorentzian(x, scale2, center2, hwhm2)
    return model


# Step 4: create convolution function
# code from https://lmfit.github.io/lmfit-py/model.html

def convolve(arr, kernel):
    # simple convolution of two arrays
    npts = min(len(arr), len(kernel))
    pad = np.ones(npts)
    tmp = np.concatenate((pad * arr[0], arr, pad * arr[-1]))

    out = np.convolve(tmp, kernel, mode='valid')
    noff = int((len(out) - npts) / 2)
    return out[noff:noff + npts]


# Create model for the fit
gmodel = CompositeModel(Model(irf_gate), Model(model_2lorentzians), convolve)

print('Names of parameters:', gmodel.param_names)
print('Independent variable(s):', gmodel.independent_vars)


# Load reference data - extract x and y values
two_lorentzians_iris = np.loadtxt(path_to_data + 'data_2lorentzians.dat')
xx = two_lorentzians_iris[:, 0]
yy = two_lorentzians_iris[:, 1]


# Fit
result = gmodel.fit(yy, x=xx, scale1=1., center1=0., hwhm1=0.25, scale2=1., center2=1., hwhm2=0.25)

fig1, ax1 = plt.subplots()
ax1.plot(xx, yy, '+', label='experimental data')
ax1.plot(xx, result.init_fit, 'k--', label='model with initial guesses')
ax1.legend()
ax1.set(xlabel='Energy transfer (meV)',
        title='Plot before fitting: experimental data and mode with initial guesses')
ax1.grid();


# display result
print('Result of fit:\n', result.fit_report())

# plot selected results: experimental data and best fit
fig2, ax2 = plt.subplots()
ax2.plot(xx, yy, '+', label='experimental data')
ax2.plot(xx, result.best_fit, 'r-', label='best fit')
ax2.grid()
ax2.set(xlabel='Energy transfer (meV)',
        title='Plot selected fitting results: experimental data and best fit')
ax2.legend();


# other option to plot result using lmfit's features
result.plot()


for item in result.params.keys():
    print(item[:-1],
          result.params[item].value,
          '+/-',
          result.params[item].stderr,
          dict_physical_units[item[:-1]])



plt.show()

