"""MERSCOPE (Vizgen) dataset metadata extractor.

Extracts metadata from Vizgen MERSCOPE data following SOPA input requirements.
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

logger = logging.getLogger('datalad_metalad_fairextract.merscope')


class MerscopeDatasetExtractor(DatasetMetadataExtractor):
    """Extract metadata from MERSCOPE directories following SOPA requirements.

    SOPA expects the following raw files:
    - detected_transcripts.csv: Transcript locations and names (REQUIRED)
    - images/: Directory containing all microscopy images
    - images/micron_to_mosaic_pixel_transform.csv: Affine transformation matrix
    """

    extractor_name = "fairmeta_merscope"
    extractor_version = "1.0.0"

    MERSCOPE_PATTERNS = ['detected_transcripts', 'micron_to_mosaic_pixel_transform']

    @staticmethod
    def get_id() -> UUID:
        return UUID("b1c2d3e4-5f6a-7b8c-9d0e-1f2a3b4c5d6e")

    @staticmethod
    def get_version() -> str:
        return "1.0.0"

    @staticmethod
    def get_data_output_category() -> DataOutputCategory:
        return DataOutputCategory.IMMEDIATE

    def get_required_content(self) -> bool:
        return True

    def extract(self, _=None) -> ExtractorResult:
        """Extract MERSCOPE metadata from the directory."""
        metadata = {
            "$schema": "https://datalad-metalad-fairmeta.github.io/schemas/merscope.schema.json",
            "schema_version": "1.0.0"
        }
        warnings = []
        errors = []

        dataset_path = str(self.dataset.path)
        logger.info(f"Extracting MERSCOPE metadata from: {dataset_path}")

        try:
            merscope_metadata = self._extract_merscope_metadata(dataset_path)
            metadata.update(merscope_metadata)

            if not merscope_metadata.get("transcript_file"):
                errors.append("No MERSCOPE transcript file (detected_transcripts.csv) found in directory")
        except Exception as e:
            errors.append(f"Failed to extract MERSCOPE metadata: {str(e)}")

        validation_errors = validate_metadata(metadata, "merscope")
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

    def _extract_merscope_metadata(self, dataset_path: str) -> dict[str, Any]:
        """Extract MERSCOPE metadata from SOPA files."""
        merscope_data = {}

        transcripts_file = self._find_file(dataset_path, ['detected_transcripts.csv'])
        if transcripts_file:
            merscope_data["transcript_file"] = transcripts_file.name
            try:
                with open(transcripts_file) as f:
                    reader = csv.DictReader(f)
                    transcript_count = sum(1 for _ in reader)
                    merscope_data["transcript_count"] = transcript_count

                transcripts_file_path = Path(transcripts_file)
                transcripts_file_path.seek(0)
                with open(transcripts_file_path) as f:
                    reader = csv.DictReader(f)
                    first_row = next(reader, None)
                    if first_row:
                        merscope_data["transcript_columns"] = list(first_row.keys())
            except Exception as e:
                logger.warning(f"Could not read detected_transcripts.csv: {e}")

        images_dir = Path(dataset_path) / 'images'
        if images_dir.exists() and images_dir.is_dir():
            merscope_data["images_directory"] = "images"

            image_files = []
            for ext in ['.tif', '.tiff', '.png', '.jpg']:
                image_files.extend(list(images_dir.glob(f'*{ext}')))

            merscope_data["image_count"] = len(image_files)
            if image_files:
                merscope_data["sample_image"] = image_files[0].name

        transform_file = self._find_file(dataset_path, ['micron_to_mosaic_pixel_transform.csv'])
        if transform_file:
            merscope_data["transform_file"] = transform_file.name
            try:
                with open(transform_file) as f:
                    reader = csv.reader(f)
                    rows = list(reader)
                    if len(rows) >= 6:
                        merscope_data["transform_matrix"] = rows[:6]
            except Exception as e:
                logger.warning(f"Could not read transform file: {e}")

        cell_boundaries_path = self._find_file(dataset_path, ['cell_boundaries.csv'])
        if cell_boundaries_path:
            merscope_data["cell_boundaries_file"] = cell_boundaries_path.name

        cells_file = self._find_file(dataset_path, ['cells.csv', 'cells.csv.gz'])
        if cells_file:
            merscope_data["cells_file"] = cells_file.name
            try:
                is_gzipped = str(cells_file).endswith('.gz')
                if is_gzipped:
                    import gzip
                    with gzip.open(cells_file, 'rt') as f:
                        reader = csv.DictReader(f)
                        cell_count = sum(1 for _ in reader)
                else:
                    with open(cells_file) as f:
                        reader = csv.DictReader(f)
                        cell_count = sum(1 for _ in reader)
                merscope_data["cell_count"] = cell_count
            except Exception as e:
                logger.warning(f"Could not read cells file: {e}")

        return merscope_data

    def _find_file(self, directory: str, patterns: list[str]) -> Path | None:
        """Find a file matching any of the given patterns."""
        dir_path = Path(directory)
        for pattern in patterns:
            for f in dir_path.rglob(f"*{pattern}*"):
                if f.is_file():
                    return f
        return None