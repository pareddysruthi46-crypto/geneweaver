# GPU Array Operation Prototype

## Objective

Build a small array-operation prototype to check whether GPU acceleration is available for GeneWeaver.

## Hardware and Compatibility

- Operating System: Windows 11
- GPU: Intel Iris Xe Graphics
- NVIDIA GPU: Not available
- CUDA: Not available
- CuPy: Not installed
- Numba: Installed (0.66.0)
- PyOpenCL: Not installed

The current system does not have a configured GPU array-computing backend.

## Prototype

File: `gpu/prototype.py`

The prototype squares each value in an input array.

Example:

- Input: `[1, 2, 3, 4, 5]`
- Output: `[1, 4, 9, 16, 25]`

It attempts to use CuPy when a compatible CUDA device is available. Otherwise, it automatically uses standard Python CPU execution.

## Current Result

Execution device: CPU

GPU execution could not be verified because a compatible CUDA device and CuPy installation are unavailable.

## CPU Fallback

The CPU fallback uses a standard Python list operation:

`[value * value for value in values]`

This requires no additional GPU libraries and works on the current system.

## Tests

Dedicated tests are available in `tests/test_gpu_prototype.py`.

They cover:
- Array squaring
- Execution device reporting
- Empty input
- Negative values

## Conclusion

The prototype works correctly using CPU fallback. GPU acceleration is not currently feasible on the available hardware and software configuration. CPU execution remains the supported path. GPU support can be evaluated later on a compatible system.
