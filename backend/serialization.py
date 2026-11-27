"""Helpers for predictable JSON API and CLI responses."""

import json
from dataclasses import asdict, is_dataclass


def _serialize_error(error):
    """Convert an error into a consistent dictionary."""
    if is_dataclass(error):
        return asdict(error)

    return {
        "code": "ANALYSIS_ERROR",
        "message": str(error),
        "field": None,
    }


def response_to_dict(response) -> dict:
    """Convert a success or error response into a standard dictionary."""
    result = getattr(response, "result", None)

    if result is not None and is_dataclass(result):
        result = asdict(result)

    errors = [
        _serialize_error(error)
        for error in getattr(response, "errors", [])
    ]

    errors.extend(
        _serialize_error(error)
        for error in getattr(response, "error_details", [])
    )

    return {
        "success": response.success,
        "message": response.message,
        "request_id": response.request_id,
        "result": result,
        "errors": errors,
    }


def response_to_json(response, indent: int = 2) -> str:
    """Serialize a response as JSON text."""
    return json.dumps(
        response_to_dict(response),
        indent=indent,
    )
