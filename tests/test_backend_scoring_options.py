import json
import unittest
from contextlib import redirect_stdout
from io import StringIO

from backend import (
    AnalysisRequest,
    AppConfig,
    RequestValidationError,
    validate_analysis_request,
)
from backend.cli import main


class TestBackendScoringOptions(unittest.TestCase):

    def run_cli(self, args):
        output = StringIO()
        with redirect_stdout(output):
            code = main(args)
        return code, json.loads(output.getvalue())

    def test_request_accepts_scoring_parameters(self):
        request = AnalysisRequest(
            "ATGC",
            "ATGA",
            match_score=2,
            mismatch_score=-1,
            minimum_score=5,
        )
        result = validate_analysis_request(request)

        self.assertEqual(result.match_score, 2.0)
        self.assertEqual(result.mismatch_score, -1.0)
        self.assertEqual(result.minimum_score, 5.0)

    def test_config_provides_default_scoring_parameters(self):
        config = AppConfig(
            match_score=3,
            mismatch_score=-2,
            minimum_score=4,
        )
        request = AnalysisRequest("ATGC", "ATGA")

        result = validate_analysis_request(request, config)

        self.assertEqual(result.match_score, 3.0)
        self.assertEqual(result.mismatch_score, -2.0)
        self.assertEqual(result.minimum_score, 4.0)

    def test_cli_exposes_custom_scoring_parameters(self):
        code, response = self.run_cli([
            "--guide", "ATGC",
            "--target", "ATGA",
            "--match-score", "2",
            "--mismatch-score", "-1",
            "--minimum-score", "5",
        ])

        self.assertEqual(code, 0)
        self.assertTrue(response["success"])
        self.assertEqual(response["result"]["alignment_score"], 5.0)
        self.assertEqual(response["result"]["match_score"], 2.0)
        self.assertEqual(response["result"]["mismatch_score"], -1.0)
        self.assertEqual(response["result"]["minimum_score"], 5.0)

    def test_cli_rejects_alignment_below_minimum_score(self):
        code, response = self.run_cli([
            "--guide", "ATGC",
            "--target", "ATGA",
            "--match-score", "2",
            "--mismatch-score", "-1",
            "--minimum-score", "6",
        ])

        self.assertEqual(code, 2)
        self.assertFalse(response["success"])
        self.assertIn("below the minimum", response["errors"][0]["message"])

    def test_invalid_scoring_parameter_is_rejected(self):
        request = AnalysisRequest(
            "ATGC",
            "ATGC",
            match_score=float("nan"),
        )

        with self.assertRaises(RequestValidationError) as context:
            validate_analysis_request(request)

        self.assertEqual(
            context.exception.errors[0].code,
            "INVALID_SCORING_PARAMETER",
        )
        self.assertEqual(
            context.exception.errors[0].field,
            "match_score",
        )

    def test_boolean_scoring_parameter_is_rejected(self):
        request = AnalysisRequest(
            "ATGC",
            "ATGC",
            mismatch_score=True,
        )

        with self.assertRaises(RequestValidationError):
            validate_analysis_request(request)


if __name__ == "__main__":
    unittest.main()
