# Spatial Omics Workflow

Complete workflow for spatial transcriptomics data from acquisition to publication.

## Scenario

You have a Visium experiment with:
- Raw images (TIFF)
- h5ad counts matrix + spatial data
- Associated metadata

## Step 1: Create Dataset

```bash
datalad create visium-experiment
cd visium-experiment
```

## Step 2: Add Raw Data

```bash
# Add tissue image
datalad add tissue_image.tiff

# Add counts matrix and spatial data
datalad add h5ad_output/

# Save
datalad save -m "Added raw Visium data"
```

## Step 3: Extract Image Metadata

```bash
datalad meta-extract -d . fairmeta_tiff tissue_image.tiff | datalad meta-add -d . -
```

## Step 4: Extract h5ad Metadata

```bash
# Find all h5ad files
find . -name "*.h5ad"

# Extract metadata
datalad meta-extract -d . fairmeta_h5ad h5ad_output/filtered_feature_bc_matrix.h5 | \
  datalad meta-add -d . -
```

## Step 5: Add Study-Level Metadata

```bash
# Interactive metadata entry
datalad meta-extract -d . --force-dataset-level fairmeta_manual \
  interactive true \
  schema h5ad
```

## Step 6: Save All Metadata

```bash
datalad save -m "Added fairmeta metadata"
```

## Step 7: Export for Sharing

```bash
# Export all metadata
datalad meta-dump -d . -r > metadata.jsonl

# Create summary
datalad meta-dump -d . -r | jq -c '{type, extractor: .extractor_name}' | sort | uniq -c
```

## Result Summary

Your dataset now contains:

| File | Metadata Type |
|------|--------------|
| `tissue_image.tiff` | TIFF technical metadata |
| `filtered_feature_bc_matrix.h5` | scRNA-seq counts + annotations |
| Study-level | Ontology terms, title, description |

## Query Examples

```bash
# Get all image metadata
datalad meta-dump -d . -r | jq 'select(.type == "file" and (.extractor_name | startswith("fairmeta_tiff")))'

# Get all h5ad data
datalad meta-dump -d . -r | jq 'select(.extractor_name == "fairmeta_h5ad")'

# Get cell counts
datalad meta-dump -d . -r | jq 'select(.immediate_data.cell_count != null) | {file: .datalad_result_dict.path, cells: .immediate_data.cell_count}'
```
