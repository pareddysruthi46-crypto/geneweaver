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
            "--guide", "atgc",
            "--target", "ATGCGG",
            "--algorithm", "global",
        ])
        self.assertEqual(code, 0)
        self.assertTrue(response["success"])

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
