# Edge Cases

This section documents common edge cases and how to handle them.

## Overview

| Edge Case | Symptom | Solution |
|-----------|--------|----------|
| [Missing Files](missing_files.md) | File not found | Check paths, use `--force-dataset-level` |
| [Annexed Files](annex_files.md) | Content not available | Run `datalad get` first |
| [Validation Errors](validation_errors.md) | Schema validation fails | Review and fix metadata |
| [Interactive Mode](interactive_mode.md) | Prompt issues | Use config file mode |
| [Large Datasets](large_datasets.md) | Slow extraction | Use batch processing |

## Common Patterns

### Handling Missing Optional Fields

If optional fields are not available:

```json
{
  "tissue_ontology_term_id": null
}
```

Validators treat `null` and missing fields equivalently for optional properties.

### Partial Extraction

When some metadata can be extracted but not all:

```json
{
  "extraction_success": true,
  "warnings": [
    "disease_ontology_term_id: Recommended field not extracted"
  ]
}
```

### Failed Extraction

When extraction completely fails:

```json
{
  "extraction_success": false,
  "datalad_result_dict": {
    "status": "error"
  }
}
```

## Next Steps

- [Missing Files](missing_files.md)
- [Annexed Files](annex_files.md)
- [Validation Errors](validation_errors.md)
- [Interactive Mode](interactive_mode.md)
- [Large Datasets](large_datasets.md)
