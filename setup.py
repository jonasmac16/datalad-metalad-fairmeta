#!/usr/bin/env python
"""Setup configuration for datalad-metalad-fairmeta."""

import sys
from setuptools import setup, find_namespace_packages

SETUP_REQUIRES = ['setuptools >= 30.3.0', 'wheel']

setup(
    name="datalad-metalad-fairmeta",
    version="0.1.0",
    description="FAIR metadata extractors for spatial biology data",
    long_description=open("README.md").read() if __import__("os").path.exists("README.md") else "",
    long_description_content_type="text/markdown",
    author="Jonas Michels",
    author_email="jonas@example.com",
    url="https://github.com/jonasmac16/datalad-metalad-fairmeta",
    license="MIT",
    packages=find_namespace_packages(include=['datalad_metalad_fairextract']),
    package_data={
        'datalad_metalad_fairextract': ['schemas/*.json'],
    },
    python_requires=">=3.9",
    install_requires=[
        "datalad>=0.18",
        "datalad-metalad>=0.4",
        "jsonschema>=4.0",
        "click>=8.0",
    ],
    extras_require={
        'ome_tiff': ["ome-types>=0.4.0"],
        'h5ad': ["anndata>=1.7.0"],
        'spatialdata': ["spatialdata>=0.7.0"],
        'all': [
            "ome-types>=0.4.0",
            "anndata>=1.7.0",
            "spatialdata>=0.7.0",
            "tifffile>=2021.0",
        ],
        'docs': [
            "mkdocs>=1.5",
            "mkdocs-material>=9.0",
            "mkdocstrings[python]>=0.20",
        ],
        'test': [
            "pytest",
            "pytest-cov",
        ],
    },
    entry_points={
        'console_scripts': [
            'fairmeta-merge=datalad_metalad_fairextract.cli:merge',
        ],
        'datalad.extensions': [
            'metalad-fairmeta=datalad_metalad_fairextract:command_suite',
        ],
        'datalad.metadata.extractors': [
            'fairmeta_ome_tiff=datalad_metalad_fairextract.extractors.ome_tiff:OmeTiffFileExtractor',
            'fairmeta_tiff=datalad_metalad_fairextract.extractors.tiff:TiffFileExtractor',
            'fairmeta_spatialdata=datalad_metalad_fairextract.extractors.spatialdata:SpatialDataDatasetExtractor',
            'fairmeta_h5ad=datalad_metalad_fairextract.extractors.h5ad:H5adFileExtractor',
            'fairmeta_cosmx=datalad_metalad_fairextract.extractors.cosmx:CosMxDatasetExtractor',
            'fairmeta_xenium=datalad_metalad_fairextract.extractors.xenium:XeniumDatasetExtractor',
            'fairmeta_visium_hd=datalad_metalad_fairextract.extractors.visium_hd:VisiumHDDatasetExtractor',
            'fairmeta_merscope=datalad_metalad_fairextract.extractors.merscope:MerscopeDatasetExtractor',
            'fairmeta_macsima=datalad_metalad_fairextract.extractors.macsima:MacsimaDatasetExtractor',
            'fairmeta_phenocycler=datalad_metalad_fairextract.extractors.phenocycler:PhenoCyclerDatasetExtractor',
            'fairmeta_molecular_cartography=datalad_metalad_fairextract.extractors.molecular_cartography:MolecularCartographyDatasetExtractor',
            'fairmeta_hyperion=datalad_metalad_fairextract.extractors.hyperion:HyperionDatasetExtractor',
            'fairmeta_fastq=datalad_metalad_fairextract.extractors.fastq:FastqFileExtractor',
            'fairmeta_manual=datalad_metalad_fairextract.extractors.manual:FairmetaManualDatasetExtractor',
        ],
        'datalad.tests': [
            'metalad-fairmeta=datalad_metalad_fairextract',
        ],
    },
    classifiers=[
        "Programming Language :: Python",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
    ],
)
