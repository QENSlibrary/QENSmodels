import numpy as np
import QENSmodels


def hwhmBrownianTranslationalDiffusion(q, D=1.):
    """
    Returns some characteristics of `BrownianTranslationalDiffusion`

    Parameters
    ----------
    q: :class:`~numpy:numpy.ndarray`
        wavevector
    D: float
        diffusion coefficient. Default to 1.

    Returns
    -------
    `hwhm`:
        half-width half maximum
    `eisf`:
        elastic incoherent structure factor
    `qisf`:
        quasi-elastic incoherent structure factor
    """
    eisf = np.zeros(q.size)
    qisf = np.ones(q.size)
    hwhm = D * q ** 2
    # Force hwhm to be numpy array, even if single value
    hwhm = np.asarray(hwhm, dtype=np.float32)
    hwhm = np.reshape(hwhm, hwhm.size)
    return hwhm, eisf, qisf


#def sqwBrownianTranslationalDiffusion(w, q, scale, center, D, background,
#                                      resolution=None):
def sqwBrownianTranslationalDiffusion(w, q, scale=1., center=0., D=1.):
    r"""
    Model = Brownian Translational diffusion = Lorentzian of HWHM = :math:`Dq^2`

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
    D: float
        Diffusion coefficient. Default to

    Notes
    -----
    .. math::
        S(\omega, q) = Lorentzian (\omega, scale, center, Dq^2)
    """

    # Input validation
    q = np.asarray(q, dtype=np.float32)

    # Create output array
    sqw = np.zeros((q.size, w.size))

    # Get widths, EISFs and QISFs of model
    hwhm, eisf, qisf = hwhmBrownianTranslationalDiffusion(q, D)

    # Model
    for i in range(q.size):
        sqw[i, :] = QENSmodels.lorentzian(w, scale, center, hwhm[i])

    # Convolution with resolution function (if given)
    # if resolution is not None:
        # # Input validation: Check if single resolution function or N spectra
        # #                   Check dimensions agree with sqw

        # for i in range(q.size):
        #
        #     if resolution.ndim == 1:
        #         tmp = np.convolve(sqw[i, :], resolution / resolution.sum())
        #     else:
        #         tmp = np.convolve(sqw[i, :],
        #                           resolution[i, :] / resolution[i, :].sum())
        #
        #         # Energy axis non necessarily symmetric --> Position model at center
        #     idxMax = np.argmax(tmp)
        #     idxMin = np.argmin(np.abs(w - center))
        #     sqw[i, :] = tmp[idxMax - idxMin:idxMax - idxMin + w.size]

    # Add flat background
    # sqw += background

    # For Bumps use (needed for final plotting)
    # Using a 'Curve' in bumps for each Q --> needs vector array
    if q.size == 1:
        sqw = np.reshape(sqw, w.size)

    return sqw
