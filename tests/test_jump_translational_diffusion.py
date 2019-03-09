import unittest
import numpy

import QENSmodels


class TestJumpTranslationalDiffusion(unittest.TestCase):
    """ Tests functions related to QENSmodels Jump Translational Diffusion
    model """

    def test_size_hwhm_jump_translational_diffusion(self):
        """ Test size of output of hwhmJumpTranslationalDiffusion
                 The output should contains 3 elements """
        self.assertEqual(
            len(QENSmodels.hwhmJumpTranslationalDiffusion(1.)), 3)

        self.assertEqual(
            len(QENSmodels.hwhmJumpTranslationalDiffusion([1., 2.])), 3)

    def test_type_size_hwhm_jump_translational_diffusion_q_nb(self):
        """ Tests type and size of outputs if input q is a number """
        hwhm, eisf, qisf = QENSmodels.hwhmJumpTranslationalDiffusion(1.)
        self.assertIsInstance(hwhm, numpy.ndarray)
        self.assertIsInstance(eisf, numpy.ndarray)
        self.assertIsInstance(qisf, numpy.ndarray)

        self.assertEqual(eisf, 0.)
        self.assertEqual(qisf, 1.)

    def test_type_size_hwhm_jump_translational_diffusion_q_array(self):
        """ Tests type and size of outputs if input q is an array """
        q_input = [1., 2.]
        hwhm, eisf, qisf = QENSmodels.hwhmJumpTranslationalDiffusion(q_input,
                                                                     0.5,
                                                                     1.5)
        self.assertIsInstance(hwhm, numpy.ndarray)
        self.assertIsInstance(eisf, numpy.ndarray)
        self.assertIsInstance(qisf, numpy.ndarray)

        numpy.testing.assert_array_almost_equal(hwhm, [0.2857143, 0.5])

        self.assertSequenceEqual(eisf.tolist(), numpy.zeros(2).tolist())

        self.assertSequenceEqual(qisf.tolist(), numpy.ones(2).tolist())

    def test_raised_error_negative_coeffs(self):
        """ test that an error is raised if D or resTime are negative
        """
        # D = -1, resTime = 1
        self.assertRaises(ValueError,
                          QENSmodels.hwhmJumpTranslationalDiffusion,
                          1,
                          -1, 1)
        # D = 1, resTime = -1
        self.assertRaises(ValueError,
                          QENSmodels.hwhmJumpTranslationalDiffusion,
                          1,
                          1, -1)
        # D = -1, resTime = -1
        self.assertRaises(ValueError,
                          QENSmodels.hwhmJumpTranslationalDiffusion,
                          1,
                          -1, -1)

    def test_type_sqw_jump_translational_diffusion(self):
        """ Test type of output """
        # w, q are floats
        self.assertIsInstance(QENSmodels.sqwJumpTranslationalDiffusion(1, 1),
                              numpy.ndarray)
        # w, q are vectors
        output = QENSmodels.sqwJumpTranslationalDiffusion([1, 2, 3],
                                                          [0.3, 0.4])
        self.assertIsInstance(output, numpy.ndarray)
        self.assertEqual(output.size, 6)
        self.assertEqual(output.shape, (2, 3))

    def test_raised_error_no_q_input(self):
        """ test that an error is raised if no values of q are given as input
        """
        self.assertRaises(TypeError,
                          QENSmodels.sqwJumpTranslationalDiffusion,
                          1)

    def test_reference_data(self):
        """ Test output values in comparison with reference data
                  (file in 'reference data' folder) """

        # load reference data
        ref_data = numpy.loadtxt(
            "./reference_data/jump_translational_diffusion_ref_data.dat")

        # generate data from current model
        # for info: the parameters' values used for the reference data are
        # specified in the README file in the 'reference data' folder
        w = numpy.arange(-2, 2.01, 0.01)
        q = 0.7
        actual_data = numpy.column_stack(
            [w, QENSmodels.sqwJumpTranslationalDiffusion(w, q,
                                                         scale=1,
                                                         center=0,
                                                         D=0.23,
                                                         resTime=1.25)])
        # compare the 2 arrays
        numpy.testing.assert_array_almost_equal(ref_data,
                                                actual_data,
                                                decimal=12)


if __name__ == '__main__':
    unittest.main()
