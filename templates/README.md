# Metadata Templates

Templates for recording FAIR-compliant metadata that cannot be automatically 
extracted from scientific data files.

## Purpose

These templates capture **curated metadata** that requires human expertise:

- **Ontology terms** - Require expert knowledge to assign
- **Sample relationships** - Link samples to donors/tissues  
- **Disease state** - Requires pathology assessment
- **Creator information** - Who generated the data
- **License & terms** - Legal metadata

## Files

| File | Purpose |
|------|---------|
| `dataset_metadata.yaml.template` | Dataset-level metadata |
| `samples.yaml.template` | Per-sample metadata |

## Quick Start

### Step 1: Copy Templates

```bash
# Copy to your dataset directory
cp templates/dataset_metadata.yaml.template ./dataset_metadata.yaml
cp templates/samples.yaml.template ./samples.yaml
```

### Step 2: Edit the Files

Open `dataset_metadata.yaml` and fill in your dataset's information.

Open `samples.yaml` and add one entry per sample.

### Step 3: Run Extraction

```bash
# Extract with curated metadata
datalad meta-extract -d . --force-dataset-level fairmeta_manual \
    config dataset_metadata.yaml
```

## Understanding Auto-Extraction vs Manual Entry

### What Extractors Auto-Extract

| Data Type | Auto-Extracted Fields |
|-----------|---------------------|
| h5ad (AnnData) | cell_count, gene_count, obsm_keys, layers |
| Xenium | cells_detected, transcripts, gene panel |
| SpatialData | element_types, element_counts |
| FASTQ | read_count, quality scores |
| OME-TIFF | pixel dimensions, channel count |

### What Requires Manual Entry

| Field | Why Manual Required |
|-------|-------------------|
| `organism_ontology_term_id` | Not always in raw data |
| `assay_ontology_term_id` | May not be standardized |
| `disease_ontology_term_id` | Requires pathology expertise |
| `cell_type_ontology_term_id` | Requires annotation |
| `creators` | Attribution data |
| `license` | Legal terms |

## Merging Auto + Curated Metadata

See `docs/templates/merging.md` for detailed instructions on how to combine 
auto-extracted metadata with curated templates.

## Ontology Reference

See `docs/templates/ontology.md` for complete list of ontology terms, including 
liver-specific terms for your samples.

## Examples

See `docs/templates/examples.md` for liver-specific examples (healthy liver, CRC 
metastasis, HCC, gallbladder carcinoma).

## Documentation

For full documentation, see:

- [Templates Overview](../docs/templates.md)
- [Quick Start Guide](../docs/templates/quickstart.md)
- [Merging Guide](../docs/templates/merging.md)
- [Ontology Reference](../docs/templates/ontology.md)

## Troubleshooting

### Missing Required Fields

- `$schema` must exactly match the schema URL
- `schema_version` must be "1.0.0"
- `title` is required for manual schema

### Invalid Ontology Terms

- Check CURIEs match format: `PREFIX:ID` (e.g., `NCBITaxon:9606`)
- Use the Ontology Reference for valid terms
- Verify at: https://www.ebi.ac.uk/ols4/

## Support

- Issues: https://github.com/datalad/datalad-metalad-fairmeta/issues
- Docs: https://datalad-metalad-fairmeta.readthedocs.io/