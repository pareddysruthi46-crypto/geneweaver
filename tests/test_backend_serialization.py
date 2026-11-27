import json
from dataclasses import dataclass

from backend.errors import ErrorDetail, ErrorResponse
from backend.schemas import AnalysisResponse
from backend.serialization import response_to_dict, response_to_json


@dataclass
class SampleResult:
    start_position: int
    end_position: int
    matches: int
    mismatches: int


def test_success_response_has_predictable_json_fields():
    result = SampleResult(2, 5, 4, 0)
    response = AnalysisResponse(
        success=True,
        message="Alignment completed.",
        result=result,
        request_id="test-123",
    )

    data = response_to_dict(response)

    assert list(data.keys()) == [
        "success", "message", "request_id", "result", "errors"
    ]
    assert data["success"] is True
    assert data["request_id"] == "test-123"
    assert data["result"]["start_position"] == 2
    assert data["errors"] == []


def test_error_response_has_consistent_error_structure():
    response = ErrorResponse(
        message="Request validation failed.",
        errors=[
            ErrorDetail(
                code="INVALID_SEQUENCE",
                message="Invalid DNA sequence.",
                field="guide_sequence",
            )
        ],
        request_id="error-123",
    )

    data = response_to_dict(response)

    assert data["success"] is False
    assert data["result"] is None
    assert data["errors"][0]["code"] == "INVALID_SEQUENCE"
    assert data["errors"][0]["field"] == "guide_sequence"


def test_response_to_json_returns_valid_json():
    response = AnalysisResponse(
        success=True,
        message="Alignment completed.",
        request_id="json-123",
    )

    output = response_to_json(response)
    data = json.loads(output)

    assert data["success"] is True
    assert data["request_id"] == "json-123"


def test_string_errors_are_serialized_consistently():
    response = AnalysisResponse(
        success=False,
        message="Analysis failed.",
        errors=["Unexpected alignment error."],
    )

    data = response_to_dict(response)

    assert data["errors"][0]["code"] == "ANALYSIS_ERROR"
    assert data["errors"][0]["message"] == "Unexpected alignment error."
