"""FASTQ file metadata extractor.

Extracts metadata from FASTQ sequencing files.
"""

import gzip
import logging
from pathlib import Path
from typing import Any
from uuid import UUID

from datalad_metalad.extractors.base import (
    DataOutputCategory,
    ExtractorResult,
    FileMetadataExtractor,
)

from .base import create_extraction_result, create_provenance, validate_metadata

logger = logging.getLogger('datalad_metalad_fairextract.fastq')

FASTQ_EXTENSIONS = ['.fastq', '.fastq.gz', '.fq', '.fq.gz']


class FastqFileExtractor(FileMetadataExtractor):
    """Extract metadata from FASTQ sequencing files.

    This extractor reads the header of FASTQ files to extract
    metadata following SRA/ENA conventions.
    """

    extractor_name = "fairmeta_fastq"
    extractor_version = "1.0.0"

    @staticmethod
    def get_id() -> UUID:
        return UUID("b8c9d0e1-2f3a-4b5c-6d7e-8f9a0b1c2d3e")

    @staticmethod
    def get_version() -> str:
        return "1.0.0"

    @staticmethod
    def get_data_output_category() -> DataOutputCategory:
        return DataOutputCategory.IMMEDIATE

    def is_content_required(self) -> bool:
        return True

    def extract(self, _=None) -> ExtractorResult:
        """Extract FASTQ metadata from the file."""
        metadata = {
            "$schema": "https://datalad-metalad-fairmeta.github.io/schemas/fastq.schema.json",
            "schema_version": "1.0.0"
        }
        warnings = []
        errors = []

        file_path = self.file_info.path
        logger.info(f"Extracting FASTQ metadata from: {file_path}")

        try:
            fastq_metadata = self._extract_fastq_metadata(file_path)
            metadata.update(fastq_metadata)

            metadata['file_size'] = self.file_info.byte_size

        except Exception as e:
            errors.append(f"Failed to extract FASTQ metadata: {str(e)}")

        validation_errors = validate_metadata(metadata, "fastq")
        success = len(errors) == 0 and len(validation_errors) == 0

        return create_extraction_result(
            metadata=metadata,
            extractor_version=self.extractor_version,
            extraction_parameter=self.parameter,
            success=success,
            result_type="file",
            validation_errors=validation_errors,
            warnings=warnings,
            provenance=create_provenance(
                self.extractor_name,
                self.extractor_version,
                [file_path]
            )
        )

    def _extract_fastq_metadata(self, file_path: str) -> dict[str, Any]:
        """Extract FASTQ metadata from header."""
        import csv

        metadata = {}
        is_gzipped = file_path.endswith('.gz')

        opener = gzip.open if is_gzipped else open

        with opener(file_path, 'rt') as f:
            header = f.readline().strip()

        if not header.startswith('@'):
            raise ValueError("Invalid FASTQ file: missing header")

        parts = header.split(' ')
        header_parts = parts[0].lstrip('@').split(':')

        metadata['filename'] = Path(file_path).name

        if len(header_parts) >= 5:
            metadata['instrument'] = header_parts[0]
            metadata['run_id'] = header_parts[1]

            if len(header_parts) >= 6:
                try:
                    metadata['lane'] = int(header_parts[4])
                except ValueError:
                    pass

        for part in parts[1:]:
            if ':' in part:
                key, value = part.split(':', 1)
                key = key.lower()

                if key == 'run':
                    metadata['run_id'] = value
                elif key == 'sample':
                    metadata['sample_id'] = value
                elif key == 'study':
                    metadata['study_id'] = value
                elif key == 'library':
                    metadata['library_name'] = value
                elif key == 'lib':
                    metadata['library_name'] = value
                elif key == 'platform':
                    metadata['instrument'] = value
                elif key == 'flowcell':
                    metadata['flowcell'] = value
                elif key == 'fc':
                    metadata['flowcell'] = value

        filename_lower = Path(file_path).stem.lower()
        if '_1.' in filename_lower or '_r1.' in filename_lower:
            metadata['read_number'] = 1
        elif '_2.' in filename_lower or '_r2.' in filename_lower:
            metadata['read_number'] = 2

        return metadata
