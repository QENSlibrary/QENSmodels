# This script reproduces data reduction and fitting for the water data
# at 5 Angstrom using MAntid in Python
# To run the script, the last version of Mantid (3.12)
# The fitting is not finished yet: setting ties, constraints and initial guesses.
from __future__ import print_function

from mantid.simpleapi import *
import numpy as np
from scipy.constants import pi

# Specify path where the data for the examples are i.e. to the content of
# the /QENSmodels/examples/ folder
path = '/QENSmodels/examples/'

# Load experimental data
ws_5Aini = LoadLamp(path+'H2O_293K_5A.hdf')

# Load vanadium data
res_5Aini = LoadLamp(path+'V_273K_5A.hdf')

# Extract Energy tranfer
hw_5A = ws_5Aini.readX(0)

# Force resolution function to have unit area
norm_res_5A = CloneWorkspace(res_5Aini)

for i in range(res_5Aini.getNumberHistograms()):
    area = Integration(res_5Aini, StartWorkspaceIndex=i, EndWorkspaceIndex=i)
    y_norm = norm_res_5A.dataY(i)
    y_norm /= area.readY(0)[0]

# Select range of energy transfer to consider for data treatment: ]-1meV , 1meV[
idx_5A = np.where(np.logical_and(hw_5A > -1.0, hw_5A < 1.0))
index_4_trunc_5A = idx_5A[0].tolist()

# Fit range -1meV < energy < 1 meV
x = hw_5A[index_4_trunc_5A]
ws_5A = CropWorkspace(ws_5Aini, XMin=-1, Xmax=1)
# Same procedure for the normalised resolution
res_5A = CropWorkspace(norm_res_5A,  XMin=-1, XMax=1)

# Extract values of q to be used in parameters of fitting models
q_5A = ws_5A.getAxis(1).extractValues()

# Remove invalid data (negative errors)
for ii in range(len(q_5A)):
    yy = ws_5A.dataY(ii)
    err = ws_5A.dataE(ii)
    for jj in range(ws_5A.blocksize()):
        if err[jj] <= 0:
            yy[jj] = 0
            err[jj] = 0

# Fitting
# Model:
# Resolution convoluted with IsoRotDiff
# + Lorentzian with hwhm proportional to Q**2

single_model_template="""(composite=Convolution,FixResolution=true,NumDeriv=true;\
name=Resolution,Workspace=res_5A,WorkspaceIndex=_WI_;\
(name=IsoRotDiff,Q=_Q_,Height=1,Centre=0,Radius=0.98,Tau=10,N=10,constraints=(0.9<Radius<1.1, -0.1<Centre<0.1, Tau >0);\
name=UserFunction, Formula=scale_factor*D*Q*Q/{pi}/( (x-Centre)*(x-Centre) + D*D*Q*Q*Q*Q ), scale_factor=20., Centre=0., D=0.1, Q=_Q_,constraints=(0.<D<1.)))""".format(pi=pi)

# Loop over Q values
for ii in range(len(q_5A)):

    single_model = single_model_template.replace("_Q_", str(q_5A[ii]))
    single_model = single_model.replace("_WI_", str(ii))

    fit_output = Fit(Function=single_model, InputWorkspace=ws_5A,
                      WorkspaceIndex=ii, StartX=-1, EndX=1,Output='fit')
    # table containing the optimal fit parameters
    paramTable = fit_output.OutputParameters
    print(ii, fit_output.OutputChi2overDoF)
    # print results
    numbers_fitted_param = len(paramTable.column(0))
    for j in range(numbers_fitted_param):
        print(paramTable.column(0)[j], paramTable.column(1)[j])
