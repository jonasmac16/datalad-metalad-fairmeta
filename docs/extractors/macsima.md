# MACSima Extractor

The `fairmeta_macsima` extractor reads Bruker MACSima imaging data following SOPA input requirements.

## Usage

```bash
datalad meta-extract -d . --force-dataset-level fairmeta_macsima path/to/macsima_output
```

## SOPA Input Files

This extractor looks for the following SOPA-compatible input files:

| File Pattern | Description | Required |
|--------------|-------------|----------|
| `*.tif` | Multi-channel TIF images | Yes |

Two formats are supported:
- **Standard OME-TIF**: Channel names from OME metadata
- **Non-standard**: Files with `A-` in name - channel names from antibody identifiers in filename pattern: `_A-{antibody}_C-{channel}.tif`

## Extracted Metadata

| Field | Description | Ontology |
|-------|-------------|----------|
| image_count | Number of TIF files | - |
| sample_file | Sample file name | - |
| format | Data format (ome-tiff or non-standard) | - |
| image_width | Image width in pixels | - |
| image_height | Image height in pixels | - |
| samples_per_pixel | Samples per pixel | - |
| ome_metadata_available | Whether OME metadata is available | - |
| non_standard_files | Number of non-standard format files | - |
| antibodies | List of antibody names | - |
| antibody_count | Number of unique antibodies | - |
| channels | List of channel numbers | - |
| channel_count | Number of channels | - |

## Example Output

```json
{
  "$schema": "https://datalad-metalad-fairmeta.github.io/schemas/macsima.schema.json",
  "schema_version": "1.0.0",
  "image_count": 50,
  "sample_file": "sample_A-DAPI_C-001.tif",
  "format": "non-standard",
  "image_width": 2048,
  "image_height": 2048,
  "non_standard_files": 50,
  "antibodies": ["DAPI", "Cy3", "FITC", "Alexa488"],
  "antibody_count": 4,
  "channels": ["1", "2", "3", "4"],
  "channel_count": 4,
  "provenance": {
    "extractor_id": "fairmeta_macsima",
    "extractor_version": "1.0.0",
    "extraction_date": "2024-01-15T12:00:00Z"
  }
}
```

## Channel Naming Extraction

The extractor parses antibody names from filenames using regex pattern `_A-([^_]+)`:

Example filenames:
- `sample_A-DAPI_C-001.tif` → antibody: DAPI, channel: 1
- `sample_A-Cy3_C-002.tif` → antibody: Cy3, channel: 2
- `sample_A-FITC_C-003.tif` → antibody: FITC, channel: 3

## Requirements

- `tifffile` (optional, for image metadata reading)

## Edge Cases

- No TIF files found: Error raised
- Missing tifffile: Image dimensions omitted
- Mixed formats: Reports dominant format
- Duplicate antibodies: Gets unique count

See [Edge Cases: Missing Files](../edge_cases/missing_files.md) for handling corrupted files.