# PhenoCycler Extractor

The `fairmeta_phenocycler` extractor reads Akoya PhenoCycler imaging data following SOPA input requirements.

## Usage

```bash
datalad meta-extract -d . --force-dataset-level fairmeta_phenocycler path/to/phenocycler_output
```

## SOPA Input Files

This extractor looks for the following SOPA-compatible input files:

| File Pattern | Description | Required |
|--------------|-------------|----------|
| `.qptiff` | Multi-channel QuPath-exported TIFF | Yes* |
| `.tif` | ImageJ/Fiji exported multi-channel TIFF | Yes* |

*At least one of these formats must be present.

## Channel Extraction

- **.qptiff**: XML metadata with biomarker names
- **.tif**: IJMetadata tag "Labels" for channel names

## Extracted Metadata

| Field | Description | Ontology |
|-------|-------------|----------|
| image_file | Image file name | - |
| format | Image format (qptiff or tif) | - |
| image_width | Image width in pixels | - |
| image_height | Image height in pixels | - |
| channels | Number of channels | - |
| qptiff_metadata_available | Whether QPTIFF metadata is available | - |
| channel_names | List of channel/b biomarker names | - |
| channel_count | Number of channels | - |
| imagej_metadata_available | Whether ImageJ metadata is available | - |

## Example Output

```json
{
  "$schema": "https://datalad-metalad-fairmeta.github.io/schemas/phenocycler.schema.json",
  "schema_version": "1.0.0",
  "image_file": "sample.qptiff",
  "format": "qptiff",
  "image_width": 2048,
  "image_height": 2048,
  "channels": 60,
  "qptiff_metadata_available": true,
  "channel_names": ["DAPI", "CD3", "CD4", "CD8", "PanCK", ...],
  "channel_count": 60,
  "provenance": {
    "extractor_id": "fairmeta_phenocycler",
    "extractor_version": "1.0.0",
    "extraction_date": "2024-01-15T12:00:00Z"
  }
}
```

## Requirements

- `tifffile` (optional, for image metadata reading)

## Edge Cases

- No image file found: Error raised
- Multiple .qptiff files: Uses first one found
- Missing channel metadata: Field omitted
- Missing tifffile: Image dimensions omitted

See [Edge Cases: Missing Files](../edge_cases/missing_files.md) for handling corrupted files.