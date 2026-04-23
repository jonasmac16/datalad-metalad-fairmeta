#!/usr/bin/env python3
"""CLI tool for merging FAIR metadata with datalad integration.

Usage:
    fairmeta-merge auto.json curated.json -o merged.json
    fairmeta-merge auto.json curated.json -o merged.json -m "Custom message"
    fairmeta-merge auto.json curated.json -o merged.json --no-save

Install:
    pip install -e .
"""

import json
import subprocess
import sys
from pathlib import Path

import click


@click.command()
@click.argument('auto_file', type=click.Path(exists=True))
@click.argument('curated_file', type=click.Path(exists=True))
@click.option('-o', '--output', 'output_file', type=click.Path(),
              help='Output file (default: stdout)')
@click.option('--add-provenance/--no-provenance', default=True,
              help='Add field source provenance')
@click.option('--no-save', is_flag=True,
              help='Skip datalad add/save (only write output file)')
@click.option('-m', '--message', default='Merged auto-extracted and curated metadata',
              help='Commit message')
def merge(auto_file, curated_file, output_file, add_provenance, no_save, message):
    """Merge auto-extracted and curated metadata.
    
    AUTO_FILE: JSON file from auto-extractor (e.g., h5ad, xenium, spatialdata)
    CURATED_FILE: YAML/JSON file from templates or manual entry
    
    Merges the metadata from two files, with curated fields overriding
    auto-extracted fields for any overlaps. Optionally tracks the source
    of each field via provenance tracking.
    """
    click.echo(f"Reading auto-extracted: {auto_file}")
    with open(auto_file) as f:
        auto = json.load(f)
    
    click.echo(f"Reading curated: {curated_file}")
    with open(curated_file) as f:
        curated = json.load(f)
    
    auto_meta = auto.get('metadata', {})
    curated_meta = curated.get('metadata', {})
    
    if not auto_meta:
        click.echo("Warning: No 'metadata' key found in auto_file", err=True)
    if not curated_meta:
        click.echo("Warning: No 'metadata' key found in curated_file", err=True)
    
    merged = {**auto_meta, **curated_meta}
    
    if add_provenance and auto_meta and curated_meta:
        merged['_field_sources'] = {
            **{k: 'auto' for k in auto_meta},
            **{k: 'curated' for k in curated_meta if k not in auto_meta}
        }
        click.echo("Added provenance tracking")
    
    output_content = json.dumps(merged, indent=2)
    
    if output_file:
        Path(output_file).write_text(output_content)
        click.echo(f"Written: {output_file}")
        
        if not no_save:
            try:
                click.echo(f"Running: datalad add {output_file}")
                subprocess.run(['datalad', 'add', output_file], check=True, capture_output=True)
                
                click.echo(f"Running: datalad save -m '{message}'")
                subprocess.run(['datalad', 'save', '-m', message], check=True, capture_output=True)
                
                click.echo(f"Committed: {message}")
            except subprocess.CalledProcessError as e:
                click.echo(f"Error during datalad save: {e.stderr}", err=True)
                sys.exit(1)
    else:
        click.echo(output_content)


if __name__ == '__main__':
    merge()