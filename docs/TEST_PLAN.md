# GeneWeaver Test Plan

## 1. Purpose
This document defines the initial testing strategy for GeneWeaver, a Python application for DNA guide and target sequence processing.

## 2. Testing Strategy
- Use Python's built-in unittest framework.
- Test individual functions and data models.
- Test valid and invalid DNA sequences.
- Test guide and target sequence input handling.
- Verify alignment output when the alignment module is implemented.
- Run tests locally using Python.

## 3. Test Areas
1. Application startup
2. Sequence input validation
3. DNA sequence format
4. Alignment result data models
5. Error handling for invalid inputs

## 4. Acceptance Criteria
- Application starts without errors.
- Valid DNA sequences containing A, T, G, and C are accepted.
- Empty sequences are rejected when validation is implemented.
- Invalid DNA characters are rejected when validation is implemented.
- Alignment results contain guide and target sequence information.
- Automated tests run successfully.
- Test failures provide understandable error messages.

## 5. Test Execution
Run all tests using:

`python -m unittest discover -s tests -v`

## 6. Scope Notes
These are initial acceptance criteria. Features not yet implemented should be marked as pending rather than treated as passing.

## 7. FASTA Input Tests
- Parse a single FASTA record.
- Parse multiple FASTA records.
- Support sequences split across multiple lines.
- Convert lowercase DNA characters to uppercase.
- Read records directly from a FASTA file.
- Reject missing headers and empty sequences.
- Reject characters outside A, T, G, and C.
