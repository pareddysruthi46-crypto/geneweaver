from dataclasses import dataclass, field
from typing import Optional

from alignment.models import AlignmentResult


@dataclass
class AnalysisRequest:
    """Input schema for a sequence analysis request."""

    guide_sequence: str
    target_sequence: str
    algorithm: str = "global"
    request_id: Optional[str] = None


@dataclass
class AnalysisResponse:
    """Output schema for a sequence analysis request."""

    success: bool
    message: str
    result: Optional[AlignmentResult] = None
    errors: list[str] = field(default_factory=list)
    request_id: Optional[str] = None


@dataclass
class AppConfig:
    """Application configuration settings."""

    app_name: str = "GeneWeaver"
    version: str = "0.1.0"
    debug: bool = False
    max_sequence_length: int = 10000
    default_algorithm: str = "global"
