from typing import NamedTuple
import numpy as np
import galois
from pprint import pprint

# TODO: Map lights and grids to arrays of modification vectors
# TODO: Customize GF class
# INFO: Core logic for linear algebra is to be implemented.


class Point(NamedTuple):
    x: int
    y: int


def distance(point1: Point, point2: Point) -> int:
    return abs(point1.x - point2.x) + abs(point1.y - point2.y)


GF = galois.GF(2)


class Solver:
    def __init__(self, grid: np.ndarray):
        self._grid = grid
        self._canvas = tuple(
            Point(x, y)
            for x in range(grid.shape[0])
            for y in range(grid.shape[1])
            if grid[x][y] == 1
        )
        self._A = GF(
            [
                [1 if distance(point, other) <= 1 else 0 for other in self.canvas]
                for point in self.canvas
            ]
        ).transpose()

    @property
    def A(self):
        return self._A

    @property
    def canvas(self):
        return self._canvas

    @property
    def grid(self):
        return self._grid

    @grid.setter
    def grid(self, grid: np.ndarray):
        self._grid = grid
        self._canvas = tuple(
            Point(x, y)
            for x in range(grid.shape[0])
            for y in range(grid.shape[1])
            if grid[x][y] == 1
        )
        self._A = GF(
            [
                [1 if distance(point, other) <= 1 else 0 for other in self.canvas]
                for point in self.canvas
            ]
        ).transpose()

    def solve(self, current: list[Point], expect: list[Point]) -> list[Point]:
        """Solve equation Ax+b=c in GF(2)"""
        b = GF([1 if point in current else 0 for point in self.canvas])
        c = GF([1 if point in expect else 0 for point in self.canvas])
        x = np.linalg.solve(self.A, c - b)
        return [self.canvas[i] for i in range(len(self.canvas)) if x[i] == 1]


grid = np.array([[1, 1, 1], [1, 1, 1], [1, 1, 1]], dtype=bool)
solver = Solver(grid)
pprint(solver.solve([Point(0, 0)], []))
