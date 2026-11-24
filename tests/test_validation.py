import unittest

from alignment.validation import validate_dna_sequence


class TestDNAValidation(unittest.TestCase):

    def test_valid_uppercase_sequence(self):
        self.assertEqual(validate_dna_sequence("ATGC"), "ATGC")

    def test_lowercase_sequence_is_normalized(self):
        self.assertEqual(validate_dna_sequence("atgc"), "ATGC")

    def test_mixed_case_sequence_is_normalized(self):
        self.assertEqual(validate_dna_sequence("AtGc"), "ATGC")

    def test_whitespace_is_removed(self):
        self.assertEqual(validate_dna_sequence("at gc\nTA"), "ATGCTA")

    def test_empty_sequence_is_rejected(self):
        with self.assertRaisesRegex(ValueError, "cannot be empty"):
            validate_dna_sequence("")

    def test_invalid_symbols_are_reported(self):
        with self.assertRaisesRegex(ValueError, "Invalid DNA symbol"):
            validate_dna_sequence("ATGX")

    def test_invalid_symbol_positions_are_reported(self):
        with self.assertRaisesRegex(ValueError, "position 4"):
            validate_dna_sequence("ATGX")

    def test_non_string_input_is_rejected(self):
        with self.assertRaises(TypeError):
            validate_dna_sequence(None)


if __name__ == "__main__":
    unittest.main()
