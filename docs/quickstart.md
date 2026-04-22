# Quick Start

This guide will help you get started with datalad-metalad-fairmeta.

## Prerequisites

Make sure you have:

1. A DataLad dataset (or create one)
2. datalad-metalad installed
3. datalad-metalad-fairmeta installed

## Step 1: Create or Clone a DataLad Dataset

```bash
# Create a new dataset
datalad create my-spatial-study
cd my-spatial-study

# Or clone an existing one
datalad clone https://github.com/user/spatial-data-repo
cd spatial-data-repo
```

## Step 2: Add Your Data

```bash
# Add your spatial biology data
datalad add path/to/your/data/

# Save changes
datalad save -m "Added spatial omics data"
```

## Step 3: Extract Metadata

### Extract from a Single File

```bash
# Extract OME-TIFF metadata
datalad meta-extract -d . fairmeta_ome_tiff path/to/image.ome.tiff

# Extract h5ad metadata
datalad meta-extract -d . fairmeta_h5ad path/to/data.h5ad
```

### Extract from a Directory

```bash
# Extract CosMx metadata from a directory
datalad meta-extract -d . --force-dataset-level fairmeta_cosmx path/to/cosmx_output/

# Extract Visium HD metadata
datalad meta-extract -d . --force-dataset-level fairmeta_visium_hd path/to/visium_hd/

# Extract MERSCOPE metadata
datalad meta-extract -d . --force-dataset-level fairmeta_merscope path/to/merscope_output/
```

## Step 4: Add Metadata to Dataset

```bash
# Extract and add metadata in one step
datalad meta-extract -d . fairmeta_ome_tiff image.ome.tiff | \
  datalad meta-add -d . -
```

## Step 5: Aggregate Metadata from Subdatasets

```bash
# Create a subdataset
datalad create -d . subds1

# Add data to subdataset
datalad add -d subds1 path/to/subdata/

# Extract metadata in subdataset
datalad meta-extract -d subds1 fairmeta_h5ad data.h5ad | \
  datalad meta-add -d subds1 -

# Aggregate to parent
datalad meta-aggregate -d . subds1
```

## Step 6: View Metadata

```bash
# Dump all metadata
datalad meta-dump -d . -r

# Filter for specific extractor
datalad meta-dump -d . -r | jq 'select(.extractor_name == "fairmeta_ome_tiff")'

# Export to JSON Lines file
datalad meta-dump -d . -r > metadata.jsonl
```

## Interactive Metadata Entry

For non-standard formats or missing metadata:

```bash
# Interactive metadata entry
datalad meta-extract -d . --force-dataset-level fairmeta_manual \
  interactive true \
  schema h5ad
```

This will prompt you for:
- Title
- Organism (NCBITaxon ontology)
- Tissue (UBERON ontology)
- Cell type (Cell Ontology)
- Assay (EFO ontology)
- Disease state (MONDO/PATO ontology)

## Batch Processing with meta-conduct

Process all files of a type in your dataset:

```bash
# Extract all h5ad files
datalad meta-conduct extract_metadata \
  traverser.top_level_dir=. \
  traverser.item_type=file \
  traverser.traverse_sub_datasets=True \
  traverser.file_filter='.*\.h5ad$' \
  extractor.extractor_name=fairmeta_h5ad \
  adder.aggregate=True
```

## Next Steps

- Learn about [all extractors](extractors/index.md)
- Understand [Metalad integration](metalad/index.md)
- Explore [schema validation](schemas/index.md)
- Check out [examples](examples/index.md)
- Review [edge cases handling](edge_cases/index.md)
