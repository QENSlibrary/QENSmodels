from __future__ import print_function
import numpy as np

try:
    import QENSmodels
except ImportError:
    print('Module QENSmodels not found')


def hwhmBrownianTranslationalDiffusion(q, D=1.):
    """ Lorentzian model with half width half maximum equal to :math:`Dq^2`

    Parameters
    ----------
    q: :class:`~numpy:numpy.ndarray`
        momentum transfer (non-fitting, in 1/Angstrom).

    D: float
        diffusion coefficient (in Angstrom:math:`^2`/ps). Default to 1.


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
    >>> hwhm, eisf, qisf = hwhmBrownianTranslationalDiffusion(1.)
    >>> hwhm[0]
    1.0
    >>> eisf[0]
    0.0
    >>> qisf[0]
    1.0

    >>> hwhm, eisf, qisf = hwhmBrownianTranslationalDiffusion([1., 2.], 1.)
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
    if D > 0:
        hwhm = D * q ** 2
    else:
        raise ValueError('D, the diffusion coefficient, should be positive')
    # Force hwhm to be numpy array, even if single value
    hwhm = np.asarray(hwhm, dtype=np.float32)
    hwhm = np.reshape(hwhm, hwhm.size)
    return hwhm, eisf, qisf


def sqwBrownianTranslationalDiffusion(w, q, scale=1., center=0., D=1.):
    r""" Lorentzian model with half width half maximum  equal to :math:`Dq^2`

    It corresponds to a continuous long-range isotropic translational
    diffusion.

    This model corresponds to a Brownian motion, where particles collide
    randomly between them. Between two collisions, one particle moves
    along a straight line. After a collision, it goes in a random direction,
    independent of the previous one.

    This model can be used to represent the translation component of the
    dynamic structure factor at low Q, where the corresponding investigated
    distance in real space are large enough to imply a large number of jumps.
    Deviations are expected at high Q values, where specific details of the
    jump mechanism start to be observable. In this case, such details need
    to be introduced in the scattering model, as e.g. in the Chudley-Elliot
    model.

    Parameters
    ----------
    w: float, list or :class:`~numpy:numpy.ndarray`
        energy transfer (in 1/ps)

    q: float, list or :class:`~numpy:numpy.ndarray`
        momentum transfer (non-fitting, in 1/Angstrom)

    scale: float
        scale factor. Default to 1.

    center: float
        peak center. Default to 0.

    D: float
        diffusion coefficient (in Angstrom:math:`^2`/ps). Default to 1.

    Return
    ------
    :class:`~numpy:numpy.ndarray`
        output array

    Examples
    --------
    >>> sqw = sqwBrownianTranslationalDiffusion(1, 1, 1, 0, 1)
    >>> round(sqw[0], 3)
    0.159

    >>> sqw = sqwBrownianTranslationalDiffusion([1, 2, 3], [0.3, 0.4], 1, 0, 1)
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


if __name__ == "__main__":
    import doctest
    doctest.testmod()
