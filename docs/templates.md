# Metadata Templates

Templates for capturing curated metadata that cannot be automatically extracted from 
scientific data files.

## Overview

The metadata templates provide a human-readable YAML format for recording study metadata 
that requires manual curation. These templates work alongside the automated extractors 
to produce complete FAIR-compliant metadata.

## Why Use Templates?

Automated extractors can read many fields directly from data files:

- **Auto-extractable**: cell counts, gene counts, image dimensions, quality scores
- **Requires manual entry**: ontology terms, disease state, creator information, licenses

The templates capture the manual fields that make your metadata truly FAIR-compliant.

## When to Use Templates

| Scenario | Template Approach |
|----------|------------------|
| New study with spatial omics data | Use templates + run auto-extractors |
| Augment existing auto-extracted metadata | Use templates to fill gaps |
| Interactive mode not practical | Use templates for batch metadata entry |
| Multi-sample datasets | Use samples.yaml for sample-level metadata |

## Files

| File | Description |
|------|-------------|
| `templates/dataset_metadata.yaml.template` | Dataset-level metadata template |
| `templates/samples.yaml.template` | Per-sample metadata template |
| `templates/README.md` | Quick reference |

## Documentation Guide

### For Users

- **[Quick Start](templates/quickstart.md)** - Step-by-step guide to using templates
- **[Examples](templates/examples.md)** - Liver-specific examples for your samples
- **[Merging Guide](templates/merging.md)** - Combine auto + curated metadata

### For Developers

- **[Ontology Reference](templates/ontology.md)** - Complete ontology term list
- **[Schema Reference](../schemas/index.md)** - JSON schema definitions
- **[Manual Extractor](../extractors/manual.md)** - Config file mode details

## Workflow Summary

```
1. Copy templates to dataset directory
2. Fill in curated metadata
3. Run auto-extractor (h5ad, xenium, spatialdata, etc.)
4. Run manual extractor with config file
5. Merge results for complete metadata
```

## Related Documentation

- [Manual Extractor](../extractors/manual.md) - Config file mode
- [Schema Reference](../schemas/index.md) - All metadata schemas
- [Ontology Reference](../schemas/ontologies.md) - Basic ontology terms
- [Extractors Overview](../extractors/index.md) - All available extractors