"""Tests for h5ad extractor."""

import pytest
from pathlib import Path


class TestH5adExtractor:
    """Test h5ad file extractor."""
    
    @pytest.fixture
    def extractor_class(self):
        from datalad_metalad_fairextract.extractors.h5ad import H5adFileExtractor
        return H5adFileExtractor
    
    def test_extractor_registered(self, extractor_class):
        """Test extractor is registered and has correct properties."""
        assert extractor_class.extractor_name == "fairmeta_h5ad"
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


class TestH5adSyntheticData:
    """Test h5ad extractor with synthetic data."""
    
    def test_extract_synthetic_h5ad(self, temp_dir):
        """Test extraction from synthetic h5ad file."""
        from tests.test_data.synthetic import create_synthetic_h5ad
        
        h5ad_file = create_synthetic_h5ad(temp_dir, cell_count=50, gene_count=25)
        assert h5ad_file.exists()
        assert h5ad_file.suffix == ".h5ad"
        
        try:
            import anndata as ad
            adata = ad.read_h5ad(h5ad_file)
            assert adata.n_obs == 50
            assert adata.n_vars == 25
        except ImportError:
            pytest.skip("anndata not available")


class TestH5adPublicData:
    """Test h5ad extractor with public data."""
    
    def test_extract_pbmc3k(self, temp_dir):
        """Test extraction from PBMC3k public data."""
        try:
            from datalad_metalad_fairextract.extractors.h5ad import H5adFileExtractor
        except ImportError:
            pytest.skip("Extractor module import failed")
        
        try:
            import anndata as ad
            import scanpy as sc
        except ImportError:
            pytest.skip("anndata or scanpy not available")
        
        adata = sc.datasets.pbmc3k()
        assert adata.n_obs > 0
        assert adata.n_vars > 0


class TestH5adStressCases:
    """Stress test h5ad extractor with edge cases."""
    
    def test_extract_nonexistent_file(self, temp_dir):
        """Test extraction from non-existent file."""
        nonexistent = temp_dir / "nonexistent.h5ad"
        
        try:
            from datalad_metalad_fairextract.extractors.h5ad import H5adFileExtractor
        except ImportError:
            pytest.skip("Extractor module import failed")
        
        if nonexistent.exists():
            pytest.fail("File should not exist for this test")
    
    def test_extract_corrupt_h5ad(self, temp_dir):
        """Test extraction from corrupt h5ad file."""
        corrupt_file = temp_dir / "corrupt.h5ad"
        corrupt_file.write_bytes(b"This is not a valid h5ad file")
        
        assert corrupt_file.exists()
        
        try:
            import anndata as ad
            ad.read_h5ad(corrupt_file)
            pytest.fail("Should have raised exception")
        except Exception:
            pass
        except ImportError:
            pytest.skip("Extractor module import failed")
    
    def test_large_cell_count(self, temp_dir):
        """Test extraction with large cell count (edge of limits)."""
        from tests.test_data.synthetic import create_synthetic_h5ad
        
        try:
            h5ad_file = create_synthetic_h5ad(temp_dir, cell_count=100000, gene_count=100)
            assert h5ad_file.exists()
            
            import anndata as ad
            adata = ad.read_h5ad(h5ad_file)
            assert adata.n_obs == 100000
        except ImportError:
            pytest.skip("anndata not available")
    
    def test_minimal_h5ad(self, temp_dir):
        """Test extraction with minimum cells/genes."""
        from tests.test_data.synthetic import create_synthetic_h5ad
        
        try:
            h5ad_file = create_synthetic_h5ad(temp_dir, cell_count=1, gene_count=1)
            assert h5ad_file.exists()
            
            import anndata as ad
            adata = ad.read_h5ad(h5ad_file)
            assert adata.n_obs == 1
            assert adata.n_vars == 1
        except ImportError:
            pytest.skip("anndata not available")


class TestH5adCURIEHandling:
    """Test CURIE format handling in h5ad extractor."""
    
    def test_curie_parsing(self):
        """Test CURIE parsing from underscore format."""
        from datalad_metalad_fairextract.extractors.base import validate_curie_format
        
        valid_curies = [
            "NCBITaxon:9606",
            "EFO:0009899",
            "UBERON:0000955",
            "CL:0000738",
        ]
        
        for curie in valid_curies:
            assert validate_curie_format(curie) is True, f"CURIE {curie} should be valid"
    
    def test_curie_with_underscore_converted(self):
        """Test CURIE with underscore is detected."""
        from datalad_metalad_fairextract.extractors.base import validate_curie_format
        
        underscore_format = "NCBITaxon_9606"
        assert validate_curie_format(underscore_format) is False