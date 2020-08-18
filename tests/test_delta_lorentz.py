import os
import sys
import unittest
import numpy
from os.path import join as pjn

import QENSmodels

# resolve path to reference_data
this_module_path = sys.modules[__name__].__file__
data_dir = pjn(os.path.dirname(this_module_path), 'reference_data')


class TestDeltaLorentz(unittest.TestCase):
    """ Tests QENSmodels.sqwDeltaLorentz function"""

    def test_type_output(self):
        """ test type of output"""
        output = QENSmodels.sqwDeltaLorentz([1, 2, 3], 0.1)
        self.assertIsInstance(output, numpy.ndarray)

    def test_size_output(self):
        """ test size of output depending on size of input """
        # q is a float
        w_input = [1, 2, 3]
        q_input_nb = 0.1
        output = QENSmodels.sqwDeltaLorentz(w_input, q_input_nb)
        self.assertEqual(len(output), len(w_input))

        # q is an array
        q_input_array = [0.1, 0.2]
        output_array = QENSmodels.sqwDeltaLorentz(w_input, q_input_array, 1, 0, [0, 0], [1, 1])
        size_output = output_array.shape
        self.assertEqual(size_output[0], len(q_input_array))
        self.assertEqual(size_output[1], len(w_input))

    def test_raised_exception(self):
        """ test that exceptions are raised if the sizes of A0 and hwhm do
         not match the size of q """
        w = [0, 1, 2]
        q = [0.1, 0.2, 0.3]
        self.assertRaises(TypeError, QENSmodels.sqwDeltaLorentz, w, q)
        self.assertRaises(IndexError, QENSmodels.sqwDeltaLorentz, w, q, 1, 0, [1, 1], [1, 1])

    def test_raised_error_no_q_input(self):
        """ test that an error is raised if no values of q are given as input """
        self.assertRaises(TypeError, QENSmodels.sqwDeltaLorentz, 1)

    def test_reference_data(self):
        """ Test output values in comparison with reference data
                   (file in 'reference data' folder) """

        # load reference data
        ref_data = numpy.loadtxt(pjn(data_dir, "delta_lorentz_ref_data.dat"))

        # generate data from current model
        # for info: the parameters' values used for the reference data are
        # specified in the README file in the 'reference data' folder
        w = numpy.arange(-2, 2.01, 0.01)
        q = 0.7
        actual_data = numpy.column_stack(
            [w, QENSmodels.sqwDeltaLorentz(w, q, scale=1., center=0.5, A0=0.01, hwhm=1.0)])
        # compare the 2 arrays
        numpy.testing.assert_array_almost_equal(ref_data, actual_data, decimal=13)


if __name__ == '__main__':
    unittest.main()
