"""Synthetic test data generators for various file formats."""

import gzip
import json
import struct
import tempfile
from pathlib import Path
from typing import Any, Optional

import pytest


def create_synthetic_fastq(path: Path, read_number: int = 1) -> Path:
    """Create a synthetic FASTQ file for testing.
    
    Args:
        path: Directory to create the file in
        read_number: Read number (1 or 2)
    
    Returns:
        Path to created FASTQ file
    """
    fastq_content = (
        f"@TEST instrument:12345:67890 flowcellA:1:1101:12345:67890:ABCDEF "
        f"run:SRR1234567 sample:Sample1 study:PRJNA123456 "
        f"library:Library1 platform:ILLUMINA\n"
        f"ACGTACGTACGTACGTACGTACGTACGTACGT\n"
        f"+\n"
        f"IIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIII\n"
    )
    
    suffix = f"_R{read_number}.fastq" if read_number > 1 else ".fastq"
    file_path = path / f"test_sample{suffix}"
    file_path.write_text(fastq_content)
    return file_path


def create_synthetic_fastq_gz(path: Path, read_number: int = 1) -> Path:
    """Create a synthetic gzipped FASTQ file for testing.
    
    Args:
        path: Directory to create the file in
        read_number: Read number (1 or 2)
    
    Returns:
        Path to created gzipped FASTQ file
    """
    fastq_content = (
        f"@TEST instrument:12345:67890 flowcellA:1:1101:12345:67890:ABCDEF "
        f"run:SRR1234567 sample:Sample1 study:PRJNA123456 "
        f"library:Library1 platform:ILLUMINA\n"
        f"ACGTACGTACGTACGTACGTACGTACGTACGT\n"
        f"+\n"
        f"IIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIII\n"
    )
    
    suffix = f"_R{read_number}.fastq.gz" if read_number > 1 else ".fastq.gz"
    file_path = path / f"test_sample{suffix}"
    
    with gzip.open(file_path, 'wt') as f:
        f.write(fastq_content)
    return file_path


def create_synthetic_tiff(path: Path) -> Path:
    """Create a minimal synthetic TIFF file for testing.
    
    Args:
        path: Directory to create the file in
    
    Returns:
        Path to created TIFF file
    """
    file_path = path / "test_image.tiff"
    
    tiff_header = b'II'  # Little-endian
    tiff_header += struct.pack('<H', 42)  # TIFF magic
    tiff_header += struct.pack('<I', 8)   # IFD offset
    
    ifd_data = struct.pack('<H', 6)  # Number of entries
    ifd_data += struct.pack('<HHII', 256, 3, 1, 100)   # ImageWidth
    ifd_data += struct.pack('<HHII', 257, 3, 1, 100)   # ImageLength
    ifd_data += struct.pack('<HHII', 258, 3, 1, 8)     # BitsPerSample
    ifd_data += struct.pack('<HHII', 259, 3, 1, 1)     # Compression
    ifd_data += struct.pack('<HHII', 262, 3, 1, 1)    # PhotometricInterpretation
    ifd_data += struct.pack('<HHII', 277, 3, 1, 3)    # SamplesPerPixel
    ifd_data += b'\x00\x00\x00\x00'  # Next IFD offset (0 = none)
    
    file_path.write_bytes(tiff_header + ifd_data)
    return file_path


def create_synthetic_h5ad(path: Path, cell_count: int = 100, gene_count: int = 50) -> Path:
    """Create a synthetic h5ad file for testing.
    
    Args:
        path: Directory to create the file in
        cell_count: Number of cells
        gene_count: Number of genes
    
    Returns:
        Path to created h5ad file
    """
    try:
        import anndata as ad
        import numpy as np
        import pandas as pd
    except ImportError:
        raise ImportError("anndata and numpy are required for h5ad generation")
    
    file_path = path / "test_sample.h5ad"
    
    obs = pd.DataFrame(
        {
            "organism_ontology_term_id": ["NCBITaxon:9606"] * cell_count,
            "tissue_ontology_term_id": ["UBERON:0000955"] * cell_count,
            "cell_type_ontology_term_id": ["CL:0000738"] * cell_count,
            "assay_ontology_term_id": ["EFO:0009899"] * cell_count,
            "disease_ontology_term_id": ["MONDO:0000001"] * cell_count,
        },
        index=[f"cell_{i}" for i in range(cell_count)],
    )
    
    var = pd.DataFrame(
        {"gene_name": [f"gene_{i}" for i in range(gene_count)]},
        index=[f"gene_{i}" for i in range(gene_count)],
    )
    
    X = np.random.random((cell_count, gene_count))
    adata = ad.AnnData(X=X, obs=obs, var=var)
    adata.uns = {
        "title": "Test Dataset",
        "schema_version": "7.1",
    }
    adata.write_h5ad(file_path)
    return file_path


def create_synthetic_ome_tiff(path: Path) -> Optional[Path]:
    """Create a synthetic OME-TIFF file for testing.
    
    Args:
        path: Directory to create the file in
    
    Returns:
        Path to created OME-TIFF file
    """
    try:
        import numpy as np
    except ImportError:
        raise ImportError("numpy is required for OME-TIFF generation")
    
    file_path = path / "test_image.ome.tiff"
    file_path.write_text("dummy ome-tiff content")
    return file_path


def create_synthetic_spatialdata(path: Path) -> Optional[Path]:
    """Create a synthetic SpatialData .zarr store for testing.
    
    Args:
        path: Directory to create the SpatialData in
    
    Returns:
        Path to created SpatialData directory
    """
    try:
        import spatialdata as sd
        from spatialdata import SpatialData
        import numpy as np
        import dask.array as da
        from spatialdata.models import Image2DModel
    except ImportError:
        pytest.skip("spatialdata not installed")
        return None
    
    try:
        spatialdata_dir = path / "test_spatialdata.zarr"
        spatialdata_dir.mkdir(parents=True, exist_ok=True)
        
        try:
            image_data = da.zeros((1, 100, 100), dtype=np.uint8, chunks=(1, 100, 100))
            image = Image2DModel.parse(image_data, dims=('c', 'y', 'x'))
            sdata = SpatialData(images={'test': image})
            sdata.write(str(spatialdata_dir))
        except Exception as e:
            zarr_file = spatialdata_dir / "test.zarr"
            import zarr
            zarr.save(str(zarr_file), np.zeros((10, 10), dtype=np.uint8))
        
        return spatialdata_dir
    except Exception as e:
        pytest.skip(f"spatialdata API error: {e}")
        return None


def create_synthetic_xenium_dir(path: Path) -> Path:
    """Create a synthetic Xenium directory structure for testing.
    
    Args:
        path: Directory to create Xenium structure in
    
    Returns:
        Path to created Xenium directory
    """
    xenium_dir = path / "xenium_sample"
    xenium_dir.mkdir(parents=True, exist_ok=True)
    
    transcripts_parquet = xenium_dir / "transcripts.parquet"
    experiment_file = xenium_dir / "experiment.xenium"
    morphology_file = xenium_dir / "morphology_focus.ome.tif"
    
    try:
        import pyarrow as pa
        import pyarrow.parquet as pq
        
        table = pa.table({
            "x": [1.0, 2.0, 3.0],
            "y": [1.0, 2.0, 3.0],
            "gene": ["GENE1", "GENE2", "GENE3"],
            "cell_id": [1, 1, 2],
        })
        pq.write_table(table, str(transcripts_parquet))
    except ImportError:
        transcripts_parquet.write_text("")
    
    experiment_file.write_text(
        json.dumps({
            "run_id": "TEST_RUN_001",
            "software_version": "1.0.0",
        })
    )
    
    create_synthetic_tiff(xenium_dir)
    if morphology_file.exists():
        morphology_file.unlink()
    tiff_path = xenium_dir / "morphology_focus.ome.tif"
    if tiff_path.exists():
        (xenium_dir / "morphology_focus.ome.tif").write_bytes(tiff_path.read_bytes())
    
    return xenium_dir


def create_synthetic_cosmx_dir(path: Path) -> Path:
    """Create a synthetic CosMx directory structure for testing.
    
    Args:
        path: Directory to create CosMx structure in
    
    Returns:
        Path to created CosMx directory
    """
    cosmx_dir = path / "cosmx_sample"
    cosmx_dir.mkdir(parents=True, exist_ok=True)
    
    (cosmx_dir / "spatial").mkdir(exist_ok=True)
    (cosmx_dir / "cells.gz").write_text("")
    (cosmx_dir / "transcripts.csv").write_text("gene,count\ngene1,10\ngene2,20\n")
    (cosmx_dir / "metadata.json").write_text(json.dumps({
        "run_id": "TEST_COSMX_001",
    }))
    
    return cosmx_dir


def create_synthetic_visium_hd_dir(path: Path) -> Path:
    """Create a synthetic Visium HD directory structure for testing.
    
    Args:
        path: Directory to create Visium HD structure in
    
    Returns:
        Path to created Visium HD directory
    """
    visium_dir = path / "visium_hd_sample"
    visium_dir.mkdir(parents=True, exist_ok=True)
    
    (visium_dir / "spatial").mkdir(exist_ok=True)
    (visium_dir / "count_matrix").mkdir(exist_ok=True)
    (visium_dir / "metadata.json").write_text(json.dumps({
        "slide_id": "TEST_SLIDE_001",
    }))
    
    return visium_dir


def create_synthetic_merscope_dir(path: Path) -> Path:
    """Create a synthetic MERSCOPE directory structure for testing.
    
    Args:
        path: Directory to create MERSCOPE structure in
    
    Returns:
        Path to created MERSCOPE directory
    """
    merscope_dir = path / "merscope_sample"
    merscope_dir.mkdir(parents=True, exist_ok=True)
    
    (merscope_dir / "cells.parquet").write_text("")
    (merscope_dir / "transcripts.parquet").write_text("")
    (merscope_dir / "metadata.json").write_text(json.dumps({
        "run_id": "TEST_MERSCOPE_001",
    }))
    
    return merscope_dir


def create_synthetic_macsima_dir(path: Path) -> Path:
    """Create a synthetic MACSima directory structure for testing.
    
    Args:
        path: Directory to create MACSima structure in
    
    Returns:
        Path to created MACSima directory
    """
    macsima_dir = path / "macsima_sample"
    macsima_dir.mkdir(parents=True, exist_ok=True)
    
    (macsima_dir / "metadata.json").write_text(json.dumps({
        "run_id": "TEST_MACSIMA_001",
    }))
    (macsima_dir / "images").mkdir(exist_ok=True)
    
    return macsima_dir


def create_synthetic_phenocycler_dir(path: Path) -> Path:
    """Create a synthetic PhenoCycler directory structure for testing.
    
    Args:
        path: Directory to create PhenoCycler structure in
    
    Returns:
        Path to created PhenoCycler directory
    """
    phenocycler_dir = path / "phenocycler_sample"
    phenocycler_dir.mkdir(parents=True, exist_ok=True)
    
    (phenocycler_dir / "metadata.json").write_text(json.dumps({
        "run_id": "TEST_PHENOCYCLER_001",
    }))
    (phenocycler_dir / "images").mkdir(exist_ok=True)
    
    return phenocycler_dir


def create_synthetic_molecular_cartography_dir(path: Path) -> Path:
    """Create a synthetic Molecular Cartography directory structure for testing.
    
    Args:
        path: Directory to create Molecular Cartography structure in
    
    Returns:
        Path to created Molecular Cartography directory
    """
    mc_dir = path / "molecular_cartography_sample"
    mc_dir.mkdir(parents=True, exist_ok=True)
    
    (mc_dir / "metadata.json").write_text(json.dumps({
        "run_id": "TEST_MC_001",
    }))
    (mc_dir / "results").mkdir(exist_ok=True)
    
    return mc_dir


def create_synthetic_hyperion_dir(path: Path) -> Path:
    """Create a synthetic Hyperion directory structure for testing.
    
    Args:
        path: Directory to create Hyperion structure in
    
    Returns:
        Path to created Hyperion directory
    """
    hyperion_dir = path / "hyperion_sample"
    hyperion_dir.mkdir(parents=True, exist_ok=True)
    
    (hyperion_dir / "metadata.json").write_text(json.dumps({
        "run_id": "TEST_HYPERION_001",
    }))
    (hyperion_dir / "images").mkdir(exist_ok=True)
    
    return hyperion_dir


def create_corrupt_fastq(path: Path) -> Path:
    """Create a corrupt FASTQ file (missing header).
    
    Args:
        path: Directory to create the file in
    
    Returns:
        Path to created corrupt FASTQ file
    """
    file_path = path / "corrupt.fastq"
    file_path.write_text("This is not a valid FASTQ file\n")
    return file_path


def create_corrupt_tiff(path: Path) -> Path:
    """Create a corrupt TIFF file.
    
    Args:
        path: Directory to create the file in
    
    Returns:
        Path to created corrupt TIFF file
    """
    file_path = path / "corrupt.tiff"
    file_path.write_text("This is not a valid TIFF file\n")
    return file_path


def create_empty_file(path: Path, extension: str) -> Path:
    """Create an empty file with given extension.
    
    Args:
        path: Directory to create the file in
        extension: File extension (e.g., '.fastq', '.h5ad')
    
    Returns:
        Path to created empty file
    """
    file_path = path / f"empty{extension}"
    file_path.write_text("")
    return file_path


def create_special_char_path_test_file(path: Path) -> Path:
    """Create a test file with special characters in path.
    
    Args:
        path: Directory to create the file in
    
    Returns:
        Path to created file
    """
    special_dir = path / "test with spaces"
    special_dir.mkdir(parents=True, exist_ok=True)
    file_path = special_dir / "sample.fastq"
    file_path.write_text(
        "@TEST:1:1\nACGT\n+\nIIII\n"
    )
    return file_path