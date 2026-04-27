# Merging Auto-Extracted and Curated Metadata

How to combine automatically extracted metadata with curated template data 
for complete FAIR-compliant records using the `fairmeta-merge` CLI command.

## CLI Command (Recommended)

The easiest way to merge metadata is using the built-in CLI command:

```bash
# Install the package to enable the command
pip install -e .

# Basic merge (smart preserve by default - recommended)
fairmeta-merge auto.json curated.json -o merged.json

# Explicit smart preserve (preserves all technical fields from auto)
fairmeta-merge auto.json curated.json -o merged.json --preserve-auto smart

# Preserve specific fields only
fairmeta-merge auto.json curated.json -o merged.json \
    --preserve-auto cell_count,gene_count

# No smart preserve - curated overrides everything (old behavior)
fairmeta-merge auto.json curated.json -o merged.json --preserve-auto none

# Multi-sample merge (see Multi-Sample section below)
fairmeta-merge auto.json samples.yaml -o results/
```

## Understanding Smart Merge

The CLI uses smart merging by default to preserve technical fields from auto-extracted 
metadata while allowing curated fields to override for annotation fields.

### What --preserve-auto Does

| Value | Behavior |
|-------|----------|
| `smart` (default) | Preserve ~35 technical fields from auto (cell_count, gene_count, etc.) |
| `none` | Curated overrides everything (old behavior) |
| comma-separated | Preserve only the specified fields |

### Technical Fields Preserved (Smart Mode)

When `--preserve-auto smart` (default), these fields are preserved from auto-extracted metadata:

**h5ad/AnnData:**
- `cell_count`, `gene_count`, `obsm_keys`, `layers`, `default_embedding`, `batch`

**Xenium:**
- `transcript_count`, `transcript_columns`, `morphology_width`, `morphology_height`,
  `morphology_channels`, `cells_detected`, `gene_count`, `transcripts_detected`

**SpatialData:**
- `spatialdata_version`, `element_types`, `element_counts`, `coordinate_systems`,
  `images`, `labels`, `points`, `shapes`, `tables`

**TIFF/OME-TIFF:**
- `width`, `height`, `bits_per_sample`, `samples_per_pixel`, `pixel_type`,
  `dimension_order`, `channel_count`, `rgb_channels`, `pixel_size`

**FASTQ:**
- `read_count`, `quality_scores`, `read_lengths`, `read_number`, `sequence_length`

### What It Does

The CLI command automatically:
1. Reads both auto-extracted and curated JSON files
2. Merges them with smart field preservation
3. Adds provenance tracking (`_field_sources`) showing which source each field came from
4. Writes the output file
5. Runs `datalad add` and `datalad save` (unless `--no-save` is specified)

### Output Example

The merged output includes a `_field_sources` field for provenance:

```json
{
  "$schema": "https://datalad-metalad-fairmeta.github.io/schemas/h5ad.schema.json",
  "cell_count": 5000,
  "gene_count": 20000,
  "organism_ontology_term_id": {"id": "NCBITaxon:9606", "label": "Homo sapiens"},
  "disease_ontology_term_id": {"id": "MONDO:0004992", "label": "colorectal carcinoma"},
  "title": "My Study",
  "_field_sources": {
    "cell_count": "auto",
    "gene_count": "auto",
    "organism_ontology_term_id": "curated",
    "disease_ontology_term_id": "curated",
    "title": "curated"
  }
}
```

## Why Merge?

| Source | What It Provides |
|--------|----------------|
| Auto-extractors | cell_count, gene_count, image dimensions, quality scores |
| Templates | ontology terms, disease state, creators, licenses |

Merging gives you the best of both: technical metrics + curated annotations.

## Quick Start

### Step 1: Run Both Extractions

```bash
# Auto-extract from data files
datalad meta-extract -d . fairmeta_h5ad data.h5ad > auto.json

# Curated metadata from template
datalad meta-extract -d . --force-dataset-level fairmeta_manual \
    config dataset_metadata.yaml > curated.json
```

### Step 2: Merge with CLI

```bash
# Smart merge with auto-commit (recommended!)
fairmeta-merge auto.json curated.json -o merged.json
```

The merged file will be automatically added and committed to git.

## Multi-Sample Merge

For datasets with multiple samples, use the samples.yaml format:

```bash
# Multi-sample merge
fairmeta-merge auto.json samples.yaml -o results/
```

### Samples.yaml Format

```yaml
samples:
  - sample_id: "sample_001"
    donor_id: "donor_001"
    tissue_ontology_term_id:
      id: "UBERON:0002114"
      label: "liver"
    disease_ontology_term_id:
      id: "PATO:0000461"
      label: "normal"

  - sample_id: "sample_002"
    donor_id: "donor_002"
    tissue_ontology_term_id:
      id: "UBERON:0002114"
      label: "liver"
    disease_ontology_term_id:
      id: "MONDO:0004992"
      label: "colorectal carcinoma"
```

### Output

The CLI creates a directory with individual JSON files:

```
results/
├── sample_001.json    # Auto base + sample_001 overrides
├── sample_002.json    # Auto base + sample_002 overrides
└── _merged_manifest.json  # Index of all samples
```

Each sample file contains the merged metadata for that sample.

## Command Reference

```
fairmeta-merge AUTO_FILE [CURATED_FILE] -o OUTPUT [OPTIONS]

Arguments:
  AUTO_FILE          JSON file from auto-extractor (required)
  CURATED_FILE       JSON/YAML file from templates (required for basic merge,
                    use samples.yaml for multi-sample)

Options:
  -o, --output FILE          Output file or directory
  --preserve-auto TEXT        smart=all technical (default), none=curated overrides,
                             or comma-separated list (default: smart)
  --add-provenance         Add field source tracking (default: True)
  --no-provenance         Skip provenance tracking
  --no-save             Skip datalad add/save
  -m, --message TEXT    Commit message (default: "Merged auto-extracted 
                             and curated metadata")

Examples:
  # Basic smart merge
  fairmeta-merge auto.json curated.json -o merged.json

  # Preserve specific fields
  fairmeta-merge auto.json curated.json -o merged.json \
      --preserve-auto cell_count,gene_count

  # No smart preserve (old behavior)
  fairmeta-merge auto.json curated.json -o merged.json --preserve-auto none

  # Multi-sample
  fairmeta-merge auto.json samples.yaml -o results/

  # Without auto-commit
  fairmeta-merge auto.json curated.json -o merged.json --no-save
```

## Validation

After merging, verify the required fields are present:

```bash
# Check merged.json has required fields
python -c "
import json
with open('merged.json') as f:
    meta = json.load(f)

required = ['\$schema', 'schema_version', 'organism_ontology_term_id', 'assay_ontology_term_id']
missing = [r for r in required if r not in meta]
if missing:
    print(f'WARNING: Missing fields: {missing}')
else:
    print('Validation PASSED')
"
```

## Common Issues

| Issue | Solution |
|-------|----------|
| Missing ontology terms | Check template fields are filled |
| Empty cell_count | Auto-extraction may have failed |
| Schema mismatch | Ensure schema URLs match |

## Next Steps

- [Quick Start](quickstart.md) - Basic template usage
- [Examples](examples.md) - Liver-specific examples  
- [Ontology Reference](ontology.md) - Find correct ontology terms