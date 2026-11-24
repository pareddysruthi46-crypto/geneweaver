def validate_dna_sequence(sequence: str) -> str:
    """Normalize a DNA sequence and reject symbols outside A, T, G and C."""

    if not isinstance(sequence, str):
        raise TypeError("DNA sequence must be a string.")

    normalized = "".join(sequence.split()).upper()

    if not normalized:
        raise ValueError("DNA sequence cannot be empty.")

    invalid_positions = [
        (symbol, position)
        for position, symbol in enumerate(normalized, start=1)
        if symbol not in "ATGC"
    ]

    if invalid_positions:
        details = ", ".join(
            f"'{symbol}' at position {position}"
            for symbol, position in invalid_positions
        )
        raise ValueError(
            f"Invalid DNA symbol(s): {details}. "
            "Allowed symbols are A, T, G and C."
        )

    return normalized
