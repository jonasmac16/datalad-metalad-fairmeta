# SpatialData Extractor

The `fairmeta_spatialdata` extractor reads SpatialData .zarr stores and extracts metadata about all contained elements (Images, Labels, Points, Shapes, Tables) following OME-NGFF standards.

## Usage

```bash
datalad meta-extract -d . --force-dataset-level fairmeta_spatialdata path/to/spatialdata.zarr
```

## Extracted Metadata

| Field | Description | Ontology |
|-------|-------------|----------|
| spatialdata_version | SpatialData library version | - |
| element_types | List of element types present | - |
| element_counts | Count of each element type | - |
| coordinate_systems | Available coordinate systems | - |
| images | List of image elements with details | - |
| labels | List of label/segmentation elements | - |
| points | List of points elements | - |
| shapes | List of shapes/regions | - |
| tables | List of annotation tables | - |

### Image Element Details

| Field | Description |
|-------|-------------|
| name | Image name |
| dims | Dimensions (e.g., "cyx") |
| shape | Shape tuple |
| dtype | Data type |

### Label Element Details

| Field | Description |
|-------|-------------|
| name | Label name |
| shape | Shape tuple |

### Points Element Details

| Field | Description |
|-------|-------------|
| name | Points name |
| n_obs | Number of points |
| n_vars | Number of attributes |
| attributes | Attribute names |

### Shapes Element Details

| Field | Description |
|-------|-------------|
| name | Shapes name |
| shape_type | Geometry type (Polygon, etc.) |
| n_obs | Number of shapes |

### Table Element Details

| Field | Description |
|-------|-------------|
| name | Table name |
| n_obs | Number of rows |
| n_vars | Number of columns |
| obs_columns | Column names |
| var_columns | Variable columns |
| uns_keys | Additional metadata keys |

## Example Output

```json
{
  "$schema": "https://datalad-metalad-fairmeta.github.io/schemas/spatialdata.schema.json",
  "schema_version": "1.0.0",
  "spatialdata_version": "0.1.0",
  "element_types": ["Images", "Labels", "Points", "Shapes", "Tables"],
  "element_counts": {
    "Images": 2,
    "Labels": 1,
    "Points": 3,
    "Shapes": 5,
    "Tables": 2
  },
  "coordinate_systems": ["pixels", "global"],
  "images": [
    {
      "name": "image_hires",
      "dims": "cyx",
      "shape": [3, 1000, 1000],
      "dtype": "uint16"
    },
    {
      "name": "image_lowres",
      "dims": "cyx",
      "shape": [3, 250, 250],
      "dtype": "uint16"
    }
  ],
  "labels": [
    {
      "name": "cell_segmentation",
      "shape": [1000, 1000]
    }
  ],
  "points": [
    {
      "name": "transcripts",
      "n_obs": 50000,
      "n_vars": 3,
      "attributes": ["gene", "cell_id", "x", "y"]
    }
  ],
  "shapes": [
    {
      "name": "cell_boundaries",
      "shape_type": "Polygon",
      "n_obs": 1000
    }
  ],
  "tables": [
    {
      "name": "cell_table",
      "n_obs": 1000,
      "n_vars": 15,
      "obs_columns": ["cell_id", "cell_type", "cluster"],
      "var_columns": ["gene"]
    }
  ],
  "provenance": {
    "extractor_id": "fairmeta_spatialdata",
    "extractor_version": "1.0.0",
    "extraction_date": "2024-01-15T12:00:00Z"
  }
}
```

## Requirements

- `spatialdata` library

Install with: `pip install spatialdata`

## Edge Cases

- Missing optional elements: Those element types omitted from element_types and element_counts
- Empty zarr store: Returns basic structure with empty element lists
- Corrupted elements: Warning logged, element skipped
- No coordinate systems: Field omitted

See [Edge Cases: Missing Files](../edge_cases/missing_files.md) for handling corrupted files.