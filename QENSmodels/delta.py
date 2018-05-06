import numpy as np


def delta(x, scale=1, center=0):
    """ Dirac Delta function is equal to zero except for the value of x
       closest to center.

    Parameters
    ----------
    x: :class:`~numpy:numpy.ndarray` or list
        Domain of the function

    scale : float
        Integrated intensity of the curve

    center : float
        Position of the peak

    Return
    ------
    :class:`~numpy:numpy.ndarray`

    Examples
    --------
    >>> QENSmodels.delta([0, 1, 2], 1, 0)
    array([ 0.,  1.,  0.])

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
