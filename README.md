# DOC-pan-Arctic
Code for dissolved organic carbon in pan-Arctic rivers during 1984-2018

# Arctic River Dissolved Organic Carbon Flux (1984–2018)

This repository contains the scripts, models, and documentation used in the study **"Dissolved organic carbon decline across the pan-Arctic in ice-free season (1984-2018)"**, which is currently under review at *Nature Geoscience*.

## Overview

Arctic warming is reshaping carbon fluxes, with implications for climate feedbacks and global biogeochemical cycles. However, the magnitude and trend of dissolved organic carbon (DOC) export from pan-Arctic rivers remain uncertain, especially for small rivers. Here, we use multiband statistical models to quantify DOC fluxes from 10,566 rivers and 38,420 catchments to the Arctic Ocean during the ice-free season (1984–2018), finding a mean annual export of 65.91 ± 12.28 Tg C, and a declining trend of -0.44 Tg C yr⁻¹ (p < 0.001).

DOC export exhibits strong interannual and seasonal variability, peaking in June, and marked spatial heterogeneity:

Large catchments contribute higher total fluxes.

Small catchments export more DOC per unit area.

Trends diverge across basins: Lena shows an increasing trend, while Ob, Yenisey, Kolyma, Yukon, and Mackenzie show declines. Across the pan-Arctic, DOC export is primarily governed by:

Soil carbon availability,

Permafrost-driven freeze–thaw hydrological perturbations,

Ecological disturbances.

Scaling from micro to meso catchments reveals a shift from source-dominated control → hydrological transport capacity → transport-mediated loss and disturbance attenuation.

## Repository Structure
```bash
DOC-pan-Arctic/
│── Analyze_environmental_factors/    # Scripts for environmental driver analysis (climate, soil, permafrost, vegetation, etc.)
│── CDOM_Absorbance_rivers/           # CDOM absorbance processing from in-situ and satellite data
│── Calculate_total_river_DOC/        # DOC flux calculation: discharge × DOC concentration
│── Cross_validate/                   # Cross-validation of models (satellite vs in-situ)
│── Figures/                          # Scripts to generate figures and visualizations for publication
│── River_catchment_matchup/          # River network & catchment delineation, river–catchment matching
│── River_discharge/                  # River discharge datasets and preprocessing
│── calculate_environmental_factors/  # Statistical analysis of environmental variables
│── catboost_info/                    # CatBoost ML model training info and parameters
│── matchup_insitu_remotesensing/     # Matchup dataset between in-situ measurements and remote sensing
│── README.md                         # Project documentation (this file)
│── token.pickle                      # Authentication token for Google APIs (if used for Drive/Sheets)
```

## Key Features
```bash
Satellite data integration: CDOM retrieval from Landsat 5/7/8/9 and Sentinel-2.
DOC estimation: CDOM → DOC conversion using multiband statistical models.
Flux calculation: DOC concentration × river discharge × daily time steps.
Spatiotemporal analysis: Trends across 10,566 rivers and 38,420 catchments from 1984–2018.
Uncertainty quantification: Cross-validation with in-situ observations.
Environmental factor analysis: XGBoost models and SHAP methods.
```
## Dataset Availability

The full dataset has been published at the [National Tibetan Plateau Data Center (TPDC)](https://data.tpdc.ac.cn/) under the title:  
**Pan-Arctic River DOC Flux Dataset (1984–2018)**  
DOI and access link will be added once officially released.

## How to Use
1. Clone this repository:
```bash
   git clone https://github.com/aixiaodetianshi/DOC-pan-Arctic.git
   cd DOC-pan-Arctic
```
2. Run scripts by module. For example, to calculate DOC flux:
```bash
   python Calculate_total_river_DOC/calc_flux.py
```

Citation
If you use this code or dataset in your work, please cite:

Han, W. et al. (2025). Dissolved organic carbon decline across the pan-Arctic in ice-free season (1984-2018). Nature geoscience, under review.

##  Contact

Weixiao Han
Postdoctoral Researcher
University of Zurich
📧 weixiao.han@uzh.ch
