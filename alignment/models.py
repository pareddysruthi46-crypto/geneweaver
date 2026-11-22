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
