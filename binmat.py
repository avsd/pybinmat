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
        return bool(self.dump & (1 << (item[1] + item[0] * self.cols)))

    def __str__(self):
        return 'Bin2dMatrix {}x{}\n{}'.format(
            self.cols,
            self.rows,
            '\n'.join([
                self.row_template.format(((1 << self.cols) - 1) & (self.dump >> (y * self.cols)))[::-1]
                for y in range(self.rows)
            ])
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

