import QENSmodels

def jump_diffusion(x, scale_factor=1.0, peak_centre=0.0, diffusion_coeff=1.0,
                   Q=1.0):
    """ Long range translational diffusion (random walk)
    This model corresponds to a Brownian motion, where particles collide
    randomly between them. Between two collisions, one particle moves
    along a straight line. After a collision, it goes into a random
    direction, independent of the previous one.
    This requirement for 'memory loss' between two steps limits the
    minimum length and time that can be described by the model.

    Parameters
    ----------
    scale_factor (float): Scale factor. Default to 1.0

    peak_centre (float): Centre of peak. Default to 0.0

    diffusion_coeff (float): self-diffusion coefficient (Angstrom**2.meV).
                             Default to 1.0
    Q (float): . Default to 1.0
    Examples
    --------
        >>> QENSmodels.jump_diffusion(1,1,0,1,1)
        0.15915494309189535
        
    The function is defined as:
    .. math::
        \text{jump_diffusion}(x, \text{scale}, \text{centre}, \text{D}, \text{Q})
        = \frac{\text{scale}}{\pi}
        \frac{\frac{1}{2}\text{DQ}^2}{(x-\text{centre})^2
        + \big(\frac{1}{2}\text{DQ}^2\big)^2}
    References
    ----------
    None
    """
    fwhm = 2. * diffusion_coeff * Q ** 2
    model = QENSmodels.lorentzian(x, scale_factor, peak_centre, fwhm)

    return model