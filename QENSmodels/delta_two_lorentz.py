import numpy as np
import QENSmodels


def sqwDeltaTwoLorentz(w, q, scale, center, A0, A1, hwhm1, hwhm2):
    """
    Model = A0*delta + A1*Lorentzian(Gamma1) + (1-A0-A1)*Lorentzian(Gamma2)

    Parameters
    ----------
    w: float, list or :class:`~numpy:numpy.ndarray`
        to be added

    q: float, list or :class:`~numpy:numpy.ndarray`
        Momentum transfer

    scale: float
        Scale factor.

    center: float
        Peak center.

    A0: to be added
        to be added

    A1: to be added
        to be added

    hwhm1: to be added
        half-width half maximum

    hwhm2: to be added
        half-width half maximum
    """

    # Input validation
    q = np.asarray(q, dtype=np.float32)

    # Create output array
    sqw = np.zeros((q.size, w.size))

    # Model
    if q.size > 1:
        for i in range(q.size):
            sqw[i, :] = A0[i] * QENSmodels.delta(w, scale, center)
            sqw[i, :] += A1[i] * QENSmodels.lorentzian(w, scale, center, hwhm1[i])
            sqw[i, :] += (1 - A0[i] - A1[i]) * QENSmodels.lorentzian(w, scale, center,
                                                       hwhm2[i])
    else:
        sqw[0, :] = A0 * QENSmodels.delta(w, scale, center)
        sqw[0, :] += A1 * QENSmodels.lorentzian(w, scale, center, hwhm1)
        sqw[0, :] += (1 - A0 - A1) * QENSmodels.lorentzian(w, scale, center, hwhm2)


    # For Bumps use (needed for final plotting)
    # Using a 'Curve' in bumps for each Q --> needs vector array
    if q.size == 1:
        sqw = np.reshape(sqw, w.size)

    return sqw
