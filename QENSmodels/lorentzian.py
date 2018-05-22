import numpy as np
import QENSmodels


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

    Examples
    --------
    >>> QENSmodels.lorentzian(1, 1, 1, 1)
    0.31830988618379069

    >>> QENSmodels.lorentzian(3., 2., 2., 5.)
    0.12242687930145796

    >>> QENSmodels.lorentzian([1, 3.], 1., 1., 1.)
    array([ 0.31830987,  0.06366198], dtype=float32)

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
    x = np.asarray(x, dtype=np.float32)

    if hwhm == 0:
        model = QENSmodels.delta(x, scale, center)
    else:
        model = scale * hwhm / ((x-center)**2 + hwhm**2) / np.pi

    return model
