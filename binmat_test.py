import unittest
from binmat import Bin2dMatrix


class Bin2dMatrixTest(unittest.TestCase):

    def test_create_and_stringify(self):

        with self.subTest('2x2 0s'):
            self.assertEqual(
                str(Bin2dMatrix(2, 2, 0)),
                'Bin2dMatrix 2x2\n'
                '00\n'
                '00'
            )

        with self.subTest('3x3 1s'):
            self.assertEqual(
                str(Bin2dMatrix(3, 3, 0b111111111)),
                'Bin2dMatrix 3x3\n'
                '111\n'
                '111\n'
                '111'
            )

        with self.subTest('3x3 chess'):
            self.assertEqual(
                str(Bin2dMatrix(3, 3, 0b010101010)),
                'Bin2dMatrix 3x3\n'
                '010\n'
                '101\n'
                '010'
            )

        with self.subTest('2x2 1s'):
            self.assertEqual(
                str(Bin2dMatrix(2, 2, 0b1111)),
                'Bin2dMatrix 2x2\n'
                '11\n'
                '11'
            )

        with self.subTest('4x3 with top/left item only'):
            self.assertEqual(
                str(Bin2dMatrix(4, 3, 1)),
                'Bin2dMatrix 4x3\n'
                '1000\n'
                '0000\n'
                '0000'
            )

    def test_from_iterables(self):

        with self.subTest('2x2 0s'):
            self.assertEqual(
                str(Bin2dMatrix.from_iterables([[0,0], [0,0]])),
                'Bin2dMatrix 2x2\n'
                '00\n'
                '00'
            )

        with self.subTest('3x3 1s'):
            self.assertEqual(
                str(Bin2dMatrix.from_iterables(['111', '111', '111'])),
                'Bin2dMatrix 3x3\n'
                '111\n'
                '111\n'
                '111'
            )

        with self.subTest('3x3 chess'):
            self.assertEqual(
                str(Bin2dMatrix.from_iterables([[0,1,0], [1,0,1], [0,1,0]])),
                'Bin2dMatrix 3x3\n'
                '010\n'
                '101\n'
                '010'
            )

        with self.subTest('4x3 with top/left item only'):
            self.assertEqual(
                str(Bin2dMatrix.from_iterables([[1, 0, 0, 0], [], []])),
                'Bin2dMatrix 4x3\n'
                '1000\n'
                '0000\n'
                '0000'
            )

    def test_from_strings(self):

        with self.subTest('2x2 0s'):
            self.assertEqual(
                str(Bin2dMatrix.from_strings(['00', '..'])),
                'Bin2dMatrix 2x2\n'
                '00\n'
                '00'
            )

        with self.subTest('3x3 1s'):
            self.assertEqual(
                str(Bin2dMatrix.from_strings(['111', 'AAA', '***'], ones='[1A*]')),
                'Bin2dMatrix 3x3\n'
                '111\n'
                '111\n'
                '111'
            )

        with self.subTest('3x3 chess'):
            self.assertEqual(
                str(Bin2dMatrix.from_strings(['010', '101', '010'])),
                'Bin2dMatrix 3x3\n'
                '010\n'
                '101\n'
                '010'
            )

        with self.subTest('4x3 with top/left item only'):
            self.assertEqual(
                str(Bin2dMatrix.from_strings(['x...', [], []])),
                'Bin2dMatrix 4x3\n'
                '1000\n'
                '0000\n'
                '0000'
            )
