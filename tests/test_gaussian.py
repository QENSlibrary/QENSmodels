import os
import sys
import unittest
import numpy
from os.path import join as pjn

import QENSmodels

# resolve path to reference_data
this_module_path = sys.modules[__name__].__file__
data_dir = pjn(os.path.dirname(this_module_path), 'reference_data')


class TestGaussian(unittest.TestCase):
    """ Tests QENSmodels.gaussian function"""

    def test_type_output(self):
        """ Test type of output depending on type of input """
        # variable is a float
        self.assertIsInstance(QENSmodels.gaussian(3, 1, 1, 1), numpy.float64)
        # variable is an array
        self.assertIsInstance(QENSmodels.gaussian([1, 3], 1, 1, 1),
                              numpy.ndarray)

    def test_length_output(self):
        """ Test length of output depending on length of input """
        input_array = [1, 3]
        self.assertEqual(len(QENSmodels.gaussian(input_array, 1, 1, 1)),
                         len(input_array))

        input_array1 = [1, 2, 3]
        self.assertEqual(len(QENSmodels.gaussian(input_array1, 1, 1, 1)),
                         len(input_array1))

    def test_parameter_value(self):
        """ Test the definition of function in border edge cases"""
        # sigma = 0
        x = [0, 1, 2, 3, 4, 5]
        numpy.testing.assert_array_equal(
            QENSmodels.gaussian(x, 0.3, 0.4, 0.0),
            QENSmodels.delta(x, 0.3, 0.4))

    def test_reference_data(self):
        """ Test output values in comparison with reference data
        (file in 'reference data' folder)
        """

        # load reference data
        ref_data = numpy.loadtxt(pjn(data_dir, "gaussian_ref_data.dat"))

        # generate data from current model
        # for info: the parameters' values used for the reference data are
        # specified in the README file in the 'reference data' folder
        w = numpy.arange(-2, 2.01, 0.01)
        actual_data = numpy.column_stack([w,
                                          QENSmodels.gaussian(w,
                                                              scale=1,
                                                              center=0.25,
                                                              sigma=0.4)])

        # compare the 2 arrays
        numpy.testing.assert_array_almost_equal(ref_data,
                                                actual_data,
                                                decimal=13)


if __name__ == '__main__':
    unittest.main()
