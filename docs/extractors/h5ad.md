# h5ad (AnnData) Extractor

The `fairmeta_h5ad` extractor reads AnnData h5ad files and extracts single-cell genomics metadata following scFAIR and CELLxGENE standards.

## Usage

```bash
datalad meta-extract -d . fairmeta_h5ad path/to/data.h5ad
```

## Extracted Metadata

| Field | Description | Ontology |
|-------|-------------|----------|
| cell_count | Number of cells | - |
| gene_count | Number of features/genes | - |
| organism_ontology_term_id | Species | NCBITaxon |
| tissue_ontology_term_id | Tissue of origin | UBERON |
| cell_type_ontology_term_id | Cell type annotation | CL |
| assay_ontology_term_id | Assay/technology used | EFO |
| disease_ontology_term_id | Disease state | MONDO |
| development_stage_ontology_term_id | Developmental stage | - |
| sex_ontology_term_id | Biological sex | - |
| self_reported_ethnicity_ontology_term_id | Ethnicity | - |
| obsm_keys | Keys in obsm (embeddings) | - |
| default_embedding | Default embedding name | - |
| layers | Available data layers | - |
| title | Dataset title | - |
| description | Dataset description | - |
| batch | Batch identifier | - |
| is_primary_data | Whether primary | - |
| tissue_type | Tissue type | - |
| suspension_type | Cell suspension type | - |

## Example Output

```json
{
  "$schema": "https://datalad-metalad-fairmeta.github.io/schemas/h5ad.schema.json",
  "schema_version": "1.0.0",
  "cell_count": 5000,
  "gene_count": 20000,
  "organism_ontology_term_id": {
    "id": "NCBITaxon:9606",
    "label": "Homo sapiens"
  },
  "tissue_ontology_term_id": {
    "id": "UBERON:0002113",
    "label": "kidney"
  },
  "cell_type_ontology_term_id": {
    "id": "CL:0001000",
    "label": "kidney cell"
  },
  "assay_ontology_term_id": {
    "id": "EFO:0009899",
    "label": "10x 3' v3"
  },
  "obsm_keys": ["X_umap", "X_pca"],
  "default_embedding": "X_umap",
  "layers": ["raw", "counts", "normalized"],
  "title": "Kidney Spatial Transcriptomics",
  "description": "Single-cell RNA-seq from kidney tissue",
  "provenance": {
    "extractor_id": "fairmeta_h5ad",
    "extractor_version": "1.0.0",
    "extraction_date": "2024-01-15T12:00:00Z"
  }
}
```

## Requirements

- `anndata` library

Install with: `pip install anndata`

## Ontology Mapping

The extractor supports both ontology ID formats:
- Full IDs: `NCBITaxon:9606`, `UBERON:0002113`
- Short labels: `Homo sapiens`, `kidney`

## Edge Cases

- Multiple values in ontology columns: First value used, warning logged
- Missing obsm keys: Field omitted
- Raw layer without explicit layers entry: Added automatically
- Empty h5ad file: Returns basic structure with null counts

See [Edge Cases: Missing Files](../edge_cases/missing_files.md) for handling corrupted files.