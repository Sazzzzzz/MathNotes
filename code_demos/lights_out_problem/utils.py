"""
Module for the Lights Out problem solver.
This module provides Solver, Config, and Point class.
"""

# This module involves linear algebra over finite fields.
# Finding packages suitable for this task is not easy, however, Mathematica handles this well.
# I guess the most silly thing about me is to find symbolic computation in Python,
# and numerical computation in Mathematica :(

from typing import Iterable, List, Literal, NamedTuple, TypeAlias, overload
from pathlib import Path
import numpy as np
import galois
import json
from pprint import pprint
from collections import OrderedDict
from sympy import Array
from wolframclient.evaluation import WolframLanguageSession
from abc import ABC, abstractmethod
from wolframclient.language import wl, wlexpr

# TODO: Customize GF class


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
    method: Literal["Python", "Mathematica"]
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
            data["method"],
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
                "method": self.method,
                "canvas": tuple(
                    [point.x, point.y, value] for point, value in self.canvas.items()
                ),
            }
            json.dump(data, f, indent=4)


GF = galois.GF(2)
Matrix: TypeAlias = List[List[bool]]
Vector: TypeAlias = List[bool]


class SolverStrategy(ABC):
    rank: int

    @abstractmethod
    def __init__(self):
        pass

    @abstractmethod
    def solve(self, current: Vector, expect: Vector) -> Vector:
        """Solve equation Ax+b=c in GF(2)"""
        pass

    @abstractmethod
    def close(self) -> None:
        pass


# INFO: Here contexts are involved. But using with block is not suitable at all.
# INFO: Here we collect garbage by custom `close` method.
class MathematicaSolverStrategy(SolverStrategy):
    def __init__(self):
        self.session: WolframLanguageSession = WolframLanguageSession()

    @property
    def A(self):
        return self._A

    @A.setter
    def A(self, value: Matrix):
        self._A = value
        self.rank = self.session.evaluate(wl.MatrixRank(self.A))

    def solve(self, current: Vector, expect: Vector) -> Vector:
        # Implement Mathematica-specific logic here
        return []

    def close(self) -> None:
        self.session.terminate()


class PythonSolverStrategy(SolverStrategy):
    def __init__(self):
        super().__init__()

    @property
    def A(self):
        return self._A

    @A.setter
    def A(self, value: Matrix):
        self._A = GF(value)
        self.rank = np.linalg.matrix_rank(self.A)

    def solve(self, current: Vector, expect: Vector) -> Vector:
        b = GF(current)
        c = GF(expect)
        x = np.linalg.solve(self.A, c - b)
        return list(x)

    def close(self) -> None:
        return None


class Solver:
    def __init__(
        self,
        background: Iterable[Point],
        method: Literal["Python", "Mathematica"] = "Python",
    ):
        if method == "Mathematica":
            self.strategy = MathematicaSolverStrategy()
        elif method == "Python":
            self.strategy = PythonSolverStrategy()
        else:
            raise ValueError("Invalid method. Choose 'Python' or 'Mathematica'.")
        self.background = background

    @property
    def background(self):
        return self._background

    @background.setter
    def background(self, value: Iterable[Point]):
        self._background: tuple[Point, ...] = tuple(value)
        # * Actually the code here only gives a transpose of the matrix A
        # * But it doesn't matter since A is symmetric
        self.A = [
            [
                True if self.distance(point, other) <= 1 else False
                for other in self.background
            ]
            for point in self.background
        ]
        self.strategy.A = self.A

        self.rank = self.strategy.rank
        self.is_full_rank: bool = True if self.rank == len(self.background) else False
        self.is_empty: bool = True if self.rank == 0 else False

        if not self.is_full_rank:
            pass

    @staticmethod
    def distance(point1: Point, point2: Point) -> int:
        return abs(point1.x - point2.x) + abs(point1.y - point2.y)

    def solve(self, current: list[Point], expect: list[Point]) -> list[Point]:
        """Solve equation Ax+b=c in GF(2)"""
        b: Vector = [True if point in current else False for point in self.background]
        c: Vector = [True if point in expect else False for point in self.background]
        result: Vector = self.strategy.solve(b, c)
        return [self.background[i] for i, r in enumerate(result) if r]

    def close(self) -> None:
        self.strategy.close()


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
        ],
        method="Python",
    )
    pprint(solver.solve([Point(2, 2)], []))
