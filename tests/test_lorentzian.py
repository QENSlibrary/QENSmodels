import os
import sys
import unittest
import numpy
from os.path import join as pjn

import QENSmodels

# resolve path to reference_data
this_module_path = sys.modules[__name__].__file__
data_dir = pjn(os.path.dirname(this_module_path), 'reference_data')


class TestLorentzian(unittest.TestCase):
    """ Tests QENSmodels.lorentzian function """

    def test_type_output(self):
        """ Test type of output depending on type of input x """
        # x = float
        self.assertIsInstance(QENSmodels.lorentzian(1), numpy.float64)
        # x = list
        self.assertIsInstance(QENSmodels.lorentzian([1, 2]), numpy.ndarray)
        # x = numpy.array
        self.assertIsInstance(QENSmodels.lorentzian(numpy.array([1, 2])), numpy.ndarray)

    def test_size_output(self):
        """ Test size of output depending on type of input x """
        self.assertEqual(QENSmodels.lorentzian(1).size, 1)
        self.assertEqual(QENSmodels.lorentzian([1, 2]).size, 2)

    def test_parameter_value(self):
        """ Test the definition of function in border edge cases"""
        # hwhm = 0
        x = [0, 1, 2, 3, 4, 5]
        numpy.testing.assert_array_equal(
            QENSmodels.lorentzian(x, 0.3, 0.4, 0.0),
            QENSmodels.delta(x, 0.3, 0.4))

    def test_reference_data(self):
        """ Test output values in comparison with reference data
                   (file in 'reference data' folder) """

        # load reference data
        ref_data = numpy.loadtxt(pjn(data_dir, "lorentzian_ref_data.dat"))

        # generate data from current model
        # for info: the parameters' values used for the reference data are
        # specified in the README file in the 'reference data' folder
        w = numpy.arange(-2, 2.01, 0.01)
        actual_data = numpy.column_stack([w,
                                          QENSmodels.lorentzian(w,
                                                                scale=3.,
                                                                center=0.25,
                                                                hwhm=0.4)])

        # compare 2 arrays
        numpy.testing.assert_array_almost_equal(ref_data, actual_data, decimal=12)


if __name__ == '__main__':
    unittest.main()
