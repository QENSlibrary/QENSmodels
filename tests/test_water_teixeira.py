import unittest
import numpy

import QENSmodels


class TestWaterTeixeira(unittest.TestCase):
    """ Tests QENSmodels.water_teixeira function"""

    def test_type_output(self):
        """ Test type of output """
        self.assertIsInstance(QENSmodels.sqwWaterTeixeira(1, 1), numpy.ndarray)

    def test_size_output(self):
        """ Test size of output depending on type of input"""
        # w, q are floats

        output = QENSmodels.sqwWaterTeixeira(1, 1)
        self.assertEqual(output.size, 1)
        self.assertEqual(output.shape, (1,))

        # w, q are vectors
        output1 = QENSmodels.sqwWaterTeixeira([1, 2], [0.1, 0.2, 0.3])
        self.assertEqual(output1.size, 6)
        self.assertEqual(output1.shape, (3, 2))

    def test_raised_error_no_q_input(self):
        """ test that an error is raised if no values of q are given as input
        """
        self.assertRaises(TypeError,
                          QENSmodels.sqwWaterTeixeira,
                          1)

    def test_reference_data(self):
        """ Test output values in comparison with reference data
           (file in 'reference data' folder) """

        # load reference data
        ref_data = \
            numpy.loadtxt("./reference_data/water_teixeira_ref_data.dat")

        # generate data from current model
        # for info: the parameters' values used for the reference data are
        # specified in the README file in the 'reference data' folder
        w = numpy.arange(-2, 2.01, 0.01)
        q = 0.7
        actual_data = numpy.column_stack(
            [w, QENSmodels.sqwWaterTeixeira(w, q,
                                            scale=1,
                                            center=0,
                                            D=1,
                                            resTime=1,
                                            radius=1,
                                            DR=1)])
        # compare the 2 arrays
        numpy.testing.assert_array_almost_equal(ref_data,
                                                actual_data,
                                                decimal=13)


if __name__ == '__main__':
    unittest.main()
