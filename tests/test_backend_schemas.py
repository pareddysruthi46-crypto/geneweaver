import unittest

from alignment.models import AlignmentResult
from backend import AnalysisRequest, AnalysisResponse, AppConfig


class TestAnalysisRequest(unittest.TestCase):

    def test_request_stores_sequences(self):
        request = AnalysisRequest(
            guide_sequence="ATGC",
            target_sequence="TACG",
        )
        self.assertEqual(request.guide_sequence, "ATGC")
        self.assertEqual(request.target_sequence, "TACG")

    def test_request_default_options(self):
        request = AnalysisRequest("ATGC", "TACG")
        self.assertEqual(request.algorithm, "global")
        self.assertIsNone(request.request_id)


class TestAnalysisResponse(unittest.TestCase):

    def test_successful_response(self):
        result = AlignmentResult(
            guide_sequence="ATGC",
            target_sequence="TACG",
            score=2.5,
        )
        response = AnalysisResponse(
            success=True,
            message="Analysis completed",
            result=result,
        )
        self.assertTrue(response.success)
        self.assertEqual(response.result.score, 2.5)

    def test_error_response(self):
        response = AnalysisResponse(
            success=False,
            message="Analysis failed",
            errors=["Invalid sequence"],
        )
        self.assertFalse(response.success)
        self.assertEqual(response.errors, ["Invalid sequence"])

    def test_error_lists_are_independent(self):
        first = AnalysisResponse(success=False, message="Failed")
        second = AnalysisResponse(success=False, message="Failed")
        first.errors.append("Error")
        self.assertEqual(second.errors, [])


class TestAppConfig(unittest.TestCase):

    def test_default_configuration(self):
        config = AppConfig()
        self.assertEqual(config.app_name, "GeneWeaver")
        self.assertEqual(config.version, "0.1.0")
        self.assertFalse(config.debug)
        self.assertEqual(config.max_sequence_length, 10000)
        self.assertEqual(config.default_algorithm, "global")

    def test_custom_configuration(self):
        config = AppConfig(debug=True, max_sequence_length=5000)
        self.assertTrue(config.debug)
        self.assertEqual(config.max_sequence_length, 5000)


if __name__ == "__main__":
    unittest.main()
