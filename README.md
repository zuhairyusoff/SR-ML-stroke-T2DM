# Machine learning versus regression for predicting stroke in type 2 diabetes

[![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.23233257.svg)](https://doi.org/10.5281/zenodo.23233257)

Analysis code and data for the systematic review and meta-analysis
"Machine Learning versus Conventional Regression Models for Predicting Incident Stroke in Adults with Type 2 Diabetes: A Systematic Review and Meta-analysis".

PROSPERO registration: CRD420261530818

## Contents

| Folder | What it holds |
| --- | --- |
| `search/` | Full PubMed search strategy (final search 8 October 2026) |
| `data/ma_data.csv` | C-statistics extracted from the included studies (one row per estimate), with N, events, flag for approximated events and overall risk of bias |
| `data/ma_data_with_se.csv` | Same data with logit C-statistic and standard error |
| `data/ma_results.csv` | Pooled results for each model group and the main sensitivity analyses |
| `data/ma_sensitivity_extra.csv` | Stroke only and unspecified diabetes type sensitivity analyses |
| `data/probast_ratings.csv` | PROBAST+AI domain ratings for the 22 included studies |
| `analysis/` | Python meta-analysis, extra sensitivity analyses, and an R `metafor` script to verify the pooled estimates |
| `figures/` | Scripts that draw Figures 1 to 4 and the forest plots, plus the rendered figures |

## Methods in brief

C-statistics were pooled on the logit scale with random effects (REML), Hartung, Knapp, Sidik and Jonkman confidence intervals, and 95% prediction intervals using a t distribution with k minus 2 degrees of freedom (Debray et al., BMJ 2017). Where a confidence interval was not reported, the standard error was approximated with the Hanley and McNeil method.

## How to reproduce

```
pip install -r requirements.txt
python analysis/meta_analysis.py        # pooled estimates, forest plots
python analysis/sensitivity_extra.py    # extra sensitivity analyses
python figures/figure1_prisma.py
python figures/figure2_pooled_summary.py
python figures/figure3_4_probast.py
```

To verify in R (from the `analysis/` folder): `Rscript verify_in_R_metafor.R` (requires the `metafor` package).

## Licence

The code in this repository is released under the MIT License (see `LICENSE`). The data files contain summary results extracted from published studies and are shared to allow the analyses to be reproduced. When using these data, please cite the original studies listed in the manuscript.

## Citation

The manuscript is currently in preparation. Until it is published, please cite this repository as:

Mohamed Yusoff MZ, Isa MR, Razak TR, et al. Machine learning versus conventional regression models for predicting incident stroke in adults with type 2 diabetes: analysis code and data. Version 1.0. Zenodo; 2026. doi:10.5281/zenodo.23233257

## Contact

Dr Mohamad Zuhair Mohamed Yusoff, Department of Public Health Medicine, Faculty of Medicine, Universiti Teknologi MARA, Malaysia.
