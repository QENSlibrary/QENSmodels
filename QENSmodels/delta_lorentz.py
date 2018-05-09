import numpy as np
import QENSmodels


def sqwDeltaLorentz(w, q, scale=1, center=0, A0=0.0, hwhm=1):
    """
    Model corresponding to a delta representing a fraction p of
    fixed atoms and a Lorentzian corresponding to a Brownian
    Translational diffusion model for the remaining (1 - p) atoms.

    Model = A0*delta + (1-A0)*Lorentz(Gamma)

    Parameters
    ----------
    w: float, list or :class:`~numpy:numpy.ndarray`
        to be added

    q: float, list or :class:`~numpy:numpy.ndarray`
        Momentum transfer ()

    scale: float
        Scale factor. Default to 1.

    center: float
        Peak center. Default to 0.

    A0: to be added
        to be added

    hwhm: to be added
        Half Width Half Maximum. Default to 1.

    Examples
    --------
    >>> QENSmodels.sqwDeltaLorentz()

    """

    # Input validation
    q = np.asarray(q, dtype=np.float32)

    # Create output array
    sqw = np.zeros((q.size, w.size))

    # Model
    if q.size > 1:
        for i in range(q.size):
            sqw[i, :] = A0[i] * QENSmodels.delta(w, scale, center)
            sqw[i,:] += (1-A0[i]) * QENSmodels.lorentzian(w, scale, center, hwhm[i])
    else:
        sqw[0,:] = A0 * QENSmodels.delta(w, scale, center)
        sqw[0,:] += (1-A0) * QENSmodels.lorentzian(w, scale, center, hwhm)

    # For Bumps use (needed for final plotting)
    # Using a 'Curve' in bumps for each Q --> needs vector array
    if q.size == 1:
        sqw = np.reshape(sqw, w.size)

    return sqw
