import numpy as np

try:
    import QENSmodels
except ImportError:
    print('Module QENSmodels not found')


def sqwWaterTeixeira(w, q, scale=1, center=0, D=0.23, resTime=1.25, radius=1,
                     DR=1):
    r""" Model corresponding to the convolution of `Jump Translational
    diffusion` (model T) and `Isotropic rotational diffusion` (model R)

    Model = convolution(T, R), where

    T = Jump Translational diffusion = Lorentz(Gamma_T)

    R = Isotropic rotational diffusion = A0 + A1*L1 + A2*L2 + ...

    This results in

    Model = A0*Lorentz(Gamma_T) + A1*Lorentz(Gamma_T+Gamma_1)
    + A2*Lorentz(Gamma_T+Gamma_2) + ...

    Parameters
    ----------
    w: float, list or :class:`~numpy:numpy.ndarray`
        energy transfer (in 1/ps)

    q: float, list or :class:`~numpy:numpy.ndarray`
        momentum transfer (non-fitting, in 1/Angstrom)

    scale: float
        scale factor. Default to 1.

    center: float
        center of peak. Default to 0.

    D: float
        Diffusion coefficient (in Angstrom^2/ps). Default to 1.

    resTime: float
        Residence time (in ps). Default to 1.

    radius: float
        radius of rotation (in Angstrom). Default to 1.

    DR: float
        rotational diffusion coefficient (in 1/ps). Default to 1.


    Return
    ------
    :class:`~numpy:numpy.ndarray`
        output array


    Examples
    --------

    >>> result = sqwWaterTeixeira(1, 1, 1, 1, 1, 1, 1, 1)
    >>> round(result[0], 3)
    0.486

     Notes
    -----

    * The default values for the fitting parameters come from the values
      for water at 298K and 1 atm, water has D=0.23 Angstrom^2/ps and
      ResTime=1.25 ps.

    References
    ----------

    J. Teixeira, M.-C. Bellissent-Funel, S.H. Chen, and A.J, Dianoux,
    *Phys. Rev. A* **31**, 1913-1917 (1985)
    `link <https://journals.aps.org/pra/abstract/10.1103/PhysRevA.31.1913>`_

    """
    # Input validation
    w = np.asarray(w, dtype=np.float32)

    q = np.asarray(q, dtype=np.float32)

    # Create output array
    sqw = np.zeros((q.size, w.size))

    # Get widths, EISFs and QISFs of each model
    hwhm1, eisf1, qisf1 = QENSmodels.jump_translational_diffusion.\
        hwhmJumpTranslationalDiffusion(q, D, resTime)
    hwhm2, eisf2, qisf2 = QENSmodels.isotropic_rotational_diffusion.\
        hwhmIsotropicRotationalDiffusion(q, radius, DR)

    # Number of Lorentzians used to represent the infinite sum in R
    numberLorentz = hwhm2.shape[1]

    # Sum of Lorentzians giving the full model
    for i in range(q.size):
        sqw[i, :] = eisf2[i] * QENSmodels.lorentzian(w, scale, center,
                                                     hwhm1[i])
        for j in range(1, numberLorentz):
            sqw[i, :] += qisf2[i, j] * QENSmodels.lorentzian(w, scale, center,
                                                             hwhm1[i] + hwhm2[i, j])  # noqa: E501

    # For Bumps use (needed for final plotting)
    # Using a 'Curve' in bumps for each Q --> needs vector array
    if q.size == 1:
        sqw = np.reshape(sqw, w.size)

    return sqw


if __name__ == "__main__":
    import doctest
    doctest.testmod()
