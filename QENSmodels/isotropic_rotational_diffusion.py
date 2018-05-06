import numpy as np
from scipy.special import jn
import QENSmodels


def hwhmIsotropicRotationalDiffusion(q, radius, DR):
    """
    Parameters
    ----------
    q: to be added
        to be added
    radius: float
        to be added
    DR: float
        to be added

    Returns
    -------
    `hwhm`, `eisf`, and `qisf` of IsotropicRotationalDiffusion
    """
    # eisf = np.zeros(q.size)
    numberLorentz = 6
    qisf = np.zeros((q.size, numberLorentz))
    hwhm = np.zeros((q.size, numberLorentz))
    jl = np.zeros((q.size, numberLorentz))
    arg = q * radius
    idx = np.argwhere(arg == 0)
    for i in range(numberLorentz):
        jl[:, i] = np.sqrt(np.pi / 2 / arg) * jn(i + 0.5,
                                                 arg)  # to solve warnings for arg=0
        hwhm[:, i] = np.repeat(i * (i + 1) * DR, q.size)
        if idx.size > 0:
            if i == 0:
                jl[idx, i] = 1.0
            else:
                jl[idx, i] = 0.0
    eisf = jl[:, 0] ** 2
    for i in range(1, numberLorentz):
        qisf[:, i] = (2 * i + 1) * jl[:, i] ** 2
    return hwhm, eisf, qisf


# def sqwIsotropicRotationalDiffusion(w, q, scale, center, radius, DR,
#                                    background, resolution=None):
def sqwIsotropicRotationalDiffusion(w, q, scale, center, radius, DR):
    """
    Model = Isotropic rotational diffusion = A0 + Sum of Lorentzians ...

    Parameters
    ----------
    w: to be added
        to be added
    q: to be added
        to be added
    scale: float
        Scale factor.
    center: float
        Center of peak
    radius: float
        to be added
    DR: float
        to be added
    """

    # Input validation
    q = np.asarray(q, dtype=np.float32)

    # Create output array
    sqw = np.zeros((q.size, w.size))

    # Get widths, EISFs and QISFs of model
    hwhm, eisf, qisf = hwhmIsotropicRotationalDiffusion(q, radius, DR)

    # Number of Lorentzians used to represent the infinite sum in R
    numberLorentz = hwhm.shape[1]

    # Sum of Lorentzians
    for i in range(q.size):
        sqw[i, :] = eisf[i] * QENSmodels.delta(w, scale, center)
        for j in range(1, numberLorentz):
            sqw[i, :] += qisf[i, j] * QENSmodels.lorentzian(w, scale, center, hwhm[i, j])

    # Convolution with resolution function (if given)
    # if resolution is not None:
    #
    #     # Input validation: Check if single resolution function or N spectra
    #     #                   Check dimensions agree with sqw
    #
    #     for i in range(q.size):
    #
    #         if resolution.ndim == 1:
    #             tmp = np.convolve(sqw[i, :], resolution / resolution.sum())
    #         else:
    #             tmp = np.convolve(sqw[i, :],
    #                               resolution[i, :] / resolution[i, :].sum())
    #
    #             # Energy axis non necessarily symmetric --> Position model at center
    #         idxMax = np.argmax(tmp)
    #         idxMin = np.argmin(np.abs(w - center))
    #         sqw[i, :] = tmp[idxMax - idxMin:idxMax - idxMin + w.size]

    # Add flat background
    # sqw += background

    # For Bumps use (needed for final plotting)
    # Using a 'Curve' in bumps for each Q --> needs vector array
    if q.size == 1:
        sqw = np.reshape(sqw, w.size)

    return sqw
