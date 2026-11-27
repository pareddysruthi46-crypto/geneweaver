"""Simple CPU baseline for guide-to-target sequence matching."""

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
    alignment_length = len(guide)
    score = (best_matches / alignment_length) * 100
    end_position = best_position + alignment_length - 1

    summary = (
        f"{best_matches} matches, {mismatches} mismatches "
        f"over {alignment_length} bases; "
        f"target positions {best_position}-{end_position}."
    )

    return AlignmentResult(
        guide_sequence=guide,
        target_sequence=target,
        aligned_guide=guide,
        aligned_target=best_target,
        score=score,
        start_position=best_position,
        end_position=end_position,
        matches=best_matches,
        mismatches=mismatches,
        alignment_length=alignment_length,
        summary=summary,
    )
