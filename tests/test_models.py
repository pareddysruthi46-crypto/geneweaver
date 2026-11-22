import unittest

from alignment.models import SequenceInput, AlignmentResult


class TestSequenceInput(unittest.TestCase):

    def test_sequence_input_stores_guide_and_target(self):
        sequence = SequenceInput(
            guide_sequence="ATGCGTAC",
            target_sequence="TACGCATG"
        )

        self.assertEqual(sequence.guide_sequence, "ATGCGTAC")
        self.assertEqual(sequence.target_sequence, "TACGCATG")


class TestAlignmentResult(unittest.TestCase):

    def test_alignment_result_stores_sequences(self):
        result = AlignmentResult(
            guide_sequence="ATGCGTAC",
            target_sequence="TACGCATG"
        )

        self.assertEqual(result.guide_sequence, "ATGCGTAC")
        self.assertEqual(result.target_sequence, "TACGCATG")

    def test_alignment_fields_default_to_none(self):
        result = AlignmentResult(
            guide_sequence="ATGCGTAC",
            target_sequence="TACGCATG"
        )

        self.assertIsNone(result.aligned_guide)
        self.assertIsNone(result.aligned_target)
        self.assertIsNone(result.score)


if __name__ == "__main__":
    unittest.main()
