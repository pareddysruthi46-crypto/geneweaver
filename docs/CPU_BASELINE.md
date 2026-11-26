# GeneWeaver CPU Baseline Sequence Matching

## Purpose

This module provides a simple CPU-based baseline for matching a guide DNA
sequence against a target DNA sequence.

## Algorithm

The `match_guide_to_target()` function in `alignment/baseline.py`:

1. Validates and normalizes guide and target DNA sequences.
2. Creates target windows having the same length as the guide.
3. Compares each guide base with the corresponding window base.
4. Counts matching bases and calculates percentage identity.
5. Returns the window with the highest identity score.

## Assumptions and limitations

- Only DNA bases A, T, G and C are supported.
- Lowercase input is normalized to uppercase.
- Whitespace is removed during validation.
- Matching is ungapped: insertions and deletions are not considered.
- Reverse-complement matching is not performed.
- Every base has equal weight.
- The first window is selected when scores are tied.
- Start position is zero-based.
- A guide longer than the target raises a ValueError.
- Empty or invalid sequences are rejected.

## Result fields

The function returns an `AlignmentResult` containing:

| Field | Description |
|---|---|
| guide_sequence | Normalized guide sequence |
| target_sequence | Normalized full target sequence |
| aligned_guide | Guide sequence used for comparison |
| aligned_target | Best matching target window |
| score | Percentage identity from 0 to 100 |
| start_position | Zero-based start position in target |
| mismatches | Number of non-matching bases |

## Complexity

Let G be the guide length and T be the target length.

The algorithm compares T - G + 1 windows, each containing G bases.

- Time complexity: O((T - G + 1) * G)
- Extra working space: O(G) for the selected target window.

## Execution

This baseline uses standard Python CPU execution and does not require GPU
hardware or GPU-specific libraries.

## Testing

Unit tests are provided in `tests/test_baseline.py`.

The full project test suite currently passes with 74 tests.
