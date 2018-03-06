import numpy as np


def lorentzian(x, scale_factor=1.0, peak_centre=0.0, fwhm=1.0):
    """
    Lorentzian model

    Args:
        scale_factor (float): Scale factor. Default to 1.0
        peak_centre (float): Centre of peak. Default to 0.0
        fwhm (float): Full Width at Half Maximum. Default to 1.0

    Returns:
        Value (float) of Lorentzian function


    Examples:
        >>> QENSmodels.lorentzian(1,1,1,1)
        0.6366197723675814

    A Lorentzian function is defined as:

    $\text{Lorentzian}(x, \text{scale_factor}, \text{peak_centre}, \text{fwhm})
    = \frac{\text{scale_factor}}{\pi}\frac{\frac{1}{2}\text{fwhm}}{(x-\text{peak_centre})^2+\big(\frac{1}{2}\text{fwhm}\big)^2}$

    """

    return scale_factor * fwhm / ( np.pi * 2. ) / (
                (x - peak_centre) ** 2 + (fwhm / 2.) ** 2)


name = "Lorentzian"
category = "peak"

# pylint: disable=bad-whitesapce, line-too-long
# parameters = [['scale_factor', 1, [], ' Scale factor'],
#              ['peak_centre', 0, [], 'Centre of peak '],
#              ['fwhm', 1, [], 'Full Width at Half Maximum']]
