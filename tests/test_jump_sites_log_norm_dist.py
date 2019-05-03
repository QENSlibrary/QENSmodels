import os
import sys
import unittest
import numpy
from os.path import join as pjn

import QENSmodels

# resolve path to reference_data
this_module_path = sys.modules[__name__].__file__
data_dir = pjn(os.path.dirname(this_module_path), 'reference_data')


class TestJumpsSitesLogNorm(unittest.TestCase):
    """ Tests QENSmodels.jump_sites_log_norm_dist function"""

    def test_size_hwhm_jump_sites_log_norm(self):
        """ Test size of output of hwhmJumpSitesLogNormDist
         The output should contains 3 elements """
        self.assertEqual(
            len(QENSmodels.hwhmJumpSitesLogNormDist(1.)), 3)

        self.assertEqual(
            len(QENSmodels.hwhmJumpSitesLogNormDist([1., 2.])), 3)

    def test_type_size_hwhm_jump_sites_log_norm_q_nb(self):
        """ Tests type and size of outputs if input q is a float """
        hwhm, eisf, qisf = QENSmodels.hwhmJumpSitesLogNormDist(1.)
        self.assertIsInstance(hwhm, numpy.ndarray)
        self.assertIsInstance(eisf, numpy.ndarray)
        self.assertIsInstance(qisf, numpy.ndarray)

        self.assertEqual(hwhm.shape, (1, 3, 21))
        self.assertEqual(len(eisf), 1)
        self.assertEqual(qisf.shape, (1, 2, 21))

        self.assertEqual(round(eisf[0], 3), 0.713)
        # eisf should be the same as in hwhmEquivalentSitesCircle
        hwhm_equiv, eisf_equiv, qisf_equiv = \
            QENSmodels.hwhmEquivalentSitesCircle(1.)
        self.assertEqual(eisf[0], eisf_equiv[0])

        self.assertSequenceEqual(numpy.round(qisf[0, 0], 3).tolist(),
                                 [0.001, 0.002, 0.003, 0.004, 0.005,
                                  0.007, 0.009, 0.01, 0.011, 0.012,
                                  0.013, 0.012, 0.011, 0.01, 0.009,
                                  0.007, 0.005, 0.004, 0.003, 0.002,
                                  0.001])

    def test_type_size_hwhm_jump_sites_log_norm_q_array(self):
        """ Tests type and size of outputs if input q is an array """
        # new parameters: q as an array of several values
        q_input = [1., 2.]
        hwhm1, eisf1, qisf1 = QENSmodels.hwhmJumpSitesLogNormDist(
            q_input, N=6, radius=1.0, resTime=1.0, sigma=0.5)

        self.assertIsInstance(hwhm1, numpy.ndarray)
        self.assertIsInstance(eisf1, numpy.ndarray)
        self.assertIsInstance(qisf1, numpy.ndarray)

        # hwhm, eisf, qisf contain len(q) lists of 6 elements each
        self.assertEqual(hwhm1.shape, (2, 6, 21))
        self.assertEqual(len(eisf1), len(q_input))
        self.assertEqual(qisf1.shape, (2, 5, 21))

        numpy.testing.assert_array_equal(numpy.round(hwhm1[0, 1], 3),
                                         [0.171, 0.19, 0.212, 0.236,
                                          0.263, 0.292, 0.326, 0.362,
                                          0.403, 0.449, 0.5, 0.557,
                                          0.62, 0.69, 0.768, 0.855,
                                          0.952, 1.06, 1.18, 1.313,
                                          1.462])

        numpy.testing.assert_array_equal(numpy.round(eisf1, 3), [0.713, 0.256])
        # eisf should be the same as in hwhmEquivalentSitesCircle
        hwhm_equiv, eisf_equiv, qisf_equiv = \
            QENSmodels.hwhmEquivalentSitesCircle(q_input,
                                                 N=6,
                                                 radius=1.0,
                                                 resTime=1.0)

        self.assertSequenceEqual(eisf1.tolist(), eisf_equiv.tolist())

        numpy.testing.assert_array_equal(numpy.round(qisf1[1, 1], 3),
                                         [0.001, 0.001, 0.001, 0.002,
                                          0.003, 0.004, 0.005, 0.005,
                                          0.006, 0.006, 0.007, 0.006,
                                          0.006, 0.005, 0.005, 0.004,
                                          0.003, 0.002, 0.001, 0.001,
                                          0.001])

    def test_raised_error_negative_coeffs(self):
        """ test that an error is raised if radius, resTime are negative or N <2
        """
        # N < 2
        self.assertRaises(ValueError,
                          QENSmodels.hwhmJumpSitesLogNormDist,
                          1, 1, 1, 1, 1)
        # radius < 0
        self.assertRaises(ValueError,
                          QENSmodels.hwhmJumpSitesLogNormDist,
                          1, 4, -1, 1, 1)
        # resTime < 0
        self.assertRaises(ValueError,
                          QENSmodels.hwhmJumpSitesLogNormDist,
                          1, 4, 1, -1, 1)

    def test_raised_error_no_q_input(self):
        """ test that an error is raised if no values of q are given as input
        """
        self.assertRaises(TypeError,
                          QENSmodels.sqwJumpSitesLogNormDist,
                          1)

    def test_type_sqw_jump_sites_log_norm(self):
        """ Test type of output """
        # w, q are floats
        self.assertIsInstance(QENSmodels.sqwJumpSitesLogNormDist(1, 1),
                              numpy.ndarray)
        # w, q are vectors
        output = QENSmodels.sqwJumpSitesLogNormDist([1, 2, 3],
                                                    [0.3, 0.4])
        self.assertIsInstance(output, numpy.ndarray)
        self.assertEqual(output.size, 6)
        self.assertEqual(output.shape, (2, 3))

    def test_reference_data(self):
        """ Test output values in comparison with reference data
                  (file in 'reference data' folder) """
        # load reference data
        ref_data = numpy.loadtxt(
           pjn(data_dir, "jump_sites_log_norm_dist_ref_data.dat"))

        # generate data from current model
        # for info: the parameters' values used for the reference data are
        # specified in the README file in the 'reference data' folder
        w = numpy.arange(-2, 2.01, 0.01)
        q = 0.7
        actual_data = numpy.column_stack(
            [w, QENSmodels.sqwJumpSitesLogNormDist(w, q,
                                                   scale=2,
                                                   center=0.8,
                                                   N=7,
                                                   radius=5,
                                                   resTime=2,
                                                   sigma=0.6)])

        numpy.testing.assert_array_almost_equal(ref_data,
                                                actual_data,
                                                decimal=12)


if __name__ == '__main__':
    unittest.main()
