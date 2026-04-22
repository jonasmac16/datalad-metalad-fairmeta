"""CosMx (Nanostring/Bruker) dataset metadata extractor.

Extracts metadata from NanoString CosMx data following SOPA input requirements.
CosMx data must be exported as flat files from AtomX (not the native format).
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

logger = logging.getLogger('datalad_metalad_fairextract.cosmx')


class CosMxDatasetExtractor(DatasetMetadataExtractor):
    """Extract metadata from CosMx directories following SOPA requirements.

    SOPA expects the following raw files (exported from AtomX):
    - *tx_file.csv.gz: Transcript locations and names (REQUIRED)
    - *fov_positions_file.csv: FOV (Field of View) positions
    - Morphology2D/: Directory containing FOV morphology images (TIF format)
    - *metadata.csv.gz: Cell metadata
    - *counts.csv.gz: Expression counts matrix
    - *-polygons.csv.gz: Cell polygon boundaries
    - CellLabels/: Directory containing cell segmentation labels
    """

    extractor_name = "fairmeta_cosmx"
    extractor_version = "1.0.0"

    COSMX_PATTERNS = ['tx_file', 'fov_positions', 'counts', 'metadata', 'polygons']

    @staticmethod
    def get_id() -> UUID:
        return UUID("e5f6a7b8-9c0d-1e2f-3a4b-5c6d7e8f9a0b")

    @staticmethod
    def get_version() -> str:
        return "1.0.0"

    @staticmethod
    def get_data_output_category() -> DataOutputCategory:
        return DataOutputCategory.IMMEDIATE

    def get_required_content(self) -> bool:
        return True

    def extract(self, _=None) -> ExtractorResult:
        """Extract CosMx metadata from the directory."""
        metadata = {
            "$schema": "https://datalad-metalad-fairmeta.github.io/schemas/cosmx.schema.json",
            "schema_version": "1.0.0"
        }
        warnings = []
        errors = []

        dataset_path = str(self.dataset.path)
        logger.info(f"Extracting CosMx metadata from: {dataset_path}")

        try:
            cosmx_metadata = self._extract_cosmx_metadata(dataset_path)
            metadata.update(cosmx_metadata)

            if not cosmx_metadata.get("transcript_file"):
                errors.append("No CosMx transcript file (*tx_file.csv.gz) found in directory")
        except Exception as e:
            errors.append(f"Failed to extract CosMx metadata: {str(e)}")

        validation_errors = validate_metadata(metadata, "cosmx")
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

    def _extract_cosmx_metadata(self, dataset_path: str) -> dict[str, Any]:
        """Extract CosMx metadata from SOPA raw files."""
        cosmx_data = {}
        source_files = []

        tx_file = self._find_file(dataset_path, ['_tx_file.csv.gz', '_tx_file.csv'])
        if tx_file:
            source_files.append(str(tx_file))
            cosmx_data["transcript_file"] = tx_file.name
            try:
                transcript_count = self._count_lines_gzip(tx_file) - 1
                cosmx_data["transcript_count"] = transcript_count
            except Exception as e:
                logger.warning(f"Could not count transcripts: {e}")

            try:
                with gzip.open(tx_file, 'rt') as f:
                    reader = csv.DictReader(f)
                    first_row = next(reader, None)
                    if first_row:
                        column_mapping = {
                            'gene': 'gene_column',
                            'x': 'x_column',
                            'y': 'y_column',
                            'fov': 'fov_column',
                            'z': 'z_column',
                        }
                        for csv_col, meta_field in column_mapping.items():
                            if csv_col in first_row:
                                cosmx_data[meta_field] = csv_col
            except Exception as e:
                logger.warning(f"Could not read transcript file header: {e}")

        fov_file = self._find_file(dataset_path, ['_fov_positions_file.csv', '_fov_positions_file.csv.gz'])
        if fov_file:
            source_files.append(str(fov_file))
            cosmx_data["fov_positions_file"] = fov_file.name
            try:
                is_gzipped = str(fov_file).endswith('.gz')
                if is_gzipped:
                    with gzip.open(fov_file, 'rt') as f:
                        reader = csv.DictReader(f)
                        fov_count = sum(1 for _ in reader)
                else:
                    with open(fov_file) as f:
                        reader = csv.DictReader(f)
                        fov_count = sum(1 for _ in reader)
                cosmx_data["fov_count"] = fov_count

                if is_gzipped:
                    with gzip.open(fov_file, 'rt') as f:
                        reader = csv.DictReader(f)
                        first_row = next(reader, None)
                else:
                    with open(fov_file) as f:
                        reader = csv.DictReader(f)
                        first_row = next(reader, None)
                if first_row:
                    field_mapping = {
                        'fov': 'fov_id_column',
                        'x': 'x_column',
                        'y': 'y_column',
                    }
                    for csv_field, meta_field in field_mapping.items():
                        if csv_field in first_row:
                            cosmx_data[f"fov_{meta_field}"] = csv_field
            except Exception as e:
                logger.warning(f"Could not read FOV positions file: {e}")

        metadata_file = self._find_file(dataset_path, ['_metadata.csv.gz', '_metadata.csv'])
        if metadata_file:
            source_files.append(str(metadata_file))
            cosmx_data["cell_metadata_file"] = metadata_file.name
            try:
                cell_count = self._count_lines_gzip(metadata_file) - 1
                cosmx_data["cell_count"] = cell_count

                with gzip.open(metadata_file, 'rt') as f:
                    reader = csv.DictReader(f)
                    first_row = next(reader, None)
                    if first_row:
                        standard_fields = ['cell_id', 'Cell_ID', 'cell_label', 'cell_type', 'cluster']
                        available_fields = [f for f in standard_fields if f in first_row]
                        if available_fields:
                            cosmx_data["cell_id_column"] = available_fields[0]
            except Exception as e:
                logger.warning(f"Could not read cell metadata file: {e}")

        counts_file = self._find_file(dataset_path, ['_counts.csv.gz', '_counts.csv'])
        if counts_file:
            source_files.append(str(counts_file))
            cosmx_data["counts_file"] = counts_file.name
            try:
                if str(counts_file).endswith('.gz'):
                    with gzip.open(counts_file, 'rt') as f:
                        reader = csv.reader(f)
                        header = next(reader)
                        cosmx_data["gene_count"] = len(header) - 1
                else:
                    with open(counts_file) as f:
                        reader = csv.reader(f)
                        header = next(reader)
                        cosmx_data["gene_count"] = len(header) - 1
            except Exception as e:
                logger.warning(f"Could not read counts file: {e}")

        polygons_file = self._find_file(dataset_path, ['-polygons.csv.gz', '_polygons.csv.gz'])
        if polygons_file:
            source_files.append(str(polygons_file))
            cosmx_data["polygons_file"] = polygons_file.name

        morphology_dir = Path(dataset_path) / 'Morphology2D'
        if morphology_dir.exists() and morphology_dir.is_dir():
            cosmx_data["morphology_directory"] = "Morphology2D"
            try:
                tif_files = list(morphology_dir.glob('*.tif')) + list(morphology_dir.glob('*.tiff'))
                cosmx_data["morphology_image_count"] = len(tif_files)
                if tif_files:
                    cosmx_data["morphology_image_extension"] = ".tif"
            except Exception as e:
                logger.warning(f"Could not read Morphology2D directory: {e}")

        celllabels_dir = Path(dataset_path) / 'CellLabels'
        if celllabels_dir.exists() and celllabels_dir.is_dir():
            cosmx_data["celllabels_directory"] = "CellLabels"
            try:
                label_files = list(celllabels_dir.glob('*.tif')) + list(celllabels_dir.glob('*.tiff'))
                cosmx_data["celllabel_count"] = len(label_files)
            except Exception as e:
                logger.warning(f"Could not read CellLabels directory: {e}")

        return cosmx_data

    def _count_lines_gzip(self, file_path: Path) -> int:
        """Count lines in a gzipped file."""
        count = 0
        try:
            with gzip.open(file_path, 'rt') as f:
                for _ in f:
                    count += 1
        except Exception:
            count = 0
        return count

    def _find_file(self, directory: str, patterns: list[str]) -> Path | None:
        """Find a file matching any of the given patterns."""
        dir_path = Path(directory)
        for pattern in patterns:
            for f in dir_path.rglob(f"*{pattern}*"):
                if f.is_file():
                    return f
        return None