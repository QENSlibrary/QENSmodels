import numpy as np
import QENSmodels


def hwhmBrownianTranslationalDiffusion(q, D=1.):
    """ Lorentzian model with HWHM equal to :math:`Dq^2`

    Parameters
    ----------
    q: :class:`~numpy:numpy.ndarray`
        momentum transfer (non-fitting, in 1/Angstrom).

    D: float
        diffusion coefficient (in Angstrom^2/ps). Default to 1.

    Returns
    -------
    hwhm: :class:`~numpy:numpy.ndarray`
        half-width half maximum

    eisf: :class:`~numpy:numpy.ndarray`
        elastic incoherent structure factor

    qisf: :class:`~numpy:numpy.ndarray`
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
    r""" Lorentzian model with HWHM equal to :math:`Dq^2`

    Parameters
    ----------
    w: float, list or :class:`~numpy:numpy.ndarray`
        energy transfer (in ps)

    q: float, list or :class:`~numpy:numpy.ndarray`
        momentum transfer (non-fitting, in 1/Angstrom)

    scale: float
        scale factor. Default to 1.

    center: float
        peak center. Default to 0.

    D: float
        diffusion coefficient (in Angstrom^2/ps). Default to 1.

    Return
    ------
    :class:`~numpy:numpy.ndarray`

    Examples
    --------
    >>> QENSmodels.sqwBrownianTranslationalDiffusion(1, 1, 1, 0, 1)
    array([ 0.15915494])

    >>> QENSmodels.sqwBrownianTranslationalDiffusion([1, 2, 3], [0.3, 0.4], 1, 0, 1)
    array([[ 0.02841771,  0.0071475 ,  0.00318024],
           [ 0.04965834,  0.01265143,  0.00564279]])


    Notes
    -----
    The `sqwBrownianTranslationalDiffusion` is expressed as

    .. math::

        S(q, \omega) =
        \text{Lorentzian}(\omega, \text{scale}, \text{center}, Dq^2)

    """
    # Input validation
    w = np.asarray(w, dtype=np.float32)

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
