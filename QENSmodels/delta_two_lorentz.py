import numpy as np
import QENSmodels


# def sqwDeltaTwoLorentz(w, q, scale, center, A0, A1, hwhm1, hwhm2, background,
#                        resolution=None):
def sqwDeltaTwoLorentz(w, q, scale, center, A0, A1, hwhm1, hwhm2):
    """
    Model = A0*delta + A1*Lorentzian(Gamma1) + (1-A0-A1)*Lorentzian(Gamma2)

    Parameters
    ----------
    w: to be added
        to be added
    q: to be added
        to be added
    scale: float
        Scale factor.
    center: float
        Peak center.
    A0: to be added
        to be added
    A1: to be added
        to be added
    hwhm1: to be added
        to be added
    hwhm2: to be added
        to be added
    """

    # Input validation
    q = np.asarray(q, dtype=np.float32)

    # Create output array
    sqw = np.zeros((q.size, w.size))

    # Model
    if q.size > 1:
        for i in range(q.size):
            sqw[i, :] = A0[i] * QENSmodels.delta(w, scale, center)
            sqw[i, :] += A1[i] * QENSmodels.lorentzian(w, scale, center, hwhm1[i])
            sqw[i, :] += (1 - A0[i] - A1[i]) * QENSmodels.lorentzian(w, scale, center,
                                                       hwhm2[i])
    else:
        sqw[0, :] = A0 * QENSmodels.delta(w, scale, center)
        sqw[0, :] += A1 * QENSmodels.lorentzian(w, scale, center, hwhm1)
        sqw[0, :] += (1 - A0 - A1) * QENSmodels.lorentzian(w, scale, center, hwhm2)

    # Convolution with resolution function (if given)
    # if resolution is not None:
    #
    #     # Input validation: Check if single resolution function or N spectra
    #     #                   Check dimensions agree with sqw
    #
    #     for i in range(q.size):
    #         if resolution.ndim == 1:
    #             tmp = np.convolve(sqw[i, :], resolution / resolution.sum())
    #         else:
    #             tmp = np.convolve(sqw[i, :],
    #                               resolution[i, :] / resolution[i, :].sum())
    #
    #             # Energy axis non necessarily symmetric --> Position model at center
    #         idxMax = np.argmax(tmp)
    #         idxMin = np.argmin(np.abs(w - center))
    #         sqw[i, :] = tmp[idxMax - idxMin: idxMax - idxMin + w.size]
    #
    # # Add flat background
    # sqw += background

    # For Bumps use (needed for final plotting)
    # Using a 'Curve' in bumps for each Q --> needs vector array
    if q.size == 1:
        sqw = np.reshape(sqw, w.size)

    return sqw
