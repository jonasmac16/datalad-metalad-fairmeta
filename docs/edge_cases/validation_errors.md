# Edge Case: Validation Errors

## Problem

Extracted metadata fails schema validation.

## Symptoms

```json
{
  "extraction_success": true,
  "validation_errors": [
    "organism_ontology_term_id: '9606' does not match pattern '^[A-Z]+:\\d+$'",
    "assay_ontology_term_id: 'EFO' is a required property"
  ]
}
```

## Causes

1. Invalid CURIE format (should be `EFO:0009899`, not `EFO`)
2. Missing required fields
3. Wrong data type (string instead of integer)
4. Invalid ontology ID

## Solutions

### Fix Invalid CURIEs

```bash
# Wrong format
organism_ontology_term_id: "9606"  # Incorrect

# Correct format
organism_ontology_term_id:
  id: "NCBITaxon:9606"
  label: "Homo sapiens"
```

### Use Interactive Mode to Fill Missing Fields

```bash
datalad meta-extract -d . --force-dataset-level fairmeta_manual \
  interactive true \
  schema h5ad
```

### Validate Before Adding

```bash
# Extract and check validation
result=$(datalad meta-extract -d . fairmeta_h5ad data.h5ad)

# Check for errors
echo "$result" | jq '.validation_errors'

# Only add if valid
if [ $(echo "$result" | jq '.validation_errors | length') -eq 0 ]; then
  echo "$result" | datalad meta-add -d . -
fi
```

### Common Fixes

| Issue | Wrong | Correct |
|-------|-------|---------|
| Missing organism | Not included | `{"id": "NCBITaxon:9606", "label": "Homo sapiens"}` |
| Invalid CURIE | `"EFO"` | `"EFO:0009899"` |
| Wrong separator | `"NCBITaxon_9606"` | `{"id": "NCBITaxon:9606", "label": "..."}` |

## Prevention

1. Use ontology lookup services to get correct IDs
2. Validate CURIEs before saving
3. Use interactive mode to verify ontology terms
4. Keep ontology mappings documented
