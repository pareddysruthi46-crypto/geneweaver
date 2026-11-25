from alignment.models import GuideSequence, TargetSequence
from alignment.validation import validate_dna_sequence


def preprocess_guide_sequence(sequence: str) -> GuideSequence:
    """Validate and prepare a guide DNA sequence."""
    normalized = validate_dna_sequence(sequence)
    return GuideSequence(sequence=normalized)


def preprocess_target_sequence(sequence: str) -> TargetSequence:
    """Validate and prepare a target DNA sequence."""
    normalized = validate_dna_sequence(sequence)
    return TargetSequence(sequence=normalized)
