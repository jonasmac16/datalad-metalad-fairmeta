# Metalad Integration Guide

This guide explains how datalad-metalad-fairmeta integrates with DataLad Metalad.

## Overview

Metalad provides metadata extraction, aggregation, and reporting commands. fairmeta extractors plug into this framework to produce standardized FAIR metadata.

## Metalad Commands

### meta-extract

Extract metadata from files or datasets:

```bash
# File-level extraction
datalad meta-extract -d . fairmeta_ome_tiff image.ome.tiff

# Dataset-level extraction
datalad meta-extract -d . --force-dataset-level fairmeta_cosmx

# With parameters
datalad meta-extract -d . --force-dataset-level fairmeta_manual \
  interactive true \
  schema h5ad
```

### meta-add

Add extracted metadata to the dataset:

```bash
# From pipe
datalad meta-extract -d . fairmeta_h5ad data.h5ad | datalad meta-add -d . -

# From file
datalad meta-extract -d . fairmeta_h5ad data.h5ad > metadata.json
datalad meta-add -d . metadata.json

# Batch add
cat metadata_list.txt | while read f; do
  datalad meta-extract -d . fairmeta_ome_tiff "$f" | datalad meta-add -d . -
done
```

### meta-aggregate

Combine metadata from subdatasets:

```bash
# Aggregate subdatasets into parent
datalad meta-aggregate -d . subds1 subds2

# Recursive aggregation
datalad meta-aggregate -d . -r

# Show what will be aggregated
datalad meta-aggregate -d . subds1 subds2 --dry-run
```

### meta-dump

View stored metadata:

```bash
# All metadata
datalad meta-dump -d . -r

# Filter by extractor
datalad meta-dump -d . -r | jq 'select(.extractor_name == "fairmeta_h5ad")'

# Filter by type
datalad meta-dump -d . -r | jq 'select(.type == "dataset")'

# Export to JSON Lines
datalad meta-dump -d . -r > metadata.jsonl

# Pretty print
datalad meta-dump -d . -r | jq .
```

### meta-conduct

Batch processing pipeline:

```bash
# Extract all h5ad files
datalad meta-conduct extract_metadata \
  traverser.top_level_dir=. \
  traverser.item_type=file \
  traverser.file_filter='.*\.h5ad$' \
  extractor.extractor_name=fairmeta_h5ad \
  adder.aggregate=True
```

## Integration with Existing Workflows

### Complete Workflow Example

```bash
# 1. Create dataset
datalad create my-spatial-study
cd my-spatial-study

# 2. Add data
datalad add path/to/data/

# 3. Extract and add metadata
for f in $(find . -name "*.ome.tiff"); do
  datalad meta-extract -d . fairmeta_ome_tiff "$f" | datalad meta-add -d . -
done

for f in $(find . -name "*.h5ad"); do
  datalad meta-extract -d . fairmeta_h5ad "$f" | datalad meta-add -d . -
done

# 4. Save metadata
datalad save -m "Added fairmeta metadata"

# 5. View metadata
datalad meta-dump -d . -r | jq .

# 6. Export
datalad meta-dump -d . -r > metadata.jsonl
```

### Subdataset Workflow

```bash
# Create subdatasets
datalad create -d . experiment1
datalad create -d . experiment2

# Add data and metadata to subdatasets
datalad add -d experiment1 path/to/data1/
datalad meta-extract -d experiment1 fairmeta_h5ad data1.h5ad | datalad meta-add -d experiment1 -

datalad add -d experiment2 path/to/data2/
datalad meta-extract -d experiment2 fairmeta_h5ad data2.h5ad | datalad meta-add -d experiment2 -

# Save subdatasets
datalad save -d experiment1 -m "Added data and metadata"
datalad save -d experiment2 -m "Added data and metadata"

# Aggregate to parent
datalad meta-aggregate -d . experiment1 experiment2

# Save aggregated metadata
datalad save -m "Aggregated metadata from subdatasets"
```

## Metadata Storage

Metalad stores metadata in `.datalad/metadata/` within the Git repository. Metadata is versioned with Git, allowing you to track metadata changes over time.

## Best Practices

1. **Extract early**: Add metadata when you add data
2. **Validate**: Check for validation errors after extraction
3. **Aggregate regularly**: Keep parent datasets up-to-date
4. **Export**: Save exports for analysis and sharing
5. **Version control**: Commit metadata changes with your data
