import numpy as np
import QENSmodels
import doctest


def delta(x, scale=1, center=0):
    r""" Dirac Delta function

    It is equal to zero except for the value of x closest to center.

    Parameters
    ----------
    x: list or :class:`~numpy:numpy.ndarray`
        domain of the function

    scale: float
        integrated intensity of the curve. Default to 1.

    center: float
        position of the peak. Default to 0.

    Return
    ------
    :class:`~numpy:numpy.ndarray`
        output array containing an impulse signal

    Examples
    --------
    >>> delta = QENSmodels.delta([0, 1, 2], 1, 0)
    >>> delta[0]
    1.0
    >>> delta[1]
    0.0
    >>> delta[2]
    0.0

    >>> delta = QENSmodels.delta([0, 1, 2, 3, 4], 5, 2)
    >>> delta[0]
    0.0
    >>> delta[1]
    0.0
    >>> delta[2]
    5.0
    >>> delta[3]
    0.0
    >>> delta[4]
    0.0

    Notes
    -----
    * A Delta (Dirac)function is defined as

    .. math::

        \text{Delta}(x, \text{scale}, \text{center}) = \text{scale}
        \delta(x- \text{center})


    * For non-zero values, the amplitude of the Delta function is divided by
      the x-spacing.

    * **Equivalence**

      +-------------+--------------------+
      | Equivalence | Mantid             |
      +=============+====================+
      | ``delta``   | ``DeltaFunction``  |
      +-------------+--------------------+
      | ``scale``   |  Height            |
      +-------------+--------------------+
      | ``center``  |  Centre            |
      +-------------+--------------------+


    """
    # Input validation
    if isinstance(x, (float, int)):
        x = [float(x)]

    x = np.asarray(x)

    # sort x in ascending order if x has more than 1 element
    # if x.size > 1:
    #    x.sort()

    model = np.zeros(x.size)

    try:
        if x.min() <= center <= x.max():
            # if center within x-range, delta is non-zero in this interval
            # otherwise do nothing
            idx = np.argmin(np.abs(x - center))
            if len(x) > 1:
                dx = (x[-1] - x[0]) / (len(x) - 1)  # domain spacing
            else:
                dx = 1.
            model[idx] = scale / dx
        # dx = 0.5 * np.abs(x[idx + 1] - x[idx - 1])

        return model
    except ZeroDivisionError:
        print('Division by zero')
    except IndexError:
        print('Index error: x does not have enough elements')
