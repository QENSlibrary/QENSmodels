"""
mantid_BrownianDiff_fit
===========================

This example shows how to use one of the models of the QENS library in
MantidWorkbench.
To use, simply open this script in MantidWorkbench and run it.
"""

import mantid.simpleapi as mapi
import matplotlib.pyplot as plt
import numpy as np
import QENSmodels

# make fake data
# number of points for the x-axis
nb_points = 500
# number of workspace i.e. number of Q values
selected_wi = 4

# min and max of energy transfer (used below for fitting boundaries)
minE = -4.95
maxE = 4.95

# generated x- and Q-values
hw = np.linspace(-5, 5, nb_points)

Q = np.linspace(0.1, 0.4, selected_wi)
# created fake reference data adding noise to one of the QENS models
added_noise = np.random.normal(0, 1, nb_points)

brownian_diff_noisy = QENSmodels.sqwBrownianTranslationalDiffusion(hw, Q,
                                                                   scale=10,
                                                                   center=0.1,
                                                                   D=5) * \
                      (1 + 0.1 * added_noise) + 0.01 * added_noise

# store in mantid workspace
QENS_data = mapi.CreateWorkspace(DataX=hw,
                                 DataY=brownian_diff_noisy,
                                 NSpec=selected_wi)


# wrap to create mantid fitting function
class my_sqwBrownian_Diffusion(mapi.IFunction1D):
    """ """

    def init(self):
        self.declareParameter("scale", 7.)
        self.declareParameter("center", 0.)
        self.declareParameter("D", 2.)

        self.declareAttribute("Q", 0.2)

    def category(self):
        return 'QuasiElastic'

    def function1D(self, xvals):
        scale = self.getParameterValue("scale")
        center = self.getParameterValue("center")
        D = self.getParameterValue("D")

        q = self.getAttributeValue("Q")

        return QENSmodels.sqwBrownianTranslationalDiffusion(xvals,
                                                            q,
                                                            scale=scale,
                                                            center=center,
                                                            D=D)


# add it to Mantid fitting functions
mapi.FunctionFactory.subscribe(my_sqwBrownian_Diffusion)

""" Fitting
    The following analysis can also be done in Mantid Workbench Fit wizard
"""

""" Below is the template string to create individual model for each spectrum.

    A similar string can be obtained after defining the fitting model on Mantid
    Workbench fit  wizard:

    "Setup" --> "Manage Settup" --> "Copy to Clipboard". This action will save
    the model as a string which you can later paste onto this script.

    Our initial guesses are scale=7., center= 0. and D=2.
"""

single_model_template = \
    """name=my_sqwBrownian_Diffusion,
    $domains=i,scale=7.,center=0.,D=2.,Q=_Q_"""

# Create the string representation of the global model for all spectra:
global_model = "composite=MultiDomainFunction,NumDeriv=true;"
for wi in range(selected_wi):
    # insert Q-value
    single_model = single_model_template.replace("_Q_", str(Q[wi]))
    global_model += f'{single_model};'

# Add ties
global_model += 'ties=(f0.D=f1.D=f2.D=f3.D);constraints=(f0.D>0)'

# Now relate each spectrum to each single-spectrum model: specify range
domain_model = dict()
for wi in range(selected_wi):
    if wi == 0:
        domain_model.update({"InputWorkspace": 'QENS_data',
                             "WorkspaceIndex": str(wi),
                             "StartX": str(-4.95),
                             "EndX": str(4.95)})
    else:
        domain_model.update(
            {"InputWorkspace_" + str(wi): 'QENS_data',
             "WorkspaceIndex_" + str(wi): str(wi),
             "StartX_" + str(wi): str(minE),
             "EndX_" + str(wi): str(maxE)})

# Perform fitting
mapi.Fit(Function=global_model, **domain_model,
         CreateOutput=True, MaxIteractions=500, Output='fit')

"""
 As a result of the fit, three workspaces are created:
 'fit'+"_Parameters" : optimized parameters and Chi-square
 'fit'+"_NormalisedCovarianceMatrix" : correlations between parameters
 'fit'+"_Workspace"  : data, fit, residuals, and model
"""

paramTable = mapi.mtd['fit_Parameters']

# print results
for i in range(4):
    print(f'Workspace {i}:')
    print(f'scale: {paramTable.column(1)[3 * i]:.2f}')
    print(f'center: {paramTable.column(1)[3 * i + 1]:.2f}')
    print(f'D: {paramTable.column(1)[3 * i + 2]:.2f}')

# plot results
fig, ax = plt.subplots(2, 2)

indx_plot = [(0, 0), (0, 1), (1, 0), (1, 1)]
for indx, item in enumerate(mapi.mtd['fit_Workspaces']):
    ax[indx_plot[indx][0], indx_plot[indx][1]].grid()
    ax[indx_plot[indx][0], indx_plot[indx][1]].plot(item.readX(0),
                                                    item.readY(0),
                                                    label='exp')
    ax[indx_plot[indx][0], indx_plot[indx][1]].plot(item.readX(1),
                                                    item.readY(1),
                                                    label='calc')
    ax[indx_plot[indx][0], indx_plot[indx][1]].plot(item.readX(2),
                                                    item.readY(2),
                                                    label='diff')

ax[indx_plot[indx][0], indx_plot[indx][1]].legend()
fig.show()
