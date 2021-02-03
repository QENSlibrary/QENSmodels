import os
import sys
import unittest
import numpy
from os.path import join as pjn

import QENSmodels

# resolve path to reference_data
this_module_path = sys.modules[__name__].__file__
data_dir = pjn(os.path.dirname(this_module_path), 'reference_data')


class TestBrownianTranslationDiffusion(unittest.TestCase):
    """ Tests functions related to QENSmodels Brownian Translation Diffusion
    model
    """

    def test_size_hwhm_brownian_translation_diffusion(self):
        """ test number of output of hwhm function of
        Brownian Translation Diffusion model
        it should be 3: hwhm, eisf and qisf
        """
        output = QENSmodels.hwhmBrownianTranslationalDiffusion(1.)
        self.assertEqual(len(output), 3)

    def test_type_output_hwhm_brownian_translation_diffusion(self):
        """ test type of output: numpy array for the 3 outputs """
        hwhm, eisf, qisf = QENSmodels.hwhmBrownianTranslationalDiffusion(1.)
        self.assertIsInstance(hwhm, numpy.ndarray)
        self.assertIsInstance(eisf, numpy.ndarray)
        self.assertIsInstance(qisf, numpy.ndarray)

        self.assertEqual(eisf, 0.)
        self.assertEqual(qisf, 1.)

    def test_size_output_fct_q_hwhm_brownian_translation_diffusion(self):
        """ these numpy arrays have a size depending on the input q-values """
        hwhm1, eisf1, qisf1 = \
            QENSmodels.hwhmBrownianTranslationalDiffusion([1., 2.], 0.33)
        self.assertEqual(len(hwhm1), 2)
        self.assertEqual(len(eisf1), 2)
        self.assertEqual(len(qisf1), 2)

    def test_content_output_fct_q_hwhm_brownian_translation_diffusion(self):
        """ test values of outputs """
        hwhm, eisf, qisf = \
            QENSmodels.hwhmBrownianTranslationalDiffusion([1., 2.], 0.33)

        numpy.testing.assert_array_almost_equal(hwhm, [0.33, 1.32], decimal=2)

        self.assertSequenceEqual(eisf.tolist(), numpy.zeros(2).tolist())

        self.assertSequenceEqual(qisf.tolist(), numpy.ones(2).tolist())

    def test_type_sqw_brownian_translation_diffusion(self):
        """ test type of output of sqw function """
        self.assertIsInstance(
            QENSmodels.sqwBrownianTranslationalDiffusion(1, 1, 1, 0, 1),
            numpy.ndarray)

    def test_size_sqw_brownian_translation_diffusion(self):
        """ test size of output of sqwBrownianTranslationalDiffusion """
        output = QENSmodels.sqwBrownianTranslationalDiffusion([1, 2, 3],
                                                              [0.3, 0.4],
                                                              1, 0, 1)
        self.assertIsInstance(output, numpy.ndarray)
        self.assertEqual(output.size, 6)
        self.assertEqual(output.shape, (2, 3))

    def test_raised_error_no_q_input(self):
        """ test that an error is raised if no values of q are given as input
        """
        self.assertRaises(TypeError,
                          QENSmodels.sqwBrownianTranslationalDiffusion,
                          1)

    def test_raised_error_negative_diffusion_coeff(self):
        """ test that an error is raised if the diffusion coefficient is
        negative
        """
        self.assertRaises(ValueError,
                          QENSmodels.hwhmBrownianTranslationalDiffusion,
                          1,
                          -1)

    def test_reference_data(self):
        """ test output values in comparison with reference data
        (file in 'reference data' folder)
        """

        # load reference data
        ref_data = numpy.loadtxt(
            pjn(data_dir, 'brownian_translational_diffusion_ref_data.dat'))

        # generate data from current model
        # for info: the parameters' values used for the reference data are
        # specified in the README file in the 'reference data' folder
        w = numpy.arange(-2, 2.01, 0.01)
        q = 0.7
        actual_data = numpy.column_stack(
            [w,
             QENSmodels.sqwBrownianTranslationalDiffusion(w, q, 1., 0., 1.)])

        # compare the 2 arrays
        numpy.testing.assert_array_almost_equal(ref_data,
                                                actual_data,
                                                decimal=13)


if __name__ == '__main__':
    unittest.main()
