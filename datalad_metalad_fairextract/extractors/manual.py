"""Manual/Interactive metadata extractor.

Allows manual metadata entry for non-standard formats or augmenting automated extraction.
"""

import json
import logging
from pathlib import Path
from typing import Any
from uuid import UUID

import click

from datalad_metalad.extractors.base import (
    DataOutputCategory,
    DatasetMetadataExtractor,
    ExtractorResult,
)

from .base import (
    create_extraction_result,
    create_provenance,
    load_schema,
    prompt_ontology_term,
    prompt_optional_field,
    prompt_required_fields,
    prompt_text_field,
    validate_metadata,
)

logger = logging.getLogger('datalad_metalad_fairextract.manual')

SUPPORTED_SCHEMAS = [
    "h5ad",
    "fastq",
    "spatialdata",
    "xenium",
    "cosmx",
    "visium_hd",
    "merscope",
    "macsima",
    "phenocycler",
    "molecular_cartography",
    "hyperion",
    "tiff",
    "ome_tiff",
    "manual",
]


def get_supported_schemas() -> list[str]:
    """Get list of schemas supported by the manual extractor.
    
    The manual extractor can be used with any of the supported schemas
    as it allows manual metadata entry for any data format.
    
    Returns:
        List of supported schema names
    """
    return SUPPORTED_SCHEMAS.copy()


class FairmetaManualDatasetExtractor(DatasetMetadataExtractor):
    """Manual/interactive metadata extractor for non-standard formats.

    This extractor provides interactive metadata entry via command-line prompts
    or can read metadata from a YAML/JSON config file.

    Usage:
        datalad meta-extract -d . --force-dataset-level fairmeta_manual \\
            interactive true schema h5ad

        datalad meta-extract -d . --force-dataset-level fairmeta_manual \\
            config metadata.yaml schema h5ad
    """

    extractor_name = "fairmeta_manual"
    extractor_version = "1.0.0"

    @staticmethod
    def get_id() -> UUID:
        return UUID("c9d0e1f2-3a4b-5c6d-7e8f-9a0b1c2d3e4f")

    @staticmethod
    def get_version() -> str:
        return "1.0.0"

    @staticmethod
    def get_data_output_category() -> DataOutputCategory:
        return DataOutputCategory.IMMEDIATE

    @staticmethod
    def get_required_content() -> bool:
        return False

    def extract(self, _=None) -> ExtractorResult:
        """Extract or prompt for metadata."""
        metadata = {
            "$schema": "https://datalad-metalad-fairmeta.github.io/schemas/manual.schema.json",
            "schema_version": "1.0.0"
        }
        warnings = []
        errors = []

        interactive = self.parameter.get("interactive", "false").lower() == "true"
        config_path = self.parameter.get("config")
        schema_name = self.parameter.get("schema", "manual")
        use_defaults = self.parameter.get("defaults", "false").lower() == "true"

        dataset_path = str(self.dataset.path)
        logger.info(f"Manual metadata extraction from: {dataset_path}")

        try:
            if interactive:
                metadata.update(self._prompt_interactive(schema_name))
            elif config_path:
                metadata.update(self._load_from_config(config_path))
            elif use_defaults:
                metadata.update(self._use_schema_defaults(schema_name))
            else:
                errors.append(
                    "No interactive mode, config file, or defaults specified. "
                    "Use 'interactive true', 'config <path>', or 'defaults true'"
                )
        except Exception as e:
            errors.append(f"Failed to collect metadata: {str(e)}")

        validation_errors = validate_metadata(metadata, schema_name)
        success = len(errors) == 0 and len(validation_errors) == 0

        return create_extraction_result(
            metadata=metadata,
            extractor_version=self.extractor_version,
            extraction_parameter=self.parameter,
            success=success,
            result_type="dataset",
            validation_errors=validation_errors,
            warnings=warnings,
            provenance=create_provenance(
                self.extractor_name,
                self.extractor_version,
                [dataset_path]
            )
        )

    def _prompt_interactive(self, schema_name: str) -> dict[str, Any]:
        """Prompt user for metadata interactively."""
        click.echo(f"\n{'='*60}")
        click.echo("FAIR Metadata Entry - Interactive Mode")
        click.echo(f"{'='*60}")
        click.echo(f"Dataset: {self.dataset.path}")
        click.echo(f"Schema: {schema_name}")
        click.echo(f"{'='*60}\n")

        metadata = {}

        click.echo("Required Fields:")
        metadata['title'] = prompt_text_field(
            "Title",
            "A descriptive title for this dataset",
            required=True
        )

        click.echo("\nBiological Context (optional but recommended):")

        organism = prompt_ontology_term(
            "Organism",
            "NCBITaxon",
            "The organism studied (e.g., Homo sapiens)",
            required=False
        )
        if organism:
            metadata['organism_ontology_term_id'] = organism

        tissue = prompt_ontology_term(
            "Tissue",
            "UBERON",
            "The tissue or organ studied",
            required=False
        )
        if tissue:
            metadata['tissue_ontology_term_id'] = tissue

        cell_type = prompt_ontology_term(
            "Cell Type",
            "CL",
            "The cell type (if applicable)",
            required=False
        )
        if cell_type:
            metadata['cell_type_ontology_term_id'] = cell_type

        assay = prompt_ontology_term(
            "Assay/Technology",
            "EFO",
            "The experimental assay or technology used",
            required=False
        )
        if assay:
            metadata['assay_ontology_term_id'] = assay

        disease = prompt_ontology_term(
            "Disease State",
            "MONDO",
            "The disease state (PATO:0000461 for normal)",
            required=False
        )
        if disease:
            metadata['disease_ontology_term_id'] = disease

        click.echo("\nOptional Fields:")

        description = prompt_optional_field(
            "Description",
            "Additional description or notes"
        )
        if description:
            metadata['description'] = description

        donor_id = prompt_optional_field(
            "Donor ID",
            "Identifier for the donor/subject"
        )
        if donor_id:
            metadata['donor_id'] = donor_id

        sample_id = prompt_optional_field(
            "Sample ID",
            "Identifier for the biological sample"
        )
        if sample_id:
            metadata['sample_id'] = sample_id

        keywords_str = prompt_optional_field(
            "Keywords",
            "Comma-separated keywords for discoverability"
        )
        if keywords_str:
            metadata['keywords'] = [k.strip() for k in keywords_str.split(',')]

        click.echo(f"\n{'='*60}")
        click.echo("Metadata collection complete!")
        click.echo(f"{'='*60}\n")

        return metadata

    def _load_from_config(self, config_path: str) -> dict[str, Any]:
        """Load metadata from a YAML or JSON config file."""
        path = Path(config_path)

        if not path.is_absolute():
            path = Path(self.dataset.path) / config_path

        if not path.exists():
            raise FileNotFoundError(f"Config file not found: {path}")

        if path.suffix in ['.yaml', '.yml']:
            try:
                import yaml
                with open(path) as f:
                    return yaml.safe_load(f)
            except ImportError:
                raise ImportError("PyYAML required for YAML config files: pip install pyyaml")
        elif path.suffix == '.json':
            with open(path) as f:
                return json.load(f)
        else:
            raise ValueError(f"Unsupported config file format: {path.suffix}")

    def _use_schema_defaults(self, schema_name: str) -> dict[str, Any]:
        """Use schema defaults for metadata."""
        metadata = {
            "$schema": f"https://datalad-metalad-fairmeta.github.io/schemas/{schema_name}.schema.json",
            "schema_version": "1.0.0"
        }

        try:
            schema = load_schema(schema_name)
            props = schema.get("properties", {})

            for field, spec in props.items():
                if "default" in spec:
                    metadata[field] = spec["default"]

        except FileNotFoundError:
            logger.warning(f"Schema not found: {schema_name}")

        return metadata
