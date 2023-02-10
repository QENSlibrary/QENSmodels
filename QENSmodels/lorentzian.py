import numpy as np
from typing import Union

try:
    import QENSmodels
except ImportError:
    print('Module QENSmodels not found')


def lorentzian(
        x: Union[float, list, np.ndarray],
        scale: Union[float, list, np.ndarray] = 1.0,
        center: Union[float, list, np.ndarray] = 0.0,
        hwhm: Union[float, list, np.ndarray] = 1.0
) -> Union[float, list, np.ndarray]:
    r""" Lorentzian model

    Parameters
    ----------
    x: float or list or :class:`~numpy:numpy.ndarray`
        domain of the function

    scale: float
        scale factor. Default to 1.

    center: float
        center of peak. Default to 0.

    hwhm: float
        Half Width at Half Maximum. Default to 1.

    Return
    ------
    float or :class:`~numpy:numpy.ndarray`
        output number or array

    Examples
    --------
    >>> round(lorentzian(1, 1, 1, 1), 3)
    0.318

    >>> round(lorentzian(3., 2., 2., 5.), 3)
    0.122

    >>> result = lorentzian([1, 3.], 1., 1., 1.)
    >>> round(result[0], 3)
    0.318
    >>> round(result[1], 3)
    0.064

    Notes
    -----
    * A Lorentzian function is defined as

    .. math::

       \text{Lorentzian}(x, \text{scale}, \text{center}, \text{hwhm}) =
       \frac{\text{scale}}{\pi} \frac{\text{hwhm}}
       {(x-\text{center})^2+\text{hwhm}^2}

    * Note that the maximum of a Lorentzian is
      :math:`\text{Lorentzian}(\text{center}, \text{scale}, \text{center},
      \text{hwhm})=\frac{\text{scale}}{\pi \text{hwhm}}`.

    * **Equivalence between different implementations**
      ``Lorentzian`` corresponds to the following implementations in
      `Mantid
      <http://docs.mantidproject.org/nightly/fitfunctions/Lorentzian.html>`__
      and
      `DAVE <https://www.ncnr.nist.gov/dave/documentation/pandoc_DAVE.pdf>`__

      +------------------+-----------------+------------------+
      | QENSmodels       | Mantid          |  DAVE            |
      +==================+=================+==================+
      | ``Lorentzian``   | ``Lorentzian``  |  ``Lorentzian``  |
      +------------------+-----------------+------------------+
      | ``scale``        | Amplitude       |  A               |
      +------------------+-----------------+------------------+
      | ``center``       | PeakCentre      |  :math:`x_0`     |
      +------------------+-----------------+------------------+
      | ``hwhm``         | FWHM /2         | W/2              |
      +------------------+-----------------+------------------+

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
    # Input validation
    x = np.asarray(x)
    hwhm = np.asarray(hwhm)

    if hwhm == 0:
        model = QENSmodels.delta(x, 1.0, center)
    else:
        model = hwhm / ((x - center) ** 2 + hwhm ** 2) / np.pi

    # Area normalization
    if x.size > 1:
        area = np.trapz(model, x)
        if area > 1:
            model /= area

    # Scale by amplitude
    model *= np.asarray(scale)

    return model
