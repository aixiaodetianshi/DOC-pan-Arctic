# DOC-pan-Arctic
Code for dissolved organic carbon in pan-Arctic rivers during 1984-2018

# Arctic River Dissolved Organic Carbon Flux (1984–2018)

This repository contains the scripts, models, and documentation used in the study **"Spatiotemporal Trends and Drivers of Dissolved Organic Carbon Flux from Pan-Arctic Rivers (1984–2018)"**, which is currently under review at *Nature [Journal Name]*.

## Overview

This research investigates the changes in dissolved organic carbon (DOC) fluxes across 10,566 rivers and 38,420 watersheds in the Pan-Arctic region over a 35-year period. The study combines multi-source satellite data, in-situ observations, and hydrological modeling to produce the first consistent DOC flux dataset for the Arctic rivers.

## Contents

- `src/` — Python scripts for:
  - CDOM retrieval from multi-source satellite imagery
  - CDOM → DOC model construction and application
  - DOC flux calculation using river discharge
  - Temporal and spatial statistical analysis

- `data/` — Sample or placeholder datasets (only metadata here; raw data available upon request or from data repository)

- `model/` — Trained model files for DOC prediction (e.g., regression or ML models)

- `figures/` — Visualization scripts and example output figures

- `notebooks/` — Jupyter notebooks for exploratory data analysis and validation

## Dataset Availability

The full dataset has been published at the [National Tibetan Plateau Data Center (TPDC)](https://data.tpdc.ac.cn/) under the title:  
**Pan-Arctic River DOC Flux Dataset (1984–2018)**  
DOI and access link will be added once officially released.

## How to Use

Citation
If you use this code or dataset in your work, please cite:

Han, W. et al. (2025). Spatiotemporal Trends and Drivers of Dissolved Organic Carbon Flux from Pan-Arctic Rivers (1984–2018). Nature geoscience, under review.

Contact
For questions or collaborations, please contact:
Weixiao Han
Postdoctoral Researcher, University of Zurich
weixiao.han@uzh.ch

1. Clone this repository:
   ```bash
   git clone https://github.com/aixiaodetianshi/DOC-pan-Arctic.git
