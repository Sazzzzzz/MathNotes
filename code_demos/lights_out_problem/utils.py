"""
Module for the Lights Out problem solver.
This module provides Solver, Config, and Point class.
"""

from typing import Iterable, NamedTuple, overload
from pathlib import Path
import numpy as np
import galois
import json
from pprint import pprint
from collections import OrderedDict

# TODO: Customize GF class
# INFO: Core logic for linear algebra is to be implemented.


# As for performance, the algorithm is pretty bad.
# TODO: Optimize grid renew method to add the nth row of matrix A
class Point(NamedTuple):
    x: int
    y: int


class Config(NamedTuple):
    row: int
    col: int
    is_idle: bool
    highlight_active: bool
    is_edit_mode: bool
    canvas: OrderedDict[Point, bool]

    @classmethod
    def load(cls, path: Path) -> "Config":
        with open(path, "r") as f:
            data = json.load(f)
        config = cls(
            data["row"],
            data["col"],
            data["is_idle"],
            data["highlight_active"],
            data["is_edit_mode"],
            OrderedDict(
                {Point(entry[0], entry[1]): entry[2] for entry in data["canvas"]}
            ),
        )
        return config

    @overload
    def save(self, path: Path): ...
    @overload
    def save(self, path: str): ...

    def save(self, path):
        if isinstance(path, str):
            path = Path(path)
        with open(path, "w") as f:
            data = {
                "row": self.row,
                "col": self.col,
                "is_idle": self.is_idle,
                "highlight_active": self.highlight_active,
                "is_edit_mode": self.is_edit_mode,
                "canvas": tuple(
                    [point.x, point.y, value] for point, value in self.canvas.items()
                ),
            }
            json.dump(data, f, indent=4)


def distance(point1: Point, point2: Point) -> int:
    return abs(point1.x - point2.x) + abs(point1.y - point2.y)


GF = galois.GF(2)


class Solver:
    def __init__(self, /, background: Iterable[Point]):
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
        self.rank = np.linalg.matrix_rank(self.A)

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
