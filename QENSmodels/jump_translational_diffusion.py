import numpy as np
import QENSmodels


def hwhmJumpTranslationalDiffusion(q, D=2.3, resTime=1.25):
    """
    Returns some characteristics of `JumpTranslationalDiffusion`

    Parameters
    ----------
    q: float, list or :class:`~numpy:numpy.ndarray`
        Momentum transfer

    D: float
        Diffusion coefficient. Default to 2.3.

    resTime: float
        to be added. Default to 1.25.

    Returns
    -------
    `hwhm`: :class:`~numpy:numpy.ndarray`
        half-width half maximum

    `eisf`: :class:`~numpy:numpy.ndarray`
        elastic incoherent structure factor

    `qisf`: :class:`~numpy:numpy.ndarray`
        quasi-elastic incoherent structure factor

    Notes
    -----
    Default values

    """
    eisf = np.zeros(q.size)
    qisf = np.ones(q.size)
    hwhm = D * q ** 2 / (1.0 + resTime * D * q ** 2)
    # Force hwhm to be numpy array, even if single value
    hwhm = np.asarray(hwhm, dtype=np.float32)
    hwhm = np.reshape(hwhm, hwhm.size)
    return hwhm, eisf, qisf


def sqwJumpTranslationalDiffusion(w, q, scale=1, center=0, D=2.3, resTime=1.25):
    """
    Model = Jump Translational diffusion = Lorentzian of HWHM = D*Q^2 / (1+tau*D*Q^2)

    Parameters
    ----------
    w: float, list or :class:`~numpy:numpy.ndarray`
        to be added

    q: float, list or :class:`~numpy:numpy.ndarray`
        Momentum transfer.

    scale: float
        Scale factor. Default to 1.

    center: float
        Center of peak. Default to 0.

    D: float
        Diffusion coefficient. Default to 1

    resTime: float
        Residence time. Default to 1.
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

    # For Bumps use (needed for final plotting)
    # Using a 'Curve' in bumps for each Q --> needs vector array
    if q.size == 1:
        sqw = np.reshape(sqw, w.size)

    return sqw
