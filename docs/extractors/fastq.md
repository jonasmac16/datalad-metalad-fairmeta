# FASTQ Extractor

The `fairmeta_fastq` extractor reads FASTQ sequencing files and extracts metadata from the header line following SRA (Sequence Read Archive) and ENA (European Nucleotide Archive) conventions.

## Usage

```bash
datalad meta-extract -d . fairmeta_fastq path/to/sample.fastq.gz
```

## Extracted Metadata

| Field | Description | Ontology |
|-------|-------------|----------|
| filename | Name of the FASTQ file | - |
| instrument | Sequencing instrument ID | - |
| run_id | Run identifier | - |
| lane | Flow cell lane number | - |
| sample_id | Sample identifier | - |
| study_id | Study/project identifier | - |
| library_name | Library name | - |
| flowcell | Flow cell identifier | - |
| read_number | Read pair number (1 or 2) | - |
| file_size | File size in bytes | - |

## Example Output

```json
{
  "$schema": "https://datalad-metalad-fairmeta.github.io/schemas/fastq.schema.json",
  "schema_version": "1.0.0",
  "filename": "sample_R1.fastq.gz",
  "instrument": "NB501086",
  "run_id": "203ADNT",
  "lane": 1,
  "sample_id": "HMS_IAD_123456",
  "study_id": "PRJNA123456",
  "library_name": "MyLibrary",
  "flowcell": "ADNT23",
  "read_number": 1,
  "file_size": 524288000,
  "provenance": {
    "extractor_id": "fairmeta_fastq",
    "extractor_version": "1.0.0",
    "extraction_date": "2024-01-15T12:00:00Z"
  }
}
```

## Header Format

The extractor parses FASTQ headers in the standard CASAVA/Illumina format:

```
@<instrument>:<run_id>:<flowcell>:<lane>:<tile>:<x>:<y> <read_number>:<filter_flag>:<barcode_sequence>:<sample_id> ...
```

Example:
```
@NB501086:203ADNT:ADNT23:1:0:0:0 1:N:0:HG2JKHD3:HMS_IAD_123456
```

## Requirements

- No additional dependencies (uses Python standard library)

## Edge Cases

- Non-standard header format: Only extracts available fields, missing fields omitted
- Paired-end files: Read number inferred from filename (`_1`, `_r1`, `_2`, `_r2`)
- Gzipped files: Automatically detected by `.gz` extension
- Missing sample ID: Field omitted from output
- Multi-line headers: Only first line is parsed

See [Edge Cases: Missing Files](../edge_cases/missing_files.md) for handling corrupted files.