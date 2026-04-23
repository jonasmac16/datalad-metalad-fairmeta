# Manual/Interactive Extractor

The `fairmeta_manual` extractor allows manual metadata entry via interactive prompts or configuration files.

## Usage Modes

### Interactive Mode

```bash
datalad meta-extract -d . --force-dataset-level fairmeta_manual \
  interactive true \
  schema h5ad
```

This will prompt you for metadata fields:

```
============================================================
FAIR Metadata Entry - Interactive Mode
============================================================
Dataset: /data/my-study
Schema: h5ad
============================================================

Required Fields:
Title: My Spatial Transcriptomics Study

Biological Context (optional but recommended):
Organism (NCBITaxon): NCBITaxon:9606
Tissue (UBERON): UBERON:0002113
Cell Type (CL): 
Assay/Technology (EFO): EFO:0009899
Disease State (MONDO): PATO:0000461

Optional Fields:
Description: Spatial transcriptomics of kidney tissue
Donor ID: donor_001
```

### Config File Mode

```bash
datalad meta-extract -d . --force-dataset-level fairmeta_manual \
  config metadata.yaml \
  schema h5ad
```

> **Tip**: Use the [metadata templates](../templates.md) for ready-made YAML files with liver-specific examples.

Example `metadata.yaml`:

```yaml
title: My Spatial Transcriptomics Study
organism_ontology_term_id:
  id: NCBITaxon:9606
  label: Homo sapiens
tissue_ontology_term_id:
  id: UBERON:0002113
  label: kidney
assay_ontology_term_id:
  id: EFO:0009899
  label: 10x 3' v3
description: Spatial transcriptomics of kidney tissue
donor_id: donor_001
keywords:
  - spatial transcriptomics
  - kidney
  - single-cell
```

### Defaults Mode

Uses schema defaults for all fields:

```bash
datalad meta-extract -d . --force-dataset-level fairmeta_manual \
  defaults true \
  schema h5ad
```

## Parameters

| Parameter | Description | Values |
|-----------|-------------|--------|
| `interactive` | Enable interactive prompts | `true`/`false` |
| `config` | Path to YAML/JSON config file | File path |
| `schema` | Schema to use for validation | `h5ad`, `cosmx`, `xenium`, etc. |
| `defaults` | Use schema defaults | `true`/`false` |

## Supported Schemas

- `h5ad` - scFAIR/CELLxGENE metadata
- `cosmx` - CosMx metadata
- `xenium` - Xenium metadata
- `visium_hd` - Visium HD metadata
- `merscope` - MERSCOPE metadata
- `macsima` - MACSima metadata
- `phenocycler` - PhenoCycler metadata
- `molecular_cartography` - Molecular Cartography metadata
- `hyperion` - Hyperion metadata
- `spatialdata` - SpatialData metadata
- `fastq` - FASTQ metadata
- `manual` - Generic manual entry
- `base` - Base schema only

## Output

```json
{
  "$schema": "https://datalad-metalad-fairmeta.github.io/schemas/manual.schema.json",
  "schema_version": "1.0.0",
  "title": "My Spatial Transcriptomics Study",
  "organism_ontology_term_id": {
    "id": "NCBITaxon:9606",
    "label": "Homo sapiens"
  },
  "tissue_ontology_term_id": {
    "id": "UBERON:0002113",
    "label": "kidney"
  },
  "assay_ontology_term_id": {
    "id": "EFO:0009899",
    "label": "10x 3' v3"
  },
  "provenance": {
    "extractor_id": "fairmeta_manual",
    "extractor_version": "1.0.0",
    "extraction_date": "2024-01-15T12:00:00Z"
  }
}
```

## Use Cases

1. **Non-standard formats**: Add metadata for formats without dedicated extractors
2. **Augment automated extraction**: Fill in missing ontology terms
3. **Study-level metadata**: Add project-level information
4. **Quality control**: Verify and correct extracted metadata
