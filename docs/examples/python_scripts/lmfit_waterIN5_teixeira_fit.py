#!/usr/bin/env python
# coding: utf-8

# Imported required libraries
from __future__ import print_function
import h5py
from scipy.integrate import simps
import numpy as np
import matplotlib.pyplot as plt


# required imports from lmfit
from lmfit import Model, CompositeModel
from scipy.interpolate import interp1d


import QENSmodels


path_to_data = '../data/'

with h5py.File(path_to_data + 'H2O_293K_5A.hdf', 'r') as f:
    data_in = f['entry1']
    w = data_in['data1']
    x = w['X'][()]  # energy or time values
    unit_w = w['X'].attrs['long_name']
    unit_q = w['Y'].attrs['long_name']
    y = w['DATA'][()]  # intensities
    e = w['errors'][()]  # errors for the intensities
    # Obtain the momentum transfer values
    q = w['Y'][()]
    data_5A = dict(q=q, x=x, y=y, e=e)


# number of spectra (i.e. number of different q-values)
nb_q_values = len(data_5A['q'])


print(f"""The names and units of `w` (`x`axis) and `q` are: 
{str(unit_w[0], 'utf-8')} and {str(unit_q[0], 'utf-8')}, respectively.""")


path_to_data = '../data/'

with h5py.File(path_to_data + 'V_273K_5A.hdf', 'r') as f:
    data = f['entry1']
    w = data['data1']
    res_5A_x = w['X'][()]
    res_5A = np.transpose(w['DATA'][()])

# Force resolution function to have unit area
for i in range(len(data_5A['q'])):
    area = simps(res_5A[:, i], data_5A['x'])
    res_5A[:, i] /= area


# Filter according to energy-range
mask = np.intersect1d(np.where(data_5A['x'] > -1.), np.where(data_5A['x'] < 1.))

f_5A_mask = dict()
f_5A_mask['x'] = np.asarray([data_5A['x'][mask] for i in range(nb_q_values)])
f_5A_mask['y'] = np.asarray([y[mask] for y in data_5A['y']])
f_5A_mask['e'] = np.asarray([e[mask] for e in data_5A['e']])

# Select resolution according to energy range
res_5A_x = res_5A_x[mask]
res_5A = res_5A[mask, :]


# Filter according to negative error values
# resolution
selected_indices = np.where(f_5A_mask['e'][i] > 0.0)
resol_5A_x = np.asarray([res_5A_x[selected_indices] for i in range(nb_q_values)])
resol_5A = np.asarray([res_5A[selected_indices, i][0] for i in range(nb_q_values)])

# data
f_5A = dict()
f_5A['x'] = np.asarray([x[selected_indices] for i, x in enumerate(f_5A_mask['x'])])
f_5A['y'] = np.asarray([y[selected_indices] for i, y in enumerate(f_5A_mask['y'])])
f_5A['e'] = np.asarray([e[selected_indices] for i, e in enumerate(f_5A_mask['e'])])


# plot experimental data
fig0, ax0 = plt.subplots()
[ax0.semilogy(f_5A['x'][i], f_5A['y'][i]) for i in range(nb_q_values)]
ax0.set(xlabel=r'Energy transfer (meV)', title='Reference data - 5 Angstrom')
ax0.grid();


# plot experimental data
fig1, ax1 = plt.subplots()
[ax1.semilogy(resol_5A_x[i], resol_5A[i]) for i in range(nb_q_values)]
ax1.set(xlabel=r'Energy transfer (meV)', title='Resolution function - 5 Angstrom')
ax1.grid();


f_interp = [interp1d(resol_5A_x[i],
                     resol_5A[i] / np.sum(resol_5A[i]),
                     kind='cubic',
                     bounds_error=False,
                     fill_value='extrapolate') for i in range(nb_q_values)]

def irf_gate(w, spectrum_nb=0):
    """ Function defined from the interpolation of instrument resolution data
    Used to define fitting model and plot """
    return f_interp[spectrum_nb](w)


# check interpolation for first spectrum of resolution function: 
# plot tabulated data and interpolated data
indx = 0

fig2, ax2 = plt.subplots()
ax2.plot(resol_5A_x[indx],
         resol_5A[indx] / np.sum(resol_5A[indx]),
         '.',
         label=f"tabulated data. q={data_5A['q'][indx]:.2}")
ax2.plot(f_5A['x'][indx],
         irf_gate(f_5A['x'][indx], indx),
         '--',
         label=f"extrapolated data. q={data_5A['q'][indx]:.2}")
ax2.legend(bbox_to_anchor=(1.1, .95))
ax2.set_xlabel('w')
ax2.set_title(f'Instrument resolution: tabulated data and interpolated data for spectrum {indx}')
ax2.grid();


# Create convolution function
# code from https://lmfit.github.io/lmfit-py/model.html

def convolve(arr, kernel):
    # simple convolution of two arrays
    npts = min(len(arr), len(kernel))
    pad = np.ones(npts)
    tmp = np.concatenate((pad * arr[0], arr, pad * arr[-1]))

    out = np.convolve(tmp, kernel, mode='valid')
    noff = int((len(out) - npts) / 2)
    return out[noff:noff + npts]


model = CompositeModel(Model(irf_gate), Model(QENSmodels.sqwWaterTeixeira), convolve)

print('Names of parameters:', model.param_names)
print('Independent variable(s):', model.independent_vars)

# Define boundaries for parameters to be refined
model.set_param_hint('scale', min=0, max=100)
model.set_param_hint('center', min=-0.1, max=0.1)
model.set_param_hint('D', min=0.05, max=0.25)
model.set_param_hint('resTime', min=0, max=1)
model.set_param_hint('radius', min=0.9, max=1.1)
model.set_param_hint('DR', min=0, max=1)

# Fix some of the parameters
model.set_param_hint('q', vary=False)
model.set_param_hint('spectrum_nb', vary=False)

params = model.make_params()


# Plot of the fitting models without and convoluted with the resolution function
# The values of the parameters are specified below.
# Therefore they could be different from those used in the fitting.

fig, ax = plt.subplots(1, 2)
# First subplot
for i in range(nb_q_values):
    xx = f_5A['x'][i]
    ax[0].plot(xx,
               QENSmodels.sqwWaterTeixeira(xx,
                                           data_5A['q'][i],
                                           scale=1,
                                           center=0,
                                           D=1,
                                           resTime=1,
                                           radius=1,
                                           DR=1),
               label=f"q={data_5A['q'][i]:.2}")  

ax[0].grid(True)
ax[0].set(xlabel='Omega',
          ylabel='S(Q,w)',
          xlim=(-1, 1),
          title='No resolution')
ax[0].tick_params()
plt.tight_layout(rect=[0, 0, 1, 0.8])
ax[0].legend(bbox_to_anchor=(0., 1.1, 2., 0.102),
             loc='lower right',
             ncol=5,
             mode="expand",
             borderaxespad=0.,
             fontsize=8)
# Second subplot
for i in range(nb_q_values):
    params_plot = model.make_params(nb_spectrum=i,
                                    q=data_5A['q'][i],
                                    scale=10.,
                                    center=0.,
                                    D=0.13,
                                    resTime=0.1,
                                    radius=1.,
                                    DR=0.3)
    xx = f_5A['x'][i]
    ax[1].plot(xx, model.eval(params_plot, w=xx))

ax[1].grid(True)
ax[1].set(xlabel='w',
          ylabel=r'R $\otimes$ S(Q,w)',
          xlim=(-1, 1),
          title='Convoluted with resolution')
ax[1].tick_params();


ini_values = {'scale': 10., 'center': 0., 'D': 0.13, 'resTime': 0.1, 'radius': 1., 'DR': 0.3}

result_fit = [None, ] * nb_q_values  # store fits for all spectra
for i in range(nb_q_values):
    params = model.make_params(nb_spectrum=i,
                               q=data_5A['q'][i],
                               scale=ini_values['scale'],
                               center=ini_values['center'],
                               D=ini_values['D'],
                               resTime=ini_values['resTime'],
                               radius=ini_values['radius'],
                               DR=ini_values['DR'])

    # Q-independent parameters
    if i == 0:
        D_value = params['D'].value
        resTime_value = params['resTime'].value
        radius_value = params['radius'].value
        DR_value = params['DR'].value
    else:
        params['D'].set(value=D_value)
        params['resTime'].set(value=resTime_value)
        params['radius'].set(value=radius_value)
        params['DR'].set(value=DR_value)

    result_fit[i] = model.fit(f_5A['y'][i], params, w=f_5A['x'][i])


# display result
for i in range(nb_q_values):
    print(f'Result of fit {i}:\n', result_fit[i].fit_report())


# plot results using lmfit's features
for i in range(nb_q_values):
    result_fit[i].plot();


# other option to plot: experimental data, initial fitting model and fitted model for each spectrum

for indx in range(nb_q_values):
    fig1, ax1 = plt.subplots()
    ax1.plot(f_5A['x'][indx],
             f_5A['y'][indx],
             'bo',
             label='exp')
    ax1.plot(f_5A['x'][indx],
             result_fit[indx].init_fit,
             'k--',
             label='ini')
    ax1.plot(f_5A['x'][indx],
             result_fit[indx].best_fit,
             'r-',
             label='fin')
    ax1.set_title("q={data_5A['q'][indx]:.2}")
    ax1.legend()
    ax1.grid()



plt.show()

