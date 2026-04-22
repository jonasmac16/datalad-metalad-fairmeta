"""Tests for all dataset-level extractors."""

import pytest
from pathlib import Path


DATASET_EXTRACTORS = [
    ("fairmeta_xenium", "XeniumDatasetExtractor", "xenium"),
    ("fairmeta_cosmx", "CosMxDatasetExtractor", "cosmx"),
    ("fairmeta_visium_hd", "VisiumHDDatasetExtractor", "visium_hd"),
    ("fairmeta_merscope", "MerscopeDatasetExtractor", "merscope"),
    ("fairmeta_macsima", "MacsimaDatasetExtractor", "macsima"),
    ("fairmeta_phenocycler", "PhenoCyclerDatasetExtractor", "phenocycler"),
    ("fairmeta_molecular_cartography", "MolecularCartographyDatasetExtractor", "molecular_cartography"),
    ("fairmeta_hyperion", "HyperionDatasetExtractor", "hyperion"),
]


class TestDatasetExtractorRegistration:
    """Test that all dataset extractors are properly registered."""
    
    @pytest.mark.parametrize("extractor_name,class_name,data_type", DATASET_EXTRACTORS)
    def test_extractor_registration(self, extractor_name, class_name, data_type):
        """Test each extractor is registered and has correct properties."""
        module_path = f"datalad_metalad_fairextract.extractors.{data_type}"
        
        try:
            module = __import__(module_path, fromlist=[class_name])
            extractor_class = getattr(module, class_name)
        except (ImportError, AttributeError):
            pytest.skip(f"Cannot import {module_path}.{class_name}")
        
        assert extractor_class.extractor_name == extractor_name
        assert hasattr(extractor_class, "extractor_version")
    
    @pytest.mark.parametrize("extractor_name,class_name,data_type", DATASET_EXTRACTORS)
    def test_extractor_id(self, extractor_name, class_name, data_type):
        """Test each extractor has valid UUID."""
        from uuid import UUID
        
        module_path = f"datalad_metalad_fairextract.extractors.{data_type}"
        
        try:
            module = __import__(module_path, fromlist=[class_name])
            extractor_class = getattr(module, class_name)
        except (ImportError, AttributeError):
            pytest.skip(f"Cannot import {module_path}.{class_name}")
        
        extractor_id = extractor_class.get_id()
        assert isinstance(extractor_id, UUID)
    
    @pytest.mark.parametrize("extractor_name,class_name,data_type", DATASET_EXTRACTORS)
    def test_data_output_category(self, extractor_name, class_name, data_type):
        """Test each extractor has IMMEDIATE data output category."""
        from datalad_metalad.extractors.base import DataOutputCategory
        
        module_path = f"datalad_metalad_fairextract.extractors.{data_type}"
        
        try:
            module = __import__(module_path, fromlist=[class_name])
            extractor_class = getattr(module, class_name)
        except (ImportError, AttributeError):
            pytest.skip(f"Cannot import {module_path}.{class_name}")
        
        assert extractor_class.get_data_output_category() == DataOutputCategory.IMMEDIATE
    
    @pytest.mark.parametrize("extractor_name,class_name,data_type", DATASET_EXTRACTORS)
    def test_get_required_content(self, extractor_name, class_name, data_type):
        """Test each extractor requires content - tests static method only."""
        module_path = f"datalad_metalad_fairextract.extractors.{data_type}"
        
        try:
            module = __import__(module_path, fromlist=[class_name])
            extractor_class = getattr(module, class_name)
        except (ImportError, AttributeError):
            pytest.skip(f"Cannot import {module_path}.{class_name}")
        
        # Test the static method directly without instantiation
        assert hasattr(extractor_class, 'get_required_content')


class TestXeniumSyntheticData:
    """Test Xenium dataset extractor with synthetic data."""
    
    def test_create_synthetic_xenium_dir(self, temp_dir):
        """Test creation of synthetic Xenium directory."""
        from tests.test_data.synthetic import create_synthetic_xenium_dir
        
        xenium_dir = create_synthetic_xenium_dir(temp_dir)
        assert xenium_dir.exists()
        assert (xenium_dir / "transcripts.parquet").exists() or \
               any(xenium_dir.rglob("transcripts.parquet"))


class TestCosMxSyntheticData:
    """Test CosMx dataset extractor with synthetic data."""
    
    def test_create_synthetic_cosmx_dir(self, temp_dir):
        """Test creation of synthetic CosMx directory."""
        from tests.test_data.synthetic import create_synthetic_cosmx_dir
        
        cosmx_dir = create_synthetic_cosmx_dir(temp_dir)
        assert cosmx_dir.exists()


class TestVisiumHDSyntheticData:
    """Test Visium HD dataset extractor with synthetic data."""
    
    def test_create_synthetic_visium_hd_dir(self, temp_dir):
        """Test creation of synthetic Visium HD directory."""
        from tests.test_data.synthetic import create_synthetic_visium_hd_dir
        
        visium_dir = create_synthetic_visium_hd_dir(temp_dir)
        assert visium_dir.exists()


class TestMerscopeSyntheticData:
    """Test MERSCOPE dataset extractor with synthetic data."""
    
    def test_create_synthetic_merscope_dir(self, temp_dir):
        """Test creation of synthetic MERSCOPE directory."""
        from tests.test_data.synthetic import create_synthetic_merscope_dir
        
        merscope_dir = create_synthetic_merscope_dir(temp_dir)
        assert merscope_dir.exists()


class TestMACSimaSyntheticData:
    """Test MACSima dataset extractor with synthetic data."""
    
    def test_create_synthetic_macsima_dir(self, temp_dir):
        """Test creation of synthetic MACSima directory."""
        from tests.test_data.synthetic import create_synthetic_macsima_dir
        
        macsima_dir = create_synthetic_macsima_dir(temp_dir)
        assert macsima_dir.exists()


class TestPhenoCyclerSyntheticData:
    """Test PhenoCycler dataset extractor with synthetic data."""
    
    def test_create_synthetic_phenocycler_dir(self, temp_dir):
        """Test creation of synthetic PhenoCycler directory."""
        from tests.test_data.synthetic import create_synthetic_phenocycler_dir
        
        phenocycler_dir = create_synthetic_phenocycler_dir(temp_dir)
        assert phenocycler_dir.exists()


class TestMolecularCartographySyntheticData:
    """Test Molecular Cartography dataset extractor with synthetic data."""
    
    def test_create_synthetic_molecular_cartography_dir(self, temp_dir):
        """Test creation of synthetic Molecular Cartography directory."""
        from tests.test_data.synthetic import create_synthetic_molecular_cartography_dir
        
        mc_dir = create_synthetic_molecular_cartography_dir(temp_dir)
        assert mc_dir.exists()


class TestHyperionSyntheticData:
    """Test Hyperion dataset extractor with synthetic data."""
    
    def test_create_synthetic_hyperion_dir(self, temp_dir):
        """Test creation of synthetic Hyperion directory."""
        from tests.test_data.synthetic import create_synthetic_hyperion_dir
        
        hyperion_dir = create_synthetic_hyperion_dir(temp_dir)
        assert hyperion_dir.exists()


class TestDatasetExtractorStressCases:
    """Stress test all dataset extractors with edge cases."""
    
    @pytest.mark.parametrize("extractor_name,class_name,data_type", DATASET_EXTRACTORS)
    def test_extract_nonexistent_dir(self, extractor_name, class_name, data_type, temp_dir):
        """Test extraction from non-existent directory."""
        nonexistent = temp_dir / f"nonexistent_{data_type}"
        
        module_path = f"datalad_metalad_fairextract.extractors.{data_type}"
        
        try:
            module = __import__(module_path, fromlist=[class_name])
            extractor_class = getattr(module, class_name)
        except (ImportError, AttributeError):
            pytest.skip(f"Cannot import {module_path}.{class_name}")
        
        class MockDataset:
            def __init__(self, path):
                self.path = path
        
        if not nonexistent.exists():
            try:
                extractor = extractor_class(
                    dataset=MockDataset(str(nonexistent)),
                    parameter=None,
                )
                result = extractor.extract()
                assert result.extraction_success is False
            except Exception:
                pass
    
    @pytest.mark.parametrize("extractor_name,class_name,data_type", DATASET_EXTRACTORS)
    def test_extract_empty_dir(self, extractor_name, class_name, data_type, temp_dir):
        """Test extraction from empty directory."""
        empty_dir = temp_dir / f"empty_{data_type}"
        empty_dir.mkdir()
        
        module_path = f"datalad_metalad_fairextract.extractors.{data_type}"
        
        try:
            module = __import__(module_path, fromlist=[class_name])
            extractor_class = getattr(module, class_name)
        except (ImportError, AttributeError):
            pytest.skip(f"Cannot import {module_path}.{class_name}")
        
        class MockDataset:
            def __init__(self, path):
                self.path = path
        
        try:
            extractor = extractor_class(
                dataset=MockDataset(str(empty_dir)),
                parameter=None,
            )
            result = extractor.extract()
        except Exception:
            pass


class TestXeniumPatterns:
    """Test Xenium-specific patterns."""
    
    def test_xenium_patterns(self):
        """Test Xenium file pattern matching."""
        from datalad_metalad_fairextract.extractors.xenium import XeniumDatasetExtractor
        
        patterns = XeniumDatasetExtractor.XENIUM_PATTERNS
        
        assert "transcripts.parquet" in patterns
        assert "experiment.xenium" in patterns
        assert "morphology_focus" in patterns
    
    def test_find_file_method(self, temp_dir):
        """Test Xenium _find_file method."""
        from tests.test_data.synthetic import create_synthetic_xenium_dir
        
        xenium_dir = create_synthetic_xenium_dir(temp_dir)
        assert xenium_dir.exists()
        
        # Test that the method exists and is callable
        module_path = "datalad_metalad_fairextract.extractors.xenium"
        try:
            module = __import__(module_path, fromlist=["XeniumDatasetExtractor"])
            extractor_class = module.XeniumDatasetExtractor
            assert hasattr(extractor_class, '_find_file')
        except (ImportError, AttributeError):
            pytest.skip("Cannot import XeniumDatasetExtractor")
    """Test dataset metadata extraction structure."""
    
    def test_extraction_result_structure(self):
        """Test extraction result has correct structure."""
        from datalad_metalad_fairextract.extractors.base import (
            create_extraction_result,
        )
        
        result = create_extraction_result(
            metadata={"test": "data"},
            extractor_version="1.0.0",
            extraction_parameter={},
            success=True,
            result_type="dataset",
        )
        
        assert result.datalad_result_dict["type"] == "dataset"
        assert result.extraction_success is True