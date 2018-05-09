import numpy as np
import QENSmodels


def hwhmBrownianTranslationalDiffusion(q, D=1.):
    """
    Returns some characteristics of `BrownianTranslationalDiffusion` model

    Parameters
    ----------
    q: :class:`~numpy:numpy.ndarray`
        Momentum transfer

    D: float
        Diffusion coefficient. Default to 1.

    Returns
    -------
    `hwhm`: :class:`~numpy:numpy.ndarray`
        half-width half maximum

    `eisf`: :class:`~numpy:numpy.ndarray`
        elastic incoherent structure factor

    `qisf`: :class:`~numpy:numpy.ndarray`
        quasi-elastic incoherent structure factor
    """
    eisf = np.zeros(q.size)
    qisf = np.ones(q.size)
    hwhm = D * q ** 2
    # Force hwhm to be numpy array, even if single value
    hwhm = np.asarray(hwhm, dtype=np.float32)
    hwhm = np.reshape(hwhm, hwhm.size)
    return hwhm, eisf, qisf


def sqwBrownianTranslationalDiffusion(w, q, scale=1., center=0., D=1.):
    r"""

    Model = Brownian Translational diffusion = Lorentzian of HWHM = :math:`Dq^2`

    Parameters
    ----------
    w: float, list or :class:`~numpy:numpy.ndarray`
        to be added

    q: float, list or :class:`~numpy:numpy.ndarray`
        momentum transfer

    scale: float
        Scale factor. Default to 1.

    center: float
        Peak center. Default to 0.

    D: float
        Diffusion coefficient. Default to 1.

    Examples
    --------
    >>> QENSmodels.sqwBrownianTranslationalDiffusion()


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

    # For Bumps use (needed for final plotting)
    # Using a 'Curve' in bumps for each Q --> needs vector array
    if q.size == 1:
        sqw = np.reshape(sqw, w.size)

    return sqw
