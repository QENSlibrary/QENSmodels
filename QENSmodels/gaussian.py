import numpy as np
import QENSmodels


def gaussian(x, scale=1., center=0., sigma=1.):
    r"""
    Gaussian model

    Parameters
    ----------
    scale: float
        Scale factor. Default to 1.0
    center: float
        Center of peak. Default to 0.0
    sigma: float
        Width parameter. Default to 1.0

    Examples
    --------
    >>> QENSmodels.gaussian(1,1,1,1)
    0.3989422804014327

    Notes
    -----
    - A Gaussian function is defined as:

    .. math::

       \text{Gaussian}(x, \text{scale}, \text{center}, \sigma) = \frac{\text{scale}}{\sqrt{2\pi}\sigma}\exp \big(-\frac{(x-\text{center})^2}{2\sigma^2}\big)

    - The Full Width Half Maximum of a Gaussian equals :math:`2\sqrt{2\ln 2}\mbox{sigma}`

    References
    ----------
    None
    """

    if sigma == 0:
        model = QENSmodels.delta(x, scale, center)
    else:
        model = scale * np.exp(-(x - center)**2/(2.*sigma**2)) \
                / (sigma*np.sqrt(2*np.pi))
    return model
