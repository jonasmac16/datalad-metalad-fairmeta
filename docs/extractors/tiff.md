# TIFF Extractor

The `fairmeta_tiff` extractor reads standard TIFF image files (not OME-TIFF). It extracts TIFF IFD (Image File Directory) tags including dimensions, color space, compression, and resolution.

## Usage

```bash
datalad meta-extract -d . fairmeta_tiff path/to/image.tif
```

## Extracted Metadata

| Field | Description | Ontology |
|-------|-------------|----------|
| image_name | Filename | - |
| width | Image width in pixels | - |
| height | Image height in pixels | - |
| bits_per_sample | Bits per sample | - |
| samples_per_pixel | Samples per pixel (channels) | - |
| compression | Compression scheme | - |
| photometric_interpretation | Color space (RGB, CMYK, etc.) | - |
| planar_configuration | Planar or chunky | - |
| x_resolution | Horizontal resolution | - |
| y_resolution | Vertical resolution | - |
| resolution_unit | Resolution unit (inch/cm) | - |
| software | Software that created the image | - |
| datetime | Image creation timestamp | - |
| artist | Artist/creator name | - |
| copyright | Copyright information | - |
| tile_width | Tile width (if tiled) | - |
| tile_height | Tile height (if tiled) | - |
| sample_format | Data format (unsigned, float, etc.) | - |
| image_description | Image description from TIFF tag | - |

## Example Output

```json
{
  "$schema": "https://datalad-metalad-fairmeta.github.io/schemas/tiff.schema.json",
  "schema_version": "1.0.0",
  "image_name": "sample.tif",
  "width": 2048,
  "height": 2048,
  "bits_per_sample": 16,
  "samples_per_pixel": 3,
  "compression": "LZW",
  "photometric_interpretation": "RGB",
  "planar_configuration": "Chunky",
  "x_resolution": 300.0,
  "y_resolution": 300.0,
  "resolution_unit": "Inch",
  "software": "Adobe Photoshop",
  "datetime": "2024:01:15 10:30:00",
  "provenance": {
    "extractor_id": "fairmeta_tiff",
    "extractor_version": "1.0.0",
    "extraction_date": "2024-01-15T12:00:00Z"
  }
}
```

## Requirements

- `tifffile` (optional, for full metadata extraction)
- If not available, falls back to basic TIFF parsing with limited fields

## Edge Cases

- OME-TIFF files: Use `fairmeta_ome_tiff` instead
- Multi-page TIFF: Extracts first page only
- BigTIFF: Not supported, falls back to basic parsing
- Corrupted tags: Missing or unreadable tags are omitted

See [Edge Cases: Missing Files](../edge_cases/missing_files.md) for handling corrupted files.