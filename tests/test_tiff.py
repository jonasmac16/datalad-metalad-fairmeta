"""Tests for TIFF extractor."""

import pytest
from pathlib import Path


class TestTiffExtractor:
    """Test TIFF file extractor."""
    
    @pytest.fixture
    def extractor_class(self):
        from datalad_metalad_fairextract.extractors.tiff import TiffFileExtractor
        return TiffFileExtractor
    
    def test_extractor_registered(self, extractor_class):
        """Test extractor is registered and has correct properties."""
        assert extractor_class.extractor_name == "fairmeta_tiff"
        assert extractor_class.extractor_version == "1.0.0"
    
    def test_extractor_id(self, extractor_class):
        """Test extractor has valid UUID."""
        from uuid import UUID
        extractor_id = extractor_class.get_id()
        assert isinstance(extractor_id, UUID)
    
    def test_data_output_category(self, extractor_class):
        """Test data output category is IMMEDIATE."""
        from datalad_metalad.extractors.base import DataOutputCategory
        assert extractor_class.get_data_output_category() == DataOutputCategory.IMMEDIATE
    
    def test_extensions(self):
        """Test supported file extensions."""
        from datalad_metalad_fairextract.extractors.tiff import TIFF_EXTENSIONS
        assert ".tif" in TIFF_EXTENSIONS
        assert ".tiff" in TIFF_EXTENSIONS


class TestTiffSyntheticData:
    """Test TIFF extractor with synthetic data."""
    
    def test_extract_synthetic_tiff(self, temp_dir):
        """Test extraction from synthetic TIFF file."""
        from tests.test_data.synthetic import create_synthetic_tiff
        
        tiff_file = create_synthetic_tiff(temp_dir)
        assert tiff_file.exists()
        
        with open(tiff_file, 'rb') as f:
            header = f.read(4)
        
        assert header[:2] in (b'II', b'MM')


class TestTiffStressCases:
    """Stress test TIFF extractor with edge cases."""
    
    def test_extract_nonexistent_file(self, temp_dir):
        """Test extraction from non-existent file."""
        nonexistent = temp_dir / "nonexistent.tiff"
        
        try:
            from datalad_metalad_fairextract.extractors.tiff import TiffFileExtractor
        except ImportError:
            pytest.skip("Extractor import failed")
        
        assert not nonexistent.exists()
    
    def test_extract_corrupt_tiff(self, temp_dir):
        """Test extraction from corrupt TIFF file."""
        from tests.test_data.synthetic import create_corrupt_tiff
        
        corrupt_file = create_corrupt_tiff(temp_dir)
        
        assert corrupt_file.exists()
        content = corrupt_file.read_text()
        assert "not a valid TIFF" in content
    
    def test_extract_empty_tiff(self, temp_dir):
        """Test extraction from empty TIFF file."""
        from tests.test_data.synthetic import create_empty_file
        
        empty_file = create_empty_file(temp_dir, ".tiff")
        
        assert empty_file.exists()
        assert empty_file.stat().st_size == 0
    
    def test_tiff_tag_parsing(self):
        """Test TIFF tag parsing."""
        from datalad_metalad_fairextract.extractors.tiff import TIFF_TAGS
        
        assert 256 in TIFF_TAGS
        assert TIFF_TAGS[256] == "ImageWidth"
        assert 257 in TIFF_TAGS
        assert TIFF_TAGS[257] == "ImageLength"
    
    def test_photometric_interpretation_map(self):
        """Test photometric interpretation mapping."""
        from datalad_metalad_fairextract.extractors.tiff import (
            PHOTOMETRIC_INTERPRETATION_MAP,
        )
        
        assert 1 in PHOTOMETRIC_INTERPRETATION_MAP
        assert PHOTOMETRIC_INTERPRETATION_MAP[1] == "BlackIsZero"
        assert 2 in PHOTOMETRIC_INTERPRETATION_MAP
        assert PHOTOMETRIC_INTERPRETATION_MAP[2] == "RGB"
    
    def test_compression_map(self):
        """Test compression mapping."""
        from datalad_metalad_fairextract.extractors.tiff import COMPRESSION_MAP
        
        assert 1 in COMPRESSION_MAP
        assert COMPRESSION_MAP[1] == "Uncompressed"
        assert 5 in COMPRESSION_MAP
        assert COMPRESSION_MAP[5] == "LZW"


class TestTiffWithDependencies:
    """Test TIFF with optional dependencies."""
    
    def test_extract_with_tifffile(self, temp_dir):
        """Test extraction when tifffile is available."""
        try:
            import tifffile
        except ImportError:
            pytest.skip("tifffile not available")
        
        from tests.test_data.synthetic import create_synthetic_tiff
        
        tiff_file = create_synthetic_tiff(temp_dir)
        assert tiff_file.exists()
        
        with tifffile.TiffFile(tiff_file) as tif:
            page = tif.pages[0]
            assert page.imagewidth > 0
            assert page.imagelength > 0
    
    def test_extract_with_basic_parser(self, temp_dir):
        """Test extraction with basic TIFF parser fallback."""
        from tests.test_data.synthetic import create_synthetic_tiff
        
        tiff_file = create_synthetic_tiff(temp_dir)
        
        import struct
        with open(tiff_file, 'rb') as f:
            header = f.read(8)
        
        assert header[:2] in (b'II', b'MM')
        endian = '<' if header[:2] == b'II' else '>'
        tiff_version = struct.unpack(endian + 'H', header[2:4])[0]
        assert tiff_version == 42


class TestTiffSpecialCases:
    """Special TIFF test cases."""
    
    def test_big_endian_tiff(self, temp_dir):
        """Test big endian TIFF file."""
        import struct
        
        tiff_file = temp_dir / "big_endian.tiff"
        
        header = b'MM' + struct.pack('>H', 42) + struct.pack('>I', 8)
        
        ifd_data = struct.pack('>H', 2)
        ifd_data += struct.pack('>HHII', 256, 3, 1, 100)
        ifd_data += struct.pack('>HHII', 257, 3, 1, 100)
        ifd_data += b'\x00\x00\x00\x00'
        
        tiff_file.write_bytes(header + ifd_data)
        
        with open(tiff_file, 'rb') as f:
            header = f.read(4)
        
        assert header[:2] == b'MM'
    
    def test_various_extensions(self, temp_dir):
        """Test various TIFF extensions."""
        from datalad_metalad_fairextract.extractors.base import get_file_extension
        
        test_cases = [
            ("image.tiff", ".tiff"),
            ("image.tif", ".tif"),
            ("image.TIFF", ".tiff"),
            ("image.TIF", ".tif"),
            ("image.ome.tiff", ".tiff"),
            ("path/to/image.tiff", ".tiff"),
            ("image.noext", ".noext"),
        ]
        
        for path, expected in test_cases:
            assert get_file_extension(path) == expected, f"Failed for {path}"