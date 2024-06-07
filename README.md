# VLASS-wrappers
Wrapper scripts for VLASS catalog routines.


## Overview
This repository hosts scripts that act as a wrapper for pipelines processing data from the Very Large Array Sky Survey (VLASS) to produce Science Ready Data Products (SRDPs), including various catalogs. These scripts streamline the entire process, from NRAO VLASS image retrieval to cataloging. The repository's main purpose is to create a standalone docker image for running the various pipelines end to end by using these scripts.


### Pipelines Overview

- **Pipeline 1**: Downloads VLASS images and performs source extraction to create component and subtile catalogs.
- **Pipeline 2**: Associates VLASS radio components with astronomical sources using unWISE data.
- **Pipeline 3**: Uses a self-organizing map (SOM) to cluster radio components based on morphology.
- **Pipeline 4**: Identifies doubles in VLASS and potential host candidates, resolving host identifications with a likelihood ratio code.

Each pipeline is documented further in the subsequent sections, including hardware requirements and additional operational details.

## Repository Contents

### Python Scripts

- **pipe1.py**
  - **Description**: Script automating Pipeline 1 steps.
  
- **pipe2.sh**
  - **Description**: Script automating Pipeline 1 steps.

- **pipe3_2.sh**
  - **Description**: Script to execute SOM pipeline.

- **automate.py**
  - **Description**: Script to generate bash scripts that .

- **finalize_catalogs.py**
  - **Description**: Finalizes the catalogs.

- **add_spix.py**
  - **Description**: Adds spectral index data to the SE catalogs.

- **duplicate_ridder.py**
  - **Description**: Removes duplicates from the catalogs before downloading cutouts for the SOM pipeline.

- **fix_headers.py**
  - **Description**: Some files have negative RA in their headers as a result of astrometric correction. This script corrects the headers before generating catalogs.

- **get_urls_from_nrao.py**
  - **Description**: Retrieves image URLs from the NRAO database for catalog generation.

### Shell Scripts

- **pipe1and2.sh**
  - **Description**: Combines the execution of Pipeline 1 and Pipeline 2.

- **set_workdir.sh**
  - **Description**: Sets the working directory for the pipeline operations.

### Configuration Files

- **nsswitch.conf**
  - **Description**: Configuration file to manage service lookups for installing docker image correctly on CANFAR.

### Data and Notebooks

- **Vetting_pipeline1_outputs.ipynb**
  - **Description**: Jupyter notebook for data vetting after Pipeline 1 and 2.

- **saved_counts.zip**
  - **Description**: Standard data summary against which vetting is carried out.

### Miscellaneous

- **cutout_provider_core_old.zip**
  - **Description**: Archived version of the cutout provider script modified for Pipeline 3.
 

## Additional Documentation

https://binysebastian.github.io/Documentation_cirada_pipeline/


## License
This project is licensed under the terms of the MIT license.
