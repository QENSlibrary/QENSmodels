import numpy as np
import QENSmodels


def hwhmJumpTranslationalDiffusion(q, D=1, resTime=1):
    """
    Parameters
    ----------
    q: to be added
        to be added

    D: float
        Diffusion coefficient. Default to 1.

    resTime: float
       to be added

    Returns
    -------
    hwhm, eisf, and qisf of JumpTranslationalDiffusion
    """
    eisf = np.zeros(q.size)
    qisf = np.ones(q.size)
    hwhm = D * q ** 2 / (1.0 + resTime * D * q ** 2)
    # Force hwhm to be numpy array, even if single value
    hwhm = np.asarray(hwhm, dtype=np.float32)
    hwhm = np.reshape(hwhm, hwhm.size)
    return hwhm, eisf, qisf


def sqwJumpTranslationalDiffusion(w, q, scale=1, center=0, D=1, resTime=1):
    """
    Model = Jump Translational diffusion = Lorentzian of HWHM = D*Q^2 / (1+tau*D*Q^2)

    Parameters
    ----------
    w: to be added
        to be added

    q: to be added
        to be added

    scale: float
        scale factor. Default to 1.

    center: float
        center of peak. Default to 0.

    D: float
        Diffusion coefficient. Default to 1

    resTime: float
        Default to 1.
    """
    # Input validation
    q = np.asarray(q, dtype=np.float32)

    # Create output array
    sqw = np.zeros((q.size, w.size))

    # Get widths, EISFs and QISFs of model
    hwhm, eisf, qisf = hwhmJumpTranslationalDiffusion(q, D, resTime)

    # Model
    for i in range(q.size):
        sqw[i, :] = QENSmodels.lorentzian(w, scale, center, hwhm[i])

    # # Convolution with resolution function (if given)
    # if resolution is not None:
    #  # Input validation: Check if single resolution function or N spectra
    #  #                   Check dimensions agree with sqw
    #     for i in range(q.size):
    #         if resolution.ndim == 1:
    #             tmp = np.convolve(sqw[i, :], resolution / resolution.sum())
    #         else:
    #             tmp = np.convolve(sqw[i, :],
    #                               resolution[i, :] / resolution[i, :].sum())
    # # Energy axis non necessarily symmetric --> Position model at center
    #         idxMax = np.argmax(tmp)
    #         idxMin = np.argmin(np.abs(w - center))
    #         sqw[i, :] = tmp[idxMax - idxMin:idxMax - idxMin + w.size]
    # # Add flat background
    # sqw += background

    # For Bumps use (needed for final plotting)
    # Using a 'Curve' in bumps for each Q --> needs vector array
    if q.size == 1:
        sqw = np.reshape(sqw, w.size)

    return sqw
