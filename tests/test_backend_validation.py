import unittest

from backend import (
    AnalysisRequest,
    AnalysisResponse,
    AppConfig,
    ErrorDetail,
    ErrorResponse,
    RequestValidationError,
    validate_analysis_request,
)


class TestBackendValidation(unittest.TestCase):

    def test_valid_request_normalizes_sequences(self):
        request = AnalysisRequest("atgc", "tacg")
        result = validate_analysis_request(request)

        self.assertEqual(result.guide_sequence, "ATGC")
        self.assertEqual(result.target_sequence, "TACG")
        self.assertEqual(result.algorithm, "global")

    def test_invalid_guide_sequence(self):
        request = AnalysisRequest("ATGX", "TACG")

        with self.assertRaises(RequestValidationError) as context:
            validate_analysis_request(request)

        self.assertEqual(context.exception.errors[0].code, "INVALID_SEQUENCE")
        self.assertEqual(context.exception.errors[0].field, "guide_sequence")

    def test_invalid_target_sequence(self):
        request = AnalysisRequest("ATGC", "TACX")

        with self.assertRaises(RequestValidationError) as context:
            validate_analysis_request(request)

        self.assertEqual(context.exception.errors[0].field, "target_sequence")

    def test_invalid_algorithm(self):
        request = AnalysisRequest("ATGC", "TACG", algorithm="unknown")

        with self.assertRaises(RequestValidationError) as context:
            validate_analysis_request(request)

        self.assertEqual(context.exception.errors[0].code, "INVALID_ALGORITHM")

    def test_local_algorithm_is_supported(self):
        request = AnalysisRequest("ATGC", "TACG", algorithm="LOCAL")
        result = validate_analysis_request(request)

        self.assertEqual(result.algorithm, "local")

    def test_multiple_errors_are_collected(self):
        request = AnalysisRequest("ATGX", "TACX", algorithm="unknown")

        with self.assertRaises(RequestValidationError) as context:
            validate_analysis_request(request)

        self.assertEqual(len(context.exception.errors), 3)

    def test_maximum_sequence_length(self):
        request = AnalysisRequest("ATGCA", "TACGT")
        config = AppConfig(max_sequence_length=4)

        with self.assertRaises(RequestValidationError) as context:
            validate_analysis_request(request, config)

        self.assertEqual(context.exception.errors[0].code, "SEQUENCE_TOO_LONG")

    def test_non_request_input_is_rejected(self):
        with self.assertRaises(TypeError):
            validate_analysis_request({"guide_sequence": "ATGC"})

    def test_error_response_structure(self):
        detail = ErrorDetail(
            code="INVALID_SEQUENCE",
            message="Invalid DNA symbol.",
            field="guide_sequence",
        )
        response = ErrorResponse(errors=[detail], request_id="test-1")

        self.assertFalse(response.success)
        self.assertEqual(response.errors[0].code, "INVALID_SEQUENCE")
        self.assertEqual(response.request_id, "test-1")

    def test_analysis_response_supports_structured_errors(self):
        detail = ErrorDetail(
            code="INVALID_ALGORITHM",
            message="Unsupported algorithm.",
            field="algorithm",
        )
        response = AnalysisResponse(
            success=False,
            message="Validation failed",
            error_details=[detail],
        )

        self.assertEqual(response.error_details[0].field, "algorithm")


if __name__ == "__main__":
    unittest.main()
