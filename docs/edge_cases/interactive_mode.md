# Edge Case: Interactive Mode

## Problem

The extractor prompts for user input, blocking automated pipelines and CI/CD workflows.

## Symptoms

```
$ datalad meta-extract -d . fairmeta_manual image.ome.tiff
Extracting metadata from image.ome.tiff
Enter value for 'tissue_ontology_term_id': _
```

The process hangs waiting for input that may never come.

## Causes

1. Missing required fields in the source data
2. User stopped the process to provide input manually
3. Automated scripts not configured for non-interactive mode
4. Configuration file not provided

## Solutions

### Use Configuration Files

Create a YAML configuration file with predefined values:

```yaml
# metadata_config.yaml
tissue_ontology_term_id: UBERON:0002113
assay_type: "SMA"
species_ontology_term_id: NCBITaxon:9606
```

```bash
datalad meta-extract -d . fairmeta_manual image.ome.tiff --config metadata_config.yaml
```

### Environment Variables

Set defaults via environment variables:

```bash
export DATALAD_METALAD_TISSUE_ONTOLOGY=UBERON:0002113
export DATALAD_METALAD_SPECIES=NCBITaxon:9606
export DATALAD_METALAD_ASSAY_TYPE=SMA

datalad meta-extract -d . fairmeta_manual image.ome.tiff
```

### Disable Interactive Prompts

Force non-interactive mode to fail fast instead of waiting:

```bash
export DATALAD_METALAD_NONINTERACTIVE=1

datalad meta-extract -d . fairmeta_manual image.ome.tiff
# Now fails immediately with clear error instead of hanging
```

### Batch Processing with Defaults

Process multiple files without individual prompts:

```bash
# Create default config
cat > defaults.yaml <<EOF
tissue_ontology_term_id: UBERON:0002113
assay_type: "SMA"
species_ontology_term_id: NCBITaxon:9606
EOF

# Process all files with defaults
for f in *.ome.tiff; do
  datalad meta-extract -d . fairmeta_ome_tiff "$f" --default-config defaults.yaml
done
```

## Best Practices

1. **Always provide configuration files** in production environments
2. **Use environment variables** for sensitive or environment-specific values
3. **Set defaults** for all required fields to avoid prompts
4. **Test in CI/CD** with `DATALAD_METALAD_NONINTERACTIVE=1` to catch interactive issues

## Related

- [Large Datasets](large_datasets.md) - For handling large-scale automated extraction
- [Validation Errors](validation_errors.md) - For handling schema validation issues
