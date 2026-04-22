# Visium HD Extractor

The `fairmeta_visium_hd` extractor reads 10x Genomics Visium HD data directories following SOPA input requirements.

## Usage

```bash
datalad meta-extract -d . --force-dataset-level fairmeta_visium_hd path/to/visium_hd_output
```

## SOPA Input Files

This extractor looks for the following SOPA-compatible input files:

| File/Directory | Description | Required |
|----------------|-------------|----------|
| `microscope_image/` | Full-resolution microscopy image directory | Yes |
| `*.h5` | Feature matrix H5 files | No |

## Extracted Metadata

| Field | Description | Ontology |
|-------|-------------|----------|
| microscope_image_found | Whether microscope_image directory exists | - |
| microscope_image_directory | Name of the microscope image directory | - |
| microscope_image_count | Number of image files | - |
| microscope_image_file | Single image file name (if only one) | - |
| image_width | Image width in pixels | - |
| image_height | Image height in pixels | - |
| image_channels | Number of channels | - |
| h5_files | List of H5 files found | - |
| h5_file_count | Number of H5 files | - |
| feature_matrix_file | Feature matrix H5 file name | - |

## Example Output

```json
{
  "$schema": "https://datalad-metalad-fairmeta.github.io/schemas/visium_hd.schema.json",
  "schema_version": "1.0.0",
  "microscope_image_found": true,
  "microscope_image_directory": "microscope_image",
  "microscope_image_count": 1,
  "microscope_image_file": "full_image.tif",
  "image_width": 20000,
  "image_height": 20000,
  "image_channels": 3,
  "h5_file_count": 1,
  "feature_matrix_file": "feature_slice.h5",
  "provenance": {
    "extractor_id": "fairmeta_visium_hd",
    "extractor_version": "1.0.0",
    "extraction_date": "2024-01-15T12:00:00Z"
  }
}
```

## Requirements

- `tifffile` (optional, for image dimension reading)

## Edge Cases

- No microscope_image directory: Error raised
- Single image file instead of directory: Auto-detected
- Multiple H5 files: Lists all found files
- Missing tifffile: Image dimensions omitted

See [Edge Cases: Missing Files](../edge_cases/missing_files.md) for handling corrupted files.