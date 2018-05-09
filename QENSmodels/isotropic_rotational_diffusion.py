import numpy as np
from scipy.special import jn
import QENSmodels


def hwhmIsotropicRotationalDiffusion(q, radius=1.0, DR=1.0):
    """
    Returns some characteristics of `IsotropicRotationalDiffusion`

    Parameters
    ----------
    q: float, list or :class:`~numpy:numpy.ndarray`
        Momentum transfer

    radius: float
        Radius of rotation. Default to

    DR: float
        Rotational diffusion coefficient. Default to

    Returns
    -------
    `hwhm`: :class:`~numpy:numpy.ndarray`
       half-width half maximum

    `eisf`: :class:`~numpy:numpy.ndarray`
       elastic incoherent structure factor

    `qisf`: :class:`~numpy:numpy.ndarray`
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
    """
    Model = Isotropic rotational diffusion = A0 + Sum of Lorentzians ...

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

    radius: float
        Radius of rotation. Default to 1.

    DR: float
        Rotational diffusion coefficient. Default to 1.

    Notes
    -----
    * 6 elements in the sum

    * Equivalences: Mantid
    """

    # Input validation
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
