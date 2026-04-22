# OME-TIFF Extractor

The `fairmeta_ome_tiff` extractor reads OME-XML metadata embedded in OME-TIFF files.

## Usage

```bash
datalad meta-extract -d . fairmeta_ome_tiff path/to/image.ome.tiff
```

## Extracted Metadata

| Field | Description | Ontology |
|-------|-------------|----------|
| Image.ID | Unique image identifier | - |
| Image.Name | Image name | - |
| Image.AcquisitionDate | Acquisition timestamp | - |
| Image.Pixels.SizeX | Width in pixels | - |
| Image.Pixels.SizeY | Height in pixels | - |
| Image.Pixels.SizeZ | Number of focal planes | - |
| Image.Pixels.SizeT | Number of time points | - |
| Image.Pixels.SizeC | Number of channels | - |
| Image.Pixels.Type | Data type (uint8, uint16, etc.) | - |
| Image.Pixels.PhysicalSizeX | Physical width | - |
| Image.Pixels.PhysicalSizeY | Physical height | - |
| Image.Pixels.Channels | Channel information | - |

## Example Output

```json
{
  "$schema": "https://datalad-metalad-fairmeta.github.io/schemas/ome_tiff.schema.json",
  "schema_version": "1.0.0",
  "Image": {
    "ID": "Image:0",
    "Name": "sample_image",
    "AcquisitionDate": "2024-01-15T10:30:00",
    "Pixels": {
      "SizeX": 2048,
      "SizeY": 2048,
      "SizeZ": 10,
      "SizeT": 1,
      "SizeC": 5,
      "Type": "uint16",
      "PhysicalSizeX": 0.65,
      "PhysicalSizeY": 0.65,
      "PhysicalSizeXUnit": "µm",
      "DimensionOrder": "XYZTC",
      "Channels": [
        {
          "Name": "DAPI",
          "Fluor": "DAPI",
          "EmissionWavelength": 461
        },
        {
          "Name": "FITC",
          "Fluor": "FITC",
          "EmissionWavelength": 519
        }
      ]
    }
  },
  "provenance": {
    "extractor_id": "fairmeta_ome_tiff",
    "extractor_version": "1.0.0",
    "extraction_date": "2024-01-15T12:00:00Z"
  }
}
```

## Requirements

- `ome-types>=0.4.0` (optional, provides detailed metadata)
- If not available, falls back to basic TIFF tag reading

## Edge Cases

- Files without OME-XML are handled as standard TIFF
- Multiple images in a single file: extracts first image
- Missing optional fields: fields omitted rather than null

See [Edge Cases: Missing Files](../edge_cases/missing_files.md) for handling corrupted files.
