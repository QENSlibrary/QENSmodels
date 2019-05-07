from __future__ import print_function
import numpy as np

try:
    import QENSmodels
except ImportError:
    print('Module QENSmodels not found')


def hwhmGaussianModel3D(q, D=1., variance_ux=1.):
    """ Returns some characteristics of `JumpTranslationalDiffusion`

    Parameters
    ----------

    q: float, list or :class:`~numpy:numpy.ndarray`
        momentum transfer (non-fitting, in 1/Angstrom)

    D: float
        diffusion coefficient (in Angstrom:math:`^2`/ps). Default to 1.

    variance_ux: float
        variance :math:`<u_x^2>` of Gaussian random variable :math:`u_x`
        (in Angstrom:math:`^2`), displacement from the origin.
        Default to 1.

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
    >>> hwhm, eisf, qisf = hwhmGaussianModel3D([1., 2.], 0.5, 1.5)
    >>> round(hwhm[0,10], 3), round(hwhm[1, 10], 3)
    (2.033, 2.033)
    >>> round(hwhm[0,99], 3), round(hwhm[1, 99], 3)
    (20.122, 20.122)
    >>> round(eisf[0], 3)
    0.292
    >>> round(eisf[1], 3)
    0.007
    >>> round(qisf[0, 1], 4)
    0.3595
    >>> round(qisf[1, 1], 4)
    0.0359

    """
    # Input validation
    if D <= 0:
        raise ValueError("D, the diffusion coefficient, should be positive")
    if variance_ux <= 0:
        raise ValueError("variance_ux, the variance, should be "
                         "strictly positive")

    q = np.asarray(q, dtype=np.float64)

    numberLorentz = 100

    qisf = np.zeros((q.size, numberLorentz))
    hwhm = np.zeros((q.size, numberLorentz))
    al = np.zeros((q.size, numberLorentz))

    arg = q**2 * variance_ux

    for i in range(numberLorentz):

        # to solve warnings for arg=0
        if arg.all() > 0:
            al[:, i] = np.exp(-arg) * arg**i / np.math.factorial(i)
        else:
            al[:, i] = 0.

        hwhm[:, i] = np.repeat(i*D/variance_ux, q.size)

    eisf = al[:, 0]

    for i in range(1, numberLorentz):
        qisf[:, i] = al[:, i]

    return hwhm, eisf, qisf


def sqwGaussianModel3D(w, q, scale=1, center=0, D=1., variance_ux=1.):
    r""" Gaussian model for localized translational motion in 3D

    Supposing a particle that can move along the direction x about a
    fixed point taken as the origin and being u_x the displacement
    from the origin, the model assumes that u_x is a Gaussian random
    variable with variance <u_x^2>.
    For the 3D case, the model assumes also <u_x^2> = <u_y^2> = <u_z^2>.


    Parameters
    ----------

    w: float, list or :class:`~numpy:numpy.ndarray`
        energy transfer (in 1/ps)

    q: float, list or :class:`~numpy:numpy.ndarray`
        momentum transfer (non-fitting, in 1/Angstrom).

     scale: float
        scale factor. Default to 1.

    center: float
        center of peak. Default to 0.

    D: float
        diffusion coefficient (in Angstrom:math:`^2`/ps). Default to 1.

    variance_ux: float
        variance :math:`<u_x^2>` of Gaussian random variable :math:`u_x`
        (in Angstrom:math:`^2`), displacement from the origin.
        Default to 1.

    Return
    ------

    :class:`~numpy:numpy.ndarray`
        output array


    Examples
    --------
    >>> sqw = sqwGaussianModel3D([1, 2, 3], 1, 1, 0, 1, 1)
    >>> round(sqw[0], 3)
    0.127
    >>> round(sqw[1], 3)
    0.037
    >>> round(sqw[2], 3)
    0.017

    >>> sqw = sqwGaussianModel3D(1, 1, 1, 0, 1, 1)
    >>> round(sqw[0], 3)
    0.127


    Notes
    -----

    * The `sqwGaussianModel3D` is expressed as

        .. math::

            S(q, \omega) = \text{delta}(\omega, A_0(q), \text{center} )
            + \sum_{i=1}^{N-1} A_i(Q)
            \text{Lorentzian}(\omega, A_i(Q)\Gamma_i, \text{center},
          \Gamma_i^2)

      where

      .. math::

         A_i(Q) = \exp(-q^2<u_x^2>) \frac{(q^2<u_x^2>)^i}{i!}

         \Gamma_i = \frac{i D}{<u_x^2>}

    * The number of terms in the infinite sum is limited to 100.
      According to Volino's paper, as a rule of thumb, the number of
      terms to be considered in practical calculations must be (much)
      larger than :math:`Q^2<u_x^2>`. Therefore this condition should be
      checked when using this model.

    References
    ----------

    F. Volino, J.-C. Perrin, and S. Lyonnard,
    *J. Phys. Chem. B* **110**, 11217-11223 (2006)
    `link <https://pubs.acs.org/doi/10.1021/jp061103s>`_

    """
    # Input validation
    w = np.asarray(w)

    q = np.asarray(q, dtype=np.float64)

    # Create output array
    sqw = np.zeros((q.size, w.size))

    # Get widths, EISFs and QISFs of model
    hwhm, eisf, qisf = hwhmGaussianModel3D(q, D, variance_ux)

    # Number of Lorentzians used to represent the infinite sum in R
    numberLorentz = hwhm.shape[1]

    # Sum of Lorentzians
    for i in range(q.size):
        sqw[i, :] = eisf[i] * QENSmodels.delta(w, scale, center)
        for j in range(1, numberLorentz):
            sqw[i, :] += qisf[i, j] * QENSmodels.lorentzian(w,
                                                            scale,
                                                            center,
                                                            hwhm[i, j])

    # For Bumps use (needed for final plotting)
    # Using a 'Curve' in bumps for each Q --> needs vector array
    if q.size == 1:
        sqw = np.reshape(sqw, w.size)

    return sqw


if __name__ == "__main__":
    import doctest
    doctest.testmod()
