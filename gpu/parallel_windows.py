"""Parallel sequence-window comparison with optional OpenCL acceleration."""

from alignment.validation import validate_dna_sequence


_OPENCL_KERNEL = """
__kernel void compare_windows(
    __global const char *guide,
    __global const char *target,
    __global int *scores,
    const int guide_length
)
{
    int position = get_global_id(0);
    int matches = 0;

    for (int i = 0; i < guide_length; i++) {
        if (guide[i] == target[position + i]) {
            matches++;
        }
    }

    scores[position] = matches;
}
"""


def cpu_reference_scores(guide_sequence, target_sequence):
    """Return CPU reference scores for every fixed-length target window."""
    guide = validate_dna_sequence(guide_sequence)
    target = validate_dna_sequence(target_sequence)

    if len(guide) > len(target):
        raise ValueError(
            "Guide sequence cannot be longer than target sequence."
        )

    guide_length = len(guide)
    scores = []

    for position in range(len(target) - guide_length + 1):
        window = target[position:position + guide_length]
        scores.append(
            sum(a == b for a, b in zip(guide, window))
        )

    return scores


def _cpu_scores(guide, target):
    """Backward-compatible internal wrapper for CPU reference scoring."""
    return cpu_reference_scores(guide, target)


def _opencl_scores(guide, target):
    """Calculate window scores using an available OpenCL device."""
    import numpy as np
    import pyopencl as cl

    platforms = cl.get_platforms()
    devices = [
        device
        for platform in platforms
        for device in platform.get_devices()
    ]

    if not devices:
        raise RuntimeError("No OpenCL devices found.")

    device = devices[0]
    context = cl.Context([device])
    queue = cl.CommandQueue(context)

    program = cl.Program(context, _OPENCL_KERNEL).build()

    guide_bytes = np.array(
        [ord(base) for base in guide], dtype=np.int8
    )
    target_bytes = np.array(
        [ord(base) for base in target], dtype=np.int8
    )

    window_count = len(target) - len(guide) + 1
    scores = np.empty(window_count, dtype=np.int32)

    mf = cl.mem_flags
    guide_buffer = cl.Buffer(
        context, mf.READ_ONLY | mf.COPY_HOST_PTR, hostbuf=guide_bytes
    )
    target_buffer = cl.Buffer(
        context, mf.READ_ONLY | mf.COPY_HOST_PTR, hostbuf=target_bytes
    )
    score_buffer = cl.Buffer(context, mf.WRITE_ONLY, scores.nbytes)

    program.compare_windows(
        queue,
        (window_count,),
        None,
        guide_buffer,
        target_buffer,
        score_buffer,
        np.int32(len(guide)),
    )

    cl.enqueue_copy(queue, scores, score_buffer).wait()
    return scores.tolist(), device.name


def compare_sequence_windows(
    guide_sequence,
    target_sequence,
    verify_reference=False,
):
    """Compare target windows, optionally checking OpenCL against CPU.

    Set verify_reference=True to compare accelerated scores with the
    independent CPU reference implementation.
    """
    guide = validate_dna_sequence(guide_sequence)
    target = validate_dna_sequence(target_sequence)

    if len(guide) > len(target):
        raise ValueError(
            "Guide sequence cannot be longer than target sequence."
        )

    fallback_reason = None
    reference_verified = None

    try:
        scores, device_name = _opencl_scores(guide, target)
        execution_device = f"OpenCL GPU: {device_name}"

        if verify_reference:
            reference_scores = cpu_reference_scores(guide, target)
            if scores != reference_scores:
                raise RuntimeError(
                    "OpenCL scores do not match CPU reference scores: "
                    f"OpenCL={scores}, CPU={reference_scores}"
                )
            reference_verified = True

    except RuntimeError as exc:
        # A verification mismatch must not silently fall back to CPU.
        if str(exc).startswith(
            "OpenCL scores do not match CPU reference scores:"
        ):
            raise
        scores = cpu_reference_scores(guide, target)
        execution_device = "CPU"
        fallback_reason = str(exc)

    except Exception as exc:
        scores = cpu_reference_scores(guide, target)
        execution_device = "CPU"
        fallback_reason = str(exc)

    best_position = scores.index(max(scores))
    best_matches = scores[best_position]
    alignment_length = len(guide)
    mismatches = alignment_length - best_matches
    end_position = best_position + alignment_length - 1

    return {
        "guide_sequence": guide,
        "target_sequence": target,
        "start_position": best_position,
        "end_position": end_position,
        "matches": best_matches,
        "mismatches": mismatches,
        "alignment_length": alignment_length,
        "score": (best_matches / alignment_length) * 100,
        "execution_device": execution_device,
        "fallback_reason": fallback_reason,
        "reference_verified": reference_verified,
    }
