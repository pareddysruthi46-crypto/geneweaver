"""Simple CPU baseline for guide-to-target sequence matching.

Assumptions:
- Input sequences contain only A, T, G and C.
- Matching uses ungapped, fixed-length windows.
- Each matching base contributes equally to the identity score.
- The first window is selected when multiple windows share the best score.
- The reported start_position is zero-based.
"""

from alignment.models import AlignmentResult
from alignment.validation import validate_dna_sequence


def match_guide_to_target(
    guide_sequence: str,
    target_sequence: str,
) -> AlignmentResult:
    """Find the best ungapped guide match in a target sequence."""

    guide = validate_dna_sequence(guide_sequence)
    target = validate_dna_sequence(target_sequence)

    if len(guide) > len(target):
        raise ValueError(
            "Guide sequence cannot be longer than target sequence."
        )

    best_position = 0
    best_matches = -1

    for position in range(len(target) - len(guide) + 1):
        window = target[position:position + len(guide)]

        matches = sum(
            guide_base == target_base
            for guide_base, target_base in zip(guide, window)
        )

        if matches > best_matches:
            best_matches = matches
            best_position = position

    best_target = target[best_position:best_position + len(guide)]
    mismatches = len(guide) - best_matches
    score = (best_matches / len(guide)) * 100

    return AlignmentResult(
        guide_sequence=guide,
        target_sequence=target,
        aligned_guide=guide,
        aligned_target=best_target,
        score=score,
        start_position=best_position,
        mismatches=mismatches,
    )
