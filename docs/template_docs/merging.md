# Merging Auto-Extracted and Curated Metadata

How to combine automatically extracted metadata with curated template data 
for complete FAIR-compliant records using the `fairmeta-merge` CLI command.

## CLI Command (Recommended)

The easiest way to merge metadata is using the built-in CLI command:

```bash
# Install the package to enable the command
pip install -e .

# Merge with auto-commit to git (recommended!)
fairmeta-merge auto.json curated.json -o merged.json

# Merge with custom commit message
fairmeta-merge auto.json curated.json -o merged.json -m "Added complete metadata"

# Merge without saving (just write output file)
fairmeta-merge auto.json curated.json -o merged.json --no-save
```

### What It Does

The CLI command automatically:
1. Reads both auto-extracted and curated JSON files
2. Merges them (curated fields override auto for overlaps)
3. Adds provenance tracking (`_field_sources`) showing which source each field came from
4. Writes the output file
5. Runs `datalad add` and `datalad save` (unless `--no-save` is specified)

### Output Example

The merged output includes a `_field_sources` field for provenance:

```json
{
  "$schema": "https://datalad-metalad-fairmeta.github.io/schemas/h5ad.schema.json",
  "cell_count": 5000,
  "organism_ontology_term_id": {"id": "NCBITaxon:9606", "label": "Homo sapiens"},
  "disease_ontology_term_id": {"id": "MONDO:0004992", "label": "colorectal carcinoma"},
  "title": "My Study",
  "_field_sources": {
    "cell_count": "auto",
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
# Simple merge with auto-commit
fairmeta-merge auto.json curated.json -o merged.json
```

The merged file will be automatically added and committed to git.

## Manual Merge (Alternative)

If you need more control, you can use Python directly:

```python
import json

def merge_metadata(auto_file, curated_file, output_file):
    """Merge auto-extracted + curated metadata."""
    with open(auto_file) as f:
        auto = json.load(f)
    with open(curated_file) as f:
        curated = json.load(f)
    
    auto_meta = auto.get('metadata', {})
    curated_meta = curated.get('metadata', {})
    
    # Merge: curated overrides auto for overlaps
    merged = {**auto_meta, **curated_meta}
    
    # Add provenance tracking
    merged['_field_sources'] = {
        **{k: 'auto' for k in auto_meta},
        **{k: 'curated' for k in curated_meta if k not in auto_meta}
    }
    
    with open(output_file, 'w') as f:
        json.dump(merged, f, indent=2)

merge_metadata('auto.json', 'curated.json', 'merged.json')
```

## Advanced Merge Strategies

For special cases, here are additional strategies:

### Strategy: Smart Field Selection

Keep auto-extracted values for technical fields, use curated for annotations:

```python
def smart_merge(auto_meta, curated_meta):
    """Curated for annotations, auto for technical."""
    
    # Fields that should always come from curated
    curated_fields = {
        'title', 'description', 'organism_ontology_term_id',
        'tissue_ontology_term_id', 'cell_type_ontology_term_id',
        'disease_ontology_term_id', 'assay_ontology_term_id',
        'creators', 'donor_id', 'sample_id', 'license'
    }
    
    merged = {}
    
    # Add curated fields first
    for field in curated_fields:
        if field in curated_meta:
            merged[field] = curated_meta[field]
    
    # Then add auto, preserving curated if present
    for key, value in auto_meta.items():
        if key not in merged:
            merged[key] = value
        elif key in curated_meta:
            # Keep curated, but note the auto value exists
            merged[key + '_auto'] = value
    
    return merged
```

## Validation

### CLI Validation

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

### Common Issues

| Issue | Solution |
|-------|----------|
| Missing ontology terms | Check template fields are filled |
| Empty cell_count | Auto-extraction may have failed |
| Schema mismatch | Ensure schema URLs match |

## Alternatives: Using jq

For simple merges without Python:

```bash
# jq merge (curated wins)
jq -s '.[0] * .[1]' auto.json curated.json > merged.json
```

## Command Reference

```
fairmeta-merge AUTO_FILE CURATED_FILE -o OUTPUT [OPTIONS]

Options:
  -o, --output FILE          Output file (default: stdout)
  --add-provenance         Add field source tracking (default: True)
  --no-provenance         Skip provenance tracking
  --no-save             Skip datalad add/save
  -m, --message TEXT    Commit message (default: "Merged auto-extracted and curated metadata")
```

## Next Steps

- [Quick Start](quickstart.md) - Basic template usage
- [Examples](examples.md) - Liver-specific examples  
- [Ontology Reference](ontology.md) - Find correct ontology terms