from __future__ import print_function
import numpy as np

try:
    import QENSmodels
except ImportError:
    print('Module QENSmodels not found')


def gaussian(x, scale=1., center=0., sigma=1.):
    r""" Gaussian model

    Parameters
    ----------
    x: float or list or :class:`~numpy:numpy.ndarray`
        domain of the function

    scale: float
        scale factor. Default to 1.

    center: float
        center of peak. Default to 0.

    sigma: float
        width parameter. Default to 1.

    Return
    ------
    float or :class:`~numpy:numpy.ndarray`
       output number or array

    Examples
    --------
    >>> round(gaussian(1, 1, 1, 1), 3)
    0.399

    >>> round(gaussian(3, 2, 2, 5), 3)
    0.156

    >>> result = gaussian([1, 3], 1, 1, 1)
    >>> round(result[0], 3)
    0.399
    >>> round(result[1], 3)
    0.054


    Notes
    -----

    * A Gaussian function is defined as:

    .. math::

       \text{Gaussian}(x, \text{scale}, \text{center}, \sigma) =
       \frac{\text{scale}}{\sqrt{2\pi}\sigma}\exp
       \big(-\frac{(x-\text{center})^2}{2\sigma^2}\big)

    * The Full Width Half Maximum of a Gaussian equals
      :math:`2\sqrt{2\ln 2}\sigma`

    * **Equivalence between different implementations**

      ``Gaussian`` corresponds to the following implementations in
      `Mantid
      <http://docs.mantidproject.org/nightly/fitfunctions/Gaussian.html>`_

      +--------------+----------------------------------------+
      | QENSmodels   | Mantid                                 |
      +==============+========================================+
      | ``Gaussian`` | ``Gaussian``                           |
      +--------------+----------------------------------------+
      | ``scale``    | Height=scale/sigma/:math:`\sqrt{2\pi}` |
      +--------------+----------------------------------------+
      | ``center``   | PeakCentre                             |
      +--------------+----------------------------------------+
      | ``sigma``    | Sigma                                  |
      +--------------+----------------------------------------+

    * Numerical issues:
      The definition of the Lorentzian function used here is such that
      the integral between :math:`-\infty` and :math:`-\infty` is 1.
      However, when the hwhm is comparable or smaller than the x step,
      the sampling of the function will result in a numerical integral > 1.
      E.g., in the extreme case where hwhm tends to zero, the numerical
      sampling at x points will result in a delta-like function, but with
      a value at maximum approaching :math:`-\infty` instead of the
      value 1/:math:`\Delta x` used in the definition of the delta function.
      Therefore, the value of the integral of the function is checked
      and used to renormalize the returned function whenever the integral
      is larger than 1.

    """
    x = np.asarray(x)

    if sigma == 0:
        model = QENSmodels.delta(x, scale, center)
    else:
        model = (sigma * np.sqrt(2. * np.pi)) \
            * np.exp(- (x - center) ** 2 / (2. * sigma ** 2))

    # Area normalization
    area = np.trapz(model, x)
    if area > 1:
        model /= area

    # Scale by amplitude
    model *= scale

    return model


if __name__ == "__main__":
    import doctest
    doctest.testmod()
