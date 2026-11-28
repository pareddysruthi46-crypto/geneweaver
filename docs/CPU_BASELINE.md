# GeneWeaver CPU Baseline Sequence Matching

## Purpose

This module provides CPU-based guide-to-target DNA sequence matching
with configurable match and mismatch scoring.

## Algorithm

The match_guide_to_target() function:

1. Validates and normalizes guide and target DNA sequences.
2. Creates target windows matching the guide length.
3. Compares corresponding bases.
4. Calculates a weighted score for each window.
5. Selects the window with the highest weighted score.
6. Optionally rejects alignments below minimum_score.

## Configurable scoring

| Parameter | Default | Meaning |
|---|---:|---|
| match_score | 1.0 | Points added for each matching base |
| mismatch_score | 0.0 | Points added for each mismatching base |
| minimum_score | None | Minimum acceptable weighted score |

Weighted score formula:

alignment_score = (matches * match_score) + (mismatches * mismatch_score)

Example with match_score=2 and mismatch_score=-1:

- 4 matches and 0 mismatches produce 8.
- 3 matches and 1 mismatch produce 5.
- 2 matches and 2 mismatches produce 2.

If minimum_score is provided, alignments below that threshold
raise ValueError. Otherwise, the best alignment is returned.

All scoring values must be finite numbers.

## Result fields

| Field | Description |
|---|---|
| score | Percentage identity from 0 to 100 |
| alignment_score | Configurable weighted score |
| match_score | Configured match points |
| mismatch_score | Configured mismatch points |
| minimum_score | Optional acceptance threshold |
| start_position | Zero-based start position |
| end_position | Zero-based end position |
| matches | Number of matching bases |
| mismatches | Number of mismatching bases |
| alignment_length | Number of compared bases |
| summary | Human-readable alignment summary |

The original score field remains percentage identity for backward
compatibility. alignment_score contains the weighted score.

## Assumptions and limitations

- Only DNA bases A, T, G and C are supported.
- Lowercase input is normalized to uppercase.
- Whitespace is removed during validation.
- Matching is ungapped; insertions and deletions are not considered.
- Reverse-complement matching is not performed.
- Every base uses the same configured match or mismatch value.
- The first window is selected when weighted scores are tied.
- Positions are zero-based.
- A guide longer than the target raises ValueError.
- Empty or invalid sequences are rejected.

## Complexity

Let G be guide length and T be target length.

- Time complexity: O((T - G + 1) * G)
- Extra working space: O(G)

## Execution

This baseline uses standard Python CPU execution and does not require
GPU hardware or GPU-specific libraries.

## Testing

Tests are provided in tests/test_baseline.py and
tests/test_alignment_scoring.py.
