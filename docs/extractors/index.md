# Extractors Overview

datalad-metalad-fairmeta provides extractors for the following spatial biology data formats.

## File-Level Extractors

These extractors operate on individual files:

| Extractor | File Type | Extension |
|-----------|-----------|----------|
| `fairmeta_ome_tiff` | OME-TIFF | `.ome.tiff`, `.ome.tif`, `.ome.tf2`, `.ome.tf8`, `.ome.btf` |
| `fairmeta_tiff` | TIFF | `.tif`, `.tiff` |
| `fairmeta_h5ad` | AnnData | `.h5ad` |
| `fairmeta_fastq` | FASTQ | `.fastq`, `.fastq.gz`, `.fq`, `.fq.gz` |

## Dataset-Level Extractors

These extractors operate on directories containing output from specific platforms:

| Extractor | Platform | Key Files/Directories |
|-----------|----------|----------------------|
| `fairmeta_spatialdata` | SpatialData | `.zarr` store |
| `fairmeta_cosmx` | NanoString CosMx | `*_metadata_file.csv`, `*_exprMat_file.csv` |
| `fairmeta_xenium` | 10x Xenium | `cells.csv.gz`, `analysis/` |
| `fairmeta_visium_hd` | 10x Visium HD | `microscope_image/`, feature matrix .h5 files |
| `fairmeta_merscope` | Vizgen MERSCOPE | `detected_transcripts.csv`, `images/` |
| `fairmeta_macsima` | Bruker MACSima | `.tif` files with OME metadata |
| `fairmeta_phenocycler` | Akoya PhenoCycler | `.qptiff`, `.tif` files |
| `fairmeta_molecular_cartography` | Resolve Bioscience | `*_results.txt`, channel TIFFs |
| `fairmeta_hyperion` | Fluidigm Hyperion | `*_001.tiff` channel files |
| `fairmeta_manual` | Interactive | User-provided via prompts or [config files](../templates.md) |

## Common Parameters

Most extractors support these optional runtime parameters:

```bash
# No additional parameters needed for most use cases
datalad meta-extract -d . fairmeta_ome_tiff image.ome.tiff
```

## Output Format

All extractors return JSON metadata in this format:

```json
{
  "extractor_name": "fairmeta_ome_tiff",
  "extractor_version": "1.0.0",
  "extraction_success": true,
  "datalad_result_dict": {
    "type": "file",
    "status": "ok"
  },
  "immediate_data": {
    "$schema": "https://datalad-metalad-fairmeta.github.io/schemas/...",
    "schema_version": "1.0.0",
    "...": "..."
  }
}
```

## Detailed Documentation

- [OME-TIFF Extractor](ome_tiff.md)
- [TIFF Extractor](tiff.md)
- [SpatialData Extractor](spatialdata.md)
- [h5ad Extractor](h5ad.md)
- [CosMx Extractor](cosmx.md)
- [Xenium Extractor](xenium.md)
- [Visium HD Extractor](visium_hd.md)
- [MERSCOPE Extractor](merscope.md)
- [MACSima Extractor](macsima.md)
- [PhenoCycler Extractor](phenocycler.md)
- [Molecular Cartography Extractor](molecular_cartography.md)
- [Hyperion Extractor](hyperion.md)
- [FASTQ Extractor](fastq.md)
- [Manual Extractor](manual.md)
