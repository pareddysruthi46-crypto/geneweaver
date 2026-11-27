from dataclasses import dataclass
from typing import Optional


@dataclass
class SequenceInput:
    guide_sequence: str
    target_sequence: str


@dataclass
class AlignmentResult:
    guide_sequence: str
    target_sequence: str
    aligned_guide: Optional[str] = None
    aligned_target: Optional[str] = None
    score: Optional[float] = None
    start_position: Optional[int] = None
    end_position: Optional[int] = None
    matches: Optional[int] = None
    mismatches: Optional[int] = None
    alignment_length: Optional[int] = None
    summary: Optional[str] = None


@dataclass
class GuideSequence:
    """Represents a preprocessed guide DNA sequence."""

    sequence: str

    @property
    def length(self) -> int:
        return len(self.sequence)

    @property
    def gc_content(self) -> float:
        return (
            (self.sequence.count("G") + self.sequence.count("C"))
            / self.length
        )


@dataclass
class TargetSequence:
    """Represents a preprocessed target DNA sequence."""

    sequence: str

    @property
    def length(self) -> int:
        return len(self.sequence)

    @property
    def gc_content(self) -> float:
        return (
            (self.sequence.count("G") + self.sequence.count("C"))
            / self.length
        )
