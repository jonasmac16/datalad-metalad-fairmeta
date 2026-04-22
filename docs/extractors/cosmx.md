# CosMx Extractor

The `fairmeta_cosmx` extractor reads NanoString CosMx spatial molecular imaging output directories and extracts metadata from CSV files (metadata, FOV positions, expression matrix, cell segmentation).

## Usage

```bash
datalad meta-extract -d . --force-dataset-level fairmeta_cosmx path/to/cosmx_output
```

## Extracted Metadata

| Field | Description | Ontology |
|-------|-------------|----------|
| run_name | Run name | - |
| run_id | Run identifier | - |
| tissue_name | Tissue sample name | - |
| slide_id | Slide identifier | - |
| panel_name | Protein/gene panel name | - |
| panel_version | Panel version | - |
| assay_type | Assay type | - |
| processing_date | Processing date | - |
| software_version | Software version | - |
| fov_count | Number of fields of view | - |
| cell_count | Number of cells | - |
| gene_count | Number of genes | - |

## Example Output

```json
{
  "$schema": "https://datalad-metalad-fairmeta.github.io/schemas/cosmx.schema.json",
  "schema_version": "1.0.0",
  "run_name": "CosMx_Experiment_01",
  "run_id": "RUN-2024-001",
  "tissue_name": "Human_Lung_Tumor",
  "slide_id": "SLIDE-A12345",
  "panel_name": "Human_Protein_69_Panel",
  "panel_version": "2.0",
  "assay_type": "SMI",
  "processing_date": "2024-01-15",
  "software_version": "CosMxAnalysis_v1.5",
  "fov_count": 500,
  "cell_count": 15000,
  "gene_count": 1000,
  "provenance": {
    "extractor_id": "fairmeta_cosmx",
    "extractor_version": "1.0.0",
    "extraction_date": "2024-01-15T12:00:00Z"
  }
}
```

## File Detection

The extractor looks for these files in the dataset directory:

| File Pattern | Description |
|--------------|-------------|
| `*_metadata_file.csv` | Run metadata |
| `*_fov_positions_file.csv` | Field of view positions |
| `*_exprMat_file.csv` | Expression matrix |
| `cell_segmentation.csv` | Cell segmentation data |

## Requirements

- No additional dependencies (uses Python standard library)

## Edge Cases

- Missing metadata file: Error raised
- Partial file availability: Extracts available fields only
- Non-standard column names: Field omitted, warning logged
- Empty files: Field count is null

See [Edge Cases: Missing Files](../edge_cases/missing_files.md) for handling corrupted files.