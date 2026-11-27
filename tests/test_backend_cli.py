import json
import unittest
from contextlib import redirect_stdout, redirect_stderr
from io import StringIO

from backend.cli import main


class TestBackendCLI(unittest.TestCase):

    def run_cli(self, args):
        output = StringIO()
        with redirect_stdout(output):
            exit_code = main(args)
        return exit_code, json.loads(output.getvalue())

    def test_valid_sequences(self):
        code, response = self.run_cli([
            "--guide", "ATGC",
            "--target", "ATGCGG",
            "--algorithm", "global",
        ])
        self.assertEqual(code, 0)
        self.assertTrue(response["success"])
        self.assertEqual(
            response["message"],
            "Sequence alignment completed successfully.",
        )

    def test_alignment_result_is_returned(self):
        code, response = self.run_cli([
            "--guide", "ATGC",
            "--target", "GGATGCTT",
        ])
        self.assertEqual(code, 0)
        result = response["result"]
        self.assertEqual(result["aligned_guide"], "ATGC")
        self.assertEqual(result["aligned_target"], "ATGC")
        self.assertEqual(result["score"], 100.0)
        self.assertEqual(result["start_position"], 2)
        self.assertEqual(result["mismatches"], 0)

    def test_alignment_result_with_mismatches(self):
        code, response = self.run_cli([
            "--guide", "ATGC",
            "--target", "ATGA",
        ])
        self.assertEqual(code, 0)
        self.assertEqual(response["result"]["mismatches"], 1)
        self.assertEqual(response["result"]["score"], 75.0)

    def test_request_id_is_preserved(self):
        code, response = self.run_cli([
            "--guide", "ATGC",
            "--target", "ATGC",
            "--request-id", "test-001",
        ])
        self.assertEqual(code, 0)
        self.assertEqual(response["request_id"], "test-001")

    def test_invalid_dna_sequence(self):
        code, response = self.run_cli([
            "--guide", "ATGX",
            "--target", "ATGC",
        ])
        self.assertEqual(code, 2)
        self.assertFalse(response["success"])
        self.assertEqual(response["errors"][0]["code"], "INVALID_SEQUENCE")

    def test_lowercase_sequences_are_accepted(self):
        code, response = self.run_cli([
            "--guide", "atgc",
            "--target", "atgg",
        ])
        self.assertEqual(code, 0)
        self.assertTrue(response["success"])
        self.assertEqual(response["result"]["aligned_guide"], "ATGC")

    def test_empty_guide_sequence(self):
        code, response = self.run_cli([
            "--guide", "",
            "--target", "ATGC",
        ])
        self.assertEqual(code, 2)
        self.assertFalse(response["success"])
        self.assertEqual(response["errors"][0]["field"], "guide_sequence")

    def test_empty_target_sequence(self):
        code, response = self.run_cli([
            "--guide", "ATGC",
            "--target", "",
        ])
        self.assertEqual(code, 2)
        self.assertFalse(response["success"])
        self.assertEqual(response["errors"][0]["field"], "target_sequence")

    def test_invalid_target_sequence(self):
        code, response = self.run_cli([
            "--guide", "ATGC",
            "--target", "ATGX",
        ])
        self.assertEqual(code, 2)
        self.assertFalse(response["success"])
        self.assertEqual(response["errors"][0]["field"], "target_sequence")

    def test_guide_longer_than_target_returns_alignment_error(self):
        code, response = self.run_cli([
            "--guide", "ATGCG",
            "--target", "ATGC",
        ])
        self.assertEqual(code, 2)
        self.assertFalse(response["success"])
        self.assertEqual(response["errors"][0]["code"], "ALIGNMENT_ERROR")

    def test_missing_guide_argument(self):
        with redirect_stderr(StringIO()):
            with self.assertRaises(SystemExit) as error:
                main(["--target", "ATGC"])
        self.assertEqual(error.exception.code, 2)

    def test_missing_target_argument(self):
        with redirect_stderr(StringIO()):
            with self.assertRaises(SystemExit) as error:
                main(["--guide", "ATGC"])
        self.assertEqual(error.exception.code, 2)

    def test_unsupported_algorithm(self):
        with redirect_stderr(StringIO()):
            with self.assertRaises(SystemExit) as error:
                main([
                    "--guide", "ATGC",
                    "--target", "ATGC",
                    "--algorithm", "unknown",
                ])
        self.assertEqual(error.exception.code, 2)


if __name__ == "__main__":
    unittest.main()
