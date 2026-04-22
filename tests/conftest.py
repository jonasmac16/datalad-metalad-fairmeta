"""Pytest configuration and fixtures for datalad-metalad-fairextract tests."""

import os
import shutil
import gzip
import tempfile
from pathlib import Path
from typing import Generator, Any
from uuid import UUID

import pytest


class MockDataset:
    """Mock dataset for testing extractors."""
    
    def __init__(self, path: str | Path):
        self.path = Path(path) if isinstance(path, str) else path
    
    def __repr__(self):
        return f"MockDataset({self.path})"


class MockRefCommit:
    """Mock ref_commit for testing extractors."""
    
    def __init__(self, hexsha: str = "0" * 40):
        self.hexsha = hexsha
    
    def __repr__(self):
        return f"MockRefCommit({self.hexsha[:8]}...)"


class MockFileInfo:
    """Mock file_info for testing file extractors."""
    
    def __init__(self, path: str | Path, byte_size: int = 0):
        self.path = str(path) if isinstance(path, Path) else path
        self.byte_size = byte_size
    
    def __repr__(self):
        return f"MockFileInfo({self.path}, size={self.byte_size})"


def create_mock_extractor(dataset_path: str | Path, ref_commit: Any = None):
    """Factory to create a properly initialized mock extractor."""
    if ref_commit is None:
        ref_commit = MockRefCommit()
    return {
        "dataset": MockDataset(dataset_path),
        "ref_commit": ref_commit,
    }


@pytest.fixture(scope="session")
def test_data_dir() -> Path:
    """Get or create the test data directory (cached at session scope)."""
    test_dir = Path(tempfile.gettempdir()) / "fairmeta_test_data"
    test_dir.mkdir(parents=True, exist_ok=True)
    return test_dir


@pytest.fixture
def temp_dir() -> Generator[Path, None, None]:
    """Create a temporary directory that is cleaned up after the test."""
    temp = tempfile.mkdtemp()
    yield Path(temp)
    shutil.rmtree(temp, ignore_errors=True)


@pytest.fixture
def sample_fastq_content() -> str:
    """Sample FASTQ content for testing."""
    return (
        "@instrument123:456:789 flowcellA:1:1101:12345:6789:ABCDEF "
        "run:SRR1234567 sample:Sample1 study:PRJNA123456 "
        "library:Library1 platform:ILLUMINA\n"
        "ACGTACGTACGTACGTACGTACGTACGTACGT\n"
        "+\n"
        "IIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIII\n"
    )


@pytest.fixture
def sample_fastq_gz_content() -> bytes:
    """Sample gzipped FASTQ content for testing."""
    return gzip.compress(
        b"@instrument123:456:789 flowcellA:1:1101:12345:6789:ABCDEF "
        b"run:SRR1234567 sample:Sample1 study:PRJNA123456 "
        b"library:Library1 platform:ILLUMINA\n"
        b"ACGTACGTACGTACGTACGTACGTACGTACGT\n"
        b"+\n"
        b"IIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIII\n"
    )