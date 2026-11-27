import json

from alignment.baseline import match_guide_to_target
from backend.schemas import AnalysisResponse
from backend.serialization import response_to_dict, response_to_json


def test_manual_exact_match_metrics():
    result = match_guide_to_target("ATGC", "TTATGCAA")

    assert result.start_position == 2
    assert result.end_position == 5
    assert result.matches == 4
    assert result.mismatches == 0
    assert result.alignment_length == 4
    assert result.score == 100.0


def test_manual_one_mismatch_metrics():
    result = match_guide_to_target("ATGC", "TTATACAA")

    assert result.start_position == 2
    assert result.end_position == 5
    assert result.matches == 3
    assert result.mismatches == 1
    assert result.alignment_length == 4
    assert result.score == 75.0


def test_manual_two_mismatch_metrics():
    result = match_guide_to_target("ATGC", "TTAGACAA")

    assert result.start_position == 2
    assert result.end_position == 5
    assert result.matches == 2
    assert result.mismatches == 2
    assert result.alignment_length == 4
    assert result.score == 50.0


def test_alignment_summary_contains_verified_metrics():
    result = match_guide_to_target("ATGC", "TTATACAA")

    assert "3 matches" in result.summary
    assert "1 mismatches" in result.summary
    assert "2" in result.summary
    assert "5" in result.summary


def test_serialized_alignment_result_matches_manual_values():
    result = match_guide_to_target("ATGC", "TTATACAA")

    response = AnalysisResponse(
        success=True,
        message="Sequence alignment completed successfully.",
        result=result,
        request_id="manual-test-001",
    )

    data = response_to_dict(response)

    assert data["success"] is True
    assert data["request_id"] == "manual-test-001"
    assert data["result"]["matches"] == 3
    assert data["result"]["mismatches"] == 1
    assert data["result"]["start_position"] == 2
    assert data["result"]["end_position"] == 5


def test_json_output_is_valid_and_preserves_metrics():
    result = match_guide_to_target("ATGC", "TTATACAA")

    response = AnalysisResponse(
        success=True,
        message="Sequence alignment completed successfully.",
        result=result,
        request_id="manual-json-001",
    )

    output = response_to_json(response)
    data = json.loads(output)

    assert data["success"] is True
    assert data["result"]["matches"] == 3
    assert data["result"]["mismatches"] == 1
    assert data["result"]["score"] == 75.0
