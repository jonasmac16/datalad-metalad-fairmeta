"""FAIR metadata extractors for spatial biology data.

This package provides metalad-compatible extractors for extracting
FAIR-compliant metadata from various spatial biology data formats.

Extractors:
    - OmeTiffFileExtractor: OME-TIFF image files
    - TiffFileExtractor: General TIFF files
    - SpatialDataDatasetExtractor: SpatialData .zarr stores
    - H5adFileExtractor: AnnData h5ad files
    - CosMxDatasetExtractor: CosMx (Nanostring/Bruker) directories
    - XeniumDatasetExtractor: 10x Genomics Xenium directories
    - VisiumHDDatasetExtractor: 10x Genomics Visium HD directories
    - MerscopeDatasetExtractor: Vizgen MERSCOPE directories
    - MacsimaDatasetExtractor: Bruker MACSima imaging directories
    - PhenoCyclerDatasetExtractor: Akoya PhenoCycler directories
    - MolecularCartographyDatasetExtractor: Resolve Bioscience Molecular Cartography directories
    - HyperionDatasetExtractor: Fluidigm Hyperion directories
    - FastqFileExtractor: FASTQ sequencing files
    - FairmetaManualDatasetExtractor: Manual/interactive metadata entry
"""

__version__ = "0.1.0"

__all__ = [
    "OmeTiffFileExtractor",
    "TiffFileExtractor",
    "SpatialDataDatasetExtractor",
    "H5adFileExtractor",
    "CosMxDatasetExtractor",
    "XeniumDatasetExtractor",
    "VisiumHDDatasetExtractor",
    "MerscopeDatasetExtractor",
    "MacsimaDatasetExtractor",
    "PhenoCyclerDatasetExtractor",
    "MolecularCartographyDatasetExtractor",
    "HyperionDatasetExtractor",
    "FastqFileExtractor",
    "FairmetaManualDatasetExtractor",
]