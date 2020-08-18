import os
import sys
import unittest
import numpy
from os.path import join as pjn

import QENSmodels

# resolve path to reference_data
this_module_path = sys.modules[__name__].__file__
data_dir = pjn(os.path.dirname(this_module_path), 'reference_data')


class TestDelta(unittest.TestCase):
    """ Tests QENSmodels.delta function"""

    def test_length_output(self):
        """ Test size of output """
        input_array = [0, 1, 2, 3, 4]
        output_array = QENSmodels.delta(input_array, 5, 2)
        # array([0., 0., 5., 0., 0.])
        self.assertEqual(len(input_array), len(output_array))

    def test_type_output(self):
        """ Test type of output """
        input_array = [0, 1, 2, 3, 4]
        output_array = QENSmodels.delta(input_array, 5, 2)
        self.assertIsInstance(output_array, numpy.ndarray)
        input_nb1 = 2
        output_array1 = QENSmodels.delta(input_nb1, 5, 2)
        self.assertIsInstance(output_array1, numpy.ndarray)

    def test_reference_data(self):
        """ Test output values in comparison with reference data
                   (file in 'reference data' folder) """

        # load reference data
        ref_data = numpy.loadtxt(pjn(data_dir, "delta_ref_data.dat"))

        # generate data from current model
        # for info: the parameters' values used for the reference data are
        # specified in the README file in the 'reference data' folder
        w = numpy.arange(-2, 2.01, 0.01)
        actual_data = numpy.column_stack(
            [w, QENSmodels.delta(w, scale=3.3, center=0)])

        # compare the 2 arrays
        numpy.testing.assert_array_almost_equal(ref_data, actual_data, decimal=10)


if __name__ == '__main__':
    unittest.main()
