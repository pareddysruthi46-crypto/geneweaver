import unittest

from alignment.preprocessing import (
    preprocess_guide_sequence,
    preprocess_target_sequence,
)


class TestGuidePreprocessing(unittest.TestCase):

    def test_guide_sequence_is_normalized(self):
        guide = preprocess_guide_sequence("at gc")
        self.assertEqual(guide.sequence, "ATGC")

    def test_guide_length(self):
        guide = preprocess_guide_sequence("ATGCGT")
        self.assertEqual(guide.length, 6)

    def test_guide_gc_content(self):
        guide = preprocess_guide_sequence("ATGC")
        self.assertEqual(guide.gc_content, 0.5)

    def test_invalid_guide_is_rejected(self):
        with self.assertRaises(ValueError):
            preprocess_guide_sequence("ATGX")

    def test_empty_guide_is_rejected(self):
        with self.assertRaisesRegex(ValueError, "cannot be empty"):
            preprocess_guide_sequence("")

    def test_whitespace_only_guide_is_rejected(self):
        with self.assertRaisesRegex(ValueError, "cannot be empty"):
            preprocess_guide_sequence("   ")


class TestTargetPreprocessing(unittest.TestCase):

    def test_target_sequence_is_normalized(self):
        target = preprocess_target_sequence("tt gc")
        self.assertEqual(target.sequence, "TTGC")

    def test_target_length(self):
        target = preprocess_target_sequence("ATGCGT")
        self.assertEqual(target.length, 6)

    def test_target_gc_content(self):
        target = preprocess_target_sequence("GGCC")
        self.assertEqual(target.gc_content, 1.0)

    def test_invalid_target_is_rejected(self):
        with self.assertRaises(ValueError):
            preprocess_target_sequence("ATGX")

    def test_empty_target_is_rejected(self):
        with self.assertRaisesRegex(ValueError, "cannot be empty"):
            preprocess_target_sequence("")

    def test_non_string_target_is_rejected(self):
        with self.assertRaises(TypeError):
            preprocess_target_sequence(None)


if __name__ == "__main__":
    unittest.main()
