"""Visium HD dataset metadata extractor.

Extracts metadata from 10x Genomics Visium HD data following SOPA input requirements.
"""

import csv
import gzip
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

logger = logging.getLogger('datalad_metalad_fairextract.visium_hd')


class VisiumHDDatasetExtractor(DatasetMetadataExtractor):
    """Extract metadata from Visium HD directories following SOPA requirements.

    SOPA expects the following raw files:
    - microscope_image/: Full-resolution microscopy image (REQUIRED)
    - Feature matrix H5 files (various naming patterns)
    """

    extractor_name = "fairmeta_visium_hd"
    extractor_version = "1.0.0"

    VISIUM_HD_PATTERNS = ['microscope_image', 'feature_slice', '.h5']

    @staticmethod
    def get_id() -> UUID:
        return UUID("a7b8c9d0-1e2f-3a4b-5c6d-7e8f9a0b1c2d")

    @staticmethod
    def get_version() -> str:
        return "1.0.0"

    @staticmethod
    def get_data_output_category() -> DataOutputCategory:
        return DataOutputCategory.IMMEDIATE

    def get_required_content(self) -> bool:
        return True

    def extract(self, _=None) -> ExtractorResult:
        """Extract Visium HD metadata from the directory."""
        metadata = {
            "$schema": "https://datalad-metalad-fairmeta.github.io/schemas/visium_hd.schema.json",
            "schema_version": "1.0.0"
        }
        warnings = []
        errors = []

        dataset_path = str(self.dataset.path)
        logger.info(f"Extracting Visium HD metadata from: {dataset_path}")

        try:
            visium_metadata = self._extract_visium_hd_metadata(dataset_path)
            metadata.update(visium_metadata)

            if not visium_metadata.get("microscope_image_found"):
                errors.append("No microscope_image directory found in directory")
        except Exception as e:
            errors.append(f"Failed to extract Visium HD metadata: {str(e)}")

        validation_errors = validate_metadata(metadata, "visium_hd")
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

    def _extract_visium_hd_metadata(self, dataset_path: str) -> dict[str, Any]:
        """Extract Visium HD metadata from SOPA files."""
        visium_data = {}

        microscope_dir = Path(dataset_path) / 'microscope_image'
        if microscope_dir.exists() and microscope_dir.is_dir():
            visium_data["microscope_image_found"] = True
            visium_data["microscope_image_directory"] = "microscope_image"

            image_files = []
            for ext in ['.tif', '.tiff', '.png', '.jpg', '.jpeg', '.ome.tif', '.ome.tiff']:
                image_files.extend(list(microscope_dir.glob(f'*{ext}')))

            if image_files:
                visium_data["microscope_image_count"] = len(image_files)
                if len(image_files) == 1:
                    visium_data["microscope_image_file"] = image_files[0].name
                else:
                    visium_data["microscope_image_files"] = [f.name for f in image_files[:5]]

                try:
                    import tifffile
                    for img_file in image_files[:1]:
                        if img_file.suffix in ['.tif', '.tiff', '.ome.tif', '.ome.tiff']:
                            with tifffile.TiffFile(img_file) as tif:
                                if tif.pages:
                                    page = tif.pages[0]
                                    visium_data["image_width"] = page.imagewidth
                                    visium_data["image_height"] = page.imagelength
                                    if page.samplesperpixel > 1:
                                        visium_data["image_channels"] = page.samplesperpixel
                            break
                except ImportError:
                    logger.warning("tifffile not available, cannot read image dimensions")
                except Exception as e:
                    logger.warning(f"Could not read microscope image: {e}")
        else:
            single_image = self._find_file(dataset_path, ['microscope_image.tif', 'microscope_image.tiff', 'full_image.tif', 'full_image.tiff'])
            if single_image:
                visium_data["microscope_image_found"] = True
                visium_data["microscope_image_file"] = single_image.name

        h5_files = list(Path(dataset_path).glob('*.h5')) + list(Path(dataset_path).glob('*.hdf5')) + list(Path(dataset_path).glob('*.hdf'))
        if h5_files:
            visium_data["h5_files"] = [f.name for f in h5_files]
            visium_data["h5_file_count"] = len(h5_files)

            for h5_file in h5_files:
                if 'feature' in h5_file.name.lower() or 'expression' in h5_file.name.lower():
                    visium_data["feature_matrix_file"] = h5_file.name

        return visium_data

    def _find_file(self, directory: str, patterns: list[str]) -> Path | None:
        """Find a file matching any of the given patterns."""
        dir_path = Path(directory)
        for pattern in patterns:
            for f in dir_path.rglob(f"*{pattern}*"):
                if f.is_file():
                    return f
        return None