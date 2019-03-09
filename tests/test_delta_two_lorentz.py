import unittest
import numpy

import QENSmodels


class TestDeltaTwoLorentz(unittest.TestCase):
    """ Tests QENSmodels.delta_two_lorentz function"""

    def test_type_output(self):
        """ Test type of output """
        self.assertIsInstance(QENSmodels.sqwDeltaTwoLorentz(1, 1),
                              numpy.ndarray)

    def test_size_output(self):
        """ Test size of output """
        w_input = [1, 2, 3]
        q_input = [0.05, 0.3]
        sqw = QENSmodels.sqwDeltaTwoLorentz(w_input, q_input, 0.5, 2,
                                            [0.75, 0.5], [1, 2], [0.05, 0.04],
                                            [0.02, 0.03])
        size_output = sqw.shape
        self.assertEqual(size_output[0], len(q_input))
        self.assertEqual(size_output[1], len(w_input))

    def test_raised_exception(self):
        """ Test that exceptions are raised if the sizes of A0, A1, hwhm1
        and hwhm2 do not match the size of q """
        w = [0, 1, 2]
        q = [0.1, 0.2, 0.3]
        self.assertRaises(TypeError, QENSmodels.sqwDeltaTwoLorentz, w, q)
        self.assertRaises(IndexError, QENSmodels.sqwDeltaTwoLorentz, w, q, 1,
                          0, [1, 1], [1, 1], [1, 1], [1, 1])

    def test_raised_error_no_q_input(self):
        """ test that an error is raised if no values of q are given as input
        """
        self.assertRaises(TypeError,
                          QENSmodels.sqwDeltaTwoLorentz, 1)

    def test_reference_data(self):
        """ Test output values in comparison with reference data
                   (file in 'reference data' folder) """

        # load reference data
        ref_data = numpy.loadtxt(
            "./reference_data/delta_two_lorentz_ref_data.dat")

        # generate data from current model
        # for info: the parameters' values used for the reference data are
        # specified in the README file in the 'reference data' folder
        w = numpy.arange(-2, 2.01, 0.01)
        q = 0.7
        output = numpy.column_stack(
            [w, QENSmodels.sqwDeltaTwoLorentz(w, q,
                                              scale=1.,
                                              center=0,
                                              A0=0.01,
                                              A1=0.4,
                                              hwhm1=0.25,
                                              hwhm2=0.75)])

        # compare the 2 arrays
        numpy.testing.assert_array_almost_equal(ref_data,
                                                output,
                                                decimal=12)


if __name__ == '__main__':
    unittest.main()
