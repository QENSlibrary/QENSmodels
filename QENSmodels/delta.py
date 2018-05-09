import numpy as np


def delta(x, scale=1, center=0):
    """ Dirac Delta function is equal to zero except for the value of x
       closest to center.

    Parameters
    ----------
    x: :class:`~numpy:numpy.ndarray` or list
        Domain of the function

    scale: float
        Integrated intensity of the curve. Default to 1.

    center: float
        Position of the peak. Default to 0.

    Return
    ------
    :class:`~numpy:numpy.ndarray`
        Output array containing an impulse signal

    Examples
    --------
    >>> QENSmodels.delta([0, 1, 2], 1, 0)
    array([ 0.,  1.,  0.])

    >>> QENSmodels.delta([0, 1, 2, 3, 4], 5, 2)
    array([ 0.,  0.,  5.,  0.,  0.])

    """
    # Input validation
    x = np.asarray(x, dtype=np.float32)

    model = np.zeros(x.size)
    idx = np.argmin(np.abs(x - center))
    try:
        dx = 0.5 * np.abs(x[idx + 1] - x[idx - 1])
        model[idx] = scale / dx
        return model
    except ZeroDivisionError:
        print('Division by zero')
    except IndexError:
        print('Index error: x does not hav enough elements')
