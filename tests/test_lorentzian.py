import unittest
import numpy

import QENSmodels


class TestLorentzian(unittest.TestCase):
    """ Tests QENSmodels.lorentzian function """

    def test_type_output(self):
        """ Test type of output depending on type of input x """
        # x = float
        self.assertIsInstance(QENSmodels.lorentzian(1), numpy.float64)
        # x = list
        self.assertIsInstance(QENSmodels.lorentzian([1, 2]), numpy.ndarray)
        # x = numpy.array
        self.assertIsInstance(QENSmodels.lorentzian(numpy.array([1, 2])),
                              numpy.ndarray)

    def test_size_output(self):
        """ Test size of output depending on type of input x """
        self.assertEqual(QENSmodels.lorentzian(1).size, 1)
        self.assertEqual(QENSmodels.lorentzian([1, 2]).size, 2)

    def test_reference_data(self):
        """ Test output values in comparison with reference data
                   (file in 'reference data' folder) """

        # load reference data
        ref_data = numpy.loadtxt("./reference_data/lorentzian_ref_data.dat")

        # generate data from current model
        # for info: the parameters' values used for the reference data are
        # specified in the README file in the 'reference data' folder
        w = numpy.arange(-2, 2.01, 0.01)
        actual_data = numpy.column_stack([w,
                                          QENSmodels.lorentzian(w, scale=3.,
                                                                center=0.25,
                                                                hwhm=0.4)])

        # compare 2 arrays
        numpy.testing.assert_array_almost_equal(ref_data, actual_data)


if __name__ == '__main__':
    unittest.main()
