# Templates Quick Start

A step-by-step guide to using metadata templates with your data.

## Prerequisites

- datalad-metalad-fairmeta installed
- Dataset with data files ready for extraction
- YAML editor (or any text editor)

## Step 1: Prepare Your Dataset

```bash
# Navigate to your dataset
cd /path/to/your/dataset

# Verify data files exist
ls -la
```

## Step 2: Copy Templates

```bash
# Copy templates from package
cp /path/to/datalad-metalad-fairmeta/templates/dataset_metadata.yaml.template ./dataset_metadata.yaml
cp /path/to/datalad-metalad-fairmeta/templates/samples.yaml.template ./samples.yaml

# Or use relative path from dataset
cp templates/dataset_metadata.yaml.template ./dataset_metadata.yaml
cp templates/samples.yaml.template ./samples.yaml
```

## Step 3: Edit Dataset Metadata

Open `dataset_metadata.yaml` in your editor:

```yaml
# Required fields (must be present)
$schema: "https://datalad-metalad-fairmeta.github.io/schemas/manual.schema.json"
schema_version: "1.0.0"
title: "Your Study Title"

# Recommended fields (fill in)
organism_ontology_term_id:
  id: "NCBITaxon:9606"
  label: "Homo sapiens"

disease_ontology_term_id:
  id: "PATO:0000461"
  label: "normal"

# ... add more fields as needed
```

## Step 4: Edit Sample Metadata (if multi-sample)

Open `samples.yaml` and add your samples:

```yaml
samples:
  - sample_id: "sample_001"
    donor_id: "donor_001"
    disease_ontology_term_id:
      id: "PATO:0000461"
      label: "normal"
  - sample_id: "sample_002"
    donor_id: "donor_002"
    disease_ontology_term_id:
      id: "MONDO:0004992"
      label: "colorectal carcinoma"
```

## Step 5: Run Extraction

### Option A: Config File Mode (Recommended)

```bash
# Extract dataset metadata from config
datalad meta-extract -d . --force-dataset-level fairmeta_manual \
    config dataset_metadata.yaml > dataset_metadata.json

# If using samples.yaml for sample metadata
datalad meta-extract -d . --force-dataset-level fairmeta_manual \
    config samples.yaml > sample_metadata.json
```

### Option B: Interactive Mode

```bash
# Instead of config file, use interactive prompts
datalad meta-extract -d . --force-dataset-level fairmeta_manual \
    interactive true
```

## Step 6: Verify Output

```bash
# Check the extracted metadata
cat dataset_metadata.json | python -m json.tool | less

# Look for your fields:
# - title
# - organism_ontology_term_id
# - disease_ontology_term_id
```

## Step 7: Merge with Auto-Extracted Data (Optional)

For complete metadata, combine auto-extracted + curated:

```bash
# Auto-extract from your data files
datalad meta-extract -d . fairmeta_h5ad data.h5ad > h5ad_auto.json

# Your curated metadata
datalad meta-extract -d . --force-dataset-level fairmeta_manual \
    config dataset_metadata.yaml > curated.json

# Merge (curated overrides auto for overlapping fields)
python merge_metadata.py h5ad_auto.json curated.json > complete_metadata.json
```

See [Merging Guide](merging.md) for the merge script.

## Complete Example

```bash
# Full workflow for h5ad data with liver samples

# 1. Copy and edit templates
cp templates/dataset_metadata.yaml.template dataset_metadata.yaml
# Edit dataset_metadata.yaml with your study info

# 2. Run auto-extraction
datalad meta-extract -d . fairmeta_h5ad data.h5ad > auto.json

# 3. Run manual extraction
datalad meta-extract -d . --force-dataset-level fairmeta_manual \
    config dataset_metadata.yaml > manual.json

# 4. Merge results
python -c "
import json
auto = json.load(open('auto.json'))
manual = json.load(open('manual.json'))
# Merge: manual metadata enhances/completes auto
result = {**auto.get('metadata', {}), **manual.get('metadata', {})}
print(json.dumps(result, indent=2))
" > complete_metadata.json
```

## Next Steps

- [Examples](examples.md) - See liver-specific examples
- [Ontology](ontology.md) - Find the right ontology terms
- [Merging](merging.md) - Advanced merge strategies