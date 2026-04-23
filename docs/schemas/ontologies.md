# Ontology Reference

## Standard Ontology Terms

### Organism (NCBITaxon)

| ID | Label |
|----|-------|
| NCBITaxon:9606 | Homo sapiens (Human) |
| NCBITaxon:10090 | Mus musculus (Mouse) |
| NCBITaxon:10116 | Rattus norvegicus (Rat) |

### Tissue/Organ (UBERON)

| ID | Label |
|----|-------|
| UBERON:0002114 | liver |
| UBERON:0002118 | gallbladder |
| UBERON:0002113 | kidney |
| UBERON:0000955 | brain |
| UBERON:0002048 | lung |
| UBERON:0001255 | pancreas |

> **Tip**: For more liver-specific ontology terms and template examples, see [Template Ontology Reference](../template_docs/ontology.md).

### Cell Type (CL)

| ID | Label |
|----|-------|
| CL:0000738 | T cell |
| CL:0000236 | B cell |
| CL:0000763 | neuron |
| CL:0000576 | epithelial cell |

### Assay/Technology (EFO)

| ID | Label |
|----|-------|
| EFO:0009899 | 10x 3' v3 |
| EFO:0030003 | 10x 5' v2 |
| EFO:0009918 | 10x Visium |
| EFO:0010550 | sciRNA-seq |

### Disease (MONDO/PATO)

| ID | Label |
|----|-------|
| MONDO:0005002 | disease |
| PATO:0000461 | normal |

### Development Stage (HsapDv/MmusDv)

| ID | Label |
|----|-------|
| HsapDv:0000242 | adult |
| HsapDv:0000211 | embryonic stage |
| MmusDv:0000111 | embryo |

### Sex (PATO)

| ID | Label |
|----|-------|
| PATO:0000383 | female |
| PATO:0000384 | male |
| PATO:0001341 | mixed sex |

## Ontology Lookup

### Online Resources

- [Ontology Lookup Service](https://www.ebi.ac.uk/ols/index)
- [NCBITaxon](https://www.ncbi.nlm.nih.gov/taxonomy)
- [UBERON](http://obolibrary.org/muo/umo.owl)
- [EFO](https://www.ebi.ac.uk/efo/)
- [Cell Ontology](https://obofoundry.org/ontology/cl.html)

### Programmatic Lookup

```python
import requests

def lookup_ontology(prefix, term_id):
    url = f"https://www.ebi.ac.uk/ols4/api/ontologies/{prefix}/terms/{prefix}%3A{term_id}"
    response = requests.get(url)
    return response.json()
```
