# Schema Reference

## Overview

All schemas follow JSON Schema Draft 2020-12 and include FAIR principles. Each schema includes:

- **@context**: JSON-LD context for linked data interoperability with ontology prefixes (efo, uberon, ncbitaxon, cl, mondo, pato)
- **Provenance**: Reference to base schema for extraction metadata (extractor_id, version, date, source_files)

## Base Schema

The base schema (`base.schema.json`) defines common types:

### OntologyTerm

```json
{
  "id": "NCBITaxon:9606",
  "label": "Homo sapiens"
}
```

### Person

```json
{
  "name": "Jane Doe",
  "affiliation": "University Example",
  "orcid": "0000-0000-0000-0000",
  "email": "jane@example.edu"
}
```

### Provenance

```json
{
  "extractor_id": "fairmeta_h5ad",
  "extractor_version": "1.0.0",
  "extraction_date": "2024-01-15T12:00:00Z",
  "source_files": ["data.h5ad"]
}
```

## Data Type Schemas

| Schema | Description |
|--------|-------------|
| `base.schema.json` | Common definitions |
| `tiff.schema.json` | General TIFF metadata |
| `ome_tiff.schema.json` | OME-TIFF with OME model |
| `spatialdata.schema.json` | SpatialData .zarr |
| `h5ad.schema.json` | AnnData scFAIR |
| `cosmx.schema.json` | NanoString CosMx |
| `xenium.schema.json` | 10x Xenium |
| `visium_hd.schema.json` | 10x Visium HD |
| `merscope.schema.json` | Vizgen MERSCOPE |
| `macsima.schema.json` | Bruker MACSima |
| `phenocycler.schema.json` | Akoya PhenoCycler |
| `molecular_cartography.schema.json` | Resolve Bioscience Molecular Cartography |
| `hyperion.schema.json` | Fluidigm Hyperion |
| `fastq.schema.json` | FASTQ/SRA |
| `manual.schema.json` | Manual entry |

## Validation

All metadata is validated against JSON schemas during extraction:

```python
from jsonschema import Draft7Validator

validator = Draft7Validator(schema)
for error in validator.iter_errors(metadata):
    print(error.message)
```

## Schema Features

All schemas include these common features:

| Feature | Description |
|---------|-------------|
| `$schema` | JSON Schema Draft 2020-12 identifier |
| `$id` | Unique schema URL |
| `schema_version` | Version of the metadata schema (default: 1.0.0) |
| `@context` | JSON-LD context for ontology prefixes |
| `provenance` | Extraction metadata (extractor, version, date, source files) |

## Next Steps

- [Ontology Reference](ontologies.md)
- [Metadata Templates](../templates.md) - For fields requiring manual entry
