"""Repeatable CPU benchmark for GeneWeaver sequence matching."""

import platform
import random
import statistics
import sys
from pathlib import Path
from time import perf_counter

# Add project root so the alignment package can be imported.
PROJECT_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(PROJECT_ROOT))

from alignment.baseline import match_guide_to_target


def make_sequence(length, seed):
    """Generate a deterministic DNA sequence."""
    rng = random.Random(seed)
    return "".join(rng.choices("ATGC", k=length))


def benchmark(repetitions=100):
    guide = make_sequence(20, 42)
    target_sizes = [200, 1000, 5000, 10000]

    print("GeneWeaver CPU Baseline Benchmark")
    print(f"Python: {platform.python_version()}")
    print(f"Platform: {platform.platform()}")
    print(f"Repetitions: {repetitions}")
    print("Times are measured in milliseconds.")
    print()

    print(
        f"{'Target length':>14} | {'Average ms':>12} | "
        f"{'Median ms':>11} | {'Minimum ms':>11} | {'Maximum ms':>11}"
    )
    print("-" * 75)

    for size in target_sizes:
        target = make_sequence(size, 100 + size)

        for _ in range(5):
            match_guide_to_target(guide, target)

        timings = []

        for _ in range(repetitions):
            start = perf_counter()
            match_guide_to_target(guide, target)
            timings.append((perf_counter() - start) * 1000)

        print(
            f"{size:14d} | "
            f"{statistics.mean(timings):12.6f} | "
            f"{statistics.median(timings):11.6f} | "
            f"{min(timings):11.6f} | "
            f"{max(timings):11.6f}"
        )


if __name__ == "__main__":
    benchmark()
