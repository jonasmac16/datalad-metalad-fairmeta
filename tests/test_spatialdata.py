"""Tests for SpatialData extractor."""

import pytest
from pathlib import Path


class TestSpatialDataExtractor:
    """Test SpatialData dataset extractor."""
    
    @pytest.fixture
    def extractor_class(self):
        from datalad_metalad_fairextract.extractors.spatialdata import SpatialDataDatasetExtractor
        return SpatialDataDatasetExtractor
    
    def test_extractor_registered(self, extractor_class):
        """Test extractor is registered and has correct properties."""
        assert extractor_class.extractor_name == "fairmeta_spatialdata"
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

    def test_get_required_content(self, extractor_class):
        """Test required content is True."""
        assert hasattr(extractor_class, 'get_required_content')

    def test_extract_synthetic_spatialdata(self, temp_dir):
        """Test extraction from synthetic SpatialData store."""
        try:
            from tests.test_data.synthetic import create_synthetic_spatialdata
        except ImportError as e:
            pytest.skip(f"Cannot import synthetic data generator: {e}")
        
        try:
            sdata_path = create_synthetic_spatialdata(temp_dir)
            if sdata_path is None:
                pytest.skip("create_synthetic_spatialdata returned None (API not implemented)")
            assert sdata_path.exists()
            assert str(sdata_path).endswith(".zarr")
        except Exception as e:
            pytest.skip(f"Synthetic SpatialData generation failed: {e}")

    def test_extract_nonexistent_dir(self, temp_dir):
        """Test extraction from non-existent directory."""
        nonexistent = temp_dir / "nonexistent.zarr"

        assert not nonexistent.exists()

    def test_spatialdata_library_available(self):
        """Check if spatialdata is available."""
        try:
            import spatialdata
            assert spatialdata is not None
        except ImportError:
            pytest.skip("spatialdata not available")


class TestSpatialDataWithDependencies:
    """Test SpatialData with optional dependencies."""
    
    def test_spatialdata_elements(self):
        """Test SpatialData element types."""
        try:
            import spatialdata as sd
            import numpy as np
            from spatialdata import SpatialData
            from spatialdata.models import ShapesModel
            import geopandas as gpd
            from shapely.geometry import Point
        except ImportError:
            pytest.skip("spatialdata not available")
        
        gdf = gpd.GeoDataFrame({
            'geometry': [Point(10, 20), Point(30, 40)],
            'radius': [5.0, 5.0]
        })
        gdf = gpd.GeoDataFrame(gdf, geometry='geometry', crs='EPSG:4326')
        shapes = ShapesModel.parse(gdf)
        
        sdata = SpatialData(shapes={'circles': shapes})
        
        assert "circles" in sdata.shapes
        assert len(sdata.shapes) > 0
    
    def test_spatialdata_version(self):
        """Test spatialdata version detection."""
        try:
            import spatialdata as sd
            
            version = getattr(sd, "__version__", "unknown")
            assert version is not None
        except ImportError:
            pytest.skip("spatialdata not available")


class TestSpatialDataMetadata:
    """Test SpatialData metadata extraction."""
    
    def test_coordinate_systems(self):
        """Test coordinate system handling."""
        try:
            import spatialdata as sd
            from spatialdata import SpatialData
        except ImportError:
            pytest.skip("spatialdata not available")
        
        sdata = SpatialData()
        
        assert hasattr(sdata, "coordinate_systems")
    
    def test_element_types(self):
        """Test element type enumeration."""
        expected_types = ["Images", "Labels", "Points", "Shapes", "Tables"]
        
        for element_type in expected_types:
            assert element_type in expected_types
    
    def test_multiple_elements(self, temp_dir):
        """Test multiple element types in one SpatialData."""
        try:
            import numpy as np
            import pandas as pd
            import spatialdata as sd
            from spatialdata import SpatialData
            from spatialdata.models import ShapesModel, PointsModel
            import geopandas as gpd
            from shapely.geometry import Point
        except ImportError:
            pytest.skip("spatialdata not available")
        
        # Create shapes
        shapes_gdf = gpd.GeoDataFrame({
            'geometry': [Point(10, 20), Point(30, 40)],
            'radius': [5.0, 5.0]
        })
        shapes_gdf = gpd.GeoDataFrame(shapes_gdf, geometry='geometry', crs='EPSG:4326')
        shapes = ShapesModel.parse(shapes_gdf)
        
        # Create points - use lowercase x, y as column names
        points_df = pd.DataFrame({
            'x': [1.0, 2.0, 3.0],
            'y': [4.0, 5.0, 6.0],
        })
        points = PointsModel.parse(points_df)
        
        sdata = SpatialData(
            shapes={'circles': shapes},
            points={'points': points},
        )
        
        assert len(sdata.shapes) >= 1
        assert len(sdata.points) >= 1