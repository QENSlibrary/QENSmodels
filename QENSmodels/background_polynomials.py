from __future__ import print_function
import numpy as np
from numpy.polynomial import Polynomial as P


def background_polynomials(w, list_coefficients=0.0):
    r"""
    Polynomials of variable `w` and with coefficients contained in
    'list_coefficients'

    Parameters
    ----------

    w: list or :class:`~numpy:numpy.ndarray`
        energy transfer (in ps)

    list_coefficients: list or float
        list of coefficients for the polynomials in ascending order, i.e.
        the first element is the coefficient for the constant term.
        Default to 0.0 (no background)

    Return
    ------
    `numpy.float64` or :class:`~numpy:numpy.ndarray`
        output number or array

    Examples
    --------
    >>> background_polynomials(5, 1)
    1.0

    >>> background_polynomials(5, [1, 2])
    11.0

    >>> background_polynomials([1,2,3], [1,2,3])
    array([ 6., 17., 34.])
    """

    w = np.asarray(w)  # , dtype=np.float32)

    # check that list_coeff is a list and all elements are numbers
    if isinstance(list_coefficients, list) and \
            all(isinstance(x, (int, float)) for x in list_coefficients):

        return P(list_coefficients)(w)

    elif isinstance(list_coefficients, (int, float)):

        return P(list_coefficients)(w)

    else:
        raise ValueError('problem with input')


if __name__ == "__main__":
    import doctest
    doctest.testmod()
