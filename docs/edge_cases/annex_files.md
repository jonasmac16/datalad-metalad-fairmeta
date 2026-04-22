# Edge Case: Annexed Files

## Problem

File content is not available locally (stored in git-annex).

## Symptoms

```
FileNotFoundError: image.ome.tiff
```

or

```
PermissionError: Cannot open 'image.ome.tiff' for reading
```

## Causes

1. File is stored in git-annex (not Git)
2. Content not downloaded (`datalad get` not run)
3. Annex location unavailable

## Solutions

### Get Content

```bash
# Get single file
datalad get path/to/file.ome.tiff

# Get all files matching pattern
datalad get "*.ome.tiff"

# Get entire directory
datalad get path/to/directory/

# Get with recursive
datalad get -r path/to/data/
```

### Configure Extractors to Work with Annexed Files

Some extractors can work with annexed files by getting content automatically:

```bash
# Get content before extraction
datalad get image.ome.tiff
datalad meta-extract -d . fairmeta_ome_tiff image.ome.tiff

# Or use meta-conduct which handles this
datalad meta-conduct extract_metadata \
  traverser.top_level_dir=. \
  traverser.item_type=file \
  extractor.extractor_name=fairmeta_ome_tiff \
  traverser.autoget_content=True \
  traverser.drop_after=False
```

### Check File Status

```bash
# Check if file is annexed
datalad status

# Get file info
datalad file-spec info path/to/file

# Check annex status
git annex info
```

### Drop Content After Extraction

To save space after processing:

```bash
# Get, extract, drop
datalad get image.ome.tiff
datalad meta-extract -d . fairmeta_ome_tiff image.ome.tiff | datalad meta-add -d . -
datalad drop path/to/image.ome.tiff
```

## Prevention

1. Use `--no-annex` option when adding files to avoid annexing large files
2. Keep content available for active projects
3. Use `datalad unlock` for files you need to modify
