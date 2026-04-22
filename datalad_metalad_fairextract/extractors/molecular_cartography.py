"""Molecular Cartography (Resolve Bioscience) dataset metadata extractor.

Extracts metadata from Resolve Bioscience Molecular Cartography data following SOPA input requirements.
"""

import csv
import logging
from pathlib import Path
from typing import Any
from uuid import UUID

from datalad_metalad.extractors.base import (
    DataOutputCategory,
    DatasetMetadataExtractor,
    ExtractorResult,
)

from .base import create_extraction_result, create_provenance, validate_metadata

logger = logging.getLogger('datalad_metalad_fairextract.molecular_cartography')


class MolecularCartographyDatasetExtractor(DatasetMetadataExtractor):
    """Extract metadata from Molecular Cartography directories following SOPA requirements.

    SOPA expects the following raw files:
    - {dataset_id}_results.txt: Transcript locations (tab-separated)
    - {dataset_id}_{channel}.tiff: One TIFF per channel

    The region parameter is required to specify which region to read.
    Region name found before _results.txt (e.g., A2-1)
    """

    extractor_name = "fairmeta_molecular_cartography"
    extractor_version = "1.0.0"

    MOLECULAR_CARTOGRAPHY_PATTERNS = ['_results.txt', '_results.txt.gz']

    @staticmethod
    def get_id() -> UUID:
        return UUID("e4f5a6b7-8c9d-0e1f-2a3b-4c5d6e7f8a9b")

    @staticmethod
    def get_version() -> str:
        return "1.0.0"

    @staticmethod
    def get_data_output_category() -> DataOutputCategory:
        return DataOutputCategory.IMMEDIATE

    def get_required_content(self) -> bool:
        return True

    def extract(self, _=None) -> ExtractorResult:
        """Extract Molecular Cartography metadata from the directory."""
        metadata = {
            "$schema": "https://datalad-metalad-fairmeta.github.io/schemas/molecular_cartography.schema.json",
            "schema_version": "1.0.0"
        }
        warnings = []
        errors = []

        dataset_path = str(self.dataset.path)
        logger.info(f"Extracting Molecular Cartography metadata from: {dataset_path}")

        try:
            mc_metadata = self._extract_molecular_cartography_metadata(dataset_path)
            metadata.update(mc_metadata)

            if not mc_metadata.get("results_file"):
                errors.append("No Molecular Cartography results file (*_results.txt) found in directory")
        except Exception as e:
            errors.append(f"Failed to extract Molecular Cartography metadata: {str(e)}")

        validation_errors = validate_metadata(metadata, "molecular_cartography")
        success = len(errors) == 0 and len(validation_errors) == 0

        return create_extraction_result(
            metadata=metadata,
            extractor_version=self.extractor_version,
            extraction_parameter=self.parameter,
            success=success,
            result_type="dataset",
            validation_errors=validation_errors,
            warnings=warnings,
            provenance=create_provenance(
                self.extractor_name,
                self.extractor_version,
                [dataset_path]
            )
        )

    def _extract_molecular_cartography_metadata(self, dataset_path: str) -> dict[str, Any]:
        """Extract Molecular Cartography metadata from SOPA files."""
        mc_data = {}

        results_file = self._find_file(dataset_path, ['_results.txt', '_results.txt.gz'])
        if results_file:
            mc_data["results_file"] = results_file.name

            filename = results_file.name
            region_match = filename.split('_results')[0]
            if region_match:
                mc_data["region"] = region_match

            try:
                import gzip
                is_gzipped = str(results_file).endswith('.gz')
                opener = gzip.open if is_gzipped else open

                with opener(results_file, 'rt') as f:
                    reader = csv.DictReader(f, delimiter='\t')
                    transcript_count = sum(1 for _ in reader)
                    mc_data["transcript_count"] = transcript_count

                results_file_path = Path(results_file)
                is_gzipped = str(results_file_path).endswith('.gz')
                opener = gzip.open if is_gzipped else open
                with opener(results_file_path, 'rt') as f:
                    reader = csv.DictReader(f, delimiter='\t')
                    first_row = next(reader, None)
                    if first_row:
                        mc_data["columns"] = list(first_row.keys())
            except Exception as e:
                logger.warning(f"Could not read results file: {e}")

        tif_files = list(Path(dataset_path).glob('*.tif')) + list(Path(dataset_path).glob('*.tiff'))
        channel_files = []

        if mc_data.get("region"):
            for tif_file in tif_files:
                if mc_data["region"] in tif_file.name:
                    channel_files.append(tif_file.name)

        if not channel_files:
            channel_files = [f.name for f in tif_files]

        if channel_files:
            mc_data["image_files"] = channel_files
            mc_data["image_count"] = len(channel_files)

            if mc_data.get("region"):
                channels = set()
                for fname in channel_files:
                    parts = fname.replace(mc_data["region"], '').replace('.tif', '').replace('.tiff', '').strip('_')
                    if parts:
                        channels.add(parts)
                if channels:
                    mc_data["channels"] = sorted(list(channels))
                    mc_data["channel_count"] = len(channels)

            try:
                import tifffile
                for tif_file in tif_files[:1]:
                    with tifffile.TiffFile(tif_file) as tif:
                        if tif.pages:
                            page = tif.pages[0]
                            mc_data["image_width"] = page.imagewidth
                            mc_data["image_height"] = page.imagelength
                            if hasattr(page, 'samplesperpixel'):
                                mc_data["image_channels"] = page.samplesperpixel
                    break
            except ImportError:
                logger.warning("tifffile not available, cannot read image dimensions")
            except Exception as e:
                logger.warning(f"Could not read image metadata: {e}")

        return mc_data

    def _find_file(self, directory: str, patterns: list[str]) -> Path | None:
        """Find a file matching any of the given patterns."""
        dir_path = Path(directory)
        for pattern in patterns:
            for f in dir_path.rglob(f"*{pattern}"):
                if f.is_file():
                    return f
        return None