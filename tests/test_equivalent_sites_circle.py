import os
import sys
import unittest
import numpy
from os.path import join as pjn

import QENSmodels

# resolve path to reference_data
this_module_path = sys.modules[__name__].__file__
data_dir = pjn(os.path.dirname(this_module_path), 'reference_data')


class TestEquivalentSitesCircle(unittest.TestCase):
    """ Tests QENSmodels.equivalent_sites_circle function"""

    def test_size_hwhm_equivalent_sites_circle(self):
        """ Test size of output of hwhmEquivalentSitesCircle
         The output should contains 3 elements """
        self.assertEqual(
            len(QENSmodels.hwhmEquivalentSitesCircle(1.)), 3)

        self.assertEqual(
            len(QENSmodels.hwhmEquivalentSitesCircle([1., 2.])), 3)

    def test_type_size_hwhm_equivalent_sites_circle_q_nb(self):
        """ Tests type and size of outputs if input q is a float """
        hwhm, eisf, qisf = QENSmodels.hwhmEquivalentSitesCircle(1.)
        self.assertIsInstance(hwhm, numpy.ndarray)
        self.assertIsInstance(eisf, numpy.ndarray)
        self.assertIsInstance(qisf, numpy.ndarray)

        self.assertEqual(hwhm.shape, (1, 3))
        self.assertEqual(len(eisf), 1)
        self.assertEqual(qisf.shape, (1, 2))

        self.assertEqual(round(eisf[0], 3), 0.713)
        self.assertSequenceEqual(numpy.round(qisf, 3).tolist(),
                                 [[0.143, 0.143]])

    def test_type_size_hwhm_equivalent_sites_circles_q_array(self):
        """ Tests type and size of outputs if input q is an array """
        # new parameters: q as an array of several values
        q_input = [1., 2.]
        hwhm1, eisf1, qisf1 = QENSmodels.hwhmEquivalentSitesCircle(
            q_input, N=6, radius=1.0, resTime=1.0)
        self.assertIsInstance(hwhm1, numpy.ndarray)
        self.assertIsInstance(eisf1, numpy.ndarray)
        self.assertIsInstance(qisf1, numpy.ndarray)

        # hwhm, eisf, qisf contain len(q) lists of 6 elements each
        self.assertEqual(hwhm1.shape, (2, 6))
        self.assertEqual(len(eisf1), len(q_input))
        self.assertEqual(qisf1.shape, (2, 5))

        numpy.testing.assert_array_almost_equal(hwhm1,
                                                [[0., 0.5, 1.5, 2., 1.5, 0.5],
                                                 [0., 0.5, 1.5, 2., 1.5, 0.5]])

        numpy.testing.assert_array_equal(numpy.round(eisf1, 3), [0.713, 0.256])

        numpy.testing.assert_array_equal(numpy.round(qisf1, 3),
                                         [[0.136, 0.007, 0., 0.007, 0.136],
                                          [0.289, 0.075, 0.016, 0.075, 0.289]])

    # def test_raised_error_negative_coeffs(self):
    #     """ test that an error is raised if D or L are negative
    #     """
    #     # D = -1, L = 1
    #     self.assertRaises(ValueError,
    #                       QENSmodels.hwhmEquivalentSitesCircle,
    #                       1,
    #                       -1, 1)
    #     # D = 1, L = -1
    #     self.assertRaises(ValueError,
    #                       QENSmodels.hwhmEquivalentSitesCircle,
    #                       1,
    #                       1, -1)
    #     # D = -1, L = -1
    #     self.assertRaises(ValueError,
    #                       QENSmodels.hwhmEquivalentSitesCircle,
    #                       1,
    #                       -1, -1)

    def test_raised_error_no_q_input(self):
        """ test that an error is raised if no values of q are given as input
        """
        self.assertRaises(TypeError,
                          QENSmodels.sqwEquivalentSitesCircle,
                          1)

    def test_type_sqw_equivalent_sites_circle(self):
        """ Test type of output """
        # w, q are floats
        self.assertIsInstance(QENSmodels.sqwEquivalentSitesCircle(1, 1),
                              numpy.ndarray)
        # w, q are vectors
        output = QENSmodels.sqwEquivalentSitesCircle([1, 2, 3],
                                                     [0.3, 0.4])
        self.assertIsInstance(output, numpy.ndarray)
        self.assertEqual(output.size, 6)
        self.assertEqual(output.shape, (2, 3))

    def test_reference_data(self):
        """ Test output values in comparison with reference data
                  (file in 'reference data' folder) """
        # load reference data
        ref_data = numpy.loadtxt(
            pjn(data_dir, "equivalent_sites_circle_ref_data.dat"))

        # generate data from current model
        # for info: the parameters' values used for the reference data are
        # specified in the README file in the 'reference data' folder
        w = numpy.arange(-2, 2.01, 0.01)
        q = 0.7
        actual_data = numpy.column_stack(
            [w, QENSmodels.sqwEquivalentSitesCircle(w,
                                                    q,
                                                    scale=.01,
                                                    center=0.5,
                                                    N=3,
                                                    radius=100.0,
                                                    resTime=10.)])
        numpy.testing.assert_array_almost_equal(ref_data,
                                                actual_data,
                                                decimal=12)


if __name__ == '__main__':
    unittest.main()
