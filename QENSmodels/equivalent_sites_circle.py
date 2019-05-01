from __future__ import print_function
import numpy as np

try:
    import QENSmodels
except ImportError:
    print('Module QENSmodels not found')


def hwhmEquivalentSitesCircle(q, N=3, radius=1.0, resTime=1.0):
    """
    Returns some characteristics of `EquivalentSitesCircle`

    Parameters
    ----------
    q: float, list or :class:`~numpy:numpy.ndarray`
        momentum transfer (non-fitting, in 1/Angstrom)

    N: integer
        number of sites in circle. Default to 3.

    radius: float
        radius of the circle (in Angstrom). Default to 1.

    resTime: float
        residence time (in NEED TO CHECK UNITS). Default to 1.

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
    >>> hwhm, eisf, qisf = hwhmEquivalentSitesCircle([1., 2.], 6, 0.5, 1.5)
    >>> round(hwhm[0, 1], 3)
    0.333
    >>> round(hwhm[0, 3], 3)
    1.333
    >>> round(eisf[0], 3)
    0.92
    >>> round(eisf[1], 3)
    0.713
    >>> round(qisf[0, 1], 6)
    0.000503
    >>> round(qisf[1, 4],6)
    0.13616

    """
    # input validation
    q = np.asarray(q, dtype=np.float32)

    # Need to decide what to do if N < 2:
    # Get out immediately with message that N_min = 2?
    # Set N = 2 and show warning that N_min = 2?

    # number of sites has to be an integer
    N = np.int(N)

    # index of sites in circle
    sites = np.arange(N)

    hwhm = 2.0 / resTime * np.sin(sites*np.pi/N)**2
    hwhm = np.tile(hwhm, (q.size, 1))

    # jump distances between sites
    jump_distance = 2.0 * radius * np.sin(sites*np.pi/N)

    # QR matrix [q.size, N] and corresponding spherical Bessel functions
    QR = np.outer(q, jump_distance)
    sphBessel = np.ones(QR.shape)
    idx = np.nonzero(QR)
    sphBessel[idx] = np.sin(QR[idx]) / QR[idx]

    isf = np.zeros(QR.shape)
    for i in range(N):
        for j in range(N):
            isf[:, i] += sphBessel[:, j] * np.cos(2*i*j*np.pi/N)
        isf[:, i] /= N

    eisf = isf[:, 0]
    qisf = isf[:, 1:]

    return hwhm, eisf, qisf


def sqwEquivalentSitesCircle(w, q,
                             scale=1.0, center=0.0, N=3,
                             radius=1.0, resTime=1.0):
    r"""
    Model
    `Jumps between N equivalent sites on a circle`
    = A_0 delta + Sum of Lorentzians ...


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

    N: integer
        number of sites in circle. Default to 3.

    radius: float
        radius of rotation (in Angstrom). Default to 1.

    resTime: float
        residence time in a site before jumping to another site (in 1/ps).
        Default to 1.

    Return
    ------
    :class:`~numpy:numpy.ndarray`
        output array

    Examples
    --------
    >>> sqw = sqwEquivalentSitesCircle(1, 1, 1, 0, 4, 1, 1)
    >>> round(sqw[0], 3)
    0.045

    >>> sqw = sqwEquivalentSitesCircle([1, 2, 3], [0.3, 0.4], 1, 0, 5, 1, 1)
    >>> round(sqw[0, 0], 3)
    0.004
    >>> round(sqw[0, 1], 3)
    0.001
    >>> round(sqw[0, 2], 3)
    0.001
    >>> round(sqw[1, 0], 3)
    0.008
    >>> round(sqw[1, 1], 3)
    0.003
    >>> round(sqw[1, 2], 3)
    0.001


    Notes
    -----

    """
    # Input validation
    w = np.asarray(w)

    q = np.asarray(q, dtype=np.float32)

    # Create output array
    sqw = np.zeros((q.size, w.size))

    # Get widths, EISFs and QISFs of model
    hwhm, eisf, qisf = hwhmEquivalentSitesCircle(q, N, radius, resTime)
    # Number of Lorentzians (= N-1)
    numberLorentz = hwhm.shape[1] - 1
    # Sum of Lorentzians
    # (Note that hwhm has dimensions [q.size, N], as hwhm[:,0]
    # contains a width=0, corresponding to the elastic line
    # (eisf), while qisf has dimensions [q.size, N-1])
    for i in range(q.size):
        sqw[i, :] = eisf[i] * QENSmodels.delta(w, scale, center)
        for j in range(numberLorentz):
            sqw[i, :] += qisf[i, j] * QENSmodels.lorentzian(w,
                                                            scale,
                                                            center,
                                                            hwhm[i, j+1])

    # For Bumps use (needed for final plotting)
    # Using a 'Curve' in bumps for each Q --> needs vector array
    if q.size == 1:
        sqw = np.reshape(sqw, w.size)

    return sqw


if __name__ == "__main__":
    import doctest
    doctest.testmod()
