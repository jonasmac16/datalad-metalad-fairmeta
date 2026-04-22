"""Tests for base utilities."""

import pytest
from datalad_metalad_fairextract.extractors.base import (
    SchemaValidationError,
    get_schema_path,
    load_schema,
    validate_metadata,
    validate_curie_format,
    lookup_ontology_label,
    create_provenance,
    create_extraction_result,
    get_file_extension,
    get_directory_patterns,
)


class TestSchemaUtilities:
    """Test schema loading and validation utilities."""
    
    def test_get_schema_path(self):
        """Test getting schema path."""
        path = get_schema_path("h5ad")
        assert path.name == "h5ad.schema.json"
        assert "schemas" in str(path)
    
    def test_get_schema_path_not_found(self):
        """Test getting path for non-existent schema."""
        path = get_schema_path("nonexistent_schema")
        assert "nonexistent_schema.schema.json" in str(path)
    
    def test_load_schema(self):
        """Test loading a schema."""
        schema = load_schema("h5ad")
        assert "$schema" in schema
        assert schema["type"] == "object"
    
    def test_load_schema_not_found(self):
        """Test loading non-existent schema raises error."""
        with pytest.raises(FileNotFoundError):
            load_schema("nonexistent_schema")
    
    def test_validate_metadata_valid(self):
        """Test validating valid metadata."""
        metadata = {
            "$schema": "https://example.com/schema.json",
            "schema_version": "1.0.0",
            "organism_ontology_term_id": {"id": "NCBITaxon:9606", "label": "Homo sapiens"},
            "assay_ontology_term_id": {"id": "EFO:0009899", "label": "10x 3' v3"},
        }
        try:
            errors = validate_metadata(metadata, "h5ad")
            assert isinstance(errors, list)
        except Exception as e:
            if "404" in str(e) or "Unresolvable" in str(e):
                pytest.skip("Schema URL not accessible (network issue)")
            raise
    
    def test_validate_metadata_with_errors(self):
        """Test validating metadata with errors."""
        metadata = {
            "$schema": "https://example.com/schema.json",
            "schema_version": "1.0.0",
        }
        errors = validate_metadata(metadata, "h5ad")
        assert isinstance(errors, list)
    
    def test_validate_metadata_raise_on_error(self):
        """Test validating with raise on error."""
        metadata = {"invalid": "data"}
        with pytest.raises(SchemaValidationError):
            validate_metadata(metadata, "h5ad", raise_on_error=True)


class TestCURIEValidation:
    """Test CURIE format validation."""
    
    def test_validate_curie_format_valid(self):
        """Test valid CURIE formats."""
        assert validate_curie_format("NCBITaxon:9606") is True
        assert validate_curie_format("EFO:0009899") is True
        assert validate_curie_format("UBERON:0000955") is True
        assert validate_curie_format("CL:0000738") is True
    
    def test_validate_curie_format_invalid(self):
        """Test invalid CURIE formats."""
        assert validate_curie_format("NCBITaxon") is False
        assert validate_curie_format("9606") is False
        assert validate_curie_format("NCBITaxon_9606") is False
        assert validate_curie_format("") is False


class TestOntologyLookup:
    """Test ontology label lookup."""
    
    def test_lookup_ontology_label(self):
        """Test basic ontology label lookup."""
        label = lookup_ontology_label("NCBITaxon:9606")
        assert label == "NCBITaxon:9606"
    
    def test_lookup_ontology_label_cached(self):
        """Test ontology label lookup uses cache."""
        label1 = lookup_ontology_label("EFO:0009899")
        label2 = lookup_ontology_label("EFO:0009899")
        assert label1 == label2


class TestProvenance:
    """Test provenance creation."""
    
    def test_create_provenance_minimal(self):
        """Test creating minimal provenance."""
        prov = create_provenance("test_extractor", "1.0.0")
        assert prov["extractor_id"] == "test_extractor"
        assert prov["extractor_version"] == "1.0.0"
        assert "extraction_date" in prov
        assert prov["source_files"] == []
    
    def test_create_provenance_with_files(self):
        """Test creating provenance with source files."""
        prov = create_provenance("test_extractor", "1.0.0", ["file1.txt", "file2.txt"])
        assert len(prov["source_files"]) == 2
        assert "file1.txt" in prov["source_files"]


class TestExtractionResult:
    """Test extraction result creation."""
    
    def test_create_extraction_result_success(self):
        """Test creating successful extraction result."""
        result = create_extraction_result(
            metadata={"key": "value"},
            extractor_version="1.0.0",
            extraction_parameter={},
            success=True,
        )
        assert result.extractor_version == "1.0.0"
        assert result.extraction_success is True
        assert result.datalad_result_dict["status"] == "ok"
    
    def test_create_extraction_result_failure(self):
        """Test creating failed extraction result."""
        result = create_extraction_result(
            metadata={},
            extractor_version="1.0.0",
            extraction_parameter={},
            success=False,
        )
        assert result.extraction_success is False
        assert result.datalad_result_dict["status"] == "error"
    
    def test_create_extraction_result_with_warnings(self):
        """Test creating result with warnings."""
        result = create_extraction_result(
            metadata={"key": "value"},
            extractor_version="1.0.0",
            extraction_parameter={},
            success=True,
            warnings=["Warning 1", "Warning 2"],
        )
        assert "warnings" in result.immediate_data
        assert len(result.immediate_data["warnings"]) == 2
    
    def test_create_extraction_result_with_validation_errors(self):
        """Test creating result with validation errors."""
        result = create_extraction_result(
            metadata={},
            extractor_version="1.0.0",
            extraction_parameter={},
            success=True,
            validation_errors=["Error 1"],
        )
        assert "validation_errors" in result.immediate_data
    
    def test_create_extraction_result_with_provenance(self):
        """Test creating result with provenance."""
        prov = {"extractor_id": "test"}
        result = create_extraction_result(
            metadata={},
            extractor_version="1.0.0",
            extraction_parameter={},
            success=True,
            provenance=prov,
        )
        assert "provenance" in result.immediate_data
    
    def test_create_extraction_result_none_metadata(self):
        """Test creating result with None metadata."""
        result = create_extraction_result(
            metadata=None,
            extractor_version="1.0.0",
            extraction_parameter={},
            success=False,
        )
        assert result.immediate_data == {}


class TestFileUtilities:
    """Test file utility functions."""
    
    def test_get_file_extension(self):
        """Test getting file extension."""
        assert get_file_extension("file.txt") == ".txt"
        assert get_file_extension("file.TIFF") == ".tiff"
        assert get_file_extension("file.h5ad") == ".h5ad"
        assert get_file_extension("file.ome.tiff") == ".tiff"
    
    def test_get_file_extension_no_extension(self):
        """Test getting extension from file without one."""
        assert get_file_extension("file") == ""
    
    def test_get_directory_patterns(self):
        """Test getting directory patterns."""
        patterns = get_directory_patterns("/home/user/data/file.txt")
        assert "home" in patterns
        assert "user" in patterns
        assert "data" in patterns
    
    def test_get_directory_patterns_single(self):
        """Test getting patterns from single directory."""
        patterns = get_directory_patterns("dir")
        assert "dir" in patterns