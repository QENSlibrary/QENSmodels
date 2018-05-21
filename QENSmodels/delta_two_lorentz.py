import numpy as np
import QENSmodels


def sqwDeltaTwoLorentz(w, q, scale=1, center=0, A0=1, A1=1, hwhm1=1, hwhm2=1):
    """
    Model = A0*delta + A1*Lorentzian(Gamma1) + (1-A0-A1)*Lorentzian(Gamma2)

    Parameters
    ----------
    w: float, list or :class:`~numpy:numpy.ndarray`
        energy transfer in hbar units

    q: float, list or :class:`~numpy:numpy.ndarray`
        momentum transfer (non-fitting, in 1/Angstrom)

    scale: float
        scale factor. Default to 1.

    center: float
        peak center. Default to 0.

    A0: float, list or :class:`~numpy:numpy.ndarray` of the same size as q
        amplitude of the delta function. Default to 1.

    A1: float, list or :class:`~numpy:numpy.ndarray` of the same size as q
        amplitude of the first Lorentzian. Default to 1.

    hwhm1: float, list or :class:`~numpy:numpy.ndarray` of the same size as q
        half-width half maximum of the first Lorentzian. Default to 1.

    hwhm2: float, list or :class:`~numpy:numpy.ndarray` of the same size as q
        half-width half maximum of the second Lorentzian. Default to 1

    Return
    ------
    :class:`~numpy:numpy.ndarray`
        output array


    Examples
    --------
    >>> QENSmodels.sqwDeltaTwoLorentz([1, 2, 3], [0.1, 0.2], 1, 1, [1, 1], [1, 1], [0.01, 0.01], [0.01, 0.01])
    array([[ 1.,  0.,  0.],
           [ 1.,  0.,  0.]])


    >>>  QENSmodels.sqwDeltaTwoLorentz([1, 2, 3], [0.1, 0.2], 1, 1, [0.1, 0.5], [0.2, 0.3], [0.01, 0.02], [0.03, 0.06])
    array([[  1.39934275e+01,   7.31505209e-03,   1.82990197e-03],
           [  6.83568108e+00,   5.71511278e-03,   1.43148794e-03]])


    Notes
    -----
    .. math::

        S(\omega, q) = A_0 \text{delta}(\omega - \text{center})
        + A_1 \text{Lorentzian}(\omega, \text{scale}, \text{center}, \text{hwhm_1})
        + (1 - A_0 - A_1) \text{Lorentzian}(\omega, \text{scale}, \text{center}, \text{hwhm_2})

    """

    # Input validation
    w = np.asarray(w, dtype=np.float32)

    q = np.asarray(q, dtype=np.float32)

    # Create output array
    sqw = np.zeros((q.size, w.size))

    # Model
    if q.size > 1:
        for i in range(q.size):
            sqw[i, :] = A0[i] * QENSmodels.delta(w,
                                                 scale,
                                                 center)
            sqw[i, :] += A1[i] * QENSmodels.lorentzian(w,
                                                       scale,
                                                       center,
                                                       hwhm1[i])
            sqw[i, :] += (1 - A0[i] - A1[i]) * QENSmodels.lorentzian(w,
                                                                     scale,
                                                                     center,
                                                                     hwhm2[i])
    else:
        sqw[0, :] = A0 * QENSmodels.delta(w,
                                          scale,
                                          center)
        sqw[0, :] += A1 * QENSmodels.lorentzian(w,
                                                scale,
                                                center,
                                                hwhm1)
        sqw[0, :] += (1. - A0 - A1) * QENSmodels.lorentzian(w,
                                                            scale,
                                                            center,
                                                            hwhm2)

    # For Bumps use (needed for final plotting)
    # Using a 'Curve' in bumps for each Q --> needs vector array
    if q.size == 1:
        sqw = np.reshape(sqw, w.size)

    return sqw
