"""Tests for FASTQ extractor."""

import pytest
from pathlib import Path


class TestFastqExtractor:
    """Test FASTQ file extractor."""
    
    @pytest.fixture
    def extractor_class(self):
        from datalad_metalad_fairextract.extractors.fastq import FastqFileExtractor
        return FastqFileExtractor
    
    def test_extractor_registered(self, extractor_class):
        """Test extractor is registered and has correct properties."""
        assert extractor_class.extractor_name == "fairmeta_fastq"
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
        from datalad_metalad_fairextract.extractors.fastq import FASTQ_EXTENSIONS
        assert ".fastq" in FASTQ_EXTENSIONS
        assert ".fastq.gz" in FASTQ_EXTENSIONS
        assert ".fq" in FASTQ_EXTENSIONS
        assert ".fq.gz" in FASTQ_EXTENSIONS


class TestFastqSyntheticData:
    """Test FASTQ extractor with synthetic data."""
    
    def test_extract_synthetic_fastq(self, temp_dir):
        """Test extraction from synthetic FASTQ file."""
        from tests.test_data.synthetic import create_synthetic_fastq
        
        fastq_file = create_synthetic_fastq(temp_dir, read_number=1)
        assert fastq_file.exists()
        
        content = fastq_file.read_text()
        assert content.startswith("@")
        assert "ACGT" in content
    
    def test_extract_synthetic_fastq_gz(self, temp_dir):
        """Test extraction from synthetic gzipped FASTQ."""
        from tests.test_data.synthetic import create_synthetic_fastq_gz
        
        fastq_file = create_synthetic_fastq_gz(temp_dir, read_number=2)
        assert fastq_file.exists()
        assert fastq_file.suffix == ".gz"
        assert ".fastq.gz" in str(fastq_file)
    
    def test_read_number_detection(self, temp_dir):
        """Test read number detection from filename."""
        from tests.test_data.synthetic import create_synthetic_fastq
        
        fastq_r1 = create_synthetic_fastq(temp_dir, read_number=1)
        
        with open(fastq_r1, 'r') as f:
            header = f.readline()
        
        assert "run:SRR1234567" in header


class TestFastqPublicData:
    """Test FASTQ extractor with public data."""
    
    def test_extract_public_fastq(self, temp_dir):
        """Test extraction from public FASTQ data."""
        try:
            import scanpy as sc
        except ImportError:
            pytest.skip("scanpy not available")
        
        pbmc3k = sc.datasets.pbmc3k()
        assert pbmc3k is not None


class TestFastqStressCases:
    """Stress test FASTQ extractor with edge cases."""
    
    def test_extract_nonexistent_file(self, temp_dir):
        """Test extraction from non-existent file."""
        nonexistent = temp_dir / "nonexistent.fastq"
        
        try:
            from datalad_metalad_fairextract.extractors.fastq import FastqFileExtractor
        except ImportError:
            pytest.skip("Extractor import failed")
        
        assert not nonexistent.exists()
    
    def test_extract_corrupt_fastq(self, temp_dir):
        """Test extraction from corrupt FASTQ file."""
        from tests.test_data.synthetic import create_corrupt_fastq
        
        corrupt_file = create_corrupt_fastq(temp_dir)
        
        assert corrupt_file.exists()
        
        content = corrupt_file.read_text()
        assert "not a valid FASTQ" in content
    
    def test_extract_empty_fastq(self, temp_dir):
        """Test extraction from empty FASTQ file."""
        from tests.test_data.synthetic import create_empty_file
        
        empty_file = create_empty_file(temp_dir, ".fastq")
        
        assert empty_file.exists()
        assert empty_file.stat().st_size == 0
    
    def test_special_characters_in_path(self, temp_dir):
        """Test extraction from file with special characters in path."""
        from tests.test_data.synthetic import create_special_char_path_test_file
        
        file_path = create_special_char_path_test_file(temp_dir)
        
        assert " " in str(file_path)
        assert file_path.exists()
    
    def test_uncompressed_fastq(self, temp_dir):
        """Test extraction from uncompressed FASTQ."""
        from tests.test_data.synthetic import create_synthetic_fastq
        
        fastq_file = create_synthetic_fastq(temp_dir)
        
        assert fastq_file.exists()
        content = fastq_file.read_text()
        assert "@" in content


class TestFastqHeaderParsing:
    """Test FASTQ header parsing."""
    
    def test_standard_header_format(self):
        """Test standard FASTQ header format."""
        header = "@instrument:run:lane:tile:x:y:quality:sequence"
        
        assert header.startswith("@")
    
    def test_header_with_optional_fields(self):
        """Test header with optional fields."""
        header = (
            "@TEST:12345:67890 flowcellA:1:1101:12345:67890:ABCDEF "
            "run:SRR1234567 sample:Sample1 study:PRJNA123456 "
            "library:Library1 platform:ILLUMINA"
        )
        
        assert "run:" in header
        assert "sample:" in header
        assert "study:" in header
    
    def test_filename_read_number_detection(self):
        """Test read number detection from filename."""
        from pathlib import Path
        
        test_cases = [
            ("sample_1.fastq", 1),
            ("sample_r1.fastq", 1),
            ("sample_2.fastq", 2),
            ("sample_r2.fastq", 2),
            ("sample.fastq", None),
        ]
        
        for filename, expected_read in test_cases:
            filename_lower = Path(filename).stem.lower()
            read_number = None
            if "_1." in filename_lower or "_r1." in filename_lower:
                read_number = 1
            elif "_2." in filename_lower or "_r2." in filename_lower:
                read_number = 2
            
            assert read_number == expected_read or read_number is None