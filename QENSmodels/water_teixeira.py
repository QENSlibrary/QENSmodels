import numpy as np
import QENSmodels


#class WaterTeixeira():
#    pass


def sqwWaterTeixeira(w, q, scale, center, D, resTime, radius, DR):
    r"""
    Model = convolution(T, R)
    T = Jump Translational diffusion = Lorentz(Gamma_T)
    R = Isotropic rotational diffusion = A0 + A1*L1 + A2*L2 + ...
    convolution(T,R) = A0*Lorentz(Gamma_T) + A1*Lorentz(Gamma_T+Gamma_1) + A2*Lorentz(Gamma_T+Gamma_2) + ...

    Parameters
    ----------
    w: float, list or :class:`~numpy:numpy.ndarray`
        to be added

    q: float, list or :class:`~numpy:numpy.ndarray`
        to be added

    scale: float
        Scale factor. Default to

    center: float
        Center of peak. Default to

    D: float
        Diffusion coefficient. Default to

    resTime: float
        Residence time . Default to

    radius: float
        Radius of rotation. Default to

    DR: float
        Rotational diffusion coefficient. Default to

    Notes
    -----

    .. math::
       S(\omega, q) =

    References
    ----------
    None
    """
    # Input validation
    q = np.asarray(q, dtype=np.float32)

    # Create output array
    sqw = np.zeros((q.size, w.size))

    # Get widths, EISFs and QISFs of each model
    hwhm1, eisf1, qisf1 = QENSmodels.jump_translational_diffusion.hwhmJumpTranslationalDiffusion(q, D, resTime)
    hwhm2, eisf2, qisf2 = QENSmodels.isotropic_rotational_diffusion.hwhmIsotropicRotationalDiffusion(q, radius, DR)

    # Number of Lorentzians used to represent the infinite sum in R
    numberLorentz = hwhm2.shape[1]

    # Sum of Lorentzians giving the full model
    for i in range(q.size):
        sqw[i, :] = eisf2[i] * QENSmodels.lorentzian(w, scale, center, hwhm1[i])
        for j in range(1, numberLorentz):
            sqw[i, :] += qisf2[i, j] * QENSmodels.lorentzian(w, scale, center,
                                               hwhm1[i] + hwhm2[i, j])

    # For Bumps use (needed for final plotting)
    # Using a 'Curve' in bumps for each Q --> needs vector array
    if q.size == 1:
        sqw = np.reshape(sqw, w.size)

    return sqw
