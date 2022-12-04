import numpy as np
from typing import Union

try:
    import QENSmodels
except ImportError:
    print('Module QENSmodels not found')


def sqwDeltaLorentz(
    w: Union[float, list, np.ndarray],
    q: Union[float, list, np.ndarray],
    scale: float = 1.0,
    center: float = 0.0,
    A0: Union[float, list, np.ndarray] = 0.0,
    hwhm: Union[float, list, np.ndarray] = 1.0
) -> Union[float, list, np.ndarray]:
    r"""
    Model corresponding to a delta representing a fraction p of
    fixed atoms and a Lorentzian corresponding to a Brownian
    Translational diffusion model for the remaining (1 - p) atoms.

    Model = A0*delta + (1-A0)*Lorentz(Gamma)

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

    A0: float, list or :class:`~numpy:numpy.ndarray` of the same size as q
        proportion of immobile atoms, must be between 0 and 1. Default to 0.

    hwhm: float, list or :class:`~numpy:numpy.ndarray` of the same size as q
        half width half maximum. Default to 1.

    Return
    ------
    :class:`~numpy:numpy.ndarray`
        output array


    Examples
    --------
    >>> sqw = sqwDeltaLorentz([1, 2, 3], 0.1)
    >>> round(sqw[0], 1)
    0.2
    >>> round(sqw[1], 3)
    0.064
    >>> round(sqw[2], 3)
    0.032


    Notes
    -----
    The `sqwDeltaLorentz` is expressed as

    .. math::

        S(q, \omega) &= A_0 \delta(\omega, \text{scale}, \text{center}) \\
        &+ (1 - A_0) \text{Lorentzian}(\omega, \text{scale}, \text{center},
                                    \text{hwhm})

    """
    w = np.asarray(w)

    # Input validation
    q = np.asarray(q, dtype=np.float32)

    # Create output array
    sqw = np.zeros((q.size, w.size))

    # Model
    if q.size > 1:

        # Validator for A0. We must have 0<= A0 <= 1
        if any(item > 1 or item < 0 for item in A0):
            raise ValueError('A0, the proportion of immobile atoms, '
                             'should be comprised between 0 and 1, included.')

        try:
            for i in range(q.size):
                sqw[i, :] = A0[i] * QENSmodels.delta(w, scale, center)
                sqw[i, :] += (1 - A0[i]) * QENSmodels.lorentzian(
                    w,
                    scale,
                    center,
                    hwhm[i])

        except TypeError as detail:
            msg = "At least one parameter has an incorrect type"
            raise TypeError(detail.__str__() + "\n" + msg)
        except IndexError as detail:
            msg = "At least one array has an incorrect size"
            raise IndexError(detail.__str__() + "\n" + msg)
    else:
        if A0 > 1 or A0 < 0:
            raise ValueError('A0, the proportion of immobile atoms, '
                             'should be comprised between 0 and 1, included.')

        sqw[0, :] = A0 * QENSmodels.delta(w, scale, center)
        sqw[0, :] += (1 - A0) * QENSmodels.lorentzian(w, scale, center, hwhm)

    # For Bumps use (needed for final plotting)
    # Using a 'Curve' in bumps for each Q --> needs vector array
    if q.size == 1:
        sqw = np.reshape(sqw, w.size)

    return sqw
