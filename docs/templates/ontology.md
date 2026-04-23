# Ontology Reference for Templates

Complete reference of ontology terms for liver and related samples.

## Overview

Ontology terms follow the CURIE format: `PREFIX:ID` (e.g., `NCBITaxon:9606`)

Use this reference to find the right terms for your templates.

## Organism (NCBITaxon)

| ID | Label | Common Name |
|----|-------|-----------|
| NCBITaxon:9606 | Homo sapiens | Human |
| NCBITaxon:10090 | Mus musculus | Mouse |
| NCBITaxon:10116 | Rattus norvegicus | Rat |

## Tissue/Organ (UBERON)

### Liver and Related

| ID | Label | Notes |
|----|-------|-------|
| UBERON:0002114 | liver | Main organ |
| UBERON:0002118 | gallbladder | |
| UBERON:0001002 | liver parenchyma | Functional tissue |
| UBERON:0000480 | hepatic lobule | Liver structural unit |
| UBERON:0001284 | hepatic sinusoid | Blood vessels in liver |
| UBERON:0009841 | hepatic portal vein | |
| UBERON:0001137 | hepatic artery | |
| UBERON:0001323 | bile duct | |

### Other Common Tissues

| ID | Label |
|----|-------|
| UBERON:0000955 | brain |
| UBERON:0002048 | lung |
| UBERON:0001255 | pancreas |
| UBERON:0002110 | colon |
| UBERON:0001159 | colonic epithelium |

## Cell Type (CL)

### Liver Cells

| ID | Label |
|----|-------|
| CL:0002304 | hepatocyte | Liver cell, main function |
| CL:0002138 | liver macrophage (Kupffer cell) |
| CL:0002139 | liver sinusoidal endothelial cell |
| CL:0002321 | hepatic stellate cell |
| CL:0000502 | bile duct epithelial cell |

### Cancer Cells

| ID | Label |
|----|-------|
| CL:0001003 | liver carcinoma cell | HCC |
| CL:0001000 | malignant cell | General metastatic |
| CL:0001002 | adenocarcinoma cell | glandular cancer |
| CL:1000001 | metastatic cell | General metastasis |

### Blood/Immune

| ID | Label |
|----|-------|
| CL:0000738 | T cell |
| CL:0000236 | B cell |
| CL:0000576 | macrophage |
| CL:0000767 | monocyte |

## Assay/Technology (EFO)

### Spatial Transcriptomics

| ID | Label |
|----|-------|
| EFO:0009899 | 10x Genomics 3' v3 |
| EFO:0010010 | 10x Genomics Visium |
| EFO:0010011 | 10x Genomics Visium HD |
| EFO:0008681 | MERFISH |
| EFO:0002774 | Imaging mass cytometry |

### Other Assays

| ID | Label |
|----|-------|
| EFO:0000560 | RNA-seq |
| EFO:0001450 | single-cell RNA-seq |
| EFO:0000295 | fluorescence microscopy |

## Disease (MONDO/PATO)

### Normal

| ID | Label |
|----|-------|
| PATO:0000461 | normal | Healthy tissue |

### Liver Cancers

| ID | Label |
|----|-------|
| MONDO:0002317 | hepatocellular carcinoma | Primary HCC |
| MONDO:0004992 | colorectal carcinoma | CRC (used for metastasis) |
| MONDO:0002494 | gallbladder carcinoma |
| MONDO:0004909 | cholangiocarcinoma | Bile duct cancer |

### Other Cancers

| ID | Label |
|----|-------|
| MONDO:0001627 | breast carcinoma |
| MONDO:0002974 | lung carcinoma |
| MONDO:0008909 | pancreatic carcinoma |

### Non-Cancer Disease

| ID | Label |
|----|-------|
| MONDO:0005012 | liver disease |
| MONDO:0005352 | hepatic fibrosis |
| MONDO:0005671 | liver cirrhosis |

## Sex (PATO)

| ID | Label |
|----|-------|
| PATO:0000384 | male |
| PATO:0000383 | female |
| PATO:0001341 | mixed sex | Pooled samples |

## Development Stage (HsapDv)

| ID | Label |
|----|-------|
| HsapDv:0000003 | adult |
| HsapDv:0000198 | child |
| HsapDv:0000242 | elderly |
| HsapDv:0000287 | middle age |

## Ethnicity (HANCESTRO)

| ID | Label |
|----|-------|
| HANCESTRO:0000014 | European |
| HANCESTRO:0000001 | African |
| HANCESTRO:0000005 | Asian |
| HANCESTRO:0019586 | unknown |

## Quick Reference: Liver Samples

### Healthy Liver

```
organism_ontology_term_id:    NCBITaxon:9606
tissue_ontology_term_id:   UBERON:0002114
cell_type_ontology_term_id: CL:0002304
disease_ontology_term_id:   PATO:0000461
```

### Colorectal Liver Metastasis

```
organism_ontology_term_id:    NCBITaxon:9606
tissue_ontology_term_id:   UBERON:0002114
cell_type_ontology_term_id: CL:0001000
disease_ontology_term_id:   MONDO:0004992
```

### Hepatocellular Carcinoma (HCC)

```
organism_ontology_term_id:    NCBITaxon:9606
tissue_ontology_term_id:   UBERON:0002114
cell_type_ontology_term_id: CL:0001003
disease_ontology_term_id:   MONDO:0002317
```

### Gallbladder Carcinoma

```
organism_ontology_term_id:    NCBITaxon:9606
tissue_ontology_term_id:   UBERON:0002118
cell_type_ontology_term_id: CL:0001002
disease_ontology_term_id:   MONDO:0002494
```

## Verifying Ontology Terms

### Online

- [OLS (Ontology Lookup Service)](https://www.ebi.ac.uk/ols4/)
- [NCBI Taxonomy](https://www.ncbi.nlm.nih.gov/taxonomy)
- [Cell Ontology](https://obofoundry.org/ontology/cl.html)

### Programmatic

```python
import requests

def verify_ontology(prefix, term_id):
    """Verify ontology term exists."""
    url = f"https://www.ebi.ac.uk/ols4/api/ontologies/{prefix}/terms/{prefix}%3A{term_id}"
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        print(f"Label: {data.get('label', 'N/A')}")
        return True
    else:
        print(f"Term not found: {response.status_code}")
        return False

# Usage
verify_ontology('uberon', '0002114')  # liver
verify_ontology('mondo', '0004992')  # colorectal carcinoma
```

## Related Documentation

- [Schema Reference](../schemas/index.md) - JSON schema definitions
- [Base Schema](../schemas/base.schema.json) - Core types
- [Examples](templates/examples.md) - Completed template examples