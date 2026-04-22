# Molecular Cartography Extractor

The `fairmeta_molecular_cartography` extractor reads Resolve Bioscience Molecular Cartography data following SOPA input requirements.

## Usage

```bash
datalad meta-extract -d . --force-dataset-level fairmeta_molecular_cartography path/to/mc_output
```

## SOPA Input Files

This extractor looks for the following SOPA-compatible input files:

| File Pattern | Description | Required |
|--------------|-------------|----------|
| `{region}_results.txt` | Transcript locations (tab-separated) | Yes |
| `{region}_{channel}.tiff` | One TIFF per channel | No |

The region parameter is required to specify which region to read. Region name is found before `_results.txt` (e.g., `A2-1_results.txt` → region: `A2-1`).

## Extracted Metadata

| Field | Description | Ontology |
|-------|-------------|----------|
| results_file | Results file name | - |
| region | Region identifier | - |
| transcript_count | Number of transcripts | - |
| columns | Column names in results file | - |
| image_files | List of image files | - |
| image_count | Number of image files | - |
| channels | List of channel names | - |
| channel_count | Number of channels | - |
| image_width | Image width in pixels | - |
| image_height | Image height in pixels | - |
| image_channels | Number of channels in image | - |

## Example Output

```json
{
  "$schema": "https://datalad-metalad-fairmeta.github.io/schemas/molecular_cartography.schema.json",
  "schema_version": "1.0.0",
  "results_file": "A2-1_results.txt",
  "region": "A2-1",
  "transcript_count": 850000,
  "columns": ["gene", "x", "y", "z", "cell_id"],
  "image_files": ["A2-1_DAPI.tif", "A2-1_Cy3.tif", "A2-1_FITC.tif"],
  "image_count": 3,
  "channels": ["DAPI", "Cy3", "FITC"],
  "channel_count": 3,
  "image_width": 2048,
  "image_height": 2048,
  "image_channels": 1,
  "provenance": {
    "extractor_id": "fairmeta_molecular_cartography",
    "extractor_version": "1.0.0",
    "extraction_date": "2024-01-15T12:00:00Z"
  }
}
```

## Requirements

- `tifffile` (optional, for image metadata reading)

## Edge Cases

- No results file found: Error raised
- Region not in filename: Uses full filename prefix
- No matching image files: Lists all TIF files in directory
- Missing tifffile: Image dimensions omitted

See [Edge Cases: Missing Files](../edge_cases/missing_files.md) for handling corrupted files.