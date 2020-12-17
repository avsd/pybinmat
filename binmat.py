"""
Classes for representing binary (0/1) 2D matrix
as Python integers, and efficient operations on them
"""
import re
from collections import namedtuple


class Bin2dMatrix(namedtuple('Bin2dMatrix', ('cols', 'rows', 'dump'), defaults=(0,))):
    __slots__ = ()
    @property
    def row_template(self):
        return '{{:0{}b}}'.format(self.cols)

    def __getitem__(self, item: tuple):
        if not isinstance(item, tuple):
            return super().__getitem__(item)
        x, y = item
        if 0 <= x < self.cols and 0 <= y < self.rows:
            return bool(self.dump & (1 << (x + y * self.cols)))
        raise ValueError('Coordinates {} exceed boundaries!'.format(str(item)))

    def get(self, x, y, default=False):
        return (
            bool(self.dump & (1 << (x + y * self.cols)))
            if 0 <= x < self.cols and 0 <= y < self.rows
            else default
        )

    def set(self, *coords):
        return self._replace(dump=self.dump | sum([
            1 << (x + self.cols * y)
            for x, y in set(coords)
            if 0 <= x < self.cols and 0 <= y < self.rows
        ]))

    def unset(self, *coords):
        return self._replace(dump=self.dump & self._replace(dump=0).set(*coords).__invert__().dump)

    def value_points(self, value: bool = True):
        bv = bool(value)
        for x in range(self.rows):
            for y in range(self.cols):
                if bool(self.dump & (1 << (x + y * self.cols))) == bv:
                    yield (x, y)

    @property
    def ones_count(self):
        s = 0
        d = self.dump
        while d:
            s += d & 1
            d >>=1
        return s

    def _check_dimensions(self, other):
        if self._replace(dump=0) != other._replace(dump=0):
            raise ValueError('Matrices must have the same dimensions!')

    def __and__(self, other):
        self._check_dimensions(other)
        return self._replace(dump=self.dump & other.dump)

    def __or__(self, other):
        self._check_dimensions(other)
        return self._replace(dump=self.dump | other.dump)

    def __xor__(self, other):
        self._check_dimensions(other)
        return self._replace(dump=self.dump ^ other.dump)

    def __invert__(self):
        return self ^ self.all_ones()

    def all_ones(self):
        return self._replace(dump=(1 << self.cols * self.rows) - 1)

    def __str__(self):
        return 'Bin2dMatrix {}x{}\n{}'.format(
            self.cols,
            self.rows,
            '\n'.join([
                self.row_template.format(((1 << self.cols) - 1) & (self.dump >> (y * self.cols)))[::-1]
                for y in range(self.rows)
            ] )
        )

    @classmethod
    def from_iterables(cls, iterables: list):
        rows = len(iterables)
        cols = max([len(l) for l in iterables])
        dump = sum([
            sum([int(bool(item)) * (1 << x) for x, item in enumerate(row)]) << (y * cols)
            for y, row in enumerate(iterables)
        ])
        return cls(cols, rows, dump)

    @classmethod
    def from_strings(cls, strings: list, ones='[1-9a-zA-Z]'):
        rx = re.compile(ones)
        rows = len(strings)
        cols = max([len(l) for l in strings])
        dump = sum([
            sum([int(bool(rx.match(c))) * (1 << x) for x, c in enumerate(row)]) << (y * cols)
            for y, row in enumerate(strings)
        ])
        return cls(cols, rows, dump)

    def expand(self, cols: int, rows: int, fill: bool = False):
        """
        Expands the matrix left or right (for negative or positive cols)
        and up or down (for negative or positive rows), filling the remaining
        area with the given values. If you want to expand both left and right
        or up and down, run expand twice.
        """
        newCols = self.cols + abs(cols)
        newRows = self.rows + abs(rows)
        return self.__class__(
            newCols, newRows,
            sum([
                sum([int(self[x, y]) * (1 << (x + max(0, -cols))) for x in range(self.cols)])
                << ((y + max(0, -rows)) * newCols)
                for y in range(self.rows)
            ]) | ((self.all_ones().expand(cols, rows).__invert__()).dump if fill else 0)
        )
