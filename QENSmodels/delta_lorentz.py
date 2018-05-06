import numpy as np
import QENSmodels


def sqwDeltaLorentz(w, q, scale=1, center=0, A0=0., hwhm=1):
    """
    Model corresponding to a delta representing a fraction p of
    fixed atoms and a Lorentzian corresponding to a Brownian
    Translational diffusion model for the remaining (1 - p) atoms.

    Model = A0*delta + (1-A0)*Lorentz(Gamma)

    Parameters
    ----------
    w: to be added
        to be added
    q: to be added
        to be added
    scale: float
        Scale factor. Default to 1.
    center: float
        Peak center. Default to 0.
    A0: to be added
        to be added
    hwhm: to be added
        to be added. Default to 1.
    """

    # Input validation
    q = np.asarray(q, dtype=np.float32)

    # Create output array
    sqw = np.zeros((q.size, w.size))

    # Model
    if q.size > 1:
        for i in range(q.size):
            sqw[i, :] = A0[i] * QENSmodels.delta(w, scale, center)
            sqw[i,:] += (1-A0[i]) * QENSmodels.lorentzian(w, scale, center, hwhm[i])
    else:
        sqw[0,:] = A0 * QENSmodels.delta(w, scale, center)
        sqw[0,:] += (1-A0) * QENSmodels.lorentzian(w, scale, center, hwhm)

    # Convolution with resolution function (if given)
    # if resolution is not None:
    #     # Input validation: Check if single resolution function or N spectra
    #     #                   Check dimensions agree with sqw
    #     for i in range(q.size):
    #         if resolution.ndim == 1:
    #             tmp = np.convolve(sqw[i, :], resolution / resolution.sum())
    #         else:
    #             tmp = np.convolve(sqw[i, :],
    #                               resolution[i, :] / resolution[i, :].sum())
    #      # Energy axis non necessarily symmetric --> Position model at center
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
