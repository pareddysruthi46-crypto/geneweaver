from alignment.validation import validate_dna_sequence
from backend.errors import ErrorDetail, RequestValidationError
from backend.schemas import AnalysisRequest, AppConfig


SUPPORTED_ALGORITHMS = {"global", "local"}


def validate_analysis_request(
    request: AnalysisRequest,
    config: AppConfig | None = None,
) -> AnalysisRequest:
    """Validate and normalize an analysis request."""

    config = config or AppConfig()
    errors = []

    if not isinstance(request, AnalysisRequest):
        raise TypeError("request must be an AnalysisRequest instance.")

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
    if not isinstance(algorithm, str) or algorithm.lower() not in SUPPORTED_ALGORITHMS:
        errors.append(ErrorDetail(
            code="INVALID_ALGORITHM",
            message="Algorithm must be 'global' or 'local'.",
            field="algorithm",
        ))

    if errors:
        raise RequestValidationError(errors)

    request.guide_sequence = normalized_sequences["guide_sequence"]
    request.target_sequence = normalized_sequences["target_sequence"]
    request.algorithm = algorithm.lower()

    return request
