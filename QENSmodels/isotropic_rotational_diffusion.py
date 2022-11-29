import numpy as np
from scipy.special import spherical_jn
from typing import Union, Tuple

try:
    import QENSmodels
except ImportError:
    print('Module QENSmodels not found')


def hwhmIsotropicRotationalDiffusion(
        q: Union[float, list, np.ndarray],
        radius: float = 1.0,
        DR: float = 1.0
) -> Tuple[np.ndarray, np.ndarray, np.ndarray]:
    """
    Returns some characteristics of `IsotropicRotationalDiffusion` as functions
    of the momentum transfer `q`:
    the half-width half-maximum (`hwhm`), the elastic incoherent structure
    factor (`eisf`), and the quasi-elastic incoherent structure factor (`qisf`)

    Parameters
    ----------
    q: float, list or :class:`~numpy:numpy.ndarray`
        momentum transfer (non-fitting, in 1/Angstrom)

    radius: float
        radius of rotation (in Angstrom). Default to 1.

    DR: float
        rotational diffusion coefficient (in 1/ps). Default to 1.

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
    >>> hwhm, eisf, qisf = hwhmIsotropicRotationalDiffusion(1., 1., 1.)
    >>> hwhm[0, 0]
    0.0
    >>> hwhm[0, 1]
    2.0
    >>> hwhm[0, 2]
    6.0
    >>> hwhm[0, 3]
    12.0
    >>> hwhm[0, 4]
    20.0
    >>> hwhm[0, 5]
    30.0
    >>> round(eisf[0], 3)
    0.708
    >>> qisf[0, 0]
    0.0
    >>> round(qisf[0, 1], 3)
    0.272
    >>> round(qisf[0, 2], 3)
    0.019
    >>> round(qisf[0, 3], 3)
    0.001
    >>> round(qisf[0, 4], 3)
    0.0
    >>> round(qisf[0, 5], 3)
    0.0

    """
    # input validation
    if radius <= 0:
        raise ValueError('radius should be strictly positive')
    if DR <= 0:
        raise ValueError('DR, the rotational diffusion coefficient, '
                         'should be strictly positive')

    q = np.asarray(q, dtype=np.float32)

    numberLorentz = 6
    qisf = np.zeros((q.size, numberLorentz))
    hwhm = np.zeros((q.size, numberLorentz))
    jl = np.zeros((q.size, numberLorentz))

    arg = q * radius

    idx = np.argwhere(arg == 0)
    for i in range(numberLorentz):

        # to solve warnings for arg=0
        jl[:, i] = spherical_jn(i, arg)

        hwhm[:, i] = np.repeat(i * (i + 1) * DR, q.size)

        if idx.size > 0:
            if i == 0:
                jl[idx, i] = 1.0
            else:
                jl[idx, i] = 0.0
    eisf = jl[:, 0] ** 2
    for i in range(1, numberLorentz):
        qisf[:, i] = (2 * i + 1) * jl[:, i] ** 2
    return hwhm, eisf, qisf


def sqwIsotropicRotationalDiffusion(
        w: Union[float, list, np.ndarray],
        q: Union[float, list, np.ndarray],
        scale: float = 1.0,
        center: float = 0.0,
        radius: float = 1.0,
        DR: float = 1.0
) -> Union[float, list, np.ndarray]:
    r"""
    Model `Isotropic rotational diffusion` = A_0 delta + Sum of Lorentzians ...

    Continuous rotational diffusion on the surface of a sphere of radius
    `radius`

    In this model, the reorientation of the molecule is due to small-angle
    random rotations.


    Parameters
    ----------

    w: list or :class:`~numpy:numpy.ndarray`
        energy transfer (in 1/ps)

    q: float, list or :class:`~numpy:numpy.ndarray`
        momentum transfer (non-fitting, in 1/Angstrom)

    scale: float
        scale factor. Default to 1.

    center: float
        center of peak. Default to 0.

    radius: float
        radius of rotation (in Angstrom). Default to 1.

    DR: float
        rotational diffusion coefficient (in 1/ps). Default to 1.

    Return
    ------
    :class:`~numpy:numpy.ndarray`
        output array

    Examples
    --------
    >>> sqw = sqwIsotropicRotationalDiffusion([1,2,3], 1, 1, 0, 1, 1)
    >>> round(sqw[0], 3)
    0.036
    >>> round(sqw[1], 3)
    0.023
    >>> round(sqw[2], 3)
    0.014


    >>> sqw = sqwIsotropicRotationalDiffusion([-0.1, 0., 0.1], [0.3, 0.4], 1, 0, 1, 0.5)  # noqa: E501
    >>> round(sqw[0, 0], 3)
    0.009
    >>> round(sqw[0, 1], 3)
    9.713
    >>> round(sqw[0, 2], 3)
    0.009
    >>> round(sqw[1, 0], 3)
    0.016
    >>> round(sqw[1, 1], 3)
    9.494
    >>> round(sqw[1, 2], 3)
    0.016


    Notes
    -----
    * There are 6 terms in the sum (see the mathematical expression below)

    * The `sqwIsotropicRotationalDiffusion` is expressed as

     .. math::

        S(q, \omega) &= j_0^2(q\ \text{radius})\delta(\omega, \text{scale},
        \text{center})\\
        &+ \sum_{i=1} ^6 (2i + 1) j_i^2(q\ \text{radius})
        \text{Lorentzian}(\omega, \text{scale}, \text{center}, i(i+1)\text{DR})

     where :math:`j_i, i=1..6` are spherical Bessel functions of order i.

    References
    ----------

    P. A. Egelstaff, *J. Chem. Phys.* **53**, 2590-2598 (1970)
    `link <https://aip.scitation.org/doi/abs/10.1063/1.1674374?journalCode=jcp>`__

    """

    # Input validation
    w = np.asarray(w)

    q = np.asarray(q, dtype=np.float32)

    # Create output array
    sqw = np.zeros((q.size, w.size))

    # Get widths, EISFs and QISFs of model
    hwhm, eisf, qisf = hwhmIsotropicRotationalDiffusion(q, radius, DR)

    # Number of Lorentzians used to represent the infinite sum in R
    numberLorentz = hwhm.shape[1]

    # Sum of Lorentzians
    for i in range(q.size):
        sqw[i, :] = eisf[i] * QENSmodels.delta(w, scale, center)
        for j in range(1, numberLorentz):
            sqw[i, :] += qisf[i, j] * QENSmodels.lorentzian(w, scale, center,
                                                            hwhm[i, j])

    # For Bumps use (needed for final plotting)
    # Using a 'Curve' in bumps for each Q --> needs vector array
    if q.size == 1:
        sqw = np.reshape(sqw, w.size)

    return sqw


if __name__ == "__main__":
    import doctest
    doctest.testmod()
