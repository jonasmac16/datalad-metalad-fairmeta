"""Base utilities for fairmeta extractors.

This module provides:
- Schema loading and validation
- Interactive prompt helpers
- Common extraction utilities
"""

import json
import logging
import re
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

import click

from datalad_metalad.extractors.base import (
    DataOutputCategory,
    DatasetMetadataExtractor,
    ExtractorResult,
    FileMetadataExtractor,
)
from uuid import UUID

logger = logging.getLogger('datalad_metalad_fairextract.base')

SCHEMA_DIR = Path(__file__).parent.parent / "schemas"

_schema_registry = None
_schema_resolver = None


def _get_schema_registry():
    """Get or create the schema registry for resolving local $ref references."""
    global _schema_registry, _schema_resolver
    
    if _schema_registry is None:
        _schema_registry = {}
        _schema_resolver = None
        
        for schema_file in SCHEMA_DIR.glob("*.schema.json"):
            with open(schema_file) as f:
                _schema_registry[schema_file.name] = json.load(f)
    
    return _schema_registry, _schema_resolver


class SchemaValidationError(Exception):
    """Raised when metadata validation fails."""
    pass


def get_schema_path(schema_name: str) -> Path:
    """Get the path to a schema file.
    
    Args:
        schema_name: Name of the schema (without .schema.json extension)
        
    Returns:
        Path to the schema file
    """
    return SCHEMA_DIR / f"{schema_name}.schema.json"


def load_schema(schema_name: str) -> dict[str, Any]:
    """Load a JSON schema from the schemas directory.
    
    Args:
        schema_name: Name of the schema to load
        
    Returns:
        Parsed JSON schema as dictionary
        
    Raises:
        FileNotFoundError: If schema file doesn't exist
    """
    schema_path = get_schema_path(schema_name)
    if not schema_path.exists():
        raise FileNotFoundError(f"Schema not found: {schema_path}")
    
    with open(schema_path) as f:
        return json.load(f)


def _preprocess_schema(schema: dict[str, Any], schemas: dict[str, Any]) -> dict[str, Any]:
    """Preprocess schema to inline $defs and replace file references with local refs."""
    import copy
    import json
    
    processed = copy.deepcopy(schema)
    
    base_defs = schemas.get("base.schema.json", {}).get("$defs", {})
    if base_defs:
        processed["$defs"] = {**base_defs, **processed.get("$defs", {})}
    
    schema_str = json.dumps(processed)
    schema_str = schema_str.replace('"base.schema.json#', '"#')
    processed = json.loads(schema_str)
    
    return processed


def _create_validator(schema_name: str):
    """Create a jsonschema validator with local schema resolution.
    
    Args:
        schema_name: Name of the schema to validate against
        
    Returns:
        Tuple of (schema, validator)
    """
    from jsonschema import Draft7Validator
    
    schema = load_schema(schema_name)
    schemas, _ = _get_schema_registry()
    
    schema = _preprocess_schema(schema, schemas)
    validator = Draft7Validator(schema)
    
    return schema, validator


def validate_metadata(
    metadata: dict[str, Any],
    schema_name: str,
    raise_on_error: bool = False
) -> list[str]:
    """Validate metadata against a JSON schema.
    
    Args:
        metadata: Metadata dictionary to validate
        schema_name: Name of the schema to validate against
        raise_on_error: If True, raise SchemaValidationError on failure
        
    Returns:
        List of validation error messages (empty if valid)
    """
    try:
        from jsonschema import ValidationError
        
        _, validator = _create_validator(schema_name)
        
        errors = []
        for error in validator.iter_errors(metadata):
            path = ".".join(str(p) for p in error.path) if error.path else "root"
            errors.append(f"{path}: {error.message}")
        
        if errors and raise_on_error:
            raise SchemaValidationError("\n".join(errors))
        
        return errors
        
    except ImportError:
        logger.warning("jsonschema not installed, skipping validation")
        return []


def validate_curie_format(value: str) -> bool:
    """Validate CURIE format (e.g., EFO:0009899).
    
    Args:
        value: String to validate
        
    Returns:
        True if valid CURIE format
    """
    return bool(re.match(r'^[A-Za-z]+:\d+$', value))


ONTOLOGY_LABEL_CACHE: dict[str, str] = {}


def lookup_ontology_label(curie: str) -> str | None:
    """Look up the label for an ontology term.
    
    This is a placeholder that returns the ID as label.
    In production, this could query an ontology service.
    
    Args:
        curie: CURIE identifier (e.g., "EFO:0009899")
        
    Returns:
        Human-readable label or None
    """
    if curie in ONTOLOGY_LABEL_CACHE:
        return ONTOLOGY_LABEL_CACHE[curie]
    
    return curie


def prompt_ontology_term(
    field_name: str,
    ontology_name: str,
    description: str | None = None,
    required: bool = True
) -> dict[str, str] | None:
    """Prompt user for an ontology term with validation.
    
    Args:
        field_name: Name of the field being prompted
        ontology_name: Name of the ontology (e.g., "EFO", "UBERON")
        description: Optional description of what to enter
        required: If True, user must enter a value
        
    Returns:
        Dictionary with 'id' and 'label' keys, or None if skipped
    """
    example = f"{ontology_name}:0000001"
    prompt_text = f"{field_name} ({ontology_name})"
    
    if description:
        click.echo(f"\n  {description}")
    
    click.echo(f"  Example: {example}")
    
    while True:
        id_input = click.prompt(
            f"  {prompt_text}",
            default="",
            type=str
        ).strip()
        
        if not id_input:
            if required:
                click.echo("  This field is required. Please enter a value.")
                continue
            return None
        
        if validate_curie_format(id_input):
            label = lookup_ontology_label(id_input)
            return {"id": id_input, "label": label if label else id_input}
        else:
            click.echo(f"  Invalid format. Use CURIE format: {example}")


def prompt_text_field(
    field_name: str,
    description: str | None = None,
    required: bool = True,
    default: str = ""
) -> str | None:
    """Prompt user for a text field.
    
    Args:
        field_name: Name of the field being prompted
        description: Optional description
        required: If True, user must enter a value
        default: Default value
        
    Returns:
        Entered value or None if skipped
    """
    if description:
        click.echo(f"\n  {description}")
    
    while True:
        value = click.prompt(
            f"  {field_name}",
            default=default,
            type=str
        ).strip()
        
        if not value:
            if required:
                click.echo("  This field is required. Please enter a value.")
                continue
            return None
        
        return value


def prompt_optional_field(
    field_name: str,
    description: str | None = None
) -> str | None:
    """Prompt user for an optional text field.
    
    Args:
        field_name: Name of the field being prompted
        description: Optional description
        
    Returns:
        Entered value or None if skipped/empty
    """
    if description:
        click.echo(f"\n  {description}")
    
    value = click.prompt(
        f"  {field_name} (optional)",
        default="",
        type=str
    ).strip()
    
    return value if value else None


def prompt_required_fields(
    fields: list[dict[str, Any]],
    metadata: dict[str, Any] | None = None
) -> dict[str, Any]:
    """Prompt user for required fields.
    
    Args:
        fields: List of field definitions with 'name', 'type', and optional 'description'
        metadata: Existing metadata to populate
        
    Returns:
        Dictionary of field values
    """
    if metadata is None:
        metadata = {}
    
    for field in fields:
        field_name = field.get('name', '')
        field_type = field.get('type', 'text')
        description = field.get('description', '')
        required = field.get('required', True)
        
        if field_type == 'ontology':
            value = prompt_ontology_term(
                field_name,
                field.get('ontology', ''),
                description,
                required=required
            )
        elif field_type == 'text':
            value = prompt_text_field(
                field_name,
                description,
                required=required
            )
        else:
            value = prompt_optional_field(field_name, description)
        
        if value is not None:
            metadata[field_name] = value
    
    return metadata


def create_provenance(
    extractor_id: str,
    extractor_version: str,
    source_files: list[str] | None = None
) -> dict[str, Any]:
    """Create a provenance dictionary.
    
    Args:
        extractor_id: Unique identifier of the extractor
        extractor_version: Version of the extractor
        source_files: List of source file paths
        
    Returns:
        Provenance dictionary
    """
    return {
        "extractor_id": extractor_id,
        "extractor_version": extractor_version,
        "extraction_date": datetime.now(timezone.utc).isoformat().replace("+00:00", "Z"),
        "source_files": source_files or []
    }


def create_extraction_result(
    metadata: dict[str, Any],
    extractor_version: str,
    extraction_parameter: dict[str, Any] | None,
    success: bool,
    result_type: str = "file",
    validation_errors: list[str] | None = None,
    warnings: list[str] | None = None,
    provenance: dict[str, Any] | None = None
) -> ExtractorResult:
    """Create an ExtractorResult with standard formatting.
    
    Args:
        metadata: Extracted metadata
        extractor_version: Version of the extractor
        extraction_parameter: Parameters passed to extractor
        success: Whether extraction succeeded
        result_type: Type of result ('file' or 'dataset')
        validation_errors: List of validation errors
        warnings: List of warnings
        provenance: Provenance information
        
    Returns:
        Formatted ExtractorResult
    """
    result_metadata = metadata.copy() if metadata else {}
    
    if warnings:
        result_metadata["warnings"] = warnings
    
    if validation_errors:
        result_metadata["validation_errors"] = validation_errors
    
    if provenance:
        result_metadata["provenance"] = provenance
    
    return ExtractorResult(
        extractor_version=extractor_version,
        extraction_parameter=extraction_parameter or {},
        extraction_success=success,
        datalad_result_dict={
            "type": result_type,
            "status": "ok" if success else "error"
        },
        immediate_data=result_metadata if result_metadata else {}
    )


def get_file_extension(path: str) -> str:
    """Get the file extension from a path.
    
    Args:
        path: File path
        
    Returns:
        Lowercase extension including the dot (e.g., '.tif' or '.ome.tiff')
    """
    return Path(path).suffix.lower()


def get_directory_patterns(path: str) -> tuple[str, ...]:
    """Get directory path patterns for dataset-level detection.
    
    Args:
        path: Directory path
        
    Returns:
        Tuple of path components for pattern matching
    """
    return Path(path).parts


class ExtractorBase:
    """Base class functionality shared by all extractors."""
    
    extractor_name: str = "base"
    extractor_version: str = "0.1.0"
    
    @staticmethod
    def get_uuid() -> UUID:
        """Get the unique UUID for this extractor.
        
        Override in subclasses.
        """
        return UUID("00000000-0000-0000-0000-000000000000")
    
    def log_info(self, message: str) -> None:
        """Log an info message."""
        logger.info(f"[{self.extractor_name}] {message}")
    
    def log_warning(self, message: str) -> None:
        """Log a warning message."""
        logger.warning(f"[{self.extractor_name}] {message}")
    
    def log_error(self, message: str) -> None:
        """Log an error message."""
        logger.error(f"[{self.extractor_name}] {message}")
