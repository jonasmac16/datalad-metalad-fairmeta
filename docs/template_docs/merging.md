# Merging Auto-Extracted and Curated Metadata

How to combine automatically extracted metadata with curated template data 
for complete FAIR-compliant records.

## Why Merge?

| Source | What It Provides |
|--------|----------------|
| Auto-extractors | cell_count, gene_count, image dimensions, quality scores |
| Templates | ontology terms, disease state, creators, licenses |

Merging gives you the best of both: technical metrics + curated annotations.

## Basic Merge

### Step 1: Run Both Extractions

```bash
# Auto-extract from data files
datalad meta-extract -d . fairmeta_h5ad data.h5ad > auto.json

# Curated metadata from template
datalad meta-extract -d . --force-dataset-level fairmeta_manual \
    config dataset_metadata.yaml > curated.json
```

### Step 2: Merge with Python

```python
import json

def merge_metadata(auto_file, curated_file, output_file):
    """Merge auto-extracted + curated metadata."""
    with open(auto_file) as f:
        auto = json.load(f)
    with open(curated_file) as f:
        curated = json.load(f)
    
    # Get metadata sections
    auto_meta = auto.get('metadata', {})
    curated_meta = curated.get('metadata', {})
    
    # Merge: curated enhances/overrides auto
    # Start with auto, then update with curated
    merged = {**auto_meta, **curated_meta}
    
    # Write result
    with open(output_file, 'w') as f:
        json.dump(merged, f, indent=2)
    
    return merged

# Usage
merge_metadata('auto.json', 'curated.json', 'merged.json')
```

### Step 3: Verify Result

```bash
# Check the merged metadata
cat merged.json | python -m json.tool | head -50
```

## Advanced Merge Strategies

### Strategy 1: Curated Overrides Auto

Curated fields take precedence over auto-extracted:

```python
# Curated wins for overlapping fields
merged = {**auto_meta, **curated_meta}  # curated overwrites auto
```

### Strategy 2: Preserve Auto for Technical Fields

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
    
    # Start with curated base
    merged = {}
    
    # Add curated fields first
    for field in curated_fields:
        if field in curated_meta:
            merged[field] = curated_meta[field]
    
    # Then add auto, but preserve curated if present
    for key, value in auto_meta.items():
        if key not in merged:
            merged[key] = value
        elif key in curated_meta:
            # Keep curated, but note the auto value exists
            merged[key + '_auto'] = value
    
    return merged
```

### Strategy 3: Multiple Sample Merge

For multi-sample datasets:

```python
def merge_samples(auto_json, samples_yaml):
    """Merge auto-extraction with sample metadata."""
    import yaml
    
    with open(auto_json) as f:
        auto = json.load(f)
    with open(samples_yaml) as f:
        samples_data = yaml.safe_load(f)
    
    auto_meta = auto.get('metadata', {})
    samples = samples_data.get('samples', [])
    
    # Create lookup by sample_id
    sample_lookup = {s['sample_id']: s for s in samples}
    
    # Merge each sample
    results = []
    for sample in samples:
        sample_id = sample['sample_id']
        
        # Start with dataset-level metadata
        merged = {**auto_meta}
        
        # Add sample-specific fields
        for key, value in sample.items():
            if key != 'sample_id':
                merged[key] = value
        
        results.append({
            'sample_id': sample_id,
            'metadata': merged
        })
    
    return results

# Usage
results = merge_samples('auto.json', 'samples.yaml')
for r in results:
    print(f"Sample: {r['sample_id']}")
    print(json.dumps(r['metadata'], indent=2))
```

### Strategy 4: Provenance Tracking

Track where each field came from:

```python
def merge_with_provenance(auto_meta, curated_meta):
    """Merge and track field sources."""
    
    merged = {}
    provenance = {}
    
    # All fields from both sources
    all_fields = set(auto_meta.keys()) | set(curated_meta.keys())
    
    for field in all_fields:
        if field in curated_meta:
            merged[field] = curated_meta[field]
            provenance[field] = 'curated'
        elif field in auto_meta:
            merged[field] = auto_meta[field]
            provenance[field] = 'auto'
    
    merged['_provenance'] = provenance
    
    return merged
```

## Complete Example

### Directory Structure

```
my_dataset/
├── data.h5ad                 # Your data file
├── dataset_metadata.yaml     # Curated dataset metadata
├── samples.yaml             # Per-sample metadata
└── processing.sh            # Merge script
```

### processing.sh

```bash
#!/bin/bash
set -e

# Auto-extract from h5ad
echo "Extracting from h5ad..."
datalad meta-extract -d . fairmeta_h5ad data.h5ad > auto.json

# Extract curated metadata
echo "Extracting curated metadata..."
datalad meta-extract -d . --force-dataset-level fairmeta_manual \
    config dataset_metadata.yaml > curated.json

# Merge
echo "Merging metadata..."
python merge_metadata.py auto.json curated.json > complete_metadata.json

# Validate
echo "Validating..."
python -c "
import json
with open('complete_metadata.json') as f:
    meta = json.load(f)

required = ['\$schema', 'schema_version', 'title', 'organism_ontology_term_id']
missing = [r for r in required if r not in meta]
if missing:
    print(f'WARNING: Missing fields: {missing}')
else:
    print('Validation PASSED')
"

echo "Done! Output: complete_metadata.json"
```

### merge_metadata.py

```python
#!/usr/bin/env python3
"""Merge auto-extracted + curated metadata."""

import json
import sys

def main():
    auto_file = sys.argv[1]
    curated_file = sys.argv[2]
    
    with open(auto_file) as f:
        auto = json.load(f)
    with open(curated_file) as f:
        curated = json.load(f)
    
    auto_meta = auto.get('metadata', {})
    curated_meta = curated.get('metadata', {})
    
    # Merge: curated overwrites auto
    merged = {**auto_meta, **curated_meta}
    
    # Add provenance tracking
    merged['_field_sources'] = {
        **{k: 'auto' for k in auto_meta},
        **{k: 'curated' for k in curated_meta if k not in auto_meta}
    }
    
    print(json.dumps(merged, indent=2))

if __name__ == '__main__':
    main()
```

## Validation After Merge

### Check Required Fields

```python
import json

def validate_merged(merged):
    """Validate merged metadata has required fields."""
    
    # Required for h5ad schema
    required = [
        '$schema',
        'schema_version', 
        'organism_ontology_term_id',
        'assay_ontology_term_id'
    ]
    
    errors = []
    for field in required:
        if field not in merged:
            errors.append(f"Missing required field: {field}")
    
    return errors

# Usage
with open('complete_metadata.json') as f:
    merged = json.load(f)

errors = validate_merged(merged)
if errors:
    print("Validation errors:")
    for e in errors:
        print(f"  - {e}")
else:
    print("Validation PASSED")
```

### Common Issues

| Issue | Solution |
|-------|----------|
| Missing ontology terms | Check template fields are filled |
| Empty cell_count | Auto-extraction may have failed |
| Schema mismatch | Ensure schema URLs match |

## Alternatives: Using jq

For simple merges, you can use `jq`:

```bash
# jq merge (curated wins)
jq -s '.[0] * .[1]' auto.json curated.json > merged.json
```

## Next Steps

- [Quick Start](quickstart.md) - Basic template usage
- [Examples](examples.md) - Liver-specific examples  
- [Ontology Reference](ontology.md) - Find correct ontology terms