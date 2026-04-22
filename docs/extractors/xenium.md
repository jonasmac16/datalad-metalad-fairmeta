# Xenium Extractor

The `fairmeta_xenium` extractor reads 10x Genomics Xenium in situ genomics output directories and extracts metadata from cell summary files and analysis outputs.

## Usage

```bash
datalad meta-extract -d . --force-dataset-level fairmeta_xenium path/to/xenium_output
```

## Extracted Metadata

| Field | Description | Ontology |
|-------|-------------|----------|
| sample_id | Sample identifier | - |
| run_name | Run name | - |
| panel_name | Gene panel name | - |
| panel_code | Panel code | - |
| cells_detected | Number of cells detected | - |
| transcripts_detected | Total transcripts detected | - |
| gene_count | Number of genes detected | - |
| mean_transcripts_per_cell | Mean transcripts per cell | - |
| median_transcripts_per_cell | Median transcripts per cell | - |
| focus_score | Focus score | - |
| density_score | Density score | - |
| cell_boundary_quality | Cell boundary quality | - |
| image_width | Image width | - |
| image_height | Image height | - |
| magnification | Magnification level | - |
| processing_date | Processing date | - |
| software_version | Software version | - |

## Example Output

```json
{
  "$schema": "https://datalad-metalad-fairmeta.github.io/schemas/xenium.schema.json",
  "schema_version": "1.0.0",
  "sample_id": "XENIUM_SAMPLE_001",
  "run_name": "Xenium_Experiment_A1",
  "panel_name": "Human_Brain_Panel",
  "panel_code": "XHB-2024",
  "cells_detected": 8500,
  "transcripts_detected": 12500000,
  "gene_count": 500,
  "mean_transcripts_per_cell": 1470,
  "median_transcripts_per_cell": 1320,
  "focus_score": 0.85,
  "density_score": 0.72,
  "cell_boundary_quality": "high",
  "image_width": 10320,
  "image_height": 14160,
  "magnification": "20x",
  "processing_date": "2024-01-15",
  "software_version": "Xenium Analyzer v2.0",
  "provenance": {
    "extractor_id": "fairmeta_xenium",
    "extractor_version": "1.0.0",
    "extraction_date": "2024-01-15T12:00:00Z"
  }
}
```

## File Detection

The extractor looks for these files in the dataset directory:

| File Pattern | Description |
|--------------|-------------|
| `cells.csv.gz` | Cell summary data |
| `analysis/summary.json` | Analysis summary |
| `analysis/cell_metrics.csv.gz` | Cell-level metrics |

## Requirements

- No additional dependencies (uses Python standard library)

## Edge Cases

- Missing cells file and analysis directory: Error raised
- Partial analysis outputs: Extracts available fields only
- Gzipped vs plain CSV: Automatically detected
- Empty summary.json: Field omitted

See [Edge Cases: Missing Files](../edge_cases/missing_files.md) for handling corrupted files.