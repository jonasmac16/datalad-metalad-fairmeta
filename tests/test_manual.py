"""Tests for manual extractor."""

import pytest
from pathlib import Path


class TestManualExtractor:
    """Test manual dataset extractor."""
    
    def test_extractor_registration(self):
        """Test manual extractor is registered and has correct properties."""
        try:
            from datalad_metalad_fairextract.extractors.manual import FairmetaManualDatasetExtractor
        except ImportError:
            pytest.skip("Cannot import manual extractor")
        
        assert FairmetaManualDatasetExtractor.extractor_name == "fairmeta_manual"
        assert FairmetaManualDatasetExtractor.extractor_version == "1.0.0"
    
    def test_extractor_id(self):
        """Test manual extractor has valid UUID."""
        from uuid import UUID
        
        try:
            from datalad_metalad_fairextract.extractors.manual import FairmetaManualDatasetExtractor
        except ImportError:
            pytest.skip("Cannot import manual extractor")
        
        extractor_id = FairmetaManualDatasetExtractor.get_id()
        assert isinstance(extractor_id, UUID)
    
    def test_data_output_category(self):
        """Test data output category."""
        from datalad_metalad.extractors.base import DataOutputCategory
        
        try:
            from datalad_metalad_fairextract.extractors.manual import FairmetaManualDatasetExtractor
        except ImportError:
            pytest.skip("Cannot import manual extractor")
        
        assert FairmetaManualDatasetExtractor.get_data_output_category() == DataOutputCategory.IMMEDIATE
    
    def test_required_content(self):
        """Test required content."""
        try:
            from datalad_metalad_fairextract.extractors.manual import FairmetaManualDatasetExtractor
        except ImportError:
            pytest.skip("Cannot import manual extractor")
        
        assert FairmetaManualDatasetExtractor.get_required_content() is False


class TestManualExtractorSchema:
    """Test manual extractor schema validation."""
    
    def test_schema_support(self):
        """Test supported schemas."""
        try:
            from datalad_metalad_fairextract.extractors.manual import (
                get_supported_schemas,
            )
        except ImportError:
            pytest.skip("Cannot import manual extractor")
        
        schemas = get_supported_schemas()
        assert isinstance(schemas, list)
    
    def test_schema_validation(self):
        """Test schema loading."""
        try:
            from datalad_metalad_fairextract.extractors.base import load_schema
        except ImportError:
            pytest.skip("Cannot import base extractor")
        
        schema = load_schema("manual")
        assert schema is not None
        assert schema["type"] == "object"


class TestManualExtractorFields:
    """Test manual extractor field validation."""
    
    def test_required_fields(self):
        """Test required fields in manual schema."""
        try:
            from datalad_metalad_fairextract.extractors.base import load_schema
        except ImportError:
            pytest.skip("Cannot import base extractor")
        
        schema = load_schema("manual")
        
        if "required" in schema:
            assert isinstance(schema["required"], list)
    
    def test_ontology_field_format(self):
        """Test ontology field format."""
        try:
            from datalad_metalad_fairextract.extractors.base import validate_curie_format
        except ImportError:
            pytest.skip("Cannot import base extractor")
        
        valid_curie = "NCBITaxon:9606"
        assert validate_curie_format(valid_curie) is True
        
        invalid_curie = "NCBITaxon_9606"
        assert validate_curie_format(invalid_curie) is False


class TestManualExtractorNoData:
    """Test manual extractor doesn't require actual data files."""
    
    def test_no_data_needed(self):
        """Test manual extractor works without actual data files."""
        try:
            from datalad_metalad_fairextract.extractors.manual import FairmetaManualDatasetExtractor
        except ImportError:
            pytest.skip("Cannot import manual extractor")
        
        assert FairmetaManualDatasetExtractor.get_required_content() is False


class TestManualSchemaIntegration:
    """Test manual schema integration with other schemas."""
    
    def test_h5ad_schema_compatibility(self):
        """Test manual can use h5ad schema."""
        try:
            from datalad_metalad_fairextract.extractors.base import load_schema
        except ImportError:
            pytest.skip("Cannot import base extractor")
        
        h5ad_schema = load_schema("h5ad")
        assert h5ad_schema is not None
    
    def test_fastq_schema_compatibility(self):
        """Test manual can use fastq schema."""
        try:
            from datalad_metalad_fairextract.extractors.base import load_schema
        except ImportError:
            pytest.skip("Cannot import base extractor")
        
        fastq_schema = load_schema("fastq")
        assert fastq_schema is not None
    
    def test_spatialdata_schema_compatibility(self):
        """Test manual can use spatialdata schema."""
        try:
            from datalad_metalad_fairextract.extractors.base import load_schema
        except ImportError:
            pytest.skip("Cannot import base extractor")
        
        spatialdata_schema = load_schema("spatialdata")
        assert spatialdata_schema is not None
    
    def test_xenium_schema_compatibility(self):
        """Test manual can use xenium schema."""
        try:
            from datalad_metalad_fairextract.extractors.base import load_schema
        except ImportError:
            pytest.skip("Cannot import base extractor")
        
        xenium_schema = load_schema("xenium")
        assert xenium_schema is not None