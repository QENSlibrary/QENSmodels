from mantid.simpleapi import *
import numpy as np
from scipy.integrate import simps
from scipy.constants import pi


import matplotlib.pyplot as plt

path = '/Users/celinedurniak/Documents/WorkESS/QENS_library/QENSmodels/examples/'
# path='/home/celine/development/QENSmodels-master/examples/'
# experimental data
ws_5Aini = LoadLamp(path+'H2O_293K_5A.hdf')

# vanadium
res_5Aini = LoadLamp(path+'V_273K_5A.hdf')

hw_5A = ws_5Aini.readX(0)

idx_5A = np.where(np.logical_and(hw_5A > -1.0, hw_5A < 1.0))
index_4_trunc_5A = idx_5A[0].tolist()

print(ws_5Aini.getNumberHistograms(), ws_5Aini.blocksize())
print(res_5Aini.getNumberHistograms(), res_5Aini.blocksize())

# Force resolution function to have unit area
norm_res_5A = CloneWorkspace(res_5Aini)

for i in range(res_5Aini.getNumberHistograms()):
    area = Integration(res_5Aini, StartWorkspaceIndex=i, EndWorkspaceIndex=i)
    y_norm = norm_res_5A.dataY(i)
    y_norm /= area.readY(0)[0]

# Fit range -1meV < energy < 1 meV
x = hw_5A[index_4_trunc_5A]

# Apply truncation to data
ws_5A = CropWorkspace(ws_5Aini, XMin=-1, Xmax=1)

# Same procedure for normalised resolution
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

""" Fitting Model:
 S(Q,E) = Convolution(Resolution, IsoRotDiff + Lorentzian with fwhm proportional to Q**2)
 We do a global fit (all spectra)
"""

N=6 # maximum number of components for IsoRotDiff
single_model_template="""(composite=Convolution,FixResolution=true,NumDeriv=true;\
name=Resolution,Workspace=res_5A,WorkspaceIndex=_WI_;\
(name=IsoRotDiff,Q=_Q_,f0.Height=20,f0.Centre=0,f0.Radius=0.98,Tau=2.;\
name=UserFunction, Formula=scale_factor*D*Q*Q/{pi}/( (x-Centre)*(x-Centre) + D*D*Q*Q*Q*Q ), scale_factor=20, Centre=0., D=0.1, Q=_Q_);\
ties=(f1.f0.f0.Height=f1.f1.scale_factor))""".format(pi=pi)

# Now create the string representation of the global model (all spectra, all Q-values):
global_model="composite=MultiDomainFunction,NumDeriv=true;"
wi=0
for Q in q_5A:
    single_model = single_model_template.replace("_Q_", str(Q))  # insert Q-value
    single_model = single_model.replace("_WI_", str(wi))  # workspace index
    global_model += "(composite=CompositeFunction,NumDeriv=true,$domains=i;{0});\n".format(single_model)
    wi+=1
# The Radius, Tau, and D are the same for all spectra, thus tie them:
ties=['='.join(["f{0}.f0.f1.f0.f0.Radius".format(wi) for wi in reversed(range(len(q_5A)))]),
   '='.join(["f{0}.f0.f1.f0.f1.Tau".format(wi) for wi in reversed(range(len(q_5A)))]),
   '='.join(["f{0}.f0.f1.f1.D".format(wi) for wi in reversed(range(len(q_5A)))])]
global_model += "ties=("+','.join(ties)+')'  # tie Radius, Tau and D

# Now relate each domain(i.e. spectrum) to each single model
domain_model=dict()
for wi in range(len(q_5A)):
    if wi == 0:
        domain_model.update({"InputWorkspace": ws_5A.name(), "WorkspaceIndex": str(wi),
            "StartX": "-1", "EndX": "1"})
    else:
        domain_model.update({"InputWorkspace_"+str(wi): ws_5A.name(), "WorkspaceIndex_"+str(wi): str(wi),
            "StartX_"+str(wi): "-1", "EndX_"+str(wi): "1"})

# Invoke the Fit algorithm using global_model and domain_model:
output_workspace = "glofit_"+ws_5A.name()
fit_output = Fit(Function=global_model, Output=output_workspace, CreateOutput=True, MaxIterations=500, **domain_model)

# Print some results
fitWorkspace = fit_output.OutputWorkspace
paramTable = fit_output.OutputParameters

# print results for refined parameters
print('Table of refined parameters: Name Value Error')

for i in range(paramTable.rowCount()):
    print(paramTable.column(0)[i],
          paramTable.column(1)[i],
          paramTable.column(2)[i])

# Plot results: one plot / spectrum showing experimental, fitted data
# and difference

for indx, item in enumerate(fitWorkspace.getNames()):
    x = mtd[item].readX(0)
    plt.plot(x, mtd[item].readY(0), label="Data")
    plt.plot(x, mtd[item].readY(1), label="Model")
    plt.plot(x, mtd[item].readY(2), label="Error")
    plt.xlabel('Energy transfer (meV)')
    plt.ylabel('S(Q,E)')
    plt.legend()
    plt.grid()
    plt.title(item + r", Q={:.1f} $\AA$".format(q_5A[indx]))
    plt.show()
