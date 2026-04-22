"""PhenoCycler (Akoya) dataset metadata extractor.

Extracts metadata from Akoya PhenoCycler imaging data following SOPA input requirements.
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

logger = logging.getLogger('datalad_metalad_fairextract.phenocycler')


class PhenoCyclerDatasetExtractor(DatasetMetadataExtractor):
    """Extract metadata from PhenoCycler directories following SOPA requirements.

    SOPA expects the following raw files:
    - .qptiff file: Multi-channel QuPath-exported TIFF
    - .tif file: ImageJ/Fiji exported multi-channel TIFF

    Channel extraction:
    - .qptiff: XML metadata with biomarker names
    - .tif: IJMetadata tag "Labels" for channel names
    """

    extractor_name = "fairmeta_phenocycler"
    extractor_version = "1.0.0"

    PHENOCYCLER_PATTERNS = ['.qptiff', '.tif']

    @staticmethod
    def get_id() -> UUID:
        return UUID("d3e4f5a6-7b8c-9d0e-1f2a-3b4c5d6e7f8a")

    @staticmethod
    def get_version() -> str:
        return "1.0.0"

    @staticmethod
    def get_data_output_category() -> DataOutputCategory:
        return DataOutputCategory.IMMEDIATE

    def get_required_content(self) -> bool:
        return True

    def extract(self, _=None) -> ExtractorResult:
        """Extract PhenoCycler metadata from the directory."""
        metadata = {
            "$schema": "https://datalad-metalad-fairmeta.github.io/schemas/phenocycler.schema.json",
            "schema_version": "1.0.0"
        }
        warnings = []
        errors = []

        dataset_path = str(self.dataset.path)
        logger.info(f"Extracting PhenoCycler metadata from: {dataset_path}")

        try:
            phenocycler_metadata = self._extract_phenocycler_metadata(dataset_path)
            metadata.update(phenocycler_metadata)

            if not phenocycler_metadata.get("image_file"):
                errors.append("No PhenoCycler image file (.qptiff or .tif) found in directory")
        except Exception as e:
            errors.append(f"Failed to extract PhenoCycler metadata: {str(e)}")

        validation_errors = validate_metadata(metadata, "phenocycler")
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

    def _extract_phenocycler_metadata(self, dataset_path: str) -> dict[str, Any]:
        """Extract PhenoCycler metadata from image files."""
        phenocycler_data = {}

        qptiff_file = self._find_file(dataset_path, ['.qptiff'])
        if qptiff_file:
            phenocycler_data["image_file"] = qptiff_file.name
            phenocycler_data["format"] = "qptiff"
            self._read_image_metadata(phenocycler_data, qptiff_file)
            return phenocycler_data

        tif_files = list(Path(dataset_path).glob('*.tif')) + list(Path(dataset_path).glob('*.tiff'))
        for tif_file in tif_files:
            if tif_file.name.endswith('.qptiff'):
                continue

            phenocycler_data["image_file"] = tif_file.name
            phenocycler_data["format"] = "tif"
            self._read_image_metadata(phenocycler_data, tif_file)
            break

        return phenocycler_data

    def _read_image_metadata(self, data: dict[str, Any], image_file: Path):
        """Read image metadata from the file."""
        try:
            import tifffile
            with tifffile.TiffFile(image_file) as tif:
                if tif.pages:
                    page = tif.pages[0]
                    data["image_width"] = page.imagewidth
                    data["image_height"] = page.imagelength
                    if hasattr(page, 'samplesperpixel'):
                        data["channels"] = page.samplesperpixel

                if hasattr(tif, 'qptiff_metadata'):
                    data["qptiff_metadata_available"] = True
                    if isinstance(tif.qptiff_metadata, dict):
                        channels = tif.qptiff_metadata.get('Channels', [])
                        if channels:
                            data["channel_names"] = [c.get('Name', c.get('channel', i)) for i, c in enumerate(channels)]
                            data["channel_count"] = len(channels)

                if hasattr(tif, 'imagej_metadata') and tif.imagej_metadata:
                    data["imagej_metadata_available"] = True
                    if hasattr(tif.imagej_metadata, 'Labels'):
                        labels = tif.imagej_metadata.Labels
                        if labels:
                            data["channel_names"] = labels if isinstance(labels, list) else [labels]
                            data["channel_count"] = len(labels) if isinstance(labels, list) else 1
        except ImportError:
            logger.warning("tifffile not available, cannot read image metadata")
        except Exception as e:
            logger.warning(f"Could not read image metadata: {e}")

    def _find_file(self, directory: str, patterns: list[str]) -> Path | None:
        """Find a file matching any of the given patterns."""
        dir_path = Path(directory)
        for pattern in patterns:
            for f in dir_path.rglob(f"*{pattern}"):
                if f.is_file():
                    return f
        return None