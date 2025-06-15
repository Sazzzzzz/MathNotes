from typing import TypeAlias
import numpy as np
from sympy import Rational  # type: ignore
from colorist import Color

#! This is only for testing purposes, not a working implementation of the simplex method

BaseDict: TypeAlias = dict[int, int]


def elementary_row_operation(A: np.ndarray, row: int, col: int) -> None:
    """
    Simplify row in Matrix A using the element at (row, col) by elementary row operations.
    """

    # if not A[row, col]:
    #     raise ValueError("Cannot perform operation on zero element.")

    # Preserve rational type during division
    A[row, :] = A[row, :] / A[row, col]
    for i in range(A.shape[0]):
        if i != row:
            # Preserve rational type during subtraction
            A[i, :] = A[i, :] - A[i, col] * A[row, :]


def simplex_method_iter(
    A_stack: np.ndarray, base: BaseDict, /, procedure: bool = False
) -> None:
    col_index = np.argmin(A_stack[0, 0:-1])
    if A_stack[0, col_index] >= 0:
        raise ValueError("Problem already solved, no negative coefficients.")
    elif all(A_stack[1:, col_index] <= 0):
        raise ValueError("Unbounded solution, all coefficients are non-positive.")
    # Remember to add one to the row index because the first row is the goal function
    # The code below will find the position of the smallest positive one
    mask = A_stack[1:, -1] / A_stack[1:, col_index]
    mask[mask <= 0] = np.inf
    row_index = np.argmin(mask) + 1
    # TODO: Kill the ints
    base[int(row_index)] = int(col_index) + 1
    elementary_row_operation(A_stack, int(row_index), int(col_index))
    if procedure:
        print(
            f"{Color.RED}Row {row_index+1} pivoted on column {col_index+1}{Color.OFF}."
        )
        print(A_stack)
    return None


# TODO: How to type annotation for ndarray
def simplex_method(
    A: np.ndarray,
    b: np.ndarray,
    goal: np.ndarray,
    base: BaseDict,
    /,
    max_iter: int = 100,
    procedure: bool = False,
) -> tuple[np.ndarray, float]:
    # if np.linalg.matrix_rank(A) != A.shape[0]:
    #     raise ValueError("Matrix A is not full rank.")
    if goal.shape[0] != A.shape[1]:
        raise ValueError("Goal vector size mismatch.")
    if b.shape[0] != A.shape[0]:
        raise ValueError("b vector size mismatch.")
    # `0` is just a placeholder for the last column, true value must be calculated for result may contain multiples of the unknown value
    # Add explicit dtype=Rational to preserve rational numbers
    goal = np.append(goal, goal[0])
    A_primer = np.hstack((A, b.reshape(-1, 1)))
    A_stack = np.vstack((goal, A_primer))
    if procedure:
        print(f"{Color.GREEN}Initial table:{Color.OFF}")
        print(A_stack)
    for row, col in base.items():
        elementary_row_operation(A_stack, row, col - 1)  #! This causes problems
    if procedure:
        print(f"{Color.GREEN}Initial table Reduced:{Color.OFF}")
        print(A_stack)
    for _ in range(max_iter):
        simplex_method_iter(A_stack, base, procedure)
        if all(A_stack[0, :-1] >= 0):
            break
    else:
        raise ValueError("Maximum iterations reached, problem may be unbounded.")
    result = np.zeros(goal.shape[0])
    for row, col in base.items():
        result[col - 1] = A_stack[row, -1]
    return result, np.dot(goal, result)


def two_phase_simplex_method(
    A: np.ndarray,
    b: np.ndarray,
    goal: np.ndarray,
    /,
    max_iter: int = 100,
    procedure: bool = False,
) -> tuple[np.ndarray, float]:
    """
    Solve the linear programming problem using the two-phase simplex method.
    """
    # Phase 1: Find a feasible solution
    row, col = A.shape
    # Make sure to explicitly preserve Rational dtype in all array creations
    A_phase1 = np.hstack((A, np.eye(row)))
    goal_phase1 = np.append(np.zeros(col), np.ones(row))
    base_init = {i + 1: col + i + 1 for i in range(row)}
    if procedure:
        print(f"{Color.YELLOW}Phase 1: Finding a feasible solution{Color.OFF}")
        print(f"{Color.GREEN}Initial Goal:{Color.OFF}", goal_phase1)
    simplex_method(
        A_phase1, b, goal_phase1, base_init, max_iter=max_iter, procedure=procedure
    )
    print(base_init)
    if any(base >= A.shape[1] for base in base_init.values()):
        raise ValueError("No feasible solution found in phase 1.")
    if procedure:
        print(f"{Color.YELLOW}Phase 1: Feasible solution found{Color.OFF}")
        print(f"{Color.YELLOW}Phase 1: Starting from base: {base_init}{Color.OFF}")
        print(f"{Color.YELLOW}Phase 2: Finding optimal solution{Color.OFF}")
    # Phase 2: Optimize the solution
    return simplex_method(A, b, goal, base_init, max_iter=max_iter, procedure=procedure)


def main():
    A = np.array([[1, -1, 6, -1, 0], [1, 1, 2, 0, -1]])
    b = np.array([2, 1])
    goal = np.array([5, 0, 21, 0, 0])
    # Convert to fractions
    result = two_phase_simplex_method(A, b, goal, max_iter=100, procedure=True)
    print(result)


if __name__ == "__main__":
    main()
