# Hyperion Extractor

The `fairmeta_hyperion` extractor reads Fluidigm Hyperion imaging data following SOPA input requirements.

## Usage

```bash
datalad meta-extract -d . --force-dataset-level fairmeta_hyperion path/to/hyperion_output
```

## SOPA Input Files

This extractor looks for the following SOPA-compatible input files:

| File Pattern | Description | Required |
|--------------|-------------|----------|
| `*_{channel}_001.tiff` | One TIFF per channel | Yes |

Naming convention: `{something}_{channel_name}_001.tiff` where channel name is extracted from position [1] in filename split by `_`.

## Extracted Metadata

| Field | Description | Ontology |
|-------|-------------|----------|
| image_count | Number of TIF files | - |
| channel_naming_pattern | Expected naming pattern | - |
| channels | List of channel names | - |
| channel_count | Number of channels | - |
| sample_file | Sample file name | - |
| image_width | Image width in pixels | - |
| image_height | Image height in pixels | - |
| image_channels | Number of channels in image | - |

## Example Output

```json
{
  "$schema": "https://datalad-metalad-fairmeta.github.io/schemas/hyperion.schema.json",
  "schema_version": "1.0.0",
  "image_count": 36,
  "channel_naming_pattern": "{prefix}_{channel}_001.tiff",
  "channels": ["DAPI", "Cy3", "FITC", "Alexa488", "Alexa594"],
  "channel_count": 5,
  "sample_file": "sample_DAPI_001.tiff",
  "image_width": 1024,
  "image_height": 1024,
  "image_channels": 1,
  "provenance": {
    "extractor_id": "fairmeta_hyperion",
    "extractor_version": "1.0.0",
    "extraction_date": "2024-01-15T12:00:00Z"
  }
}
```

## Channel Extraction

The extractor parses channel names from filenames:

Example filenames:
- `sample_DAPI_001.tiff` → channel: DAPI
- `sample_Cy3_001.tiff` → channel: Cy3
- `sample_FITC_001.tiff` → channel: FITC

The channel is extracted from the second part of the filename when split by `_`.

## Requirements

- `tifffile` (optional, for image metadata reading)

## Edge Cases

- No TIF files found: Error raised
- Files not matching `*_001.tiff` pattern: Uses first available TIF
- Missing tifffile: Image dimensions omitted

See [Edge Cases: Missing Files](../edge_cases/missing_files.md) for handling corrupted files.