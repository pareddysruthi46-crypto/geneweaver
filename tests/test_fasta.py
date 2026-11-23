import tempfile
import unittest
from pathlib import Path

from alignment.fasta import parse_fasta, read_fasta


FIXTURES_DIR = Path(__file__).parent / "fixtures"


class TestFastaParser(unittest.TestCase):

    def test_parse_single_record(self):
        content = ">gene1 Sample gene\nATGC"
        records = parse_fasta(content)

        self.assertEqual(len(records), 1)
        self.assertEqual(records[0].record_id, "gene1")
        self.assertEqual(records[0].description, "Sample gene")
        self.assertEqual(records[0].sequence, "ATGC")

    def test_parse_multiple_records(self):
        content = ">gene1 First gene\nATGC\n>gene2 Second gene\nGATTACA"
        records = parse_fasta(content)

        self.assertEqual(len(records), 2)
        self.assertEqual(records[0].sequence, "ATGC")
        self.assertEqual(records[1].sequence, "GATTACA")

    def test_parse_multiline_sequence(self):
        content = ">gene1\nATGC\nGATT"
        records = parse_fasta(content)

        self.assertEqual(records[0].sequence, "ATGCGATT")

    def test_sequence_is_converted_to_uppercase(self):
        records = parse_fasta(">gene1\natgc")
        self.assertEqual(records[0].sequence, "ATGC")

    def test_invalid_dna_character_is_rejected(self):
        with self.assertRaises(ValueError):
            parse_fasta(">gene1\nATGXYZ")

    def test_missing_header_is_rejected(self):
        with self.assertRaises(ValueError):
            parse_fasta("ATGC")

    def test_empty_sequence_is_rejected(self):
        with self.assertRaises(ValueError):
            parse_fasta(">gene1\n>gene2\nATGC")

    def test_empty_input_is_rejected(self):
        with self.assertRaises(ValueError):
            parse_fasta("")

    def test_read_fasta_file(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            fasta_path = Path(temp_dir) / "sample.fasta"
            fasta_path.write_text(
                ">gene1 Sample gene\nATGC\n>gene2\nGATTACA",
                encoding="utf-8"
            )

            records = read_fasta(fasta_path)

            self.assertEqual(len(records), 2)
            self.assertEqual(records[0].record_id, "gene1")
            self.assertEqual(records[0].sequence, "ATGC")
            self.assertEqual(records[1].sequence, "GATTACA")

    def test_valid_fasta_fixture(self):
        records = read_fasta(FIXTURES_DIR / "valid.fasta")

        self.assertEqual(len(records), 1)
        self.assertEqual(records[0].record_id, "valid_001")
        self.assertEqual(records[0].sequence, "ATGCGTACGTAG")

    def test_empty_fasta_fixture(self):
        with self.assertRaises(ValueError):
            read_fasta(FIXTURES_DIR / "empty.fasta")

    def test_malformed_fasta_fixture(self):
        with self.assertRaises(ValueError):
            read_fasta(FIXTURES_DIR / "malformed.fasta")

    def test_multi_record_fasta_fixture(self):
        records = read_fasta(FIXTURES_DIR / "multi_record.fasta")

        self.assertEqual(len(records), 3)
        self.assertEqual(
            [record.record_id for record in records],
            ["record_001", "record_002", "record_003"]
        )
        self.assertEqual(
            [record.sequence for record in records],
            ["ATGCGTAC", "TTGCAAGT", "GGCCTTAA"]
        )


if __name__ == "__main__":
    unittest.main()
