import math
import random
import statistics
import timeit
from typing import Callable, List

from approx_cy import (
    approx_legrende_cy,
    approx_chebyshev_cy,
    approx_legrende_cy_3ord,
    approx_lut_cy,
)  # type: ignore
from approx_rust import approx_legrende_rust  # type: ignore
from tabulate import tabulate

from approx_py import approx_legrende_jit, approx_legrende_native
from test import approx_chebyshev_native


def blank(x: float) -> float:
    return 0.0


def benchmark(
    funcs: List[Callable[[float], float]], num_samples: int = 100_000, repeats: int = 3
):
    """
    Benchmarks multiple trigonometric approximation functions against math.sin.

    Args:
        funcs: A list of functions to benchmark.
        num_samples: Number of random samples to test.
    """

    # 1. Generate random test data in [-pi/2, pi/2]
    test_data = [random.uniform(-math.pi / 2, math.pi / 2) for _ in range(num_samples)]

    # 2. Measure Overhead (Blank Function)
    # We measure the time it takes just to iterate and call a function
    start_time = timeit.default_timer()
    for x in test_data:
        blank(x)
    overhead_time = timeit.default_timer() - start_time

    results = []

    # Add standard math.sin to the comparison
    all_funcs = [math.sin] + funcs

    print(f"Benchmarking on {num_samples:,} random samples in [-π/2, π/2]...")
    print(f"Overhead (blank function loop): {overhead_time:.4f}s\n")

    for func in all_funcs:
        func_name = func.__name__
        # --- Timing with Repeats ---
        # Run the benchmark multiple times and collect timings

        # Use a wrapper function with a simple loop to avoid list allocation overhead
        def run_benchmark_loop():
            for x in test_data:
                func(x)

        times = timeit.repeat(run_benchmark_loop, number=1, repeat=repeats)

        # Compute values for accuracy calculation
        computed_values = [func(x) for x in test_data]

        # Use minimum time
        total_time = min(times)
        avg_time = statistics.mean(times)
        min_time_ns = (total_time / num_samples) * 1e9
        avg_time_ns = (avg_time / num_samples) * 1e9

        # --- Accuracy ---
        errors = []
        for i, val in enumerate(computed_values):
            true_val = math.sin(test_data[i])
            errors.append(abs(val - true_val))

        avg_error = statistics.mean(errors)
        max_error = max(errors)

        results.append(
            [
                func_name,
                min_time_ns,
                avg_time_ns,
                total_time,
                avg_error,
                max_error,
            ]
        )

    # 3. Format and Print Table
    headers = [
        "Function",
        "Min Time (ns)",
        "Avg Time (ns)",
        "Total (s)",
        "Avg Error",
        "Max Error",
    ]
    # Formatting floats for the table
    print(
        tabulate(
            results,
            headers=headers,
            floatfmt=(".4f", ".2f", ".2f", ".4f", ".2e", ".2e"),
            numalign="center",
            tablefmt="rounded_grid",
        )
    )


if __name__ == "__main__":
    benchmark(
        funcs=[
            approx_legrende_native,
            approx_legrende_jit,
            approx_legrende_cy,
            approx_legrende_rust,
            approx_chebyshev_native,
            approx_chebyshev_cy,
            approx_legrende_cy_3ord,
            approx_lut_cy,
        ]
    )
