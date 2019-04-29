import os
import sys
import unittest
import numpy
from os.path import join as pjn

import QENSmodels

# resolve path to reference_data
this_module_path = sys.modules[__name__].__file__
data_dir = pjn(os.path.dirname(this_module_path), 'reference_data')


class TestBackgroundPolynomials(unittest.TestCase):
    """ Tests QENSmodels.background_polynomials function"""

    def test_type_output(self):
        """ test types of outputs depending on types of inputs of x
        (float or array)"""
        self.assertIsInstance(QENSmodels.background_polynomials(1, [1, 2, 3]),
                              numpy.float64)

        self.assertIsInstance(QENSmodels.background_polynomials([1, 2, 3],
                                                                [1, 2, 3]),
                              numpy.ndarray)

    def test_output_when_no_coeff(self):
        """ test that output = 0 if no list of coefficients given """
        self.assertEqual(QENSmodels.background_polynomials(1), 0.0)
        self.assertEqual(QENSmodels.background_polynomials(3.21), 0.0)

    def test_raised_error(self):
        """ test that an exception is raised if the input list of coefficients
        is incorrect, for example, if not all elements are numbers"""
        self.assertRaises(ValueError, QENSmodels.background_polynomials,
                          [1, 2, 3],
                          [1, 2, 'a'])

    def test_reference_data(self):
        """ Test output values in comparison with reference data
                   (file in 'reference data' folder) """

        # load reference data
        ref_data = numpy.loadtxt(pjn(data_dir,
                                     "background_polynomials_ref_data.dat"))

        # generate data from current model
        # for info: the parameters' values used for the reference data are
        # specified in the README file in the 'reference data' folder
        w = numpy.arange(-2, 2.01, 0.01)
        actual_data = numpy.column_stack([w, QENSmodels.background_polynomials(w, [1, 2, 3])]) # noqa:

        # compare the 2 arrays
        numpy.testing.assert_array_almost_equal(ref_data,
                                                actual_data,
                                                decimal=13)


if __name__ == '__main__':
    unittest.main()
