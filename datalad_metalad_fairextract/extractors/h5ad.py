"""AnnData h5ad file metadata extractor.

Extracts metadata from AnnData h5ad files following scFAIR standards.
"""

import logging
from pathlib import Path
from typing import Any
from uuid import UUID

from datalad_metalad.extractors.base import (
    DataOutputCategory,
    ExtractorResult,
    FileMetadataExtractor,
)

from .base import create_extraction_result, create_provenance, validate_metadata

logger = logging.getLogger('datalad_metalad_fairextract.h5ad')

H5AD_EXTENSIONS = ['.h5ad']


class H5adFileExtractor(FileMetadataExtractor):
    """Extract metadata from AnnData h5ad files.

    This extractor reads h5ad files and extracts metadata following
    scFAIR v7.1 and CELLxGENE schema conventions.
    """

    extractor_name = "fairmeta_h5ad"
    extractor_version = "1.0.0"

    @staticmethod
    def get_id() -> UUID:
        return UUID("d4e5f6a7-8b9c-0d1e-2f3a-4b5c6d7e8f9a")

    @staticmethod
    def get_version() -> str:
        return "1.0.0"

    @staticmethod
    def get_data_output_category() -> DataOutputCategory:
        return DataOutputCategory.IMMEDIATE

    def is_content_required(self) -> bool:
        return True

    def extract(self, _=None) -> ExtractorResult:
        """Extract h5ad metadata from the file."""
        metadata = {
            "$schema": "https://datalad-metalad-fairmeta.github.io/schemas/h5ad.schema.json",
            "schema_version": "1.0.0"
        }
        warnings = []
        errors = []

        file_path = self.file_info.path
        logger.info(f"Extracting h5ad metadata from: {file_path}")

        try:
            h5ad_metadata, extracted_warnings = self._extract_h5ad_metadata(file_path)
            metadata.update(h5ad_metadata)
            warnings.extend(extracted_warnings)
        except ImportError:
            errors.append("anndata library not available. Install with: pip install anndata")
            return create_extraction_result(
                metadata=metadata,
                extractor_version=self.extractor_version,
                extraction_parameter=self.parameter,
                success=False,
                result_type="file",
                validation_errors=errors,
                warnings=warnings,
                provenance=create_provenance(
                    self.extractor_name,
                    self.extractor_version,
                    [file_path]
                )
            )
        except Exception as e:
            errors.append(f"Failed to parse h5ad file: {str(e)}")
            return create_extraction_result(
                metadata=metadata,
                extractor_version=self.extractor_version,
                extraction_parameter=self.parameter,
                success=False,
                result_type="file",
                validation_errors=errors,
                warnings=warnings,
                provenance=create_provenance(
                    self.extractor_name,
                    self.extractor_version,
                    [file_path]
                )
            )

        validation_errors = validate_metadata(metadata, "h5ad")
        success = len(errors) == 0 and len(validation_errors) == 0

        return create_extraction_result(
            metadata=metadata,
            extractor_version=self.extractor_version,
            extraction_parameter=self.parameter,
            success=success,
            result_type="file",
            validation_errors=validation_errors,
            warnings=warnings,
            provenance=create_provenance(
                self.extractor_name,
                self.extractor_version,
                [file_path]
            )
        )

    def _extract_h5ad_metadata(self, file_path: str) -> tuple[dict[str, Any], list[str]]:
        """Extract h5ad metadata using anndata library.
        
        Returns:
            Tuple of (metadata dict, warnings list)
        """
        import anndata as ad

        adata = ad.read_h5ad(file_path, backed='r')

        metadata = {}
        warnings = []

        if hasattr(adata, 'n_obs') and adata.n_obs:
            metadata["cell_count"] = adata.n_obs

        if hasattr(adata, 'n_vars') and adata.n_vars:
            metadata["gene_count"] = adata.n_vars

        uns = adata.uns if hasattr(adata, 'uns') else {}
        obs = adata.obs if hasattr(adata, 'obs') else None

        obs_columns = list(obs.columns) if obs is not None else []

        scfair_fields = [
            'organism_ontology_term_id',
            'tissue_ontology_term_id',
            'cell_type_ontology_term_id',
            'assay_ontology_term_id',
            'disease_ontology_term_id',
            'development_stage_ontology_term_id',
            'sex_ontology_term_id',
            'self_reported_ethnicity_ontology_term_id',
        ]

        for field in scfair_fields:
            if field in obs_columns:
                unique_vals = obs[field].dropna().unique()
                if len(unique_vals) == 1:
                    val = str(unique_vals[0])
                    if '_' in val and ':' not in val:
                        ontology, term_id = val.split('_', 1)
                        metadata[field] = {
                            "id": f"{ontology.upper()}:{term_id}",
                            "label": val
                        }
                    else:
                        metadata[field] = {"id": val, "label": val}
                elif len(unique_vals) > 1:
                    warnings.append(
                        f"{field}: Multiple values found, first value used"
                    )
                    val = str(unique_vals[0])
                    metadata[field] = {"id": val, "label": val}

            if field in uns:
                val = uns[field]
                if isinstance(val, str):
                    if '_' in val and ':' not in val:
                        ontology, term_id = val.split('_', 1)
                        metadata[field] = {
                            "id": f"{ontology.upper()}:{term_id}",
                            "label": val
                        }
                    else:
                        metadata[field] = {"id": val, "label": val}

        if hasattr(adata, 'obsm') and adata.obsm:
            metadata["obsm_keys"] = list(adata.obsm.keys())
            if 'X_emb' not in metadata.get("obsm_keys", []) and len(adata.obsm.keys()) > 0:
                first_key = list(adata.obsm.keys())[0]
                metadata["default_embedding"] = first_key

        if hasattr(adata, 'layers') and adata.layers:
            metadata["layers"] = list(adata.layers.keys())

        if hasattr(adata, 'raw') and adata.raw is not None:
            if 'raw' not in metadata.get("layers", []):
                metadata.setdefault("layers", []).append("raw")

        for key in ['title', 'description', 'batch', 'is_primary_data', 'tissue_type', 'suspension_type']:
            if key in uns:
                metadata[key] = uns[key]

        metadata["uns"] = {k: str(v) for k, v in uns.items()
                          if k not in scfair_fields and not k.startswith('_')}

        return metadata, warnings
