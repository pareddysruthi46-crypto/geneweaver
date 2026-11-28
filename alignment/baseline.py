"""Simple CPU baseline for configurable guide-to-target matching."""

import math

from alignment.models import AlignmentResult
from alignment.validation import validate_dna_sequence


def _validate_scoring_value(name: str, value: float) -> float:
    """Validate a finite numeric scoring value."""
    if isinstance(value, bool) or not isinstance(value, (int, float)):
        raise ValueError(f"{name} must be a finite number.")

    if not math.isfinite(value):
        raise ValueError(f"{name} must be a finite number.")

    return float(value)


def match_guide_to_target(
    guide_sequence: str,
    target_sequence: str,
    match_score: float = 1.0,
    mismatch_score: float = 0.0,
    minimum_score: float = None,
) -> AlignmentResult:
    """Find the best ungapped guide match using configurable scoring.

    Each matching base adds match_score. Each mismatching base adds
    mismatch_score. minimum_score optionally rejects weak alignments.
    The score field remains percentage identity for backward compatibility.
    """

    match_score = _validate_scoring_value("match_score", match_score)
    mismatch_score = _validate_scoring_value(
        "mismatch_score", mismatch_score
    )

    if minimum_score is not None:
        minimum_score = _validate_scoring_value(
            "minimum_score", minimum_score
        )

    guide = validate_dna_sequence(guide_sequence)
    target = validate_dna_sequence(target_sequence)

    if len(guide) > len(target):
        raise ValueError(
            "Guide sequence cannot be longer than target sequence."
        )

    best_position = 0
    best_matches = -1
    best_alignment_score = None

    for position in range(len(target) - len(guide) + 1):
        window = target[position:position + len(guide)]

        matches = sum(
            guide_base == target_base
            for guide_base, target_base in zip(guide, window)
        )
        mismatches = len(guide) - matches

        weighted_score = (
            matches * match_score + mismatches * mismatch_score
        )

        if (
            best_alignment_score is None
            or weighted_score > best_alignment_score
        ):
            best_alignment_score = weighted_score
            best_matches = matches
            best_position = position

    if (
        minimum_score is not None
        and best_alignment_score < minimum_score
    ):
        raise ValueError(
            f"Best alignment score {best_alignment_score} is below "
            f"the minimum required score {minimum_score}."
        )

    best_target = target[best_position:best_position + len(guide)]
    mismatches = len(guide) - best_matches
    alignment_length = len(guide)
    percentage_identity = (best_matches / alignment_length) * 100
    end_position = best_position + alignment_length - 1

    summary = (
        f"{best_matches} matches, {mismatches} mismatches "
        f"over {alignment_length} bases; "
        f"target positions {best_position}-{end_position}. "
        f"Weighted alignment score: {best_alignment_score}."
    )

    return AlignmentResult(
        guide_sequence=guide,
        target_sequence=target,
        aligned_guide=guide,
        aligned_target=best_target,
        score=percentage_identity,
        start_position=best_position,
        end_position=end_position,
        matches=best_matches,
        mismatches=mismatches,
        alignment_length=alignment_length,
        summary=summary,
        alignment_score=best_alignment_score,
        match_score=match_score,
        mismatch_score=mismatch_score,
        minimum_score=minimum_score,
    )
