# Batch Processing with meta-conduct

Use `meta-conduct` to process multiple files efficiently.

## Process All h5ad Files

```bash
datalad meta-conduct extract_metadata \
  traverser.top_level_dir=. \
  traverser.item_type=file \
  traverser.traverse_sub_datasets=True \
  traverser.file_filter='.*\.h5ad$' \
  extractor.extractor_name=fairmeta_h5ad \
  adder.aggregate=True
```

## Process All Images

```bash
# OME-TIFF files
datalad meta-conduct extract_metadata \
  traverser.top_level_dir=. \
  traverser.item_type=file \
  traverser.file_filter='.*\.ome\.tiff$' \
  extractor.extractor_name=fairmeta_ome_tiff \
  adder.aggregate=True

# TIFF files
datalad meta-conduct extract_metadata \
  traverser.top_level_dir=. \
  traverser.item_type=file \
  traverser.file_filter='.*\.tiff$' \
  extractor.extractor_name=fairmeta_tiff \
  adder.aggregate=True
```

## With Auto-Get for Annexed Files

```bash
datalad meta-conduct extract_metadata_autoget_autodrop \
  traverser.top_level_dir=. \
  traverser.item_type=file \
  traverser.traverse_sub_datasets=True \
  traverser.file_filter='.*\.h5ad$' \
  extractor.extractor_name=fairmeta_h5ad \
  traverser.autoget_content=True \
  traverser.drop_after=False \
  adder.aggregate=True
```

## Parallel Processing

```bash
# Use multiple workers
datalad meta-conduct extract_metadata \
  traverser.top_level_dir=/data \
  traverser.item_type=file \
  traverser.traverse_sub_datasets=True \
  traverser.file_filter='.*\.h5ad$' \
  extractor.extractor_name=fairmeta_h5ad \
  adder.aggregate=True \
  --max-workers 4 \
  --processing-mode process
```

## Dry Run

```bash
# See what will be processed
datalad meta-conduct extract_metadata \
  traverser.top_level_dir=. \
  traverser.item_type=file \
  traverser.file_filter='.*\.h5ad$' \
  extractor.extractor_name=fairmeta_h5ad \
  traverser.dry_run=True
```

## Custom Pipeline

Create a pipeline file `extract_metadata.json`:

```json
{
  "provider": {
    "type": "Traverser",
    "parameters": {
      "top_level_dir": ".",
      "item_type": "file",
      "traverse_sub_datasets": true,
      "file_filter": ".*\\.h5ad$"
    }
  },
  "processors": [
    {
      "type": "Extractor",
      "parameters": {
        "extractor_name": "fairmeta_h5ad"
      }
    }
  ],
  "consumers": [
    {
      "type": "Adder",
      "parameters": {
        "aggregate": true
      }
    }
  ]
}
```

Run:

```bash
datalad meta-conduct extract_metadata.json
```
