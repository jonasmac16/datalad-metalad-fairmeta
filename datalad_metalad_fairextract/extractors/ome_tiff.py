"""OME-TIFF file metadata extractor.

Extracts metadata from OME-TIFF files following the OME Data Model.
"""

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

logger = logging.getLogger('datalad_metalad_fairextract.ome_tiff')

OME_TIFF_EXTENSIONS = ['.ome.tiff', '.ome.tif', '.ome.tf2', '.ome.tf8', '.ome.btf']


class OmeTiffFileExtractor(FileMetadataExtractor):
    """Extract metadata from OME-TIFF files.

    This extractor reads OME-XML metadata embedded in TIFF files
    and extracts comprehensive image metadata following the OME Data Model.
    """

    extractor_name = "fairmeta_ome_tiff"
    extractor_version = "1.0.0"

    @staticmethod
    def get_id() -> UUID:
        return UUID("b2c3d4e5-6f7a-8b9c-0d1e-2f3a4b5c6d7e")

    @staticmethod
    def get_version() -> str:
        return "1.0.0"

    @staticmethod
    def get_data_output_category() -> DataOutputCategory:
        return DataOutputCategory.IMMEDIATE

    def is_content_required(self) -> bool:
        return True

    def extract(self, _=None) -> ExtractorResult:
        """Extract OME-TIFF metadata from the file."""
        metadata = {
            "$schema": "https://datalad-metalad-fairmeta.github.io/schemas/ome_tiff.schema.json",
            "schema_version": "1.0.0"
        }
        warnings = []
        errors = []

        file_path = self.file_info.path
        logger.info(f"Extracting OME-TIFF metadata from: {file_path}")

        try:
            ome_metadata = self._extract_ome_metadata(file_path)
            metadata.update(ome_metadata)
        except ImportError:
            errors.append("ome-types library not available. Install with: pip install ome-types")
            return create_extraction_result(
                metadata=metadata,
                extractor_version=self.extractor_version,
                extraction_parameter=self.parameter,
                success=False,
                result_type="file",
                validation_errors=errors,
                warnings=warnings,
                provenance=create_provenance(
                    self.extractor_name,
                    self.extractor_version,
                    [file_path]
                )
            )
        except Exception as e:
            errors.append(f"Failed to parse OME-TIFF file: {str(e)}")
            return create_extraction_result(
                metadata=metadata,
                extractor_version=self.extractor_version,
                extraction_parameter=self.parameter,
                success=False,
                result_type="file",
                validation_errors=errors,
                warnings=warnings,
                provenance=create_provenance(
                    self.extractor_name,
                    self.extractor_version,
                    [file_path]
                )
            )

        validation_errors = validate_metadata(metadata, "ome_tiff")
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

    def _extract_ome_metadata(self, file_path: str) -> dict[str, Any]:
        """Extract OME metadata using ome-types library."""
        from ome_types import from_tiff

        ome = from_tiff(file_path)
        image = ome.images[0] if ome.images else None

        if not image:
            raise ValueError("No image found in OME-TIFF file")

        metadata = {}

        metadata["Image"] = {
            "ID": image.id,
            "Name": image.name or Path(file_path).stem,
        }

        if image.acquisition_date:
            metadata["Image"]["AcquisitionDate"] = image.acquisition_date.isoformat()

        if image.description:
            metadata["Image"]["Description"] = image.description

        pixels = image.pixels
        if pixels:
            pixels_data = {
                "ID": pixels.id,
                "DimensionOrder": pixels.dimension_order.value if pixels.dimension_order else None,
                "Type": pixels.type.value if pixels.type else None,
                "SizeX": pixels.size_x,
                "SizeY": pixels.size_y,
                "SizeZ": pixels.size_z,
                "SizeT": pixels.size_t,
                "SizeC": pixels.size_c,
                "BigEndian": pixels.big_endian,
            }

            if pixels.physical_size_x is not None:
                pixels_data["PhysicalSizeX"] = pixels.physical_size_x
            if pixels.physical_size_y is not None:
                pixels_data["PhysicalSizeY"] = pixels.physical_size_y
            if pixels.physical_size_z is not None:
                pixels_data["PhysicalSizeZ"] = pixels.physical_size_z

            if pixels.physical_size_x_unit:
                pixels_data["PhysicalSizeXUnit"] = pixels.physical_size_x_unit
            if pixels.physical_size_y_unit:
                pixels_data["PhysicalSizeYUnit"] = pixels.physical_size_y_unit
            if pixels.physical_size_z_unit:
                pixels_data["PhysicalSizeZUnit"] = pixels.physical_size_z_unit

            channels = []
            for ch in pixels.channels:
                channel_data = {
                    "ID": ch.id,
                }
                if ch.name:
                    channel_data["Name"] = ch.name
                if ch.color:
                    channel_data["Color"] = ch.color
                if ch.fluor:
                    channel_data["Fluor"] = ch.fluor
                if ch.emission_wavelength:
                    channel_data["EmissionWavelength"] = ch.emission_wavelength
                if ch.excitation_wavelength:
                    channel_data["ExcitationWavelength"] = ch.excitation_wavelength
                if ch.nd_filter:
                    channel_data["NDFilter"] = ch.nd_filter
                if ch.pockel_cell_setting:
                    channel_data["PockelCellSetting"] = ch.pockel_cell_setting
                channels.append(channel_data)

            if channels:
                pixels_data["Channels"] = channels

            metadata["Image"]["Pixels"] = pixels_data

        if image.instrument:
            instrument_data = {
                "ID": image.instrument.id,
            }

            if image.instrument.microscope:
                instrument_data["Microscope"] = {
                    "ID": image.instrument.microscope.id,
                    "Manufacturer": image.instrument.microscope.manufacturer,
                    "Model": image.instrument.microscope.model,
                    "Type": image.instrument.microscope.type,
                    "SerialNumber": image.instrument.microscope.serial_number,
                }

            if image.instrument.objectives:
                objectives = []
                for obj in image.instrument.objectives:
                    obj_data = {
                        "ID": obj.id,
                        "Manufacturer": obj.manufacturer,
                        "Model": obj.model,
                    }
                    if obj.lens_na:
                        obj_data["LensNA"] = obj.lens_na
                    if obj.working_distance:
                        obj_data["WorkingDistance"] = obj.working_distance
                    if obj.nominal_magnification:
                        obj_data["NominalMagnification"] = obj.nominal_magnification
                    objectives.append(obj_data)
                instrument_data["Objectives"] = objectives

            metadata["Instrument"] = instrument_data

        return metadata
