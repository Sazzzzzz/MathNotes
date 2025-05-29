"""
Module for the Lights Out problem solver.
This module provides Solver, Config, and Point class.
"""

# This module involves linear algebra over finite fields.
# Finding packages suitable for this task is not easy, however, Mathematica handles this well.
# I guess the most silly thing about me is to find symbolic computation in Python,
# and numerical computation in Mathematica :(

import enum
import json
from abc import ABC, abstractmethod
from collections import OrderedDict
from functools import cached_property
from pathlib import Path
from pprint import pprint
from typing import (
    Callable,
    Iterable,
    List,
    Literal,
    NamedTuple,
    TypeAlias,
    TypedDict,
)

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


class Config(TypedDict):
    row: int
    col: int
    is_idle: bool
    highlight_active: bool
    is_edit_mode: bool
    method: Literal["Python", "Mathematica"]
    canvas: OrderedDict[Point, bool]


def load_config(path: Path) -> Config:
    with open(path, "r") as f:
        data = json.load(f)
    config = Config(
        row=data["row"],
        col=data["col"],
        is_idle=data["is_idle"],
        highlight_active=data["highlight_active"],
        is_edit_mode=data["is_edit_mode"],
        method=data["method"],
        canvas=OrderedDict(
            {Point(entry[0], entry[1]): entry[2] for entry in data["canvas"]}
        ),
    )
    return config


def save_config(config: Config, path: Path) -> None:
    with open(path, "w") as f:
        data = {
            "row": config["row"],
            "col": config["col"],
            "is_idle": config["is_idle"],
            "highlight_active": config["highlight_active"],
            "is_edit_mode": config["is_edit_mode"],
            "method": config["method"],
            "canvas": tuple(
                [point.x, point.y, value] for point, value in config["canvas"].items()
            ),
        }
        json.dump(data, f, indent=4)


Matrix: TypeAlias = List[List[int]]
Vector: TypeAlias = List[int]


class NoSolutionError(Exception):
    """Exception raised when no solution is found."""

    def __init__(self, message: str = "No solution found."):
        super().__init__(message)
        self.message = message


class SolverStrategy(ABC):
    """Abstract base class for solver strategies.
    Only handles logic of linear algebra over GF(2)."""

    rank: int
    is_full_rank: bool
    A: property

    @abstractmethod
    def __init__(self):
        pass

    @abstractmethod
    def full_rank_solve(self, current: Vector, expect: Vector) -> Vector:
        pass

    @abstractmethod
    def non_full_rank_solve(self, current: Vector, expect: Vector) -> tuple[Vector]:
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
    # NOTE: You can't really create `LinearSolve[A]` even for a full rank matrix A
    command = """F = FiniteField[2, 1];
encode[A_] := Map[F, A, {-1}];
decode[x_] := Map[#["Index"] &, x, {-1}];
rank[A_] := MatrixRank[encode[A]];
linearSolve[A_, b_, c_] := decode[LinearSolve[encode[A], encode[c] - encode[b]]];
minimalSolve[Araw_, braw_, craw_] := Module[
   {A = encode[Araw], b = encode[braw], c = encode[craw]},
   MinimalBy[
    Map[decode[Plus[LinearSolve[A, c - b], #]] &,
     Plus @@@ Subsets[NullSpace[A]]],
    Total]];"""

    def __init__(self):
        self.session: WolframLanguageSession = WolframLanguageSession()
        self.session.evaluate(wlexpr(self.command))

    @cached_property
    def get_rank(self) -> Callable[[Matrix], int]:
        return self.session.function(Global.rank)

    @cached_property
    def linear_solve(self) -> Callable[[Matrix, Vector, Vector], Vector]:
        return self.session.function(Global.linearSolve)

    @cached_property
    def minimal_solve(self) -> Callable[[Matrix, Vector, Vector], tuple[Vector]]:
        return self.session.function(Global.minimalSolve)

    def full_rank_solve(self, current: Vector, expect: Vector) -> Vector:
        return self.linear_solve(self.A, current, expect)

    def non_full_rank_solve(self, current: Vector, expect: Vector) -> tuple[Vector]:
        return self.minimal_solve(self.A, current, expect)

    @property
    def A(self):
        return self._A

    @A.setter
    def A(self, value: Matrix):
        self._A = value
        self.rank = self.get_rank(self.A)
        self.is_full_rank: bool = True if self.rank == len(self.A) else False

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

    def full_rank_solve(self, current: Vector, expect: Vector) -> Vector:
        b = self.GF(current)
        c = self.GF(expect)
        x = np.linalg.solve(self.A, c - b)
        return list(x)

    def non_full_rank_solve(self, current: Vector, expect: Vector) -> tuple[Vector]:
        return tuple()

    def close(self) -> None:
        return None


class Solver:
    class Result(enum.Enum):
        EMPTY_CANVAS = 0x0
        EMPTY_SOLUTION = 0x1
        FULL_RANK_SOLVED = 0x2
        INCOMPLETE_RANK_SOLVED = 0x3
        INCOMPLETE_RANK_UNSOLVED = 0x4

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
        self.prev_vec: Vector = []
        self.strategy.A = [
            [1 if self.distance(point, other) <= 1 else 0 for other in self.background]
            for point in self.background
        ]

        self.rank = self.strategy.rank
        self.is_full_rank = self.strategy.is_full_rank
        self.is_empty: bool = True if self._background == () else False

    @staticmethod
    def distance(point1: Point, point2: Point) -> int:
        return abs(point1.x - point2.x) + abs(point1.y - point2.y)

    @staticmethod
    def difference(solution1: Vector, solution2: Vector) -> int:
        return sum(1 for a, b in zip(solution1, solution2) if a != b)

    def solve(
        self, current: list[Point], expect: list[Point]
    ) -> tuple[Result, list[Point]]:
        """Solve equation Ax+b=c in GF(2)"""
        if self.is_empty:
            return (self.Result.EMPTY_CANVAS, [])
        b: Vector = [1 if point in current else 0 for point in self.background]
        c: Vector = [1 if point in expect else 0 for point in self.background]
        if self.is_full_rank:
            code = self.Result.FULL_RANK_SOLVED
            result = self.strategy.full_rank_solve(b, c)
        else:
            try:
                results = self.strategy.non_full_rank_solve(b, c)
                code = self.Result.INCOMPLETE_RANK_SOLVED
            except NoSolutionError:
                results = tuple()
                code = self.Result.INCOMPLETE_RANK_UNSOLVED
            result = min(
                results,
                key=lambda x: self.difference(x, self.prev_vec),
            )
        self.prev_vec = result
        points = [self.background[i] for i, r in enumerate(result) if r == 1]
        if not points:
            code = self.Result.EMPTY_SOLUTION
        return (code, points)

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
