import numpy as np
import QENSmodels
import doctest

def lorentzian(x, scale=1.0, center=0.0, hwhm=1.0):
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
    >>> round(QENSmodels.lorentzian(1, 1, 1, 1))
    0.318

    >>> round(QENSmodels.lorentzian(3., 2., 2., 5.), 3)
    0.122

    >>> result = QENSmodels.lorentzian([1, 3.], 1., 1., 1.)
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
      :math:`\text{Lorentzian}(\text{center}, \text{scale}, \text{center}, \text{hwhm})=
      \frac{\text{scale}}{\pi \text{hwhm}}`.

    * **Equivalence**
      ``Lorentzian`` corresponds to the following implementations in
      `Mantid <http://docs.mantidproject.org/nightly/fitfunctions/Lorentzian.html>`_
      and
      `DAVE <https://www.ncnr.nist.gov/dave/documentation/pandoc_DAVE.pdf>`_

      +------------------+-----------------+------------------+
      | Equivalence      | Mantid          |  DAVE            |
      +==================+=================+==================+
      | ``Lorentzian``   | ``Lorentzian``  |  ``Lorentzian``  |
      +------------------+-----------------+------------------+
      | ``scale``        | Amplitude       |  A               |
      +------------------+-----------------+------------------+
      | ``center``       | PeakCentre      |  :math:`x_0`     |
      +------------------+-----------------+------------------+
      | ``hwhm``         | FWHM /2         | W/2              |
      +------------------+-----------------+------------------+

    """
    # Input validation
    x = np.asarray(x)

    if hwhm == 0:
        model = QENSmodels.delta(x, scale, center)
    else:
        model = scale * hwhm / ((x-center)**2 + hwhm**2) / np.pi

    return model
