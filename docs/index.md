# datalad-metalad-fairmeta

**FAIR-compliant metadata extractors for spatial biology data**

datalad-metalad-fairmeta provides a suite of metadata extractors for spatial biology data formats (OME-TIFF, TIFF, SpatialData, h5ad, CosMx, Xenium, Visium HD, MERSCOPE, MACSima, PhenoCycler, Molecular Cartography, Hyperion, FASTQ) that produce standardized, FAIR-compliant metadata following scFAIR, OME, and general FAIR data principles.

## Features

- **Multiple Format Support**: Extract metadata from OME-TIFF, TIFF, SpatialData .zarr, AnnData h5ad, CosMx, Xenium, Visium HD, MERSCOPE, MACSima, PhenoCycler, Molecular Cartography, Hyperion, and FASTQ files
- **FAIR Compliance**: All extractors produce JSON metadata following established standards and ontologies
- **Schema Validation**: Built-in validation against JSON schemas
- **Interactive Entry**: Manual metadata entry for non-standard formats
- **Metalad Integration**: Seamlessly works with DataLad Metalad for metadata aggregation

## Supported Data Types

| Data Type | Extractor | Level | Description |
|-----------|-----------|-------|-------------|
| OME-TIFF | `fairmeta_ome_tiff` | File | Microscopy images with OME metadata |
| TIFF | `fairmeta_tiff` | File | General TIFF images |
| SpatialData | `fairmeta_spatialdata` | Dataset | Multi-modal spatial omics (.zarr) |
| AnnData | `fairmeta_h5ad` | File | Single-cell data (scRNA-seq) |
| CosMx | `fairmeta_cosmx` | Dataset | NanoString spatial molecular imaging |
| Xenium | `fairmeta_xenium` | Dataset | 10x Xenium in situ genomics |
| Visium HD | `fairmeta_visium_hd` | Dataset | 10x Genomics Visium HD |
| MERSCOPE | `fairmeta_merscope` | Dataset | Vizgen MERSCOPE spatial transcriptomics |
| MACSima | `fairmeta_macsima` | Dataset | Bruker MACSima imaging |
| PhenoCycler | `fairmeta_phenocycler` | Dataset | Akoya PhenoCycler imaging |
| Molecular Cartography | `fairmeta_molecular_cartography` | Dataset | Resolve Bioscience Molecular Cartography |
| Hyperion | `fairmeta_hyperion` | Dataset | Fluidigm Hyperion imaging |
| FASTQ | `fairmeta_fastq` | File | Sequencing data |
| Manual | `fairmeta_manual` | Dataset | Interactive metadata entry |

## Quick Example

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

## Ontology Support

All extractors use standardized ontology terms:

- **NCBITaxon**: Organism (e.g., `NCBITaxon:9606`)
- **UBERON**: Tissue/Organ (e.g., `UBERON:0002113`)
- **Cell Ontology (CL)**: Cell types (e.g., `CL:0000738`)
- **EFO**: Experimental factors/Assays (e.g., `EFO:0009899`)
- **MONDO/PATO**: Disease states (e.g., `MONDO:0005002`)

## Installation

```bash
# Basic installation
pip install datalad-metalad-fairmeta

# With all optional dependencies
pip install datalad-metalad-fairmeta[all]

# From source
git clone https://github.com/jonasmac16/datalad-metalad-fairmeta
cd datalad-metalad-fairmeta
pip install -e .
```

## Documentation

- [Installation Guide](installation.md)
- [Quick Start Guide](quickstart.md)
- [Extractor Documentation](extractors/index.md)
- [Metalad Integration](metalad/index.md)
- [Schema Reference](schemas/index.md)
- [Edge Cases](edge_cases/index.md)
- [Examples](examples/index.md)

## License

MIT License
