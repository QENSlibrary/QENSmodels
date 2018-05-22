import numpy as np
from scipy.special import jn
import QENSmodels


def hwhmIsotropicRotationalDiffusion(q, radius=1.0, DR=1.0):
    """
    Returns some characteristics of `IsotropicRotationalDiffusion`

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
    """

    numberLorentz = 6
    qisf = np.zeros((q.size, numberLorentz))
    hwhm = np.zeros((q.size, numberLorentz))
    jl = np.zeros((q.size, numberLorentz))
    arg = q * radius
    idx = np.argwhere(arg == 0)
    for i in range(numberLorentz):
        jl[:, i] = np.sqrt(np.pi / 2 / arg) * jn(i + 0.5,
                                                 arg)  # to solve warnings for arg=0
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


def sqwIsotropicRotationalDiffusion(w, q, scale=1.0, center=0.0, radius=1.0, DR=1.0):
    r"""
    Model `Isotropic rotational diffusion` = A_0 delta + Sum of Lorentzians ...

    Continuous rotational diffusion on the surface of a sphere

    In this model, the reorientation of the molecule is due to small-angle
    random rotations.


    Parameters
    ----------

    w: list or :class:`~numpy:numpy.ndarray`
        energy transfer (in ps)

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

    Examples
    --------
    >>> QENSmodels.sqwIsotropicRotationalDiffusion([1,2,3], 1, 1, 0, 1, 1)
    array([ 0.03565415,  0.02258717,  0.01415628])


    >>> QENSmodels.sqwIsotropicRotationalDiffusion([-0.1, 0., 0.1], [0.3, 0.4], 1, 0, 1, 0.5)
    array([[  9.30472971e-03,   9.71297465e+00,   9.30472971e-03],
          [  1.63369580e-02,   9.49441487e+00,   1.63369580e-02]])


    Notes
    -----
    * There are 6 terms in the sum

    * The `sqwIsotropicRotationalDiffusion` is expressed as

     .. math::

        S(\omega, q) = j_0^2(q \text{radius})\delta(\omega, \text{scale},
        \text{center}) + \sum_{i=1} ^6 (2i + 1) j_i^2(q\text{radius})
        \text{Lorentzian}(\omega, \text{scale}, \text{center}, \text{DR} i(i+1))

     where :math:`j_i, i=0..6` are spherical Bessel functions.

    """

    # Input validation
    w = np.asarray(w, dtype=np.float32)

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
            sqw[i, :] += qisf[i, j] * QENSmodels.lorentzian(w, scale, center, hwhm[i, j])

    # For Bumps use (needed for final plotting)
    # Using a 'Curve' in bumps for each Q --> needs vector array
    if q.size == 1:
        sqw = np.reshape(sqw, w.size)

    return sqw
