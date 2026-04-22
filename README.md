# datalad-metalad-fairmeta

**FAIR-compliant metadata extractors for spatial biology data**

`datalad-metalad-fairmeta` provides extractors for extracting standardized, FAIR-compliant metadata from spatial biology data formats (OME-TIFF, TIFF, SpatialData, h5ad, CosMx, Xenium, Visium HD, MERSCOPE, MACSima, PhenoCycler, Molecular Cartography, Hyperion, FASTQ) using DataLad Metalad.

## Features

- **Multiple Format Support**: Extract metadata from OME-TIFF, TIFF, SpatialData .zarr, AnnData h5ad, CosMx, Xenium, Visium HD, MERSCOPE, MACSima, PhenoCycler, Molecular Cartography, Hyperion, and FASTQ files
- **FAIR Compliance**: All extractors produce JSON metadata following established standards and ontologies
- **Schema Validation**: Built-in validation against JSON schemas
- **Interactive Entry**: Manual metadata entry for non-standard formats
- **Metalad Integration**: Seamlessly works with DataLad Metalad for metadata aggregation

## Installation

```bash
# Basic installation
pip install datalad-metalad-fairmeta

# With all optional dependencies
pip install datalad-metalad-fairmeta[all]
```

## Quick Start

```bash
# Extract metadata from an OME-TIFF file
datalad meta-extract -d . fairmeta_ome_tiff image.ome.tiff

# Extract metadata from a CosMx directory
datalad meta-extract -d . --force-dataset-level fairmeta_cosmx

# Aggregate metadata from subdatasets
datalad meta-aggregate -d . subds1 subds2

# Export all metadata
datalad meta-dump -d . -r > metadata.jsonl
```

## Supported Extractors

| Extractor | Data Type | Level |
|-----------|-----------|-------|
| `fairmeta_ome_tiff` | OME-TIFF | File |
| `fairmeta_tiff` | TIFF | File |
| `fairmeta_spatialdata` | SpatialData .zarr | Dataset |
| `fairmeta_h5ad` | AnnData h5ad | File |
| `fairmeta_cosmx` | NanoString CosMx | Dataset |
| `fairmeta_xenium` | 10x Xenium | Dataset |
| `fairmeta_visium_hd` | 10x Visium HD | Dataset |
| `fairmeta_merscope` | Vizgen MERSCOPE | Dataset |
| `fairmeta_macsima` | Bruker MACSima | Dataset |
| `fairmeta_phenocycler` | Akoya PhenoCycler | Dataset |
| `fairmeta_molecular_cartography` | Resolve Bioscience Molecular Cartography | Dataset |
| `fairmeta_hyperion` | Fluidigm Hyperion | Dataset |
| `fairmeta_fastq` | FASTQ | File |
| `fairmeta_manual` | Manual entry | Dataset |

## Ontology Support

All extractors use standardized ontology terms:

- **NCBITaxon**: Organism
- **UBERON**: Tissue/Organ
- **Cell Ontology (CL)**: Cell types
- **EFO**: Experimental factors/Assays
- **MONDO/PATO**: Disease states

## Documentation

Full documentation is available at: [https://jonasmac16.github.io/datalad-metalad-fairmeta](https://jonasmac16.github.io/datalad-metalad-fairmeta)

## License

MIT License
