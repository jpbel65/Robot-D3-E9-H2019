import unittest
from Gui import BaseStation
import numpy as np


class TestMethods(unittest.TestCase):

    def setUp(self):
        self.station = BaseStation

    def test_Playground_empty(self):
        test_data = np.zeros((400, 200, 3), dtype=np.uint8)
        self.assertEqual(self.station.data.all(), test_data.all())

    def test__draw_Playground(self):

        test_data = np.zeros((400, 200, 3), dtype=np.uint8)
        for i in range(50, 350):
            for j in range(20, 180):
                if (i - 56) % 16 == 0 or (j - 36) % 16 == 0:
                    test_data[i, j] = [0, 0, 0]
                else:
                    test_data[i, j] = [255, 255, 255]
        self.assertEqual(self.station.data.all(), test_data.all())

    def test_isupper(self):
        self.assertTrue('FOO'.isupper())
        self.assertFalse('Foo'.isupper())

    def test_split(self):
        s = 'hello world'
        self.assertEqual(s.split(), ['hello', 'world'])
        # check that s.split fails when the separator is not a string
        with self.assertRaises(TypeError):
            s.split(2)


if __name__ == '__main__':
    unittest.main()
