import numpy as np
import QENSmodels

def lorentzian(x, scale=1.0, center=0.0, hwhm=1.0):
    r""" Lorentzian model

    Parameters
    ----------
    scale: float
        Scale factor. Default to 1.0

    center: float
        Center of peak. Default to 0.0

    hwhm: float
        Half Width at Half Maximum. Default to 1.0

    Examples
    --------
    >>> QENSmodels.lorentzian(1,1,1,1)
    0.6366197723675814

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
      `Mantid <http://docs.mantidproject.org/nightly/fitfunctions/Lorentzian.html>`_ and
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

    References
    ----------
    None
    """
    if hwhm == 0:
        model = QENSmodels.delta(x, scale, center)
    else:
        model = scale * hwhm / ((x-center)**2 + hwhm**2) / np.pi

    return model
