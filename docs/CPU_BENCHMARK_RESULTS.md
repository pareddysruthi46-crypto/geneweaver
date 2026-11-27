# CPU Baseline Benchmark Results

## Environment
- Operating System: Windows 11
- Python Version: 3.14.4
- Guide Length: 20 bases
- Warm-up Runs: 5
- Timed Repetitions: 100
- Timing Method: time.perf_counter()

## Benchmark Results

| Target Length | Average (ms) | Median (ms) | Minimum (ms) | Maximum (ms) |
|---:|---:|---:|---:|---:|
| 200 | 0.450118 | 0.381600 | 0.343400 | 1.017700 |
| 1000 | 2.080003 | 1.937650 | 1.859700 | 3.379900 |
| 5000 | 13.265445 | 11.693750 | 9.754000 | 25.857900 |
| 10000 | 24.623574 | 22.103500 | 19.628000 | 41.264800 |

## Observations
- Runtime generally increases with target length.
- The 10000-base target took an average of 24.62 ms.
- Timings may vary with system load.
- These are CPU measurements, not GPU measurements.

## Reproducibility
Run from the project root:
python benchmarks\benchmark_cpu.py

## Limitations
- Results represent one machine and software environment.
- Runtime can vary with background processes.
- Results are not universal performance guarantees.
