import os
import sys
import unittest
import numpy
from os.path import join as pjn

import QENSmodels

# resolve path to reference_data
this_module_path = sys.modules[__name__].__file__
data_dir = pjn(os.path.dirname(this_module_path), 'reference_data')


class TestIsotropicRotationalDiffusion(unittest.TestCase):
    """ Tests functions related to QENSmodels Isotropic Rotational Diffusion
    model """

    def test_size_hwhm_isotropic_rotational_diffusion(self):
        """ Test size of output of hwhmIsotropicRotationalDiffusion
         The output should contains 3 elements """
        self.assertEqual(len(QENSmodels.hwhmIsotropicRotationalDiffusion(1.)), 3)

        self.assertEqual(len(QENSmodels.hwhmIsotropicRotationalDiffusion([1., 2.])), 3)

    def test_type_size_hwhm_isotropic_rotational_diffusion_q_nb(self):
        """ Tests type and size of outputs if input q is a float """
        hwhm, eisf, qisf = QENSmodels.hwhmIsotropicRotationalDiffusion(1.)
        self.assertIsInstance(hwhm, numpy.ndarray)
        self.assertIsInstance(eisf, numpy.ndarray)
        self.assertIsInstance(qisf, numpy.ndarray)

        # Only 6 terms considered for the sum
        self.assertEqual(hwhm.shape, (1, 6))
        self.assertEqual(eisf.shape, (1,))
        self.assertEqual(qisf.shape, (1, 6))

    def test_type_size_hwhm_isotropic_rotational_diffusion_q_array(self):
        """ Tests type and size of outputs if input q is an array """
        # new parameters: q as an array of several values
        q_input = [1., 2.]
        hwhm1, eisf1, qisf1 = QENSmodels.hwhmIsotropicRotationalDiffusion(q_input, 0.33)
        self.assertIsInstance(hwhm1, numpy.ndarray)
        self.assertIsInstance(eisf1, numpy.ndarray)
        self.assertIsInstance(qisf1, numpy.ndarray)

        # hwhm, eisf, qisf contain len(q) lists of 6 elements each
        self.assertEqual(hwhm1.shape, (len(q_input), 6))
        self.assertEqual(len(eisf1), len(q_input))
        self.assertEqual(qisf1.shape, (len(q_input), 6))

        numpy.testing.assert_array_almost_equal(hwhm1, [[0., 2., 6., 12., 20., 30.],
                                                        [0., 2., 6., 12., 20., 30.]])

        numpy.testing.assert_array_almost_equal(eisf1, [0.96422296, 0.86297592])

        numpy.testing.assert_array_almost_equal(qisf1,
                                                [[0.0,
                                                  0.03551672903086711,
                                                  0.0002594663738646704,
                                                  8.101124885204693e-07,
                                                  1.4034256030967066e-09,
                                                  1.546123570147362e-12],
                                                 [0.0,
                                                  0.13301247630412252,
                                                  0.003961353757310054,
                                                  4.999387838209268e-05,
                                                  3.4874353496359854e-07,
                                                  1.5438841983563282e-09]],
                                                decimal=9)

    def test_raised_error_negative_coeffs(self):
        """ test that an error is raised if radius or DR are negative """
        # radius = -1, DR = 1
        self.assertRaises(ValueError, QENSmodels.hwhmIsotropicRotationalDiffusion, 1, -1, 1)
        # radius = 1, DR = -1
        self.assertRaises(ValueError, QENSmodels.hwhmIsotropicRotationalDiffusion, 1, 1, -1)
        # radius = -1, DR = -1
        self.assertRaises(ValueError, QENSmodels.hwhmIsotropicRotationalDiffusion, 1, -1, -1)

    def test_raised_error_no_q_input(self):
        """ test that an error is raised if no values of q are given as input
        """
        self.assertRaises(TypeError, QENSmodels.sqwIsotropicRotationalDiffusion, 1)

    def test_type_sqw_isotropic_rotational_diffusion(self):
        """ Test type of output """
        # w, q are floats
        self.assertIsInstance(QENSmodels.sqwIsotropicRotationalDiffusion(1, 1), numpy.ndarray)
        # w, q are vectors
        output = QENSmodels.sqwIsotropicRotationalDiffusion([1, 2, 3], [0.3, 0.4])
        self.assertIsInstance(output, numpy.ndarray)
        self.assertEqual(output.size, 6)
        self.assertEqual(output.shape, (2, 3))

    def test_reference_data(self):
        """ Test output values in comparison with reference data
                  (file in 'reference data' folder) """

        # load reference data
        ref_data = numpy.loadtxt(pjn(data_dir, "isotropic_rotational_diffusion_ref_data.dat"))

        # generate data from current model
        # for info: the parameters' values used for the reference data are
        # specified in the README file in the 'reference data' folder
        w = numpy.arange(-2, 2.01, 0.01)
        q = 0.7
        actual_data = numpy.column_stack(
            [w, QENSmodels.sqwIsotropicRotationalDiffusion(w, q,
                                                           scale=1.0,
                                                           center=0.0,
                                                           radius=2.0,
                                                           DR=0.05)])

        numpy.testing.assert_array_almost_equal(ref_data, actual_data, decimal=11)


if __name__ == '__main__':
    unittest.main()
