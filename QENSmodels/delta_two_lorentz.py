from __future__ import print_function
import numpy as np

try:
    import QENSmodels
except ImportError:
    print('Module QENSmodels not found')


def sqwDeltaTwoLorentz(w, q, scale=1, center=0, A0=1, A1=1, hwhm1=1, hwhm2=1):
    r"""
    Model corresponding to a delta representing a fraction p of
    fixed atoms and two Lorentzians corresponding to Brownian
    Translational diffusion model at different time scales for the remaining
    atoms.


    Model = A0*delta + A1*Lorentzian1 + (1-A0-A1)*Lorentzian2

    Parameters
    ----------
    w: float
        energy transfer (in 1/ps)

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
        half-width half maximum of the second Lorentzian. Default to 1.

    Return
    ------
    :class:`~numpy:numpy.ndarray`
        output array


    Examples
    --------
    >>> sqw = sqwDeltaTwoLorentz([1, 2, 3], [0.1, 0.2], 1, 1, [1, 1], [1, 1], [0.01, 0.01], [0.01, 0.01])  # noqa: E501
    >>> round(sqw[0, 0])
    1
    >>> sqw[0, 1]
    0.0
    >>> sqw[0, 2]
    0.0
    >>> round(sqw[1, 0])
    1
    >>> sqw[1, 1]
    0.0
    >>> sqw[1, 2]
    0.0

    >>> sqw = sqwDeltaTwoLorentz([1, 2, 3], [0.05, 0.3], 0.5, 2, [0.75, 0.5], [1, 2], [0.05, 0.04], [0.02, 0.03])  # noqa: E501
    >>> round(sqw[0, 0], 3)
    0.001
    >>> round(sqw[0, 1], 3)
    0.499
    >>> round(sqw[0, 2], 3)
    0.001
    >>> round(sqw[1, 0], 3)
    0.001
    >>> round(sqw[1, 1], 3)
    0.499
    >>> round(sqw[1, 2], 3)
    0.001

    Notes
    -----
    .. math::

        S(q, \omega) &= A_0 \text{delta}(\omega - \text{center}) \\
        &+ A_1 \text{Lorentzian}(\omega, \text{scale}, \text{center},
        \text{hwhm}_1) \\
        &+ (1 - A_0 - A_1) \text{Lorentzian}(\omega, \text{scale},
        \text{center}, \text{hwhm}_2)

    """

    # Input validation
    w = np.asarray(w)

    q = np.asarray(q, dtype=np.float32)

    # Create output array
    sqw = np.zeros((q.size, w.size))

    # Model
    if q.size > 1:
        try:
            for i in range(q.size):
                sqw[i, :] = A0[i] * QENSmodels.delta(w, scale, center)
                sqw[i, :] += A1[i] * QENSmodels.lorentzian(
                    w,
                    scale,
                    center,
                    hwhm1[i]
                )
                sqw[i, :] += (1 - A0[i] - A1[i]) * QENSmodels.lorentzian(
                    w,
                    scale,
                    center,
                    hwhm2[i]
                )
        except TypeError as detail:
            msg = "At least one parameter has an incorrect type"
            raise TypeError(detail.__str__() + "\n" + msg)
        except IndexError as detail:
            msg = "At least one array has an incorrect size"
            raise IndexError(detail.__str__() + "\n" + msg)
    else:
        sqw[0, :] = A0 * QENSmodels.delta(
            w,
            scale,
            center
        )
        sqw[0, :] += A1 * QENSmodels.lorentzian(
            w,
            scale,
            center,
            hwhm1
        )
        sqw[0, :] += (1. - A0 - A1) * QENSmodels.lorentzian(
            w,
            scale,
            center,
            hwhm2
        )

    # For Bumps use (needed for final plotting)
    # Using a 'Curve' in bumps for each Q --> needs vector array
    if q.size == 1:
        sqw = np.reshape(sqw, w.size)

    return sqw


if __name__ == "__main__":
    import doctest
    doctest.testmod()
