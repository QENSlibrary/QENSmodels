from __future__ import print_function
import numpy as np

try:
    import QENSmodels
except ImportError:
    print('Module QENSmodels not found')


def hwhmChudleyElliottDiffusion(q, D=0.23, L=1.0):
    """ Returns some characteristics of `ChudleyElliottDiffusion` as functions
    of the momentum transfer `q`:
    the half-width half-maximum (`hwhm`), the elastic incoherent structure
    factor (`eisf`), and the quasi-elastic incoherent structure factor (`qisf`)

    Parameters
    ----------

    q: float, list or :class:`~numpy:numpy.ndarray`
        momentum transfer (non-fitting, in 1/Angstrom)

    D: float
        diffusion coefficient (in Angstrom^2/ps). Default to 0.23.

    L: float
        jump length (in Angstrom). Default to 1.0.


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
    >>> hwhm, eisf, qisf = hwhmChudleyElliottDiffusion([1., 2.], 0.5, 1.5)
    >>> round(hwhm[0], 3), round(hwhm[1], 3)
    (0.447, 1.271)
    >>> eisf
    array([0., 0.])
    >>> qisf
    array([1., 1.])

    """
    # input validation
    if D <= 0:
        raise ValueError('The diffusion coefficient should be positive')
    if L <= 0:
        raise ValueError('L, the jump length, should be positive')

    q = np.asarray(q, dtype=np.float32)

    eisf = np.zeros(q.size)
    qisf = np.ones(q.size)
    hwhm = 6. * D * (1. - np.sinc(q * L / np.pi)) / L ** 2

    # Force hwhm to be numpy array, even if single value
    hwhm = np.asarray(hwhm, dtype=np.float32)
    hwhm = np.reshape(hwhm, hwhm.size)

    return hwhm, eisf, qisf


def sqwChudleyElliottDiffusion(w, q, scale=1, center=0, D=0.23, L=1.0):
    r""" Lorentzian model with half width half maximum equal to
    :math:`\frac{6D}{L^2}(1 - \frac{sin(QL/pi)}{QL/pi})`

    It is a model originally developed for jump diffusion in
    liquids. But it can also be applied to diffusion in
    crystalline lattices.

    Atoms or molecules are `caged` by other atoms and jump into
    a neighbouring cage from time to time.

    The jump length `L` is identical for all sites.

    Parameters
    ----------

    w: float, list or :class:`~numpy:numpy.ndarray`
        energy transfer (in 1/ps)

    q: float, list or :class:`~numpy:numpy.ndarray`
        momentum transfer (non-fitting, in 1/Angstrom).

    scale: float
        scale factor. Default to 1.

    center: float
        center of peak. Default to 0.

    D: float
        diffusion coefficient (in Angstrom^2/ps). Default to 0.23.

    L: float
        jump distance (in Angstrom). Default to 1.0.

    Return
    ------

    :class:`~numpy:numpy.ndarray`
        output array


    Examples
    --------
    >>> sqw = sqwChudleyElliottDiffusion([1, 2, 3], 1, 1, 0, 1, 1)
    >>> round(sqw[0], 3)
    0.159
    >>> round(sqw[1], 3)
    0.062
    >>> round(sqw[2], 3)
    0.031

    >>> sqw = sqwChudleyElliottDiffusion(1, 1, 1, 0, 1, 1)
    >>> round(sqw[0], 3)
    0.159


    Notes
    -----

    * The `sqwChudleyElliottDiffusion` is expressed as

      .. math::

          S(q, \omega) = \text{Lorentzian}(\omega, \text{scale}, \text{center},
          \frac{6D}{l^2}(1 - \frac{sin(Ql/pi)}{Ql/pi}))

    * Note that an equivalent expression is

      .. math::

          S(q, \omega) = \text{Lorentzian}(\omega, \text{scale}, \text{center},
          \frac{1}{\tau}(1 - \frac{sin(Ql/pi)}{Ql/pi}))

      with :math:`\tau=\frac{l^2}{6D}`.


    References
    ----------

    * R. Hempelmann, Quasielastic Neutron Scattering and Solid State Diffusion
     (Oxford, 2000).

    * C. T. Chudley and R. J. Elliott,  *Proc. Phys. Soc.* **77**,
      353-361 (1961)
`link <https://iopscience.iop.org/article/10.1088/0370-1328/77/2/319/meta>`_

    """
    # Input validation
    w = np.asarray(w)

    q = np.asarray(q, dtype=np.float32)

    # Create output array
    sqw = np.zeros((q.size, w.size))

    # Get widths, EISFs and QISFs of model
    hwhm, eisf, qisf = hwhmChudleyElliottDiffusion(q, D, L)

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
