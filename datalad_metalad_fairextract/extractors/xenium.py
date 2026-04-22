"""Xenium dataset metadata extractor.

Extracts metadata from 10x Genomics Xenium data following SOPA input requirements.
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

logger = logging.getLogger('datalad_metalad_fairextract.xenium')


class XeniumDatasetExtractor(DatasetMetadataExtractor):
    """Extract metadata from Xenium directories following SOPA requirements.

    SOPA expects the following raw files:
    - transcripts.parquet: Transcript locations and names (REQUIRED)
    - experiment.xenium: Experiment metadata file
    - morphology_focus.ome.tif: Morphology focus image
    - he_image: Optional H&E image for tissue segmentation
    """

    extractor_name = "fairmeta_xenium"
    extractor_version = "1.0.0"

    XENIUM_PATTERNS = ['transcripts.parquet', 'experiment.xenium', 'morphology_focus']

    @staticmethod
    def get_id() -> UUID:
        return UUID("f6a7b8c9-0d1e-2f3a-4b5c-6d7e8f9a0b1c")

    @staticmethod
    def get_version() -> str:
        return "1.0.0"

    @staticmethod
    def get_data_output_category() -> DataOutputCategory:
        return DataOutputCategory.IMMEDIATE

    def get_required_content(self) -> bool:
        return True

    def extract(self, _=None) -> ExtractorResult:
        """Extract Xenium metadata from the directory."""
        metadata = {
            "$schema": "https://datalad-metalad-fairmeta.github.io/schemas/xenium.schema.json",
            "schema_version": "1.0.0"
        }
        warnings = []
        errors = []

        dataset_path = str(self.dataset.path)
        logger.info(f"Extracting Xenium metadata from: {dataset_path}")

        try:
            xenium_metadata = self._extract_xenium_metadata(dataset_path)
            metadata.update(xenium_metadata)

            if not xenium_metadata.get("transcript_file"):
                errors.append("No Xenium transcript file (transcripts.parquet) found in directory")
        except Exception as e:
            errors.append(f"Failed to extract Xenium metadata: {str(e)}")

        validation_errors = validate_metadata(metadata, "xenium")
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

    def _extract_xenium_metadata(self, dataset_path: str) -> dict[str, Any]:
        """Extract Xenium metadata from SOPA raw files."""
        xenium_data = {}
        source_files = []

        transcripts_file = self._find_file(dataset_path, ['transcripts.parquet'])
        if transcripts_file:
            source_files.append(str(transcripts_file))
            xenium_data["transcript_file"] = transcripts_file.name
            try:
                import pyarrow.parquet as pq
                table = pq.read_table(transcripts_file)
                xenium_data["transcript_count"] = table.num_rows
                xenium_data["transcript_columns"] = table.column_names
            except ImportError:
                logger.warning("pyarrow not available, cannot read transcript count")
            except Exception as e:
                logger.warning(f"Could not read transcripts.parquet: {e}")

        experiment_file = self._find_file(dataset_path, ['experiment.xenium'])
        if experiment_file:
            source_files.append(str(experiment_file))
            xenium_data["experiment_file"] = experiment_file.name

        morphology_file = self._find_file(dataset_path, ['morphology_focus.ome.tif', 'morphology_focus.ome.tiff'])
        if morphology_file:
            source_files.append(str(morphology_file))
            xenium_data["morphology_file"] = morphology_file.name
            try:
                import tifffile
                with tifffile.TiffFile(morphology_file) as tif:
                    if tif.pages:
                        page = tif.pages[0]
                        xenium_data["morphology_width"] = page.imagewidth
                        xenium_data["morphology_height"] = page.imagelength
                        xenium_data["morphology_channels"] = page.samplesperpixel
            except ImportError:
                logger.warning("tifffile not available, cannot read image dimensions")
            except Exception as e:
                logger.warning(f"Could not read morphology image: {e}")

        he_image_path = Path(dataset_path) / 'he_image'
        if he_image_path.exists():
            if he_image_path.is_file():
                xenium_data["he_image_file"] = he_image_path.name
            elif he_image_path.is_dir():
                he_files = list(he_image_path.glob('*'))
                if he_files:
                    xenium_data["he_image_directory"] = "he_image"
                    xenium_data["he_image_files"] = len(he_files)

        cell_boundaries_path = self._find_file(dataset_path, ['cell_boundaries.parquet'])
        if cell_boundaries_path:
            source_files.append(str(cell_boundaries_path))
            xenium_data["cell_boundaries_file"] = cell_boundaries_path.name

        nucleus_labels_path = self._find_file(dataset_path, ['nucleus_labels.parquet'])
        if nucleus_labels_path:
            source_files.append(str(nucleus_labels_path))
            xenium_data["nucleus_labels_file"] = nucleus_labels_path.name

        cell_labels_path = self._find_file(dataset_path, ['cell_labels.parquet'])
        if cell_labels_path:
            source_files.append(str(cell_labels_path))
            xenium_data["cell_labels_file"] = cell_labels_path.name

        return xenium_data

    def _find_file(self, directory: str, patterns: list[str]) -> Path | None:
        """Find a file matching any of the given patterns."""
        dir_path = Path(directory)
        for pattern in patterns:
            for f in dir_path.rglob(f"*{pattern}*"):
                if f.is_file():
                    return f
        return None