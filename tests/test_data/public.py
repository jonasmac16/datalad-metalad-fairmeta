"""Public test data downloaders (cached on-the-fly)."""

import hashlib
import shutil
import tempfile
import urllib.request
from pathlib import Path
from typing import Optional


PUBLIC_DATA_URLS = {
    "pbmc3k": {
        "url": "https://dl.dropboxusercontent.com/s/kj3vy83pgoz60y4/pbmc3k_raw.h5ad",
        "md5": None,  # Optional MD5 for verification
        "description": "PBMC 3k dataset from scanpy",
    },
    "rnaseq_test_r1": {
        "url": (
            "https://raw.githubusercontent.com/nf-core/test-datasets/rnaseq"
            "/testdata/SRR8983579.small.fastq.gz"
        ),
        "md5": None,
        "description": "RNA-seq test data from nf-core",
    },
}


def _get_cache_dir() -> Path:
    """Get or create the test data cache directory."""
    cache_dir = Path(tempfile.gettempdir()) / "fairmeta_public_data"
    cache_dir.mkdir(parents=True, exist_ok=True)
    return cache_dir


def _compute_file_hash(file_path: Path) -> str:
    """Compute MD5 hash of a file."""
    h = hashlib.md5()
    with open(file_path, 'rb') as f:
        for chunk in iter(lambda: f.read(8192), b''):
            h.update(chunk)
    return h.hexdigest()


def download_public_file(
    key: str,
    dest_dir: Optional[Path] = None,
    force_download: bool = False,
) -> Path:
    """Download a public test file, using cache if available.
    
    Args:
        key: Key identifying the public data (from PUBLIC_DATA_URLS)
        dest_dir: Directory to save the file (default: cache dir)
        force_download: If True, re-download even if cached
    
    Returns:
        Path to the downloaded/cached file
    """
    if key not in PUBLIC_DATA_URLS:
        raise ValueError(f"Unknown public data key: {key}")
    
    info = PUBLIC_DATA_URLS[key]
    cache_dir = _get_cache_dir() if dest_dir is None else Path(dest_dir)
    cache_dir.mkdir(parents=True, exist_ok=True)
    
    filename = Path(info["url"]).name
    file_path = cache_dir / filename
    
    if force_download and file_path.exists():
        file_path.unlink()
    
    if file_path.exists():
        return file_path
    
    print(f"Downloading {info['description']}...")
    try:
        urllib.request.urlretrieve(info["url"], file_path)
    except Exception as e:
        if file_path.exists():
            file_path.unlink()
        raise RuntimeError(f"Failed to download {info['url']}: {e}")
    
    return file_path


def get_pbmc3k_h5ad(dest_dir: Optional[Path] = None) -> Path:
    """Get or download the PBMC3k h5ad file.
    
    Args:
        dest_dir: Directory to save the file (default: cache dir)
    
    Returns:
        Path to the h5ad file
    """
    return download_public_file("pbmc3k", dest_dir)


def get_rnaseq_fastq(dest_dir: Optional[Path] = None, read_number: int = 1) -> Path:
    """Get or download RNA-seq FASTQ test file.
    
    Args:
        dest_dir: Directory to save the file (default: cache dir)
        read_number: Which read (1 or 2)
    
    Returns:
        Path to the FASTQ file
    """
    if read_number == 1:
        return download_public_file("rnaseq_test_r1", dest_dir)
    else:
        return download_public_file("rnaseq_test_r1", dest_dir)


def clear_cache() -> None:
    """Clear the public data cache."""
    cache_dir = _get_cache_dir()
    if cache_dir.exists():
        shutil.rmtree(cache_dir, ignore_errors=True)


def cache_exists(key: str) -> bool:
    """Check if a public data file is cached.
    
    Args:
        key: Key identifying the public data
    
    Returns:
        True if the file is cached
    """
    if key not in PUBLIC_DATA_URLS:
        return False
    
    info = PUBLIC_DATA_URLS[key]
    cache_dir = _get_cache_dir()
    filename = Path(info["url"]).name
    file_path = cache_dir / filename
    return file_path.exists()