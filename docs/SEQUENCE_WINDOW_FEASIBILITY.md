# CPU vs GPU Feasibility for Sequence-Window Comparison

## 1. Objective

Evaluate CPU and GPU implementation options for comparing fixed-length
DNA sequence windows in GeneWeaver.

The comparison assumes:
- A guide sequence or query window of length W.
- A target DNA sequence containing multiple possible windows.
- A sliding-window comparison across the target sequence.
- DNA alphabet: A, T, G, C.

A comparison may calculate exact matches or the number of mismatched
positions (Hamming distance).

## 2. CPU Implementation

### Standard Python CPU

- Iterate through each valid target window.
- Extract a window of length W.
- Compare it with the query sequence position by position.
- Count matching or mismatching bases.

Advantages:
- Simple to implement and debug.
- No GPU hardware or additional acceleration library required.
- Works on the current Windows development environment.
- Suitable as the reference implementation for correctness tests.

Limitations:
- Python-level loops may become slow for very large sequences.
- Repeated window comparisons can require significant CPU time.

### Numba CPU JIT

- Numba may compile numerical comparison loops for faster CPU execution.
- Independent window comparisons may be parallelized where appropriate.
- Benchmark against standard Python before adopting it.

Limitations:
- Numba compatibility with Python 3.14 must be verified.
- Compilation introduces startup overhead.
- Performance depends on sequence size and CPU hardware.

## 3. GPU Implementation Options

### NVIDIA CUDA with Numba or CuPy

- Assign independent target-window comparisons to GPU threads.
- Each thread or work item can calculate a window's match count.
- Suitable for large batches of independent comparisons.

Feasibility:
- Not currently feasible on the detected system because no NVIDIA GPU
  or CUDA environment is available.

### Intel GPU with OpenCL and PyOpenCL

- OpenCL can potentially execute independent window comparisons
  on compatible Intel GPU hardware.
- PyOpenCL could provide a Python interface to OpenCL kernels.

Feasibility:
- Intel Iris Xe Graphics is detected.
- PyOpenCL is not installed.
- A compatible Intel OpenCL runtime and driver configuration must
  be verified before implementation.
- GPU execution and performance have not been tested.

### PyTorch

- Tensor operations could represent batches of sequence windows.
- GPU execution depends on a compatible supported backend.

Feasibility:
- PyTorch is not installed in the current environment.
- A working Intel GPU backend has not been verified.
- It is not recommended as the first implementation choice.

## 4. Complexity and Performance Considerations

Let:
- N = target sequence length.
- W = comparison window length.
- K = N - W + 1 valid sliding windows.

For a straightforward comparison:

- Number of windows: K.
- Work per window: W character comparisons.
- Total work: O(K * W).

CPU execution is straightforward for small and moderate workloads.

GPU execution can process independent windows in parallel, but it also
introduces memory transfer, kernel launch, and setup overhead.

GPU acceleration is not automatically faster. It should be evaluated
using representative sequence lengths and batch sizes.

## 5. CPU vs GPU Comparison

| Criterion | CPU | GPU |
|---|---|---|
| Initial implementation | Simple | More complex |
| Small workloads | Usually practical | Transfer overhead may dominate |
| Large independent batches | May need optimization | Potential parallelism |
| Hardware requirement | Standard CPU | Compatible GPU and runtime |
| Debugging | Easier | More complex |
| Current environment | Available | Not configured |
| Recommended initial use | Yes | Future evaluation |

## 6. Benchmarking Plan

Before selecting an optimized implementation:

1. Implement a standard Python CPU reference.
2. Test exact-match and mismatch-count results.
3. Use identical input sequences for every implementation.
4. Benchmark multiple target lengths and window sizes.
5. Measure execution time separately from GPU initialization
   and data-transfer time.
6. Compare optimized results against the CPU reference.
7. Record hardware, software versions, and benchmark conditions.

No performance improvement should be claimed until measured.

## 7. Feasibility for the Current Environment

Detected hardware and software:

- OS: Windows 11
- Python: 3.14.4
- GPU: Intel Iris Xe Graphics
- Numba: 0.66.0 installed
- PyTorch: Not installed
- CuPy: Not installed
- PyOpenCL: Not installed
- NVIDIA CUDA: Not detected

Assessment:

- Standard Python CPU implementation: Feasible.
- Numba CPU optimization: Candidate; requires compatibility and
  benchmark testing.
- NVIDIA CUDA: Not feasible with the currently detected hardware.
- Intel OpenCL: Potential future option; runtime and compatibility
  are not verified.
- PyTorch GPU: Not currently configured.

## 8. Recommendation

1. Start with a standard Python CPU implementation.
2. Keep it as the correctness reference and fallback.
3. Evaluate Numba CPU optimization using benchmarks.
4. Investigate Intel OpenCL only if CPU performance becomes insufficient
   and a compatible runtime is available.
5. Consider GPU acceleration only when measured workloads justify
   the additional implementation complexity.

## 9. Conclusion

CPU execution is the most feasible approach for the current GeneWeaver
development environment.

GPU acceleration remains a possible future optimization, particularly
through Intel OpenCL, but it is not currently configured or verified.

Correctness, portability, and measured performance should guide the
implementation choice.
