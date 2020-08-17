import os
import sys
import unittest
import numpy
from os.path import join as pjn

import QENSmodels

# resolve path to reference_data
this_module_path = sys.modules[__name__].__file__
data_dir = pjn(os.path.dirname(this_module_path), 'reference_data')


class TestGaussianModel3D(unittest.TestCase):
    """ Tests functions related to QENSmodels Gaussian Model 3D """

    def test_size_hwhm_gaussian_model_3d(self):
        """ Test size of output of hwhmGaussianModel3D
         The output should contains 3 elements """
        self.assertEqual(
            len(QENSmodels.hwhmGaussianModel3D(1.)), 3)

        self.assertEqual(
            len(QENSmodels.hwhmGaussianModel3D([1., 2.])), 3)

    def test_type_size_hwhm_gaussian_model_3dq_nb(self):
        """ Tests type and size of outputs if input q is a float """
        hwhm, eisf, qisf = QENSmodels.hwhmGaussianModel3D(1.)
        self.assertIsInstance(hwhm, numpy.ndarray)
        self.assertIsInstance(eisf, numpy.ndarray)
        self.assertIsInstance(qisf, numpy.ndarray)

        #  100 terms considered for the sum
        self.assertEqual(hwhm.shape, (1, 100))
        self.assertEqual(eisf.shape, (1,))
        self.assertEqual(qisf.shape, (1, 100))

    def test_type_size_hwhm_gaussian_model_3d_q_array(self):
        """ Tests type and size of outputs if input q is an array """
        # new parameters: q as an array of several values
        q_input = [1., 2.]
        hwhm1, eisf1, qisf1 = QENSmodels.hwhmGaussianModel3D(q_input, 0.33)
        self.assertIsInstance(hwhm1, numpy.ndarray)
        self.assertIsInstance(eisf1, numpy.ndarray)
        self.assertIsInstance(qisf1, numpy.ndarray)

        # hwhm, eisf, qisf contain len(q) lists of 100 elements each
        self.assertEqual(hwhm1.shape, (len(q_input), 100))
        self.assertEqual(len(eisf1), len(q_input))
        self.assertEqual(qisf1.shape, (len(q_input), 100))

        vector_to_test_hwhm1 = [
            0., 0.33, 0.66, 0.99, 1.32, 1.65, 1.98, 2.31, 2.64,
            2.97, 3.3, 3.63, 3.96, 4.29, 4.62, 4.95, 5.28, 5.61,
            5.94, 6.27, 6.6, 6.93, 7.26, 7.59, 7.92, 8.25, 8.58,
            8.91, 9.24, 9.57, 9.9, 10.23, 10.56, 10.89, 11.22,
            11.55, 11.88, 12.21, 12.54, 12.87, 13.20, 13.53, 13.86,
            14.19, 14.52, 14.85, 15.18, 15.51, 15.84, 16.17, 16.50,
            16.83, 17.16, 17.49, 17.82, 18.15, 18.48, 18.81, 19.14,
            19.47, 19.80, 20.13, 20.46, 20.79, 21.12, 21.45, 21.78,
            22.11, 22.44, 22.77, 23.10, 23.43, 23.76, 24.09, 24.42,
            24.75, 25.08, 25.41, 25.74, 26.07, 26.40, 26.73, 27.06,
            27.39, 27.72, 28.05, 28.38, 28.71, 29.04, 29.37, 29.70,
            30.03, 30.36, 30.69, 31.02, 31.35, 31.68, 32.01, 32.34,
            32.67]

        numpy.testing.assert_array_almost_equal(hwhm1,
                                                [vector_to_test_hwhm1,
                                                 vector_to_test_hwhm1])

        numpy.testing.assert_array_almost_equal(eisf1,
                                                [0.36787944, 0.01831564])

        vector_to_test_part_of_qisf1 = [0.00000000e+00, 3.67879441e-01,
                                        1.83939721e-01, 6.13132402e-02,
                                        1.53283100e-02, 3.06566201e-03,
                                        5.10943668e-04, 7.29919526e-05,
                                        9.12399408e-06, 1.01377712e-06,
                                        1.01377712e-07, 9.21615563e-09,
                                        7.68012969e-10, 5.90779207e-11,
                                        4.21985148e-12, 2.81323432e-13,
                                        1.75827145e-14, 1.03427732e-15,
                                        5.74598513e-17, 3.02420270e-18]

        numpy.testing.assert_array_almost_equal(qisf1[0, 0:20],
                                                vector_to_test_part_of_qisf1,
                                                decimal=9)

    def test_raised_error_negative_coeffs(self):
        """ test that an error is raised if D or variance_ux are negative
        or variance_ux=0
        """
        # D = -1, variance_ux = 1
        self.assertRaises(ValueError,
                          QENSmodels.hwhmGaussianModel3D,
                          1,
                          -1, 1)
        # D = 1, variance_ux = -1
        self.assertRaises(ValueError,
                          QENSmodels.hwhmGaussianModel3D,
                          1,
                          1, -1)
        # D = -1, variance_ux = -1
        self.assertRaises(ValueError,
                          QENSmodels.hwhmGaussianModel3D,
                          1,
                          -1, -1)
        # D = -1, variance_ux = 0
        self.assertRaises(ValueError,
                          QENSmodels.hwhmGaussianModel3D,
                          1,
                          -1, 0)

    def test_raised_error_no_q_input(self):
        """ test that an error is raised if no values of q are given as input
        """
        self.assertRaises(TypeError,
                          QENSmodels.sqwGaussianModel3D,
                          1)

    def test_type_sqw_gaussian_model_3d(self):
        """ Test type of output """
        # w, q are floats
        self.assertIsInstance(QENSmodels.sqwGaussianModel3D(1, 1),
                              numpy.ndarray)
        # w, q are vectors
        output = QENSmodels.sqwGaussianModel3D([1, 2, 3], [0.3, 0.4])
        self.assertIsInstance(output, numpy.ndarray)
        self.assertEqual(output.size, 6)
        self.assertEqual(output.shape, (2, 3))

    def test_reference_data(self):
        """ Test output values in comparison with reference data
                  (file in 'reference data' folder) """

        # load reference data
        ref_data = numpy.loadtxt(
            pjn(data_dir, "gaussian_model_3d_ref_data.dat"))

        # generate data from current model
        # for info: the parameters' values used for the reference data are
        # specified in the README file in the 'reference data' folder
        w = numpy.arange(-2, 2.01, 0.01)
        q = 0.7
        actual_data = numpy.column_stack(
            [w, QENSmodels.sqwGaussianModel3D(w, q,
                                              scale=5.,
                                              center=0.5,
                                              D=1.,
                                              variance_ux=1.)])

        numpy.testing.assert_array_almost_equal(ref_data,
                                                actual_data,
                                                decimal=10)


if __name__ == '__main__':
    unittest.main()
