"""
Module for the Lights Out problem solver.
This module provides Solver, Config, and Point class.
"""

# This module involves linear algebra over finite fields.
# Finding packages suitable for this task is not easy, however, Mathematica handles this well.
# I guess the most silly thing about me is to find symbolic computation in Python,
# and numerical computation in Mathematica :(

import json
from abc import ABC, abstractmethod
from collections import OrderedDict
from functools import cached_property
from pathlib import Path
from pprint import pprint
from typing import Callable, Iterable, List, Literal, NamedTuple, TypeAlias, overload

import galois
import numpy as np
from wolframclient.evaluation import WolframLanguageSession
from wolframclient.language import Global, wlexpr

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


Matrix: TypeAlias = List[List[int]]
Vector: TypeAlias = List[int]


class SolverStrategy(ABC):
    """Abstract base class for solver strategies.
    Only handles logic of linear algebra over GF(2)."""

    rank: int
    is_full_rank: bool

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


# INFO: Here contexts are involved. But using with block is not suitable.
# INFO: Thus we collect garbage by custom `close` method.


# INFO: The conversion of objects between Wolfram Language and Python is not easy.
# INFO: We avoid customizing encoder and decoder for Wolfram Language objects,
# INFO: instead we pass in Matrix and Vector objects directly, and adapt functional programming inside mathematica
# INFO: to avoid any side effects of assigning variables in Wolfram Language.
class MathematicaSolverStrategy(SolverStrategy):

    command = """F = FiniteField[2, 1];
encode[A_] := Map[F, A, {-1}];
decode[x_] := Map[#["Index"] &, x, {-1}];
rank = MatrixRank@*encode;
linearSolve[A_, b_, c_] := decode[LinearSolve[encode[A], encode[c] - encode[b]]];"""

    def __init__(self):
        self.session: WolframLanguageSession = WolframLanguageSession()
        self.session.evaluate(wlexpr(self.command))

    @cached_property
    def get_rank(self) -> Callable[[Matrix], int]:
        return self.session.function(Global.rank)

    @cached_property
    def linear_solve(self) -> Callable[[Matrix, Vector, Vector], Vector]:
        return self.session.function(Global.linearSolve)

    @property
    def A(self):
        return self._A

    @A.setter
    def A(self, value: Matrix):
        self._A = value
        self.rank = self.get_rank(self.A)
        self.is_full_rank: bool = True if self.rank == len(self.A) else False

    def solve(self, current: Vector, expect: Vector) -> Vector:
        if self.is_full_rank:
            return self.linear_solve(self.A, current, expect)
        else:
            return []

    def close(self) -> None:
        self.session.terminate()


class PythonSolverStrategy(SolverStrategy):
    GF = galois.GF(2)

    def __init__(self):
        super().__init__()

    @property
    def A(self):
        return self._A

    @A.setter
    def A(self, value: Matrix):
        self._A = self.GF(value)
        self.rank = np.linalg.matrix_rank(self.A)
        self.is_full_rank = True if self.rank == len(self.A) else False

    def solve(self, current: Vector, expect: Vector) -> Vector:
        b = self.GF(current)
        c = self.GF(expect)
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
        # INFO: Actually the code here only gives a transpose of the matrix A
        # INFO: But it doesn't matter since A is symmetric
        self.strategy.A = [
            [1 if self.distance(point, other) <= 1 else 0 for other in self.background]
            for point in self.background
        ]

        self.rank = self.strategy.rank
        self.is_full_rank = self.strategy.is_full_rank
        self.is_empty: bool = True if self.rank == 0 else False

        if not self.is_full_rank:
            pass

    @staticmethod
    def distance(point1: Point, point2: Point) -> int:
        return abs(point1.x - point2.x) + abs(point1.y - point2.y)

    def solve(self, current: list[Point], expect: list[Point]) -> list[Point]:
        """Solve equation Ax+b=c in GF(2)"""
        b: Vector = [1 if point in current else 0 for point in self.background]
        c: Vector = [1 if point in expect else 0 for point in self.background]
        result: Vector = self.strategy.solve(b, c)
        return [self.background[i] for i, r in enumerate(result) if r == 1]

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
        method="Mathematica",
    )
    pprint(solver.solve([Point(2, 2)], []))
    solver.close()
