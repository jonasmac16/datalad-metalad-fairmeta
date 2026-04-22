#!/usr/bin/env python
"""datalad-metalad-fairmeta: FAIR metadata extractors for spatial biology data."""

import os
import hashlib
from pathlib import Path

__docformat__ = 'restructuredtext'

__supported_generations__ = [2, 3, 4]

command_suite = (
    "FAIR metadata extraction for spatial biology data",
    []
)

exclude_from_metadata = ('.datalad', '.git', '.gitmodules', '.gitattributes')

default_context = {
    "@vocab": "http://schema.org/",
    "datalad": "http://dx.datalad.org/",
    "efo": "http://www.ebi.ac.uk/efo/",
    "uberon": "http://purl.obolibrary.org/obo/UBERON_",
    "cl": "http://purl.obolibrary.org/obo/CL_",
    "ncbitaxon": "http://purl.obolibrary.org/obo/NCBITaxon_",
    "mondo": "http://purl.obolibrary.org/obo/MONDO_",
    "pato": "http://purl.obolibrary.org/obo/PATO_",
    "ome": "http://www.openmicroscopy.org/Schemas/OME/2016-06/",
}


def get_agent_id(name, email):
    """Return a suitable '@id' for committers/authors."""
    return hashlib.md5(
        u'{}<{}>'.format(
            name.replace(' ', '_'),
            email
        ).encode('utf-8')
    ).hexdigest()


from ._version import __version__

__all__ = ["__version__", "command_suite", "default_context"]
