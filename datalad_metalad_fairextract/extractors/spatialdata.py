"""SpatialData .zarr metadata extractor.

Extracts metadata from SpatialData .zarr stores following OME-NGFF.
"""

import logging
from pathlib import Path
from typing import Any
from uuid import UUID

from datalad_metalad.extractors.base import (
    DataOutputCategory,
    DatasetMetadataExtractor,
    ExtractorResult,
)

from .base import create_extraction_result, create_provenance, validate_metadata

logger = logging.getLogger('datalad_metalad_fairextract.spatialdata')


class SpatialDataDatasetExtractor(DatasetMetadataExtractor):
    """Extract metadata from SpatialData .zarr stores.

    This extractor reads SpatialData objects stored as Zarr files
    and extracts information about all contained elements (Images, Labels,
    Points, Shapes, Tables).
    """

    extractor_name = "fairmeta_spatialdata"
    extractor_version = "1.0.0"

    @staticmethod
    def get_id() -> UUID:
        return UUID("c3d4e5f6-7a8b-9c0d-1e2f-3a4b5c6d7e8f")

    @staticmethod
    def get_version() -> str:
        return "1.0.0"

    @staticmethod
    def get_data_output_category() -> DataOutputCategory:
        return DataOutputCategory.IMMEDIATE

    def get_required_content(self) -> bool:
        return True

    def extract(self, _=None) -> ExtractorResult:
        """Extract SpatialData metadata from the directory."""
        metadata = {
            "$schema": "https://datalad-metalad-fairmeta.github.io/schemas/spatialdata.schema.json",
            "schema_version": "1.0.0"
        }
        warnings = []
        errors = []

        dataset_path = str(self.dataset.path)
        logger.info(f"Extracting SpatialData metadata from: {dataset_path}")

        try:
            sdata_metadata = self._extract_spatialdata_metadata(dataset_path)
            metadata.update(sdata_metadata)
        except ImportError:
            errors.append("spatialdata library not available. Install with: pip install spatialdata")
            return create_extraction_result(
                metadata=metadata,
                extractor_version=self.extractor_version,
                extraction_parameter=self.parameter,
                success=False,
                result_type="dataset",
                validation_errors=errors,
                warnings=warnings,
                provenance=create_provenance(
                    self.extractor_name,
                    self.extractor_version,
                    [dataset_path]
                )
            )
        except Exception as e:
            errors.append(f"Failed to parse SpatialData store: {str(e)}")
            return create_extraction_result(
                metadata=metadata,
                extractor_version=self.extractor_version,
                extraction_parameter=self.parameter,
                success=False,
                result_type="dataset",
                validation_errors=errors,
                warnings=warnings,
                provenance=create_provenance(
                    self.extractor_name,
                    self.extractor_version,
                    [dataset_path]
                )
            )

        validation_errors = validate_metadata(metadata, "spatialdata")
        success = len(errors) == 0 and len(validation_errors) == 0

        return create_extraction_result(
            metadata=metadata,
            extractor_version=self.extractor_version,
            extraction_parameter=self.parameter,
            success=success,
            result_type="dataset",
            validation_errors=validation_errors,
            warnings=warnings,
            provenance=create_provenance(
                self.extractor_name,
                self.extractor_version,
                [dataset_path]
            )
        )

    def _extract_spatialdata_metadata(self, dataset_path: str) -> dict[str, Any]:
        """Extract SpatialData metadata using spatialdata library."""
        import spatialdata as sd

        sdata = sd.read_zarr(dataset_path)

        metadata = {
            "spatialdata_version": getattr(sd, '__version__', 'unknown'),
            "element_types": [],
            "element_counts": {},
        }

        if hasattr(sdata, 'coordinate_systems') and sdata.coordinate_systems:
            metadata["coordinate_systems"] = list(sdata.coordinate_systems)

        images_info = []
        if hasattr(sdata, 'images') and len(sdata.images) > 0:
            metadata["element_types"].append("Images")
            metadata["element_counts"]["Images"] = len(sdata.images)
            for name, img in sdata.images.items():
                img_info = {"name": name}
                if hasattr(img, 'dims'):
                    img_info["dims"] = str(img.dims)
                if hasattr(img, 'shape'):
                    img_info["shape"] = list(img.shape)
                if hasattr(img, 'dtype'):
                    img_info["dtype"] = str(img.dtype)
                images_info.append(img_info)
        metadata["images"] = images_info

        labels_info = []
        if hasattr(sdata, 'labels') and len(sdata.labels) > 0:
            metadata["element_types"].append("Labels")
            metadata["element_counts"]["Labels"] = len(sdata.labels)
            for name, label in sdata.labels.items():
                label_info = {"name": name}
                if hasattr(label, 'shape'):
                    label_info["shape"] = list(label.shape)
                labels_info.append(label_info)
        metadata["labels"] = labels_info

        points_info = []
        if hasattr(sdata, 'points') and len(sdata.points) > 0:
            metadata["element_types"].append("Points")
            metadata["element_counts"]["Points"] = len(sdata.points)
            for name, points in sdata.points.items():
                points_data = {"name": name}
                if hasattr(points, 'n_obs'):
                    points_data["n_obs"] = points.n_obs
                if hasattr(points, 'n_vars'):
                    points_data["n_vars"] = points.n_vars
                if hasattr(points, 'attrs') and 'attributes' in points.attrs:
                    points_data["attributes"] = list(points.attrs['attributes'])
                points_info.append(points_data)
        metadata["points"] = points_info

        shapes_info = []
        if hasattr(sdata, 'shapes') and len(sdata.shapes) > 0:
            metadata["element_types"].append("Shapes")
            metadata["element_counts"]["Shapes"] = len(sdata.shapes)
            for name, shape in sdata.shapes.items():
                shape_data = {"name": name}
                if hasattr(shape, 'geom_type'):
                    shape_data["shape_type"] = str(shape.geom_type)
                if hasattr(shape, 'n_obs'):
                    shape_data["n_obs"] = shape.n_obs
                shapes_info.append(shape_data)
        metadata["shapes"] = shapes_info

        tables_info = []
        if hasattr(sdata, 'tables') and len(sdata.tables) > 0:
            metadata["element_types"].append("Tables")
            metadata["element_counts"]["Tables"] = len(sdata.tables)
            for name, table in sdata.tables.items():
                table_data = {"name": name}
                if hasattr(table, 'n_obs'):
                    table_data["n_obs"] = table.n_obs
                if hasattr(table, 'n_vars'):
                    table_data["n_vars"] = table.n_vars
                if hasattr(table, 'obs'):
                    table_data["obs_columns"] = list(table.obs.columns)
                if hasattr(table, 'var'):
                    table_data["var_columns"] = list(table.var.columns) if hasattr(table.var, 'columns') else []
                if hasattr(table, 'uns') and table.uns:
                    table_data["uns_keys"] = list(table.uns.keys())
                tables_info.append(table_data)
        metadata["tables"] = tables_info

        return metadata
