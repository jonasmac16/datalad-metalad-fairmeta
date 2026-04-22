"""MACSima dataset metadata extractor.

Extracts metadata from Bruker MACSima imaging data following SOPA input requirements.
"""

import logging
import re
from pathlib import Path
from typing import Any
from uuid import UUID

from datalad_metalad.extractors.base import (
    DataOutputCategory,
    DatasetMetadataExtractor,
    ExtractorResult,
)

from .base import create_extraction_result, create_provenance, validate_metadata

logger = logging.getLogger('datalad_metalad_fairextract.macsima')


class MacsimaDatasetExtractor(DatasetMetadataExtractor):
    """Extract metadata from MACSima directories following SOPA requirements.

    SOPA expects the following raw files:
    - *.tif files with specific naming patterns:
      - Standard OME-TIF: Channel names from OME metadata
      - Non-standard: Files with A- in name - channel names from antibody
        identifiers in filename pattern: _A-{antibody}_C-{channel}.tif
    """

    extractor_name = "fairmeta_macsima"
    extractor_version = "1.0.0"

    MACSIMA_PATTERNS = ['.tif', 'A-']

    @staticmethod
    def get_id() -> UUID:
        return UUID("c2d3e4f5-6a7b-8c9d-0e1f-2a3b4c5d6e7f")

    @staticmethod
    def get_version() -> str:
        return "1.0.0"

    @staticmethod
    def get_data_output_category() -> DataOutputCategory:
        return DataOutputCategory.IMMEDIATE

    def get_required_content(self) -> bool:
        return True

    def extract(self, _=None) -> ExtractorResult:
        """Extract MACSima metadata from the directory."""
        metadata = {
            "$schema": "https://datalad-metalad-fairmeta.github.io/schemas/macsima.schema.json",
            "schema_version": "1.0.0"
        }
        warnings = []
        errors = []

        dataset_path = str(self.dataset.path)
        logger.info(f"Extracting MACSima metadata from: {dataset_path}")

        try:
            macsima_metadata = self._extract_macsima_metadata(dataset_path)
            metadata.update(macsima_metadata)

            if not macsima_metadata.get("image_count"):
                errors.append("No MACSima TIF files found in directory")
        except Exception as e:
            errors.append(f"Failed to extract MACSima metadata: {str(e)}")

        validation_errors = validate_metadata(metadata, "macsima")
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

    def _extract_macsima_metadata(self, dataset_path: str) -> dict[str, Any]:
        """Extract MACSima metadata from TIF files."""
        macsima_data = {}

        tif_files = list(Path(dataset_path).glob('*.tif')) + list(Path(dataset_path).glob('*.tiff'))

        if not tif_files:
            return macsima_data

        macsima_data["image_count"] = len(tif_files)

        antibodies = set()
        channels = set()
        non_standard_files = 0
        standard_ome_tif = 0

        sample_file = tif_files[0]
        macsima_data["sample_file"] = sample_file.name

        try:
            import tifffile
            with tifffile.TiffFile(sample_file) as tif:
                if tif.pages:
                    page = tif.pages[0]
                    macsima_data["image_width"] = page.imagewidth
                    macsima_data["image_height"] = page.imagelength

                    if hasattr(page, 'samplesperpixel'):
                        macsima_data["samples_per_pixel"] = page.samplesperpixel

                if hasattr(tif, 'ome_metadata') and tif.ome_metadata:
                    macsima_data["format"] = "ome-tiff"
                    standard_ome_tif = 1
                    macsima_data["ome_metadata_available"] = True
        except ImportError:
            logger.warning("tifffile not available, cannot read image metadata")
        except Exception as e:
            logger.warning(f"Could not read sample TIF file: {e}")

        for tif_file in tif_files:
            filename = tif_file.name

            antibody_match = re.search(r'_A-([^_]+)', filename)
            if antibody_match:
                non_standard_files += 1
                antibodies.add(antibody_match.group(1))

            channel_match = re.search(r'_C-(\d+)', filename)
            if channel_match:
                channels.add(channel_match.group(1))

        if non_standard_files > 0:
            macsima_data["format"] = "non-standard"
            macsima_data["non_standard_files"] = non_standard_files
            macsima_data["antibodies"] = sorted(list(antibodies))
            macsima_data["antibody_count"] = len(antibodies)

        if channels:
            macsima_data["channels"] = sorted(list(channels))
            macsima_data["channel_count"] = len(channels)

        if standard_ome_tif and not macsima_data.get("antibodies"):
            macsima_data["format"] = "ome-tiff"

        return macsima_data