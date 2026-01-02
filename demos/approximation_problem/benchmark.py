import random
import statistics
import timeit
from math import pi, sin
from typing import Callable, List

from rich.console import Console
from rich.table import Table
from rich import box

from approx_cy import (
    approx_chebyshev_cy,
    approx_legendre_cy,
    approx_legendre_cy_3ord,
    approx_lut_cy,
)
from approx_py import (
    approx_Bhāskara_native,
    approx_chebyshev_native,
    approx_legendre_jit,
    approx_legendre_native,
)
from approx_rust import approx_chebyshev_rust, approx_legendre_rust


def blank(x: float):
    return 0.0


def benchmark(
    funcs: List[Callable[[float], float]], num_samples: int = 100_000, repeats: int = 5
):
    """
    Benchmarks multiple trigonometric approximation functions against math.sin.

    Args:
        funcs: A list of functions to benchmark.
        num_samples: Number of random samples to test.
    """

    # 1. Generate random test data in [-pi/2, pi/2]
    test_data = [random.uniform(-pi / 2, pi / 2) for _ in range(num_samples)]

    # 2. Measure Overhead (Blank Function)
    # We measure the time it takes just to iterate and call a function
    start_time = timeit.default_timer()
    for x in test_data:
        blank(x)
    overhead_time_s = timeit.default_timer() - start_time

    results = []

    # Add standard math.sin to the comparison
    all_funcs = [sin] + funcs

    print(f"\nBenchmarking on {num_samples:,} random samples in [-π/2, π/2]...")
    print(
        f"Overhead (blank function per loop): {overhead_time_s / num_samples * 1e9:.2f} ns"
    )

    for func in all_funcs:
        func_name = func.__name__
        # --- Timing with Repeats ---
        # Run the benchmark multiple times and collect timings

        # Use a wrapper function with a simple loop to avoid list allocation overhead
        # The cost of calling func(x) is dispersed over many calls
        def run_benchmark_loop():
            for x in test_data:
                func(x)

        times = timeit.repeat(run_benchmark_loop, number=1, repeat=repeats)

        # Compute values for accuracy calculation
        computed_values = [func(x) for x in test_data]

        # Use minimum time
        total_time_ms = min(times) * 1000
        min_time_ns = (total_time_ms / num_samples) * 1e6
        execution_time = min_time_ns - (overhead_time_s / num_samples * 1e9)

        # --- Accuracy ---
        errors = []
        for i, val in enumerate(computed_values):
            true_val = sin(test_data[i])
            errors.append(abs(val - true_val))

        avg_error = statistics.mean(errors)
        max_error = max(errors)

        results.append(
            [
                func_name,
                min_time_ns,
                execution_time,
                total_time_ms,
                avg_error,
                max_error,
            ]
        )

    # 3. Format and Print Table
    console = Console()
    table = Table(show_lines=True, box=box.SQUARE_DOUBLE_HEAD)

    table.add_column("Function", style="cyan", no_wrap=True)
    table.add_column("Min Time (ns)", justify="right", style="magenta")
    table.add_column("Exec Time (ns)", justify="right", style="magenta")
    table.add_column("Total (ms)", justify="right", style="green")
    table.add_column("Avg Error", justify="right", style="yellow")
    table.add_column("Max Error", justify="right", style="red")

    for row in results:
        table.add_row(
            str(row[0]),
            f"{row[1]:.2f}",
            f"{row[2]:.2f}",
            f"{row[3]:.4f}",
            f"{row[4]:.2e}",
            f"{row[5]:.2e}",
        )

    console.print(table)


if __name__ == "__main__":
    benchmark(
        funcs=[
            approx_Bhāskara_native,
            approx_legendre_native,
            approx_legendre_jit,
            approx_legendre_cy,
            approx_legendre_rust,
            approx_chebyshev_native,
            approx_chebyshev_cy,
            approx_chebyshev_rust,
            approx_legendre_cy_3ord,
            approx_lut_cy,
        ]
    )
