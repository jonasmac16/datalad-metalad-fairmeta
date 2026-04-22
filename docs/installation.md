# Installation

## Prerequisites

- Python 3.9 or higher
- [DataLad](https://www.datalad.org/) (>= 0.18)
- [datalad-metalad](https://github.com/datalad/datalad-metalad) (>= 0.4)

## Basic Installation

### From PyPI

```bash
pip install datalad-metalad-fairmeta
```

### From GitHub

```bash
pip install git+https://github.com/your-org/datalad-metalad-fairmeta.git
```

### From Source

```bash
git clone https://github.com/your-org/datalad-metalad-fairmeta
cd datalad-metalad-fairmeta
pip install -e .
```

## Optional Dependencies

Depending on your data formats, install the relevant optional dependencies:

### For OME-TIFF Extraction

```bash
pip install datalad-metalad-fairmeta[ome_tiff]
# or
pip install ome-types>=0.4.0
```

### For AnnData/h5ad Extraction

```bash
pip install datalad-metalad-fairmeta[h5ad]
# or
pip install anndata>=1.7.0
```

### For SpatialData Extraction

```bash
pip install datalad-metalad-fairmeta[spatialdata]
# or
pip install spatialdata>=0.7.0
```

### For TIFF Extraction

```bash
pip install datalad-metalad-fairmeta[tiff]
# or
pip install tifffile>=2021.0
```

### All Dependencies

```bash
pip install datalad-metalad-fairmeta[all]
```

## Verifying Installation

After installation, verify that the extractors are registered:

```bash
datalad meta-extract --help
```

You should see the extractors listed:

- `fairmeta_ome_tiff`
- `fairmeta_tiff`
- `fairmeta_spatialdata`
- `fairmeta_h5ad`
- `fairmeta_cosmx`
- `fairmeta_xenium`
- `fairmeta_visium_hd`
- `fairmeta_merscope`
- `fairmeta_macsima`
- `fairmeta_phenocycler`
- `fairmeta_molecular_cartography`
- `fairmeta_hyperion`
- `fairmeta_fastq`
- `fairmeta_manual`

## Docker/Singularity

You can also use the containerized version:

```bash
# Pull from Docker Hub
docker pull your-org/datalad-metalad-fairmeta:latest

# Run with DataLad
docker run --rm -v /path/to/data:/data your-org/datalad-metalad-fairmeta \
  datalad meta-extract -d /data fairmeta_ome_tiff /data/image.ome.tiff
```

## Troubleshooting

### Import Errors

If you encounter import errors, ensure DataLad and datalad-metalad are properly installed:

```bash
pip install datalad datalad-metalad
```

### Permission Issues

If you encounter permission issues during installation:

```bash
pip install --user datalad-metalad-fairmeta
```

Or use a virtual environment:

```bash
python -m venv venv
source venv/bin/activate
pip install datalad-metalad-fairmeta
```
