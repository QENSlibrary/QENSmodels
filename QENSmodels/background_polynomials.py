import numpy as np
from numpy.polynomial import Polynomial
from typing import Union


def background_polynomials(
        x: Union[float, list, np.ndarray],
        list_coefficients: Union[float, list, np.ndarray] = 0.0
) -> Polynomial:
    r"""
    Polynomials of variable `w` and with coefficients contained in
    'list_coefficients'

    Parameters
    ----------

    x: list or :class:`~numpy:numpy.ndarray`
        domain of the function

    list_coefficients: list or float
        list of coefficients for the polynomials in ascending order, i.e.
        the first element is the coefficient for the constant term.
        Default to 0 (no background).

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


    Mathematically, `background_polynomials(x, [1,2,3])` corresponds to
    :math: 1 + 2x + 3x^2.
    """

    x = np.asarray(x)

    # check that list_coefficients is a list and all elements are numbers
    if isinstance(list_coefficients, list) and \
            all(isinstance(w, (int, float)) for w in list_coefficients):

        return Polynomial(list_coefficients)(x)

    elif isinstance(list_coefficients, (int, float)):

        return Polynomial(list_coefficients)(x)

    else:
        raise ValueError('problem with input')
