from __future__ import print_function
import numpy as np
# import scipy.constants as csts


try:
    import QENSmodels
except ImportError:
    print('Module QENSmodels not found')


def hwhmBrownianTranslationalDiffusion(q, D=1.):
    """ Lorentzian model with half width half maximum equal to :math:`Dq^2`

    Returns some characteristics of `BrownianTranslationalDiffusion` as
    functions of the momentum transfer `q`:
    the half-width half-maximum (`hwhm`), the elastic incoherent structure
    factor (`eisf`), and the quasi-elastic incoherent structure factor (`qisf`)

    Parameters
    ----------
    q: :class:`~numpy:numpy.ndarray`
        momentum transfer (non-fitting, in 1/Angstrom).

    D: float
        diffusion coefficient (in Angstrom**2/ps). Default to 1.

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

    # TODO discuss with users to find most suitable option for units
    # Convert units: (A^2 / ps) * A^-2 = ps^-1 --> meV
    # coefficient peta to convert eV s -> meV ps
    # hwhm *= csts.physical_constants["Planck constant over 2 pi in eV s"][0] * csts.peta  # noqa

    # Force hwhm to be numpy array, even if single value
    hwhm = np.asarray(hwhm, dtype=np.float32)
    hwhm = np.reshape(hwhm, hwhm.size)
    return hwhm, eisf, qisf


def sqwBrownianTranslationalDiffusion(w, q, scale=1., center=0., D=1.):
    r""" Lorentzian model with half width half maximum  equal to :math:`Dq^2`

    It corresponds to a continuous long-range isotropic translational
    diffusion.

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
        diffusion coefficient (in Angstrom**2/ps). Default to 1.

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
    * The `sqwBrownianTranslationalDiffusion` is expressed as

    .. math::

        S(q, \omega) =
        \text{Lorentzian}(\omega, \text{scale}, \text{center}, Dq^2)


    * The incoherent dynamic structure factor
      `sqwBrownianTranslationalDiffusion` corresponds to

      - in real space, the probability of finding a particle at a distance `r`
        from its initial position is a Gaussian function of space `r`

        .. math::

           G(r, t)=(\frac{\text{scale}}{4\pi D t})^{3/2}\exp (-\frac{r^2}{4Dt})

      - in reciprocal space, the autocorrelation function is

        .. math::

           I(q, t) = \int G(r, t) dr = \text{scale} \exp (-Dq^2 t)

    * This model works reasonably well at low *q*. Other models, such as
    "Chudley-Elliot", have been developed to describe the microscopic
    mechanisms that deviate from the Fickian behavior (`hwhm` proportional
    to `q` squared)

    References
    ----------

    * T. Springer, Quasielastic neutron scattering for the investigation
      of diffusive motions in liquids and solids,
      *Springer Tracts in Modern Physics* **64** (1972)
      `link <https://www.springer.com/gp/book/9783662149577>`_

    * G. H. Vineyard, *Phys. Rev.* **110**, 999-1010 (1958)

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
