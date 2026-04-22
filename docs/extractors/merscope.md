# MERSCOPE Extractor

The `fairmeta_merscope` extractor reads Vizgen MERSCOPE data directories following SOPA input requirements.

## Usage

```bash
datalad meta-extract -d . --force-dataset-level fairmeta_merscope path/to/merscope_output
```

## SOPA Input Files

This extractor looks for the following SOPA-compatible input files:

| File/Directory | Description | Required |
|----------------|-------------|----------|
| `detected_transcripts.csv` | Transcript locations and names | Yes |
| `images/` | Directory containing microscopy images | No |
| `images/micron_to_mosaic_pixel_transform.csv` | Affine transformation matrix | No |

## Extracted Metadata

| Field | Description | Ontology |
|-------|-------------|----------|
| transcript_file | Name of transcript file | - |
| transcript_count | Number of transcripts | - |
| transcript_columns | Column names in transcript file | - |
| images_directory | Name of images directory | - |
| image_count | Number of image files | - |
| sample_image | Sample image file name | - |
| transform_file | Transform matrix file name | - |
| transform_matrix | Transformation matrix values | - |
| cell_boundaries_file | Cell boundaries file name | - |
| cells_file | Cells file name | - |
| cell_count | Number of cells | - |

## Example Output

```json
{
  "$schema": "https://datalad-metalad-fairmeta.github.io/schemas/merscope.schema.json",
  "schema_version": "1.0.0",
  "transcript_file": "detected_transcripts.csv",
  "transcript_count": 1500000,
  "transcript_columns": ["gene", "x", "y", "z", "quality"],
  "images_directory": "images",
  "image_count": 5,
  "sample_image": "DAPI.tif",
  "transform_file": "micron_to_mosaic_pixel_transform.csv",
  "provenance": {
    "extractor_id": "fairmeta_merscope",
    "extractor_version": "1.0.0",
    "extraction_date": "2024-01-15T12:00:00Z"
  }
}
```

## Requirements

- No additional dependencies (uses Python standard library)

## Edge Cases

- No detected_transcripts.csv: Error raised
- No images directory: Field omitted
- No transform file: Field omitted

See [Edge Cases: Missing Files](../edge_cases/missing_files.md) for handling corrupted files.