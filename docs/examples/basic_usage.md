# Basic Usage Examples

## Extract from OME-TIFF

```bash
# Extract metadata from a single OME-TIFF file
datalad meta-extract -d . fairmeta_ome_tiff image.ome.tiff
```

Output:
```json
{
  "extractor_name": "fairmeta_ome_tiff",
  "extraction_success": true,
  "immediate_data": {
    "$schema": "https://...",
    "Image": {
      "Name": "sample",
      "Pixels": {
        "SizeX": 2048,
        "SizeY": 2048,
        "SizeC": 5
      }
    }
  }
}
```

## Extract from h5ad

```bash
# Extract metadata from AnnData file
datalad meta-extract -d . fairmeta_h5ad sample.h5ad
```

## Extract from Directory

```bash
# Extract dataset-level metadata
datalad meta-extract -d . --force-dataset-level fairmeta_cosmx

# Or with explicit path
datalad meta-extract -d . --force-dataset-level fairmeta_cosmx cosmx_output/
```

## Add Metadata to Dataset

```bash
# Extract and add in one step
datalad meta-extract -d . fairmeta_h5ad sample.h5ad | datalad meta-add -d . -
```

## View Metadata

```bash
# Pretty print
datalad meta-dump -d . -r | jq .

# Filter by extractor
datalad meta-dump -d . -r | jq 'select(.extractor_name == "fairmeta_h5ad")'

# Count records
datalad meta-dump -d . -r | jq -s 'length'
```

## Export Metadata

```bash
# Export all metadata to JSON Lines
datalad meta-dump -d . -r > metadata.jsonl

# Export filtered
datalad meta-dump -d . -r | jq 'select(.type == "file")' > files_metadata.jsonl
```
