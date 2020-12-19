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

    def test_ones_count(self):

        with self.subTest('2x2 0s'):
            self.assertEqual(Bin2dMatrix(2, 2, 0).ones_count, 0)

        with self.subTest('3x3 1s'):
            self.assertEqual(Bin2dMatrix(3, 3, 0b111111111).ones_count, 9)

        with self.subTest('3x3 chess'):
            self.assertEqual(Bin2dMatrix(3, 3, 0b010101010).ones_count, 4)

        with self.subTest('2x2 1s'):
            self.assertEqual(Bin2dMatrix(2, 2, 0b1111).ones_count, 4)

    def test_getitem_positive(self):
        m = Bin2dMatrix.from_strings([
            '01101',
            '10010',
            '11011',
            '01110',
        ])
        self.assertIs(m[0, 0], False)
        self.assertIs(m[0, 1], True)
        self.assertIs(m[1, 0], True)
        self.assertIs(m[4, 0], True)
        self.assertIs(m[0, 3], False)
        self.assertIs(m[4, 3], False)
        self.assertIs(m[2, 3], True)

    def test_getitem_negative(self):
        m = Bin2dMatrix.from_strings([
            '01101',
            '10010',
            '11011',
            '01110',
        ])
        for x, y in [
            [-5, -4],
            [-2, -1],
            [-4, 0],
            [4, -4],
            [0, -1],
            [-1, -1],
            [2, -1],
        ]:
            with self.subTest(f'[{x}, {y}]'):
                with self.assertRaises(ValueError):
                    m[x, y]

    def test_getitem_excess(self):
        m = Bin2dMatrix.from_strings([
            '11111',
            '11111',
            '11111',
            '11111',
        ])
        with self.assertRaises(ValueError):
            m[3, 10], False
        with self.assertRaises(ValueError):
            m[5, 4], False

    def test_expand_matrix_with_ones(self):
        m = Bin2dMatrix.from_strings([
            '11111',
            '11111',
            '11111',
            '11111',
        ])

        with self.subTest('0,0'):
            self.assertEqual(m.expand(0, 0), m)
            self.assertEqual(str(m.expand(0, 0)), str(m))

        with self.subTest('1,1'):
            self.assertEqual(
                str(m.expand(1, 1)),
                'Bin2dMatrix 6x5\n'
                '111110\n'
                '111110\n'
                '111110\n'
                '111110\n'
                '000000'
            )

        with self.subTest('-1,-1'):
            self.assertEqual(
                str(m.expand(-1, -1)),
                'Bin2dMatrix 6x5\n'
                '000000\n'
                '011111\n'
                '011111\n'
                '011111\n'
                '011111'
            )

        with self.subTest('-2,1'):
            self.assertEqual(
                str(m.expand(-2, 1)),
                'Bin2dMatrix 7x5\n'
                '0011111\n'
                '0011111\n'
                '0011111\n'
                '0011111\n'
                '0000000'
            )

        with self.subTest('3, -1'):
            self.assertEqual(
                str(m.expand(3, -1)),
                'Bin2dMatrix 8x5\n'
                '00000000\n'
                '11111000\n'
                '11111000\n'
                '11111000\n'
                '11111000'
            )

    def test_expand_diagonal_matrix(self):
        m = Bin2dMatrix.from_strings([
            '10000',
            '01000',
            '00100',
            '00001',
        ])

        with self.subTest('0,0'):
            self.assertEqual(m.expand(0, 0), m)
            self.assertEqual(str(m.expand(0, 0)), str(m))

        with self.subTest('1,1'):
            self.assertEqual(
                str(m.expand(1, 1)),
                'Bin2dMatrix 6x5\n'
                '100000\n'
                '010000\n'
                '001000\n'
                '000010\n'
                '000000'
            )

        with self.subTest('-1,-1'):
            self.assertEqual(
                str(m.expand(-1, -1)),
                'Bin2dMatrix 6x5\n'
                '000000\n'
                '010000\n'
                '001000\n'
                '000100\n'
                '000001'
            )

        with self.subTest('-2,1'):
            self.assertEqual(
                str(m.expand(-2, 1)),
                'Bin2dMatrix 7x5\n'
                '0010000\n'
                '0001000\n'
                '0000100\n'
                '0000001\n'
                '0000000'
            )

        with self.subTest('3, -1'):
            self.assertEqual(
                str(m.expand(3, -1)),
                'Bin2dMatrix 8x5\n'
                '00000000\n'
                '10000000\n'
                '01000000\n'
                '00100000\n'
                '00001000'
            )

    def test_expand_diagonal_matrix_with_ones(self):
        m = Bin2dMatrix.from_strings([
            '10000',
            '01000',
            '00100',
            '00001',
        ])

        with self.subTest('0,0'):
            self.assertEqual(m.expand(0, 0), m)
            self.assertEqual(str(m.expand(0, 0)), str(m))

        with self.subTest('1,1'):
            self.assertEqual(
                str(m.expand(1, 1, fill=True)),
                'Bin2dMatrix 6x5\n'
                '100001\n'
                '010001\n'
                '001001\n'
                '000011\n'
                '111111'
            )

        with self.subTest('-1,-1'):
            self.assertEqual(
                str(m.expand(-1, -1, fill=True)),
                'Bin2dMatrix 6x5\n'
                '111111\n'
                '110000\n'
                '101000\n'
                '100100\n'
                '100001'
            )

        with self.subTest('-2,1'):
            self.assertEqual(
                str(m.expand(-2, 1, fill=True)),
                'Bin2dMatrix 7x5\n'
                '1110000\n'
                '1101000\n'
                '1100100\n'
                '1100001\n'
                '1111111'
            )

        with self.subTest('3, -1'):
            self.assertEqual(
                str(m.expand(3, -1, fill=True)),
                'Bin2dMatrix 8x5\n'
                '11111111\n'
                '10000111\n'
                '01000111\n'
                '00100111\n'
                '00001111'
            )

    def test_set(self):
        m = Bin2dMatrix.from_strings([
            '10000',
            '01000',
            '00100',
            '00010',
            '00001',
        ])

        with self.subTest('corner one'):
            self.assertEqual(m.set((0, 0)), m)

        with self.subTest('corner one, twice'):
            self.assertEqual(m.set((0, 0), (0, 0)), m)

        with self.subTest('middle one'):
            self.assertEqual(m.set((1, 1)), m)

        with self.subTest('middle one, twice'):
            self.assertEqual(m.set((1, 1), (1, 1)), m)

        with self.subTest('corner zero'):
            self.assertEqual(
                str(m.set((4, 0))),
                'Bin2dMatrix 5x5\n'
                '10001\n'
                '01000\n'
                '00100\n'
                '00010\n'
                '00001'
            )

        with self.subTest('middle zero'):
            self.assertEqual(
                str(m.set((2, 1))),
                'Bin2dMatrix 5x5\n'
                '10000\n'
                '01100\n'
                '00100\n'
                '00010\n'
                '00001'
            )

        with self.subTest('multiple ones and zeros'):
            self.assertEqual(
                str(m.set((4, 0), (3, 1), (2, 2), (1, 3), (0, 4), (0, 0), (0, 1))),
                'Bin2dMatrix 5x5\n'
                '10001\n'
                '11010\n'
                '00100\n'
                '01010\n'
                '10001'
            )

    def test_unset(self):
        m = Bin2dMatrix.from_strings([
            '01111',
            '10111',
            '11011',
            '11101',
            '11110',
        ])

        with self.subTest('corner one'):
            self.assertEqual(m.unset((0, 0)), m)

        with self.subTest('corner one, twice'):
            self.assertEqual(m.unset((0, 0), (0, 0)), m)

        with self.subTest('middle one'):
            self.assertEqual(m.unset((1, 1)), m)

        with self.subTest('middle one, twice'):
            self.assertEqual(m.unset((1, 1), (1, 1)), m)

        with self.subTest('corner zero'):
            self.assertEqual(
                str(m.unset((4, 0))),
                'Bin2dMatrix 5x5\n'
                '01110\n'
                '10111\n'
                '11011\n'
                '11101\n'
                '11110'
            )

        with self.subTest('middle zero'):
            self.assertEqual(
                str(m.unset((2, 1))),
                'Bin2dMatrix 5x5\n'
                '01111\n'
                '10011\n'
                '11011\n'
                '11101\n'
                '11110'
            )

        with self.subTest('multiple ones and zeros'):
            self.assertEqual(
                str(m.unset((4, 0), (3, 1), (2, 2), (1, 3), (0, 4), (0, 0), (0, 1))),
                'Bin2dMatrix 5x5\n'
                '01110\n'
                '00101\n'
                '11011\n'
                '10101\n'
                '01110'
            )

    def test_value_points(self):

        with self.subTest('1x1 True'):
            m = Bin2dMatrix.from_strings(['1'])
            self.assertEqual(list(m.value_points()), [(0, 0)])
            self.assertEqual(list(m.value_points(False)), [])

        with self.subTest('1x1 False'):
            m = Bin2dMatrix.from_strings(['0'])
            self.assertEqual(list(m.value_points(False)), [(0, 0)])
            self.assertEqual(list(m.value_points()), [])

        with self.subTest('diagonal 0'):
            m = Bin2dMatrix.from_strings([
                '01111',
                '10111',
                '11011',
                '11101',
                '11110',
            ])
            self.assertEqual(list(m.value_points()), [
                (1, 0), (2, 0), (3, 0), (4, 0),
                (0, 1), (2, 1), (3, 1), (4, 1),
                (0, 2), (1, 2), (3, 2), (4, 2),
                (0, 3), (1, 3), (2, 3), (4, 3),
                (0, 4), (1, 4), (2, 4), (3, 4),
            ])
            self.assertEqual(list(m.value_points(False)), [
                (0, 0), (1, 1), (2, 2), (3, 3), (4, 4),
            ])

        with self.subTest('multiple ones and zeros'):
            m = Bin2dMatrix.from_strings([
                '01110',
                '00101',
                '11011',
                '10101',
                '01110',
            ])
            self.assertEqual(list(m.value_points()), [
                (1, 0), (2, 0), (3, 0),
                (2, 1), (4, 1),
                (0, 2), (1, 2), (3, 2), (4, 2),
                (0, 3), (2, 3), (4, 3),
                (1, 4), (2, 4), (3, 4),
            ])
            self.assertEqual(list(m.value_points(False)), [
                (0, 0), (4, 0), (0, 1), (1, 1), (3, 1), (2, 2), (1, 3), (3, 3), (0, 4), (4, 4),
            ])
