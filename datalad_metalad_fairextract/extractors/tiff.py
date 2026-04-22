"""TIFF file metadata extractor.

Extracts metadata from general TIFF files (not OME-TIFF).
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

logger = logging.getLogger('datalad_metalad_fairextract.tiff')

TIFF_EXTENSIONS = ['.tif', '.tiff']

TIFF_TAGS = {
    254: 'NewSubfileType',
    256: 'ImageWidth',
    257: 'ImageLength',
    258: 'BitsPerSample',
    259: 'Compression',
    262: 'PhotometricInterpretation',
    263: 'Threshholding',
    264: 'CellWidth',
    265: 'CellLength',
    266: 'FillOrder',
    269: 'DocumentName',
    270: 'ImageDescription',
    271: 'Make',
    272: 'Model',
    273: 'StripOffsets',
    274: 'Orientation',
    277: 'SamplesPerPixel',
    278: 'RowsPerStrip',
    279: 'StripByteCounts',
    280: 'MinSampleValue',
    281: 'MaxSampleValue',
    282: 'XResolution',
    283: 'YResolution',
    284: 'PlanarConfiguration',
    285: 'PageName',
    286: 'XPosition',
    287: 'YPosition',
    288: 'FreeOffsets',
    289: 'FreeByteCounts',
    290: 'GrayResponseUnit',
    291: 'GrayResponseCurve',
    292: 'T4Options',
    293: 'T6Options',
    296: 'ResolutionUnit',
    297: 'PageNumber',
    301: 'TransferFunction',
    305: 'Software',
    306: 'DateTime',
    315: 'Artist',
    316: 'HostComputer',
    317: 'Predictor',
    318: 'WhitePoint',
    319: 'PrimaryChromaticities',
    320: 'ColorMap',
    321: 'HalftoneHints',
    322: 'TileWidth',
    323: 'TileLength',
    324: 'TileOffsets',
    325: 'TileByteCounts',
    332: 'InkSet',
    333: 'InkNames',
    334: 'NumberOfInks',
    336: 'DotRange',
    337: 'TargetPrinter',
    338: 'ExtraSamples',
    339: 'SampleFormat',
    340: 'SMinSampleValue',
    341: 'SMaxSampleValue',
    343: 'ClippingPath',
    344: 'IPTCNavigation',
    346: 'EXIFIFD',
    36867: 'DateTimeOriginal',
    36868: 'DateTimeDigitized',
}

PHOTOMETRIC_INTERPRETATION_MAP = {
    0: 'WhiteIsZero',
    1: 'BlackIsZero',
    2: 'RGB',
    3: 'Palette',
    4: 'Transparency Mask',
    5: 'CMYK',
    6: 'YCbCr',
    8: 'CIELab',
    9: 'ICCLab',
    10: 'ITULab',
    32803: ' CFA',
    32845: 'LogL',
    32892: 'PixarLogL',
    32893: 'Spectrum',
    32894: 'TIFF_X',
    32895: 'XYZ',
    32896: 'CMYK',
    32897: 'CIELab_OETF',
    32898: 'CIELab_encoding',
    65535: 'DeepGray',
}

COMPRESSION_MAP = {
    1: 'Uncompressed',
    2: 'CCITT Group 3',
    3: 'CCITT Group 4',
    5: 'LZW',
    6: 'JPEG_old',
    7: 'JPEG_new',
    8: 'Deflate',
    32771: 'PackBits',
    32773: 'PackBits',
    32946: 'Deflate',
    34676: 'SGILog',
    34677: 'SGILog24',
}


class TiffFileExtractor(FileMetadataExtractor):
    """Extract metadata from TIFF image files.

    This extractor reads TIFF IFD tags and extracts technical metadata
    about the image. It does not handle OME-TIFF files (use OmeTiffFileExtractor).
    """

    extractor_name = "fairmeta_tiff"
    extractor_version = "1.0.0"

    @staticmethod
    def get_id() -> UUID:
        return UUID("a1b2c3d4-5e6f-4a7b-8c9d-e0f1a2b3c4d5")

    @staticmethod
    def get_version() -> str:
        return "1.0.0"

    @staticmethod
    def get_data_output_category() -> DataOutputCategory:
        return DataOutputCategory.IMMEDIATE

    def is_content_required(self) -> bool:
        return True

    def extract(self, _=None) -> ExtractorResult:
        """Extract TIFF metadata from the file."""
        metadata = {
            "$schema": "https://datalad-metalad-fairmeta.github.io/schemas/tiff.schema.json",
            "schema_version": "1.0.0"
        }
        warnings = []
        errors = []

        file_path = self.file_info.path
        logger.info(f"Extracting TIFF metadata from: {file_path}")

        try:
            tiff_metadata = self._extract_tiff_tags(file_path)
            metadata.update(tiff_metadata)
        except ImportError:
            warnings.append("tifffile library not available, using basic TIFF parsing")
            try:
                tiff_metadata = self._extract_basic_tiff(file_path)
                metadata.update(tiff_metadata)
            except Exception as e:
                errors.append(f"Failed to parse TIFF file: {str(e)}")
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
            errors.append(f"Failed to extract TIFF metadata: {str(e)}")
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

        validation_errors = validate_metadata(metadata, "tiff")
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

    def _extract_tiff_tags(self, file_path: str) -> dict[str, Any]:
        """Extract TIFF metadata using tifffile library."""
        import tifffile

        with tifffile.TiffFile(file_path) as tif:
            page = tif.pages[0]

            metadata = {
                "image_name": Path(file_path).name,
                "width": page.imagewidth,
                "height": page.imagelength,
                "bits_per_sample": page.bitspersample,
                "samples_per_pixel": page.samplesperpixel,
            }

            if page.description:
                metadata["image_description"] = page.description

            if page.compression:
                metadata["compression"] = COMPRESSION_MAP.get(
                    page.compression, str(page.compression)
                )

            if page.photometric:
                metadata["photometric_interpretation"] = PHOTOMETRIC_INTERPRETATION_MAP.get(
                    page.photometric, str(page.photometric)
                )

            if page.planarconfig:
                metadata["planar_configuration"] = "Planar" if page.planarconfig == 2 else "Chunky"

            if page.x_resolution:
                metadata["x_resolution"] = float(page.x_resolution)
            if page.y_resolution:
                metadata["y_resolution"] = float(page.y_resolution)

            if page.resolutionunit:
                units = {1: 'None', 2: 'Inch', 3: 'Centimeter'}
                metadata["resolution_unit"] = units.get(page.resolutionunit, str(page.resolutionunit))

            if page.software:
                metadata["software"] = page.software

            if page.datetime:
                metadata["datetime"] = page.datetime

            if page.artist:
                metadata["artist"] = page.artist

            if page.copyright:
                metadata["copyright"] = page.copyright

            if page.tilewidth:
                metadata["tile_width"] = page.tilewidth
            if page.tilelength:
                metadata["tile_height"] = page.tilelength

            if page.sampleformat:
                formats = {1: 'Unsigned', 2: 'Signed', 3: 'Float', 6: 'Complex'}
                metadata["sample_format"] = formats.get(page.sampleformat, str(page.sampleformat))

            return metadata

    def _extract_basic_tiff(self, file_path: str) -> dict[str, Any]:
        """Extract basic TIFF metadata without tifffile library."""
        import struct

        metadata = {
            "image_name": Path(file_path).name,
        }

        with open(file_path, 'rb') as f:
            f.seek(0)
            header = f.read(8)

            if header[:2] != b'II' and header[:2] != b'MM':
                raise ValueError("Not a valid TIFF file")

            endian = '<' if header[:2] == b'II' else '>'

            if endian == '<':
                byte_order = 'little'
            else:
                byte_order = 'big'

            tiff_version = struct.unpack(endian + 'H', header[2:4])[0]

            if tiff_version != 42:
                raise ValueError(f"Invalid TIFF version: {tiff_version}")

            ifd_offset = struct.unpack(endian + 'I', header[4:8])[0]
            f.seek(ifd_offset)

            num_entries = struct.unpack(endian + 'H', f.read(2))[0]

            width = None
            height = None
            bits_per_sample = None
            compression = None
            photometric = None

            for _ in range(num_entries):
                entry = f.read(12)
                tag = struct.unpack(endian + 'H', entry[0:2])[0]
                dtype = struct.unpack(endian + 'H', entry[2:4])[0]
                count = struct.unpack(endian + 'I', entry[4:8])[0]
                value_offset = struct.unpack(endian + 'I', entry[8:12])[0]

                if tag == 256:
                    width = value_offset if count == 1 else None
                elif tag == 257:
                    height = value_offset if count == 1 else None
                elif tag == 258:
                    bits_per_sample = value_offset if count == 1 else count
                elif tag == 259:
                    compression = value_offset if count == 1 else None
                elif tag == 262:
                    photometric = value_offset if count == 1 else None

            if width:
                metadata["width"] = width
            if height:
                metadata["height"] = height
            if bits_per_sample:
                metadata["bits_per_sample"] = bits_per_sample
            if compression:
                metadata["compression"] = COMPRESSION_MAP.get(compression, str(compression))
            if photometric:
                metadata["photometric_interpretation"] = PHOTOMETRIC_INTERPRETATION_MAP.get(
                    photometric, str(photometric)
                )

        return metadata
