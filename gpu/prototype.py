"""Small GPU array-operation prototype with a CPU fallback."""

from __future__ import annotations


def run_array_prototype(values: list[float]) -> dict:
    """Square array values using GPU when available, otherwise CPU."""

    try:
        import cupy as cp

        if cp.cuda.runtime.getDeviceCount() > 0:
            gpu_array = cp.asarray(values, dtype=cp.float64)
            result = (gpu_array * gpu_array).get().tolist()

            return {
                "device": "GPU",
                "operation": "square",
                "input": values,
                "result": result,
            }

    except (ImportError, Exception):
        pass

    # Standard Python CPU fallback
    result = [value * value for value in values]

    return {
        "device": "CPU",
        "operation": "square",
        "input": values,
        "result": result,
    }


if __name__ == "__main__":
    sample_values = [1, 2, 3, 4, 5]
    output = run_array_prototype(sample_values)

    print("=== GeneWeaver Array Prototype ===")
    print(f"Execution device: {output['device']}")
    print(f"Operation: {output['operation']}")
    print(f"Input: {output['input']}")
    print(f"Result: {output['result']}")
