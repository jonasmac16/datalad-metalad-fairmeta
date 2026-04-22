# Testing Guide

This document describes how to run tests for datalad-metalad-fairmeta.

## Running Tests

### Basic Test Run

```bash
# Install test dependencies first
pip install -e ".[test]"

# Run all tests
pytest

# Run with verbose output
pytest -v

# Run specific test file
pytest tests/test_base.py

# Run specific test class
pytest tests/test_base.py::TestSchemaUtilities

# Run specific test
pytest tests/test_base.py::TestSchemaUtilities::test_validate_metadata_valid
```

### Test Output Options

```bash
# Show skip reasons
pytest -rs

# Show full output (no capture)
pytest --capture=no

# Show short tracebacks
pytest --tb=short

# Run tests in parallel (requires pytest-xdist)
pytest -n auto
```

### Test Coverage

```bash
# Run with coverage report
pytest --cov=datalad_metalad_fairextract

# Generate HTML coverage report
pytest --cov=datalad_metalad_fairextract --cov-report=html
```

## Test Organization

- `tests/test_base.py` - Base utilities and schema validation tests
- `tests/test_dataset_extractors.py` - Dataset extractor registration tests
- `tests/test_fastq.py` - FASTQ extractor tests
- `tests/test_h5ad.py` - h5ad/AnnData extractor tests
- `tests/test_manual.py` - Manual extractor tests
- `tests/test_ome_tiff.py` - OME-TIFF extractor tests
- `tests/test_spatialdata.py` - SpatialData extractor tests
- `tests/test_tiff.py` - TIFF extractor tests
- `tests/test_data/synthetic.py` - Synthetic data generation utilities

## Test Dependencies

The following optional dependencies enable additional tests:

```bash
# Install all test dependencies
pip install -e ".[test]"

# This includes:
# - anndata>=0.7.0 - For h5ad tests
# - scanpy>=1.9.0 - For h5ad public data tests
# - ome-types>=0.4.0 - For OME-TIFF tests
# - spatialdata>=0.4.0 - For SpatialData tests
# - tifffile>=2021.0 - For TIFF tests
# - numpy>=1.20.0 - For synthetic data generation
# - pandas>=1.5.0 - For data manipulation
# - pillow>=9.0.0 - For image tests
# - pyarrow>=10.0.0 - For data format tests
```

## Expected Test Results

After installing test dependencies, all 162 tests should pass:

```
======================== 162 passed, 0 skipped, 1 warning ========================
```

The warning is from the `ome_zarr` library about deprecated `Scaler` class usage and can be ignored.

## Troubleshooting

### Tests Skipping Due to Missing Dependencies

If tests are skipped with messages like "spatialdata not available", install the optional dependencies:

```bash
pip install -e ".[test]"
```

### Tests Skipping Due to API Changes

Some tests may skip if external library APIs have changed. These tests provide informative skip messages indicating what needs to be updated.

### Import Errors

If you encounter import errors, ensure the package is installed in development mode:

```bash
pip install -e .
```