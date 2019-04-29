from __future__ import print_function
import numpy as np

try:
    import QENSmodels
except ImportError:
    print('Module QENSmodels not found')


def hwhmChudleyElliotDiffusion(q, D=0.23, L=1.0):
    """ Returns some characteristics of `ChudleyElliotDiffusion`

    Parameters
    ----------

    q: float, list or :class:`~numpy:numpy.ndarray`
        momentum transfer (in 1/Angstrom)

    D: float
        diffusion coefficient (in Angstrom^2/ps). Default to 0.23.

    L: float
        jump length (in Angstrom). Default to 1.0.


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

    Notes
    -----

    """
    # Input validation
    q = np.asarray(q, dtype=np.float32)

    eisf = np.zeros(q.size)
    qisf = np.ones(q.size)
    hwhm = 6 * D * (1-np.sin(q*L)/(q*L)) / L**2
    # Force hwhm to be numpy array, even if single value
    hwhm = np.asarray(hwhm, dtype=np.float32)
    hwhm = np.reshape(hwhm, hwhm.size)
    return hwhm, eisf, qisf


def sqwChudleyElliotDiffusion(w, q, scale=1, center=0, D=0.23,
                              L=1.00):
    r""" Lorentzian model with half width half maximum equal to
    :math:`\frac{6D}{l^2}(1 - \frac{sin(Ql)}{Ql})`

    Parameters
    ----------

    w: float, list or :class:`~numpy:numpy.ndarray`
        energy transfer (in ps)

    q: float, list or :class:`~numpy:numpy.ndarray`
        momentum transfer (non-fitting, in 1/Angstrom).

    scale: float
        scale factor. Default to 1.

    center: float
        center of peak. Default to 0.

    D: float
        diffusion coefficient (in Angstrom^2/ps). Default to 0.23.

    L: float
        jump distance (in Angstrom). Default to 1.0.

    Return
    ------

    :class:`~numpy:numpy.ndarray`
        output array


    Examples
    --------


    Notes
    -----

    * The `sqwChudleyElliotDiffusion` is expressed as

      .. math::

          S(q, \omega) = \text{Lorentzian}(\omega, \text{scale}, \text{center},
          \frac{6D}{l^2}(1 - \frac{sin(Ql)}{Ql}))

    * Note that an equivalent expression is

      .. math::

          S(q, \omega) = \text{Lorentzian}(\omega, \text{scale}, \text{center},
          \frac{1}{\tau}(1 - \frac{sin(Ql)}{Ql}))

      with

      .. math::

          \tau = \frac{l^2}{6D}


    Reference
    ----------

    R. Hempelmann,
    Quasielastic Neutron Scattering and Solid State Diffusion (Oxford, 2000)

    """
    # Input validation
    w = np.asarray(w)  # , dtype=np.float32)

    q = np.asarray(q, dtype=np.float32)

    # Create output array
    sqw = np.zeros((q.size, w.size))

    # Get widths, EISFs and QISFs of model
    hwhm, eisf, qisf = hwhmChudleyElliotDiffusion(q, D, L)

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
