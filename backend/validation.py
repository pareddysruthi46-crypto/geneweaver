import math

from alignment.validation import validate_dna_sequence
from backend.errors import ErrorDetail, RequestValidationError
from backend.schemas import AnalysisRequest, AppConfig


SUPPORTED_ALGORITHMS = {"global", "local"}


def _validate_scoring_value(name, value):
    """Return a finite float or None; reject invalid scoring values."""
    if value is None:
        return None

    if isinstance(value, bool) or not isinstance(value, (int, float)):
        raise ValueError(f"{name} must be a finite number.")

    if not math.isfinite(value):
        raise ValueError(f"{name} must be a finite number.")

    return float(value)


def validate_analysis_request(
    request: AnalysisRequest,
    config: AppConfig | None = None,
) -> AnalysisRequest:
    """Validate and normalize an analysis request."""

    config = config or AppConfig()

    if not isinstance(request, AnalysisRequest):
        raise TypeError("request must be an AnalysisRequest instance.")

    errors = []
    normalized_sequences = {}

    for field_name in ("guide_sequence", "target_sequence"):
        value = getattr(request, field_name)

        try:
            normalized = validate_dna_sequence(value)
            if len(normalized) > config.max_sequence_length:
                errors.append(ErrorDetail(
                    code="SEQUENCE_TOO_LONG",
                    message=(
                        f"{field_name} exceeds maximum length "
                        f"of {config.max_sequence_length}."
                    ),
                    field=field_name,
                ))
            else:
                normalized_sequences[field_name] = normalized
        except (TypeError, ValueError) as exc:
            errors.append(ErrorDetail(
                code="INVALID_SEQUENCE",
                message=str(exc),
                field=field_name,
            ))

    algorithm = request.algorithm
    if (
        not isinstance(algorithm, str)
        or algorithm.lower() not in SUPPORTED_ALGORITHMS
    ):
        errors.append(ErrorDetail(
            code="INVALID_ALGORITHM",
            message="Algorithm must be 'global' or 'local'.",
            field="algorithm",
        ))

    scoring_values = {}
    for field_name in (
        "match_score",
        "mismatch_score",
        "minimum_score",
    ):
        supplied_value = getattr(request, field_name)
        config_value = getattr(config, field_name)
        value = (
            config_value if supplied_value is None else supplied_value
        )

        try:
            scoring_values[field_name] = _validate_scoring_value(
                field_name, value
            )
        except ValueError as exc:
            errors.append(ErrorDetail(
                code="INVALID_SCORING_PARAMETER",
                message=str(exc),
                field=field_name,
            ))

    if errors:
        raise RequestValidationError(errors)

    request.guide_sequence = normalized_sequences["guide_sequence"]
    request.target_sequence = normalized_sequences["target_sequence"]
    request.algorithm = algorithm.lower()

    request.match_score = scoring_values["match_score"]
    request.mismatch_score = scoring_values["mismatch_score"]
    request.minimum_score = scoring_values["minimum_score"]

    return request
