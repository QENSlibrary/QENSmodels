# Data to be used for testing implementation of QENS models

## Datafiles and related models and parameters values

For all the files, the `x`-axis corresponds to `\omega`, the energy transfer 
in picoseconds. It is set to be `w = numpy.arange(-2, 2.01, 0.01)` for all the 
following reference data files.

If the model contains more than one function, only the expression of `S(q, w)` 
was considered and recorded in the data file.

For the momentum transfer, we chose `q = 0.71/Angstrom`.


- background_polynomials_ref_data.dat

  `background_polynomials(w, list_coefficients=[1,2,3])` corresponds to 
  `1+2x+3x**2`

- brownian_translational_diffusion_ref_data.dat

  `sqwBrownianTranslationalDiffusion(w, q, scale=1., center=0., D=1.)`
  
- chudley_elliot_diffusion_ref_data.dat

  `sqwChudleyElliotDiffusion(w, q, scale=1, center=0, D=0.23, L=1.)`

- delta_ref_data.dat

  `delta(w, scale=3.3, center=0)`

- delta_lorentz_ref_data.dat

  `sqwDeltaLorentz(w, q, scale=1., center=0.5, A0=0.01, hwhm=1.0)`

- delta_two_lorentz_ref_data.dat

  `sqwDeltaTwoLorentz(w, q, scale=1., center=0, A0=0.01, A1=0.4, hwhm1=0.25, hwhm2=0.75)`

- gaussian_ref_data.dat

  `gaussian(w, scale=1, center=0.25, sigma=0.4)`

- isotropic_rotational_diffusion_ref_data.dat

  `sqwIsotropicRotationalDiffusion(w, q, scale=1.0, center=0.0, radius=2.0, DR=0.05)`

- jump_translational_diffusion_ref_data.dat

  `sqwJumpTranslationalDiffusion(w, q, scale=1, center=0, D=0.23, resTime=1.25)`

- lorentzian_ref_data.dat

  `lorentzian(w, 3.,0.25, 0.4)`

- water_teixeira_ref_data.dat

  `sqwWaterTeixeira(w, q, scale=1, center=0, D=1, resTime=1, radius=1, DR=1)`

