# Edge Case: Missing Files

## Problem

The extractor cannot find the source file or directory.

## Symptoms

```
FileNotFoundError: [Errno 2] No such file or directory: 'image.ome.tiff'
```

or

```
DirectoryNotFoundError: CosMx output directory not found
```

## Causes

1. Incorrect path relative to dataset root
2. File not tracked in DataLad
3. Symlink pointing to non-existent target
4. Typos in filename

## Solutions

### Check Path

```bash
# List files in dataset
datalad status

# Find specific file
datalad ls

# Check path
ls -la path/to/file
```

### Use Absolute Paths

```bash
# Get absolute path
readlink -f path/to/file

# Use in extraction
datalad meta-extract -d . fairmeta_ome_tiff /absolute/path/to/image.ome.tiff
```

### Check Dataset Root

For dataset-level extraction, ensure you're running from the correct location:

```bash
# Navigate to dataset root
cd /path/to/dataset

# Verify
datalad status
pwd
```

### For Dataset-Level Extractors

Use `--force-dataset-level` to explicitly indicate dataset extraction:

```bash
# Correct usage
datalad meta-extract -d . --force-dataset-level fairmeta_cosmx path/to/cosmx_output/

# Check directory exists
ls -la path/to/cosmx_output/
```

### Register Missing Files

```bash
# Add file to dataset
datalad add path/to/file

# Save
datalad save -m "Added missing file"
```

## Prevention

1. Always use relative paths from dataset root
2. Verify files exist before extraction
3. Use tab completion to avoid typos
4. Keep data and dataset in sync
