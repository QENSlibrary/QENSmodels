import numpy as np
import QENSmodels


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
    >>> QENSmodels.gaussian(1, 1, 1, 1)
    0.3989422804014327

    >>> QENSmodels.gaussian(3, 2, 2, 5)
    0.15641707759018236

    >>> QENSmodels.gaussian([1, 3], 1, 1, 1)
    array([ 0.39894229,  0.05399097], dtype=float32)


    Notes
    -----

    * A Gaussian function is defined as:

    .. math::

       \text{Gaussian}(x, \text{scale}, \text{center}, \sigma) =
       \frac{\text{scale}}{\sqrt{2\pi}\sigma}\exp
       \big(-\frac{(x-\text{center})^2}{2\sigma^2}\big)

    * The Full Width Half Maximum of a Gaussian equals
      :math:`2\sqrt{2\ln 2}\sigma`

    * **Equivalence**

      ``Gaussian`` corresponds to the following implementations in
      `Mantid <http://docs.mantidproject.org/nightly/fitfunctions/Gaussian.html>`_

      +--------------+----------------------------------------+
      | Equivalence  | Mantid                                 |
      +==============+========================================+
      | ``Gaussian`` | ``Gaussian``                           |
      +--------------+----------------------------------------+
      | ``scale``    | Height=scale/sigma/:math:`\sqrt{2\pi}` |
      +--------------+----------------------------------------+
      | ``center``   | PeakCentre                             |
      +--------------+----------------------------------------+
      | ``sigma``    | Sigma                                  |
      +--------------+----------------------------------------+


    """
    x = np.asarray(x, dtype=np.float32)

    if sigma == 0:
        model = QENSmodels.delta(x, scale, center)
    else:
        model = scale * np.exp(-(x - center)**2/(2.*sigma**2)) \
                / (sigma*np.sqrt(2*np.pi))
    return model
