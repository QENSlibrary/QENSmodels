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

    Examples
    --------
    >>> hwhm, eisf, qisf = QENSmodels.hwhmBrownianTranslationalDiffusion(1.)
    >>> hwhm[0]
    1.0
    >>> eisf[0]
    0.0
    >>> qisf[0]
    1.0

    >>> hwhm, eisf, qisf = QENSmodels.hwhmBrownianTranslationalDiffusion([1., 2.], 1.)
    >>> hwhm[0]
    1.0
    >>> hwhm[1]
    4.0
    >>> eisf[0]
    0.0
    >>> eisf[1]
    0.0
    >>> qisf[0]
    1.0
    >>> qisf[1]
    1.0

    """
    # Input validation
    q = np.asarray(q, dtype=np.float32)

    eisf = np.zeros(q.size)
    qisf = np.ones(q.size)
    hwhm = D * q ** 2
    # Force hwhm to be numpy array, even if single value
    hwhm = np.asarray(hwhm, dtype=np.float32)
    hwhm = np.reshape(hwhm, hwhm.size)
    return hwhm, eisf, qisf


def sqwBrownianTranslationalDiffusion(w, q, scale=1., center=0., D=1.):
    r""" Lorentzian model with HWHM equal to :math:`Dq^2`

    It corresponds to a continuous long-range isotropic translational diffusion.

    The broadening of the elastic line is q-dependent

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
        output array

    Examples
    --------
    >>> sqw = QENSmodels.sqwBrownianTranslationalDiffusion(1, 1, 1, 0, 1)
    >>> round(sqw, 3)
    0.159

    >>> sqw = QENSmodels.sqwBrownianTranslationalDiffusion([1, 2, 3], [0.3, 0.4], 1, 0, 1)
    >>> round(sqw[0, 0], 3)
    0.028
    >>> round(sqw[0, 1], 3)
    0.007
    >>> round(sqw[0, 2], 3)
    0.003
    >>> round(sqw[1, 0], 3)
    0.05
    >>> round(sqw[1, 1], 3)
    0.013
    >>> round(sqw[1, 2], 3)
    0.006

    Notes
    -----
    The `sqwBrownianTranslationalDiffusion` is expressed as

    .. math::

        S(q, \omega) =
        \text{Lorentzian}(\omega, \text{scale}, \text{center}, Dq^2)

    """
    # Input validation
    w = np.asarray(w)
    # print('w size', w.size)

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
