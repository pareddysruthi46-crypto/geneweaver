"""Command-line entry point for GeneWeaver sequence analysis."""

import argparse

from alignment.baseline import match_guide_to_target
from backend.errors import (
    ErrorDetail,
    ErrorResponse,
    RequestValidationError,
)
from backend.schemas import AnalysisRequest, AnalysisResponse, AppConfig
from backend.serialization import response_to_json
from backend.validation import validate_analysis_request


def build_parser() -> argparse.ArgumentParser:
    """Build the command-line argument parser."""

    config = AppConfig()

    parser = argparse.ArgumentParser(
        description="GeneWeaver sequence analysis CLI"
    )
    parser.add_argument("--guide", required=True, help="Guide DNA sequence")
    parser.add_argument("--target", required=True, help="Target DNA sequence")
    parser.add_argument(
        "--algorithm",
        default=config.default_algorithm,
        choices=["global", "local"],
        help="Analysis algorithm",
    )
    parser.add_argument("--request-id", help="Optional request identifier")
    parser.add_argument(
        "--match-score",
        type=float,
        default=None,
        help="Score added for each matching base",
    )
    parser.add_argument(
        "--mismatch-score",
        type=float,
        default=None,
        help="Score added for each mismatching base",
    )
    parser.add_argument(
        "--minimum-score",
        type=float,
        default=None,
        help="Minimum weighted alignment score required",
    )

    return parser


def main(argv=None) -> int:
    """Validate input, run alignment and print a JSON response."""

    args = build_parser().parse_args(argv)

    request = AnalysisRequest(
        guide_sequence=args.guide,
        target_sequence=args.target,
        algorithm=args.algorithm,
        request_id=args.request_id,
        match_score=args.match_score,
        mismatch_score=args.mismatch_score,
        minimum_score=args.minimum_score,
    )

    try:
        validated_request = validate_analysis_request(request, AppConfig())

        result = match_guide_to_target(
            validated_request.guide_sequence,
            validated_request.target_sequence,
            match_score=validated_request.match_score,
            mismatch_score=validated_request.mismatch_score,
            minimum_score=validated_request.minimum_score,
        )

        response = AnalysisResponse(
            success=True,
            message="Sequence alignment completed successfully.",
            result=result,
            request_id=validated_request.request_id,
        )
        print(response_to_json(response))
        return 0

    except RequestValidationError as exc:
        response = ErrorResponse(
            message="Request validation failed.",
            errors=exc.errors,
            request_id=request.request_id,
        )
        print(response_to_json(response))
        return 2

    except ValueError as exc:
        response = ErrorResponse(
            message="Sequence alignment failed.",
            errors=[
                ErrorDetail(
                    code="ALIGNMENT_ERROR",
                    message=str(exc),
                    field="guide_sequence",
                )
            ],
            request_id=request.request_id,
        )
        print(response_to_json(response))
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
