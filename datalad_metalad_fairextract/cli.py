#!/usr/bin/env python3
"""CLI tool for merging FAIR metadata with datalad integration.

Usage:
    # Basic merge (smart preserve by default)
    fairmeta-merge auto.json curated.json -o merged.json

    # Explicit smart preserve
    fairmeta-merge auto.json curated.json -o merged.json --preserve-auto smart

    # Preserve specific fields
    fairmeta-merge auto.json curated.json -o merged.json --preserve-auto cell_count,gene_count

    # No smart preserve (curated overrides everything)
    fairmeta-merge auto.json curated.json -o merged.json --preserve-auto none

    # Multi-sample merge
    fairmeta-merge auto.json samples.yaml -o results/

Install:
    pip install -e .
"""

import json
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path

import click


# Comprehensive list of technical fields to preserve from auto-extracted metadata
TECHNICAL_FIELDS = {
    # h5ad/AnnData
    'cell_count', 'gene_count', 'obsm_keys', 'layers',
    'default_embedding', 'batch',

    # Xenium
    'transcript_count', 'transcript_columns',
    'morphology_width', 'morphology_height', 'morphology_channels',
    'cells_detected', 'gene_count', 'transcripts_detected',
    'transcript_file', 'experiment_file', 'morphology_file',

    # SpatialData
    'spatialdata_version', 'element_types', 'element_counts',
    'coordinate_systems',

    # Images/TIFF
    'width', 'height', 'bits_per_sample', 'samples_per_pixel',
    'pixel_type', 'interlace',

    # FASTQ
    'read_count', 'quality_scores', 'read_lengths',
    'read_number', 'sequence_length',

    # OME-TIFF
    'dimension_order', 'pixel_type', 'channel_count',
    'rgb_channels', 'pixel_size',

    # Additional technical fields
    'images', 'labels', 'points', 'shapes', 'tables',
    'transformations', 'uns',
}


def parse_preserve_auto(value: str) -> set:
    """Parse --preserve-auto option value into a set of fields.
    
    Args:
        value: 'smart' (default), 'none', or comma-separated list
    
    Returns:
        Set of field names to preserve from auto, or empty set for none
    """
    if value.lower() == 'none':
        return set()
    elif value.lower() == 'smart':
        return TECHNICAL_FIELDS
    else:
        # Parse comma-separated list
        return {f.strip() for f in value.split(',') if f.strip()}


def smart_merge(auto_meta: dict, curated_meta: dict, preserve_fields: set) -> dict:
    """Merge metadata with smart field preservation.
    
    Args:
        auto_meta: Metadata from auto-extractor
        curated_meta: Metadata from curated sources
        preserve_fields: Set of field names to preserve from auto
    
    Returns:
        Merged metadata dictionary
    """
    if not preserve_fields:
        # No smart preserve - curated overrides everything
        return {**auto_meta, **curated_meta}
    
    merged = {}
    auto_fields = set(auto_meta.keys())
    curated_fields = set(curated_meta.keys())
    all_fields = auto_fields | curated_fields
    
    for field in all_fields:
        if field in preserve_fields and field in auto_meta:
            # Preserve from auto
            merged[field] = auto_meta[field]
        elif field in curated_meta:
            # Use curated if available
            merged[field] = curated_meta[field]
        elif field in auto_meta:
            # Fall back to auto
            merged[field] = auto_meta[field]
    
    return merged


def multi_sample_merge(auto_meta: dict, samples_data: dict, output_dir: Path) -> dict:
    """Merge auto metadata with per-sample metadata.
    
    Args:
        auto_meta: Base metadata from auto-extractor
        samples_data: Dictionary with 'samples' list from samples.yaml
        output_dir: Directory to write individual sample files
    
    Returns:
        Manifest dictionary with sample_id -> filename mappings
    """
    samples = samples_data.get('samples', [])
    if not samples:
        click.echo("Warning: No samples found in samples file", err=True)
        return {}
    
    output_dir.mkdir(parents=True, exist_ok=True)
    manifest = {
        '_generated': datetime.now(timezone.utc).isoformat(),
        '_auto_base': str(auto_meta.get('$schema', 'unknown')),
        'samples': []
    }
    
    for sample in samples:
        sample_id = sample.get('sample_id', 'unknown')
        # Start with auto base, override with sample-specific fields
        merged = {**auto_meta}
        for key, value in sample.items():
            if key != 'sample_id' and value is not None:
                merged[key] = value
        
        # Write sample file
        safe_id = sample_id.replace('/', '_').replace(' ', '_')
        output_file = output_dir / f"{safe_id}.json"
        output_file.write_text(json.dumps(merged, indent=2))
        
        manifest['samples'].append({
            'sample_id': sample_id,
            'file': str(output_file.name)
        })
        
        click.echo(f"Written: {output_file}")
    
    # Write manifest
    manifest_file = output_dir / "_merged_manifest.json"
    manifest_file.write_text(json.dumps(manifest, indent=2))
    click.echo(f"Written manifest: {manifest_file}")
    
    return manifest


def add_to_git(file_path: str, message: str):
    """Add file to git and commit."""
    try:
        click.echo(f"Running: datalad add {file_path}")
        subprocess.run(['datalad', 'add', file_path], check=True, capture_output=True)
        
        click.echo(f"Running: datalad save -m '{message}'")
        subprocess.run(['datalad', 'save', '-m', message], check=True, capture_output=True)
        
        click.echo(f"Committed: {message}")
    except subprocess.CalledProcessError as e:
        click.echo(f"Error during datalad save: {e.stderr}", err=True)
        raise


@click.command()
@click.argument('auto_file', type=click.Path(exists=True))
@click.argument('curated_file', type=click.Path(exists=True), required=False)
@click.option('-o', '--output', 'output_file', type=click.Path(),
              help='Output file or directory (required for merge)')
@click.option('--preserve-auto', default='smart',
              help="Fields to preserve from auto: 'smart'=all technical (default), "
                  "'none'=curated overrides all, or comma-separated list")
@click.option('--add-provenance/--no-provenance', default=True,
              help='Add field source provenance')
@click.option('--no-save', is_flag=True,
              help='Skip datalad add/save (only write output file)')
@click.option('-m', '--message', default='Merged auto-extracted and curated metadata',
              help='Commit message')
def merge(auto_file, curated_file, output_file, preserve_auto, add_provenance, no_save, message):
    """Merge auto-extracted and curated metadata.
    
    AUTO_FILE: JSON file from auto-extractor (e.g., h5ad, xenium, spatialdata)
    CURATED_FILE: YAML/JSON file from templates or manual entry
    
    For multi-sample merge, provide AUTO_FILE and samples.yaml as CURATED_FILE,
    then use -o to specify output directory.
    
    Examples:
        fairmeta-merge auto.json curated.json -o merged.json
        fairmeta-merge auto.json curated.json -o merged.json --preserve-auto smart
        fairmeta-merge auto.json curated.json -o merged.json --preserve-auto cell_count,gene_count
        fairmeta-merge auto.json samples.yaml -o results/ --no-save
    """
    # Parse preserve-auto option
    preserve_fields = parse_preserve_auto(preserve_auto)
    click.echo(f"Preserve-auto strategy: {preserve_auto}")
    if preserve_auto.lower() == 'smart':
        click.echo(f"  Preserving {len(preserve_fields)} technical fields from auto")
    
    # Load auto-extracted metadata
    click.echo(f"Reading auto-extracted: {auto_file}")
    with open(auto_file) as f:
        auto = json.load(f)
    
    auto_meta = auto.get('metadata', {})
    if not auto_meta:
        click.echo("Warning: No 'metadata' key found in auto_file", err=True)
        auto_meta = {}
    
    # Check if this is a multi-sample merge
    is_multi_sample = False
    if curated_file:
        curated_path = Path(curated_file)
        if curated_path.suffix in ['.yaml', '.yml']:
            is_multi_sample = True
    
    if is_multi_sample and output_file:
        # Multi-sample merge
        click.echo(f"Reading samples: {curated_file}")
        try:
            import yaml
            with open(curated_file) as f:
                samples_data = yaml.safe_load(f)
        except ImportError:
            click.echo("Error: PyYAML required for samples file", err=True)
            sys.exit(1)
        
        output_dir = Path(output_file)
        manifest = multi_sample_merge(auto_meta, samples_data, output_dir)
        
        if manifest and not no_save:
            # Add each sample file and manifest to git
            for sample_info in manifest.get('samples', []):
                sample_file = output_dir / sample_info['file']
                add_to_git(str(sample_file), message)
            
            # Add manifest
            manifest_file = output_dir / "_merged_manifest.json"
            add_to_git(str(manifest_file), message)
        
        click.echo(f"Multi-sample merge complete: {len(manifest.get('samples', []))} samples")
        return
    
    # Regular merge requires curated_file
    if not curated_file:
        click.echo("Error: CURATED_FILE required for regular merge", err=True)
        sys.exit(1)
    
    if not output_file:
        click.echo("Error: -o/--output required", err=True)
        sys.exit(1)
    
    # Load curated metadata
    click.echo(f"Reading curated: {curated_file}")
    with open(curated_file) as f:
        curated = json.load(f)
    
    curated_meta = curated.get('metadata', {})
    if not curated_meta:
        click.echo("Warning: No 'metadata' key found in curated_file", err=True)
        curated_meta = {}
    
    # Merge with smart preserve
    merged = smart_merge(auto_meta, curated_meta, preserve_fields)
    
    # Add provenance tracking
    if add_provenance and auto_meta and curated_meta:
        provenance = {}
        for key in auto_meta:
            provenance[key] = 'auto'
        for key in curated_meta:
            if key not in auto_meta:
                provenance[key] = 'curated'
            elif merged.get(key) == curated_meta.get(key):
                provenance[key] = 'curated'
            elif merged.get(key) == auto_meta.get(key):
                provenance[key] = 'auto'
            else:
                provenance[key] = 'curated'
        merged['_field_sources'] = provenance
        click.echo("Added provenance tracking")
    
    # Write output
    output_content = json.dumps(merged, indent=2)
    Path(output_file).write_text(output_content)
    click.echo(f"Written: {output_file}")
    
    if not no_save:
        add_to_git(output_file, message)


if __name__ == '__main__':
    merge()