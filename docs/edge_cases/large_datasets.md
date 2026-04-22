# Edge Case: Large Datasets

## Problem

Extracting metadata from large datasets (many files or large files) is slow, memory-intensive, or times out.

## Symptoms

```
$ datalad meta-extract -d . fairmeta_spatialdata large_dataset/
Extracting metadata... (process runs for hours)

# Eventually:
TimeoutError: Extraction timed out after 3600 seconds
```

or

```
MemoryError: Cannot allocate array of size 4.2 GB
```

## Causes

1. Processing too many files in a single command
2. Loading large files entirely into memory
3. No parallelization configured
4. Network latency for remote datasets

## Solutions

### Use Batch Processing with meta-conduct

The `meta-conduct` command provides efficient batch processing:

```bash
datalad meta-conduct extract_metadata \
  traverser.top_level_dir=. \
  traverser.item_type=file \
  extractor.extractor_name=fairmeta_ome_tiff
```

### Configure Batch Size

Limit files processed per batch:

```bash
datalad meta-conduct extract_metadata \
  traverser.top_level_dir=. \
  traverser.batch_size=100 \
  traverser.item_type=file \
  extractor.extractor_name=fairmeta_ome_tiff
```

### Enable Parallel Processing

Use multiple workers for concurrent extraction:

```bash
datalad meta-conduct extract_metadata \
  traverser.top_level_dir=. \
  traverser.item_type=file \
  traverser.num_workers=4 \
  extractor.extractor_name=fairmeta_ome_tiff
```

### Set Recursion Limits

Control directory traversal depth:

```bash
# Only process top-level and one subdirectory
datalad meta-conduct extract_metadata \
  traverser.top_level_dir=. \
  traverser.recursion_limit=2 \
  traverser.item_type=file \
  extractor.extractor_name=fairmeta_ome_tiff
```

### Selective Extraction

Process specific subdirectories instead of entire datasets:

```bash
# Extract from specific sample directories
datalad meta-extract -d . fairmeta_spatialdata sample_001/
datalad meta-extract -d . fairmeta_spatialdata sample_002/
datalad meta-extract -d . fairmeta_spatialdata sample_003/
```

### Streaming Mode

For large files, use streaming mode to avoid memory issues:

```bash
datalad meta-extract -d . fairmeta_h5ad large_file.h5ad --stream
```

## Performance Tips

| Dataset Size | Recommended Workers | Batch Size |
|-------------|---------------------|------------|
| < 100 files | 2 | 50 |
| 100-1000 files | 4 | 100 |
| > 1000 files | 8 | 200 |

### Monitor Progress

```bash
# Enable verbose logging
datalad meta-conduct extract_metadata \
  traverser.top_level_dir=. \
  traverser.verbose=true \
  traverser.item_type=file \
  extractor.extractor_name=fairmeta_ome_tiff
```

### Checkpointing

For very large datasets, use checkpointing to resume interrupted runs:

```bash
datalad meta-conduct extract_metadata \
  traverser.top_level_dir=. \
  traverser.checkpoint=true \
  traverser.checkpoint_file=.metadata_checkpoint.json \
  traverser.item_type=file \
  extractor.extractor_name=fairmeta_ome_tiff
```

## Related

- [Interactive Mode](interactive_mode.md) - For automating large-scale extraction
- [Annexed Files](annex_files.md) - For managing large files in git-annex
