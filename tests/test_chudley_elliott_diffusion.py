import os
import sys
import unittest
import numpy
from os.path import join as pjn

import QENSmodels

# resolve path to reference_data
this_module_path = sys.modules[__name__].__file__
data_dir = pjn(os.path.dirname(this_module_path), 'reference_data')


class TestChudleyElliottDiffusion(unittest.TestCase):
    """ Tests QENSmodels.chudley_elliott_diffusion function"""

    def test_size_hwhm_chudley_elliott_diffusion(self):
        """ Test size of output of hwhmChudleyElliottDiffusion
        The output should contains 3 elements
        """
        self.assertEqual(
            len(QENSmodels.hwhmChudleyElliottDiffusion(1.)), 3)

        self.assertEqual(
            len(QENSmodels.hwhmChudleyElliottDiffusion([1., 2.])), 3)

    def test_type_size_hwhm_chudley_elliott_diffusion_q_nb(self):
        """ Tests type and size of outputs if input q is a float """
        hwhm, eisf, qisf = QENSmodels.hwhmChudleyElliottDiffusion(1.)
        self.assertIsInstance(hwhm, numpy.ndarray)
        self.assertIsInstance(eisf, numpy.ndarray)
        self.assertIsInstance(qisf, numpy.ndarray)

        self.assertEqual(len(hwhm), 1)
        self.assertEqual(len(eisf), 1)
        self.assertEqual(len(qisf), 1)

        self.assertEqual(eisf, 0.)
        self.assertEqual(qisf, 1.)

    def test_type_size_hwhm_chudley_elliott_diffusion_q_array(self):
        """ Tests type and size of outputs if input q is an array """
        # new parameters: q as an array of several values
        q_input = [1., 2.]
        hwhm1, eisf1, qisf1 = QENSmodels.hwhmChudleyElliottDiffusion(
            q_input, 0.33)
        self.assertIsInstance(hwhm1, numpy.ndarray)
        self.assertIsInstance(eisf1, numpy.ndarray)
        self.assertIsInstance(qisf1, numpy.ndarray)

        # hwhm, eisf, qisf contain len(q) lists of 6 elements each
        self.assertEqual(len(hwhm1), len(q_input))
        self.assertEqual(len(eisf1), len(q_input))
        self.assertEqual(len(qisf1), len(q_input))

        numpy.testing.assert_array_almost_equal(hwhm1, [0.313887, 1.079795])

        self.assertSequenceEqual(eisf1.tolist(), numpy.zeros(2).tolist())

        self.assertSequenceEqual(qisf1.tolist(), numpy.ones(2).tolist())

    def test_raised_error_negative_coeffs(self):
        """ test that an error is raised if D or L are negative
        """
        # D = -1, L = 1
        self.assertRaises(ValueError,
                          QENSmodels.hwhmChudleyElliottDiffusion,
                          1,
                          -1, 1)
        # D = 1, L = -1
        self.assertRaises(ValueError,
                          QENSmodels.hwhmChudleyElliottDiffusion,
                          1,
                          1, -1)
        # D = -1, L = -1
        self.assertRaises(ValueError,
                          QENSmodels.hwhmChudleyElliottDiffusion,
                          1,
                          -1, -1)

    def test_raised_error_no_q_input(self):
        """ test that an error is raised if no values of q are given as input
        """
        self.assertRaises(TypeError,
                          QENSmodels.sqwChudleyElliottDiffusion,
                          1)

    def test_type_sqw_chudley_elliott_diffusion(self):
        """ Test type of output """
        # w, q are floats
        self.assertIsInstance(QENSmodels.sqwChudleyElliottDiffusion(1, 1),
                              numpy.ndarray)
        # w, q are vectors
        output = QENSmodels.sqwChudleyElliottDiffusion([1, 2, 3],
                                                       [0.3, 0.4])
        self.assertIsInstance(output, numpy.ndarray)
        self.assertEqual(output.size, 6)
        self.assertEqual(output.shape, (2, 3))

    def test_reference_data(self):
        """ Test output values in comparison with reference data
        (file in 'reference data' folder)
        """

        # load reference data
        ref_data = numpy.loadtxt(
            pjn(data_dir, "chudley_elliott_diffusion_ref_data.dat"))

        # generate data from current model
        # for info: the parameters' values used for the reference data are
        # specified in the README file in the 'reference data' folder
        w = numpy.arange(-2, 2.01, 0.01)
        q = 0.7
        actual_data = numpy.column_stack(
            [w, QENSmodels.sqwChudleyElliottDiffusion(w,
                                                      q,
                                                      scale=1,
                                                      center=0,
                                                      D=0.23,
                                                      L=1.)])
        numpy.testing.assert_array_almost_equal(ref_data,
                                                actual_data,
                                                decimal=12)


if __name__ == '__main__':
    unittest.main()
