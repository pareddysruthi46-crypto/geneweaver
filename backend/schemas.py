from dataclasses import dataclass, field
from typing import Optional

from alignment.models import AlignmentResult
from backend.errors import ErrorDetail


@dataclass
class AnalysisRequest:
    """Input schema for a sequence analysis request."""

    guide_sequence: str
    target_sequence: str
    algorithm: str = "global"
    request_id: Optional[str] = None
    match_score: Optional[float] = None
    mismatch_score: Optional[float] = None
    minimum_score: Optional[float] = None


@dataclass
class AnalysisResponse:
    """Output schema for a sequence analysis request."""

    success: bool
    message: str
    result: Optional[AlignmentResult] = None
    errors: list[str] = field(default_factory=list)
    request_id: Optional[str] = None
    error_details: list[ErrorDetail] = field(default_factory=list)


@dataclass
class AppConfig:
    """Application configuration settings."""

    app_name: str = "GeneWeaver"
    version: str = "0.1.0"
    debug: bool = False
    max_sequence_length: int = 10000
    default_algorithm: str = "global"
    match_score: float = 1.0
    mismatch_score: float = 0.0
    minimum_score: Optional[float] = None
