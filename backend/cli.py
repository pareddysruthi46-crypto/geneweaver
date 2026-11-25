"""Command-line entry point for GeneWeaver sequence analysis."""

import argparse
import json
from dataclasses import asdict

from backend.errors import ErrorResponse, RequestValidationError
from backend.schemas import AnalysisRequest, AnalysisResponse, AppConfig
from backend.validation import validate_analysis_request


def build_parser() -> argparse.ArgumentParser:
    """Build the command-line argument parser."""

    parser = argparse.ArgumentParser(
        description="GeneWeaver sequence analysis CLI"
    )
    parser.add_argument("--guide", required=True, help="Guide DNA sequence")
    parser.add_argument("--target", required=True, help="Target DNA sequence")
    parser.add_argument(
        "--algorithm",
        default="global",
        choices=["global", "local"],
        help="Analysis algorithm (default: global)",
    )
    parser.add_argument("--request-id", help="Optional request identifier")

    return parser


def main(argv=None) -> int:
    """Validate CLI input and print a structured JSON response."""

    args = build_parser().parse_args(argv)

    request = AnalysisRequest(
        guide_sequence=args.guide,
        target_sequence=args.target,
        algorithm=args.algorithm,
        request_id=args.request_id,
    )

    try:
        validated_request = validate_analysis_request(request, AppConfig())

        response = AnalysisResponse(
            success=True,
            message="Input sequences accepted and validated successfully.",
            request_id=validated_request.request_id,
        )
        print(json.dumps(asdict(response), indent=2))
        return 0

    except RequestValidationError as exc:
        response = ErrorResponse(
            message="Request validation failed.",
            errors=exc.errors,
            request_id=request.request_id,
        )
        print(json.dumps(asdict(response), indent=2))
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
