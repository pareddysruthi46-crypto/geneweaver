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
