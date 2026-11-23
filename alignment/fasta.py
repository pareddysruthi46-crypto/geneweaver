from dataclasses import dataclass
from pathlib import Path


@dataclass
class FastaRecord:
    """Represents one DNA record from a FASTA file."""

    record_id: str
    description: str
    sequence: str


def parse_fasta(content: str) -> list[FastaRecord]:
    """Parse one or more DNA records from FASTA text."""

    records = []
    current_id = None
    current_description = ""
    sequence_parts = []

    def save_record():
        if current_id is None:
            return

        sequence = "".join(sequence_parts).upper()

        if not sequence:
            raise ValueError(
                f"FASTA record '{current_id}' has an empty sequence."
            )

        records.append(
            FastaRecord(
                record_id=current_id,
                description=current_description,
                sequence=sequence,
            )
        )

    for line_number, raw_line in enumerate(content.splitlines(), start=1):
        line = raw_line.strip()

        if not line:
            continue

        if line.startswith(">"):
            save_record()

            header = line[1:].strip()

            if not header:
                raise ValueError(
                    f"Missing FASTA header at line {line_number}."
                )

            header_parts = header.split(maxsplit=1)
            current_id = header_parts[0]
            current_description = (
                header_parts[1] if len(header_parts) > 1 else ""
            )
            sequence_parts = []

        else:
            if current_id is None:
                raise ValueError(
                    f"Sequence found before FASTA header at line {line_number}."
                )

            sequence_line = "".join(line.split()).upper()

            invalid = set(sequence_line) - set("ATGC")

            if invalid:
                raise ValueError(
                    f"Invalid DNA character(s) at line {line_number}: "
                    f"{', '.join(sorted(invalid))}"
                )

            sequence_parts.append(sequence_line)

    save_record()

    if not records:
        raise ValueError("No FASTA records found.")

    return records


def read_fasta(file_path: str | Path) -> list[FastaRecord]:
    """Read and parse DNA records from a FASTA file."""

    content = Path(file_path).read_text(encoding="utf-8")
    return parse_fasta(content)
