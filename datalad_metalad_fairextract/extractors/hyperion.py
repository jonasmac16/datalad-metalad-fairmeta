"""Hyperion (Fluidigm) dataset metadata extractor.

Extracts metadata from Fluidigm Hyperion imaging data following SOPA input requirements.
"""

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

logger = logging.getLogger('datalad_metalad_fairextract.hyperion')


class HyperionDatasetExtractor(DatasetMetadataExtractor):
    """Extract metadata from Hyperion directories following SOPA requirements.

    SOPA expects the following raw files:
    - *.tiff files: One TIFF per channel
    - Naming convention: {something}_{channel_name}_001.tiff
    - Channel name extracted from position [1] in filename split by '_'
    """

    extractor_name = "fairmeta_hyperion"
    extractor_version = "1.0.0"

    HYPERION_PATTERNS = ['.tif', '_001.tiff']

    @staticmethod
    def get_id() -> UUID:
        return UUID("f5a6b7c8-9d0e-1f2a-3b4c-5d6e7f8a9b0c")

    @staticmethod
    def get_version() -> str:
        return "1.0.0"

    @staticmethod
    def get_data_output_category() -> DataOutputCategory:
        return DataOutputCategory.IMMEDIATE

    def get_required_content(self) -> bool:
        return True

    def extract(self, _=None) -> ExtractorResult:
        """Extract Hyperion metadata from the directory."""
        metadata = {
            "$schema": "https://datalad-metalad-fairmeta.github.io/schemas/hyperion.schema.json",
            "schema_version": "1.0.0"
        }
        warnings = []
        errors = []

        dataset_path = str(self.dataset.path)
        logger.info(f"Extracting Hyperion metadata from: {dataset_path}")

        try:
            hyperion_metadata = self._extract_hyperion_metadata(dataset_path)
            metadata.update(hyperion_metadata)

            if not hyperion_metadata.get("image_count"):
                errors.append("No Hyperion TIF files found in directory")
        except Exception as e:
            errors.append(f"Failed to extract Hyperion metadata: {str(e)}")

        validation_errors = validate_metadata(metadata, "hyperion")
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

    def _extract_hyperion_metadata(self, dataset_path: str) -> dict[str, Any]:
        """Extract Hyperion metadata from TIF files."""
        hyperion_data = {}

        tif_files = list(Path(dataset_path).glob('*.tif')) + list(Path(dataset_path).glob('*.tiff'))

        if not tif_files:
            return hyperion_data

        hyperion_data["image_count"] = len(tif_files)

        channels = set()
        channel_pattern_files = []

        for tif_file in tif_files:
            if '_001.tiff' in tif_file.name or '_001.tif' in tif_file.name:
                channel_pattern_files.append(tif_file)

                parts = tif_file.stem.split('_')
                if len(parts) >= 2:
                    channels.add(parts[1])

        if channel_pattern_files:
            hyperion_data["channel_naming_pattern"] = "{prefix}_{channel}_001.tiff"
            hyperion_data["channels"] = sorted(list(channels))
            hyperion_data["channel_count"] = len(channels)
            hyperion_data["sample_file"] = channel_pattern_files[0].name

            try:
                import tifffile
                with tifffile.TiffFile(channel_pattern_files[0]) as tif:
                    if tif.pages:
                        page = tif.pages[0]
                        hyperion_data["image_width"] = page.imagewidth
                        hyperion_data["image_height"] = page.imagelength
                        if hasattr(page, 'samplesperpixel'):
                            hyperion_data["image_channels"] = page.samplesperpixel
            except ImportError:
                logger.warning("tifffile not available, cannot read image dimensions")
            except Exception as e:
                logger.warning(f"Could not read image metadata: {e}")
        else:
            hyperion_data["sample_file"] = tif_files[0].name

        return hyperion_data