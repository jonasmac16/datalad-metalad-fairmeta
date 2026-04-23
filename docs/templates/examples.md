# Template Examples - Liver Samples

Examples of completed templates for common liver sample types.

## Overview

This page shows complete examples for the liver samples you work with:
- Healthy liver
- Colorectal liver metastasis  
- Primary hepatocellular carcinoma (HCC)
- Gallbladder carcinoma

## Example 1: Healthy Liver

### Dataset Metadata

```yaml
$schema: "https://datalad-metalad-fairmeta.github.io/schemas/manual.schema.json"
schema_version: "1.0.0"
title: "Healthy liver control samples - Donor Study 2024"

description: "Normal liver tissue samples from patients undergoing surgical resection for non-tumor conditions. Used as controls for liver metastasis study."

creators:
  - name: "Dr. Jane Smith"
    orcid: "0000-0001-2345-6789"
    affiliation: "University Medical Center"
    role: "creator"

organism_ontology_term_id:
  id: "NCBITaxon:9606"
  label: "Homo sapiens"

tissue_ontology_term_id:
  id: "UBERON:0002114"
  label: "liver"

assay_ontology_term_id:
  id: "EFO:0009899"
  label: "10x Genomics 3' v3"

disease_ontology_term_id:
  id: "PATO:0000461"
  label: "normal"

cell_type_ontology_term_id:
  id: "CL:0002304"
  label: "hepatocyte"

sex_ontology_term_id:
  id: "PATO:0000384"
  label: "male"

donor_id: ["donor_h001", "donor_h002", "donor_h003"]
sample_id: ["sample_h001", "sample_h002", "sample_h003"]

license: "CC BY 4.0"

keywords:
  - liver
  - normal
  - control
  - spatial transcriptomics

related_identifiers: []

custom_fields:
  study_approval: "IRB-2024-0012"
  funding: "NIH R01-CA123456"
```

### Sample Metadata

```yaml
samples:
  - sample_id: "sample_h001"
    donor_id: "donor_h001"
    tissue_ontology_term_id:
      id: "UBERON:0002114"
      label: "liver"
    cell_type_ontology_term_id:
      id: "CL:0002304"
      label: "hepatocyte"
    disease_ontology_term_id:
      id: "PATO:0000461"
      label: "normal"
    sex_ontology_term_id:
      id: "PATO:0000384"
      label: "male"
    collection_date: "2024-01-15"
    collection_method: "surgical resection"
    storage_conditions: "fresh frozen"
    custom_fields:
      liver_function_tests: "normal"
      notes: "Adjacent to colon, no tumor involvement"

  - sample_id: "sample_h002"
    donor_id: "donor_h002"
    tissue_ontology_term_id:
      id: "UBERON:0002114"
      label: "liver"
    cell_type_ontology_term_id:
      id: "CL:0002304"
      label: "hepatocyte"
    disease_ontology_term_id:
      id: "PATO:0000461"
      label: "normal"
    sex_ontology_term_id:
      id: "PATO:0000383"
      label: "female"
    collection_date: "2024-01-20"
    collection_method: "surgical resection"
    storage_conditions: "fresh frozen"
    custom_fields:
      notes: "Cholecystectomy adjacent tissue"

  - sample_id: "sample_h003"
    donor_id: "donor_h003"
    tissue_ontology_term_id:
      id: "UBERON:0002114"
      label: "liver"
    cell_type_ontology_term_id:
      id: "CL:0002304"
      label: "hepatocyte"
    disease_ontology_term_id:
      id: "PATO:0000461"
      label: "normal"
    sex_ontology_term_id:
      id: "PATO:0000384"
      label: "male"
    collection_date: "2024-02-01"
    collection_method: "surgical resection"
    storage_conditions: "fresh frozen"
    custom_fields:
      notes: "Living donor, normal scans"
```

## Example 2: Colorectal Liver Metastasis

### Dataset Metadata

```yaml
$schema: "https://datalad-metalad-fairmeta.github.io/schemas/manual.schema.json"
schema_version: "1.0.0"
title: "Colorectal cancer liver metastasis - Spatial transcriptomics study"

description: "Spatial transcriptomics analysis of colorectal carcinoma metastases to liver. Primary tumor origin confirmed by pathology."

creators:
  - name: "Dr. Jane Smith"
    orcid: "0000-0001-2345-6789"
    affiliation: "University Medical Center"
    role: "creator"
  - name: "Dr. John Doe"
    affiliation: "University Medical Center"
    role: "principal_investigator"

organism_ontology_term_id:
  id: "NCBITaxon:9606"
  label: "Homo sapiens"

tissue_ontology_term_id:
  id: "UBERON:0002114"
  label: "liver"

assay_ontology_term_id:
  id: "EFO:0009899"
  label: "10x Genomics 3' v3"

disease_ontology_term_id:
  id: "MONDO:0004992"
  label: "colorectal carcinoma"

donor_id: ["donor_lm001", "donor_lm002"]
sample_id: ["sample_lm001", "sample_lm002"]

license: "CC BY 4.0"

keywords:
  - colorectal cancer
  - liver metastasis
  - spatial transcriptomics
  - CRC

related_identifiers:
  - type: "doi"
    value: "10.1038/s41587-023-0123-4"
    relation: "cites"
  - type: "geo"
    value: "GSE123456"
    relation: "is_part_of"

custom_fields:
  study_name: "Liver Metastasis Project 2024"
  study_approval: "IRB-2024-0123"
  primary_tumor: "colorectal adenocarcinoma"
```

### Sample Metadata

```yaml
samples:
  - sample_id: "sample_lm001"
    donor_id: "donor_lm001"
    tissue_ontology_term_id:
      id: "UBERON:0002114"
      label: "liver"
    cell_type_ontology_term_id:
      id: "CL:0001000"
      label: "metastatic cancer cell"
    disease_ontology_term_id:
      id: "MONDO:0004992"
      label: "colorectal carcinoma"
    sex_ontology_term_id:
      id: "PATO:0000383"
      label: "female"
    
    collection_date: "2024-02-15"
    collection_method: "surgical resection"
    storage_conditions: "fresh frozen"
    
    custom_fields:
      primary_tumor_origin: "colon adenocarcinoma"
      primary_tumor_stage: "T3N1M1"
      metastasis_location: "segment VII, right lobe"
      metastasis_size_cm: 2.5
      kras_mutation: "positive"
      braf_mutation: "negative"
      ms_status: "microsatellite stable"
      notes: "Solitary lesion, surgical margin clear"

  - sample_id: "sample_lm002"
    donor_id: "donor_lm002"
    tissue_ontology_term_id:
      id: "UBERON:0002114"
      label: "liver"
    cell_type_ontology_term_id:
      id: "CL:0001000"
      label: "metastatic cancer cell"
    disease_ontology_term_id:
      id: "MONDO:0004992"
      label: "colorectal carcinoma"
    sex_ontology_term_id:
      id: "PATO:0000384"
      label: "male"
    
    collection_date: "2024-02-20"
    collection_method: "surgical resection"
    storage_conditions: "fresh frozen"
    
    custom_fields:
      primary_tumor_origin: "colon adenocarcinoma"
      primary_tumor_stage: "T4N0M1"
      metastasis_location: "segment VIII, left lobe"
      metastasis_size_cm: 3.2
      kras_mutation: "negative"
      braf_mutation: "positive"
      notes: "Multiple small satellite lesions present"
```

## Example 3: Primary Hepatocellular Carcinoma (HCC)

### Dataset Metadata

```yaml
$schema: "https://datalad-metalad-fairmeta.github.io/schemas/manual.schema.json"
schema_version: "1.0.0"
title: "Hepatocellular carcinoma - Spatial transcriptomics"

description: "Primary liver cancer (HCC) samples with adjacent normal tissue. Includes comprehensive clinical annotation."

creators:
  - name: "Dr. Jane Smith"
    orcid: "0000-0001-2345-6789"
    affiliation: "University Medical Center"
    role: "creator"
  - name: "Dr. John Doe"
    affiliation: "University Medical Center"
    role: "principal_investigator"

organism_ontology_term_id:
  id: "NCBITaxon:9606"
  label: "Homo sapiens"

tissue_ontology_term_id:
  id: "UBERON:0002114"
  label: "liver"

assay_ontology_term_id:
  id: "EFO:0009899"
  label: "10x Genomics 3' v3"

disease_ontology_term_id:
  id: "MONDO:0002317"
  label: "hepatocellular carcinoma"

donor_id: ["donor_hcc001", "donor_hcc002"]
sample_id: ["sample_hcc001", "sample_hcc002"]

license: "CC BY 4.0"

keywords:
  - hepatocellular carcinoma
  - HCC
  - liver cancer
  - primary liver tumor

related_identifiers:
  - type: "doi"
    value: "10.1038/s41587-024-5678-9"
  - type: "geo"
    value: "GSE234567"

custom_fields:
  study_approval: "IRB-2024-0345"
```

### Sample Metadata

```yaml
samples:
  - sample_id: "sample_hcc001"
    donor_id: "donor_hcc001"
    tissue_ontology_term_id:
      id: "UBERON:0002114"
      label: "liver"
    cell_type_ontology_term_id:
      id: "CL:0001003"
      label: "hepatocellular carcinoma cell"
    disease_ontology_term_id:
      id: "MONDO:0002317"
      label: "hepatocellular carcinoma"
    sex_ontology_term_id:
      id: "PATO:0000384"
      label: "male"
    
    collection_date: "2024-03-01"
    collection_method: "surgical resection"
    storage_conditions: "fresh frozen"
    
    custom_fields:
      afp_ng_ml: 1250
      liver_cirrhosis: "yes"
      fibrosis_stage: "F3"
      tumor_grade: "Edmondson-Steiner II"
      vascular_invasion: "no"
      bCLC_stage: "A2"
      notes: "Solitary lesion, 4cm diameter"

  - sample_id: "sample_hcc002"
    donor_id: "donor_hcc002"
    tissue_ontology_term_id:
      id: "UBERON:0002114"
      label: "liver"
    cell_type_ontology_term_id:
      id: "CL:0001003"
      label: "hepatocellular carcinoma cell"
    disease_ontology_term_id:
      id: "MONDO:0002317"
      label: "hepatocellular carcinoma"
    sex_ontology_term_id:
      id: "PATO:0000383"
      label: "female"
    
    collection_date: "2024-03-10"
    collection_method: "surgical resection"
    storage_conditions: "fresh frozen"
    
    custom_fields:
      afp_ng_ml: 8500
      liver_cirrhosis: "yes"
      fibrosis_stage: "F4"
      tumor_grade: "Edmondson-Steiner III"
      vascular_invasion: "yes"
      bCLC_stage: "B"
      notes: "Multifocal lesions"
```

## Example 4: Gallbladder Carcinoma

### Dataset Metadata

```yaml
$schema: "https://datalad-metalad-fairmeta.github.io/schemas/manual.schema.json"
schema_version: "1.0.0"
title: "Gallbladder carcinoma - Tissue atlas"

creators:
  - name: "Dr. Jane Smith"
    orcid: "0000-0001-2345-6789"
    role: "creator"

organism_ontology_term_id:
  id: "NCBITaxon:9606"
  label: "Homo sapiens"

tissue_ontology_term_id:
  id: "UBERON:0002118"
  label: "gallbladder"

assay_ontology_term_id:
  id: "EFO:0009899"
  label: "10x Genomics 3' v3"

disease_ontology_term_id:
  id: "MONDO:0002494"
  label: "gallbladder carcinoma"
```

### Sample Metadata

```yaml
samples:
  - sample_id: "sample_gbc001"
    donor_id: "donor_gbc001"
    tissue_ontology_term_id:
      id: "UBERON:0002118"
      label: "gallbladder"
    cell_type_ontology_term_id:
      id: "CL:0001002"
      label: "gallbladder adenocarcinoma cell"
    disease_ontology_term_id:
      id: "MONDO:0002494"
      label: "gallbladder carcinoma"
    
    collection_date: "2024-04-01"
    collection_method: "cholecystectomy"
    storage_conditions: "formalin fixed paraffin embedded"
    
    custom_fields:
      tumor_stage: "T2N0M0"
      histology_type: "adenocarcinoma"
      notes: "Incidental finding"
```

## Quick Reference: Liver Ontology Terms

| Sample Type | Tissue (UBERON) | Disease (MONDO/PATO) | Cell Type (CL) |
|-------------|-----------------|-------------------|----------------|
| Healthy | UBERON:0002114 | PATO:0000461 | CL:0002304 |
| CRC Met | UBERON:0002114 | MONDO:0004992 | CL:0001000 |
| HCC | UBERON:0002114 | MONDO:0002317 | CL:0001003 |
| GB Ca | UBERON:0002118 | MONDO:0002494 | CL:0001002 |

## Next Steps

- [Quick Start](templates/quickstart.md) - Start from scratch
- [Merging Guide](templates/merging.md) - Combine with auto-extracted data
- [Ontology Reference](templates/ontology.md) - All available terms