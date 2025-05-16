from typing import Iterable, NamedTuple
import numpy as np
import galois
from pprint import pprint
from collections import OrderedDict

# TODO: Customize GF class
# INFO: Core logic for linear algebra is to be implemented.

# As for performance, the algorithm is pretty bad.
# TODO: Optimize grid renew method to add the nth row of matrix A


class Point(NamedTuple):
    x: int
    y: int


def distance(point1: Point, point2: Point) -> int:
    return abs(point1.x - point2.x) + abs(point1.y - point2.y)


GF = galois.GF(2)


class Solver:
    def __init__(self, background: Iterable[Point]):
        self.background = background

    @property
    def A(self):
        return self._A

    @property
    def background(self):
        return self._background

    @background.setter
    def background(self, value: Iterable[Point]):
        self._background: tuple[Point, ...] = tuple(value)
        self._A = GF(
            [
                [1 if distance(point, other) <= 1 else 0 for other in self.background]
                for point in self.background
            ]
        ).transpose()

    def solve(self, current: list[Point], expect: list[Point]) -> list[Point]:
        """Solve equation Ax+b=c in GF(2)"""
        b = GF([1 if point in current else 0 for point in self.background])
        c = GF([1 if point in expect else 0 for point in self.background])
        x = np.linalg.solve(self.A, c - b)
        return [self.background[i] for i in range(len(self.background)) if x[i] == 1]


if __name__ == "__main__":
    solver = Solver(
        [
            Point(0, 0),
            Point(0, 1),
            Point(0, 2),
            Point(1, 0),
            Point(1, 1),
            Point(1, 2),
            Point(2, 0),
            Point(2, 1),
            Point(2, 2),
        ]
    )
    pprint(solver.solve([Point(2, 1), Point(1, 2)], []))
