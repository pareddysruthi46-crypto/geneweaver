# Parallel Sequence-Window Comparison Prototype

## Goal
Compare a guide DNA sequence against every fixed-length window in a target.

## Implementation
- OpenCL through optional PyOpenCL is attempted first.
- If a usable OpenCL device and runtime are available, each window is
  compared by a separate OpenCL work item.
- If PyOpenCL, the OpenCL runtime, or a usable device is unavailable,
  the implementation falls back to CPU execution.
- The result reports the execution device and fallback reason.

## Output
The result includes:
- Best matching window
- Zero-based inclusive start and end positions
- Match and mismatch counts
- Alignment length and percentage score
- Execution device and fallback reason

## Current hardware considerations
The development machine has Intel Iris Xe Graphics.
NVIDIA CUDA is not available. PyOpenCL and an Intel-compatible
OpenCL runtime must be installed and verified before GPU execution
can be claimed.

## Limitations
- This is a prototype, not a production benchmark.
- CPU fallback currently uses a sequential Python implementation.
- OpenCL execution may not be available on every system.
- The first best-scoring window is selected when scores tie.
