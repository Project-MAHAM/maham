# MAHAM Architecture

```text
MAHAM/
├── src/
│   └── maham/
│       ├── __init__.py
│       ├── _core/
│       │   ├── __init__.py
│       │   ├── metadata.py
│       │   ├── units.py
│       │   └── typing.py
│       ├── physics/
│       │   ├── __init__.py
│       │   ├── constants.py
│       │   ├── particles/
│       │   │   └── __init__.py
│       │   ├── kinematics/
│       │   │   └── __init__.py
│       │   ├── propagation/
│       │   │   └── __init__.py
│       │   ├── spectra/
│       │   │   ├── __init__.py
│       │   │   ├── conversions.py
│       │   │   ├── limits.py
│       │   │   ├── sensitivities.py
│       │   │   └── weighting.py
│       │   └── neutrino/
│       │       ├── __init__.py
│       │       ├── flavor.py
│       │       └── interactions.py
│       ├── statistics/
│       │   ├── __init__.py
│       │   └── poisson.py
│       ├── detector/
│       │   ├── __init__.py
│       │   ├── response.py
│       │   ├── exposure/
│       │   │   └── __init__.py
│       │   ├── rates/
│       │   │   └── __init__.py
│       │   └── sensitivity/
│       │       └── __init__.py
│       ├── astronomy/
│       │   ├── __init__.py
│       │   ├── coordinates/
│       │   │   └── __init__.py
│       │   ├── time/
│       │   │   └── __init__.py
│       │   ├── visibility/
│       │   │   └── __init__.py
│       │   └── skymap/
│       │       └── __init__.py
│       ├── multimessenger/
│       │   ├── __init__.py
│       │   ├── coincidence/
│       │   │   └── __init__.py
│       │   ├── association/
│       │   │   └── __init__.py
│       │   └── transients/
│       │       └── __init__.py
│       ├── radio/
│       │   ├── __init__.py
│       │   ├── antenna/
│       │   │   └── __init__.py
│       │   ├── transmission/
│       │   │   └── __init__.py
│       │   ├── polarization/
│       │   │   └── __init__.py
│       │   └── noise/
│       │       └── __init__.py
│       ├── models/
│       │   ├── __init__.py
│       │   ├── base.py
│       │   ├── registry.py
│       │   ├── flux/
│       │   │   ├── __init__.py
│       │   │   ├── neutrino/
│       │   │   │   ├── __init__.py
│       │   │   │   ├── base.py
│       │   │   │   ├── ensemble.py
│       │   │   │   ├── cosmogenic/
│       │   │   │   │   ├── __init__.py
│       │   │   │   │   └── models.py
│       │   │   │   └── source_environment/
│       │   │   │       ├── __init__.py
│       │   │   │       ├── km3net_blazar_2026.py
│       │   │   │       └── models.py
│       │   │   ├── cosmic_ray/
│       │   │   │   └── __init__.py
│       │   │   └── gamma_ray/
│       │   │       ├── __init__.py
│       │   │       ├── base.py
│       │   │       └── source_environment/
│       │   │           ├── __init__.py
│       │   │           └── models.py
│       │   ├── cross_sections/
│       │   │   ├── __init__.py
│       │   │   └── neutrino/
│       │   │       ├── __init__.py
│       │   │       ├── base.py
│       │   │       └── ctw_2011.py
│       │   ├── sources/
│       │   │   └── __init__.py
│       │   ├── attenuation/
│       │   │   └── __init__.py
│       │   ├── backgrounds/
│       │   │   └── __init__.py
│       │   └── populations/
│       │       └── __init__.py
│       ├── datasets/
│       │   ├── __init__.py
│       │   ├── base.py
│       │   ├── registry.py
│       │   ├── spectra/
│       │   │   ├── __init__.py
│       │   │   ├── base.py
│       │   │   ├── neutrino/
│       │   │   │   ├── __init__.py
│       │   │   │   ├── base.py
│       │   │   │   ├── icecube_glashow_2021.py
│       │   │   │   ├── icecube_combined_2015.py
│       │   │   │   ├── icecube_cascade_2020.py
│       │   │   │   ├── icecube_throughgoing_muon_2022.py
│       │   │   │   ├── icecube_ngc1068_2022.py
│       │   │   │   ├── icecube_txs0506_flare_2018.py
│       │   │   │   └── km3net_230213a_flux_2025.py
│       │   │   ├── cosmic_ray/
│       │   │   │   ├── __init__.py
│       │   │   │   ├── base.py
│       │   │   │   ├── auger_spectrum_2021.py
│       │   │   │   └── telescope_array_combined_2023.py
│       │   │   └── gamma_ray/
│       │   │       ├── __init__.py
│       │   │       ├── base.py
│       │   │       └── fermi_lat_igrb_egb_2015.py
│       │   ├── limits/
│       │   │   ├── __init__.py
│       │   │   ├── cosmic_ray/
│       │   │   │   └── __init__.py
│       │   │   ├── gamma_ray/
│       │   │   │   └── __init__.py
│       │   │   └── neutrino/
│       │   │       ├── __init__.py
│       │   │       ├── anita_2019.py
│       │   │       ├── ara_five_station_2026.py
│       │   │       ├── auger_diffuse_neutrino_2023.py
│       │   │       ├── baikal_gvd_2025.py
│       │   │       └── icecube_ehe_2025.py
│       │   ├── sensitivities/
│       │   │   ├── __init__.py
│       │   │   ├── cosmic_ray/
│       │   │   │   └── __init__.py
│       │   │   ├── gamma_ray/
│       │   │   │   └── __init__.py
│       │   │   └── neutrino/
│       │   │       ├── __init__.py
│       │   │       ├── grand200k_2021.py
│       │   │       ├── icecube_ehe_2025.py
│       │   │       ├── icecube_gen2_radio_2021.py
│       │   │       ├── pueo_2025.py
│       │   │       ├── rno_g_2021.py
│       │   │       └── trinity_2025.py
│       │   ├── effective_area/
│       │   │   ├── __init__.py
│       │   │   ├── base.py
│       │   │   └── neutrino/
│       │   │       ├── __init__.py
│       │   │       ├── anita_2019.py
│       │   │       ├── ara_five_station_2026.py
│       │   │       ├── baikal_gvd_2025.py
│       │   │       ├── icecube_ehe_2025.py
│       │   │       └── km3net_230213a_2025.py
│       │   ├── effective_volume/
│       │   │   ├── __init__.py
│       │   │   ├── base.py
│       │   │   └── neutrino/
│       │   │       ├── __init__.py
│       │   │       └── rno_g_2021.py
│       │   ├── efficiencies/
│       │   │   ├── __init__.py
│       │   │   ├── base.py
│       │   │   └── neutrino/
│       │   │       ├── __init__.py
│       │   │       └── ara_five_station_2026.py
│       │   └── events/
│       │       ├── __init__.py
│       │       └── neutrino/
│       │           ├── __init__.py
│       │           ├── icecube_170922a_2017.py
│       │           └── km3net_230213a_2025.py
│       ├── data/
│       │   ├── __init__.py
│       │   ├── models/
│       │   │   ├── README.md
│       │   │   ├── cross_sections/
│       │   │   │   └── neutrino/
│       │   │   │       └── ctw_2011.json
│       │   │   └── flux/
│       │   │       ├── gamma_ray/
│       │   │       │   └── source_environment/
│       │   │       │       ├── ajello_blazar_population_2015.csv
│       │   │       │       └── km3net_blazar_population_2026_gamma_best_fit.csv
│       │   │       └── neutrino/
│       │   │           ├── cosmogenic/
│       │   │           │   ├── allard_2026_frii_model1.csv
│       │   │           │   ├── allard_2026_frii_model2.csv
│       │   │           │   ├── allard_2026_frii_model3.csv
│       │   │           │   ├── aloisio_2015.json
│       │   │           │   ├── auger_2023.json
│       │   │           │   ├── berat_2024.json
│       │   │           │   ├── boncioli_2019.json
│       │   │           │   ├── condorelli_2023.json
│       │   │           │   ├── ehlert_2024.json
│       │   │           │   ├── heinze_2019.json
│       │   │           │   ├── kuznetsov_petrov_savchenko_2026_best_fit.csv
│       │   │           │   ├── kuznetsov_petrov_savchenko_2026_local_min.csv
│       │   │           │   ├── muzio_farrar_2023.json
│       │   │           │   ├── muzio_unger_wissel_2023.json
│       │   │           │   ├── yoshida_meier_2026_log_normal.csv
│       │   │           │   ├── yoshida_meier_2026_no_evolution.csv
│       │   │           │   └── zhang_murase_2019.json
│       │   │           └── source_environment/
│       │   │               ├── boncioli_llgrb_2019.json
│       │   │               ├── fang_pulsar_2014.json
│       │   │               ├── km3net_blazar_population_2026_best_fit.csv
│       │   │               ├── rodrigues_agn_2021.json
│       │   │               ├── rodrigues_bllac_2024.json
│       │   │               ├── rodrigues_fsrq_2024.json
│       │   │               ├── tamborra_llgrb_2015.json
│       │   │               ├── tamborra_sgrb_2015.json
│       │   │               └── winter_tde_2023.json
│       │   └── datasets/
│       │       ├── README.md
│       │       ├── spectra/
│       │       │   ├── neutrino/
│       │       │   │   ├── icecube_cascade_piecewise_2020.csv
│       │       │   │   ├── icecube_throughgoing_muon_piecewise_2022.csv
│       │       │   │   ├── icecube_ngc1068_flux_2022.csv
│       │       │   │   └── icecube_txs0506_flare_flux_2018.csv
│       │       │   ├── cosmic_ray/
│       │       │   │   └── telescope_array_combined_2023_digitized.csv
│       │       │   └── gamma_ray/
│       │       ├── limits/
│       │       │   └── neutrino/
│       │       │       ├── anita_i_iv_diffuse_neutrino_limit_2019.csv
│       │       │       ├── ara_five_station_diffuse_neutrino_limit_2026.csv
│       │       │       ├── auger_diffuse_neutrino_limit_2023.csv
│       │       │       └── baikal_gvd_diffuse_neutrino_limit_2025.csv
│       │       ├── sensitivities/
│       │       │   └── neutrino/
│       │       │       ├── grand200k_diffuse_neutrino_sensitivity_2021.csv
│       │       │       ├── icecube_gen2_radio_diffuse_neutrino_sensitivity_2021.csv
│       │       │       ├── pueo_diffuse_neutrino_ses_2025.csv
│       │       │       ├── rno_g_diffuse_neutrino_sensitivity_2021.csv
│       │       │       └── trinity_diffuse_neutrino_sensitivity_2025.csv
│       │       ├── effective_area/
│       │       │   └── neutrino/
│       │       │       ├── anita_iv_acceptance_2019.csv
│       │       │       ├── ara_five_station_trigger_acceptance_2026.csv
│       │       │       └── baikal_gvd_effective_area_2025.csv
│       │       ├── effective_volume/
│       │       │   └── neutrino/
│       │       │       └── rno_g_effective_volume_2021.json
│       │       ├── efficiencies/
│       │       │   └── neutrino/
│       │       │       └── ara_five_station_signal_efficiency_2026.csv
│       │       └── events/
│       │           └── neutrino/
│       │               └── icecube_170922a_2017.csv
│       ├── integrations/
│       │   ├── __init__.py
│       │   ├── nuradio/
│       │   │   └── __init__.py
│       │   ├── root/
│       │   │   └── __init__.py
│       │   └── healpy/
│       │       └── __init__.py
│       └── plotting/
│           ├── __init__.py
│           ├── style.py
│           └── limits.py
├── tests/
│   ├── __init__.py
│   ├── core/
│   │   ├── test_metadata.py
│   │   └── test_units.py
│   ├── physics/
│   │   ├── spectra/
│   │   │   ├── test_conversions.py
│   │   │   ├── test_flux_limits.py
│   │   │   ├── test_limits.py
│   │   │   └── test_sensitivities.py
│   │   └── neutrino/
│   │       ├── test_flavor.py
│   │       └── test_interactions.py
│   ├── statistics/
│   │   └── test_poisson.py
│   ├── detector/
│   │   └── test_response.py
│   ├── astronomy/
│   ├── multimessenger/
│   ├── radio/
│   ├── models/
│   │   ├── cross_sections/
│   │   │   └── neutrino/
│   │   │       └── test_ctw_2011.py
│   │   ├── test_registry.py
│   │   ├── test_neutrino_flux.py
│   │   ├── test_neutrino_ensemble.py
│   │   ├── test_neutrino_literature_models.py
│   │   ├── test_neutrino_model_families.py
│   │   └── test_gamma_ray_literature_models.py
│   ├── datasets/
│   │   ├── test_base.py
│   │   ├── test_registry.py
│   │   ├── test_icecube_glashow.py
│   │   ├── test_icecube_ehe_2025.py
│   │   ├── test_icecube_combined_2015.py
│   │   ├── test_icecube_cascade_2020.py
│   │   ├── test_icecube_throughgoing_muon_2022.py
│   │   ├── test_icecube_ngc1068_2022.py
│   │   ├── test_icecube_txs0506_flare_2018.py
│   │   ├── test_icecube_170922a_2017.py
│   │   ├── test_auger_spectrum_2021.py
│   │   ├── test_telescope_array_combined_2023.py
│   │   ├── test_fermi_lat_igrb_egb_2015.py
│   │   ├── test_km3net_230213a_2025.py
│   │   ├── test_km3net_230213a_flux_2025.py
│   │   ├── test_km3net_230213a_effective_area_2025.py
│   │   ├── test_anita_2019.py
│   │   ├── test_ara_five_station_2026.py
│   │   ├── test_auger_diffuse_neutrino_2023.py
│   │   ├── test_baikal_gvd_2025.py
│   │   ├── test_grand200k_2021.py
│   │   ├── test_icecube_gen2_radio_2021.py
│   │   ├── test_pueo_2025.py
│   │   ├── test_rno_g_2021.py
│   │   ├── test_trinity_2025.py
│   │   └── test_upper_limit_normalization_metadata.py
│   ├── integrations/
│   └── plotting/
├── validation/
│   ├── README.md
│   ├── published_results/
│   │   ├── icecube/
│   │   │   ├── README.md
│   │   │   ├── validate.py
│   │   │   └── outputs/
│   │   │       └── .gitignore
│   │   ├── anita/
│   │   │   ├── README.md
│   │   │   ├── validate.py
│   │   │   └── outputs/
│   │   │       └── .gitignore
│   │   ├── ara/
│   │   │   ├── README.md
│   │   │   ├── validate.py
│   │   │   └── outputs/
│   │   │       └── .gitignore
│   │   ├── auger/
│   │   │   ├── README.md
│   │   │   ├── validate.py
│   │   │   └── outputs/
│   │   │       └── .gitignore
│   │   ├── baikal_gvd/
│   │   │   ├── README.md
│   │   │   ├── validate.py
│   │   │   └── outputs/
│   │   │       └── .gitignore
│   │   ├── rno_g/
│   │   │   ├── README.md
│   │   │   ├── validate.py
│   │   │   └── outputs/
│   │   │       └── .gitignore
│   │   ├── pueo/
│   │   │   ├── README.md
│   │   │   ├── validate.py
│   │   │   └── outputs/
│   │   │       └── .gitignore
│   │   ├── icecube_gen2_radio/
│   │   │   ├── README.md
│   │   │   ├── validate.py
│   │   │   └── outputs/
│   │   │       └── .gitignore
│   │   ├── grand200k/
│   │   │   ├── README.md
│   │   │   ├── validate.py
│   │   │   └── outputs/
│   │   │       └── .gitignore
│   │   ├── trinity/
│   │   │   ├── README.md
│   │   │   ├── validate.py
│   │   │   └── outputs/
│   │   │       └── .gitignore
│   │   ├── telescope_array/
│   │   ├── fermi_lat/
│   │   └── km3net/
│   └── comparisons/
│       ├── diffuse_spectra/
│       │   ├── README.md
│       │   ├── compare.py
│       │   └── outputs/
│       │       └── .gitignore
│       ├── model_spectra/
│       │   ├── README.md
│       │   ├── compare.py
│       │   └── outputs/
│       │       └── .gitignore
│       └── point_source_neutrinos/
│           ├── README.md
│           ├── compare.py
│           └── outputs/
│               └── .gitignore
├── examples/
├── benchmarks/
├── docs/
│   ├── architecture.md
│   ├── getting_started/
│   ├── user_guide/
│   ├── models/
│   ├── datasets/
│   ├── validation/
│   └── api/
├── .github/
│   ├── workflows/
│   ├── ISSUE_TEMPLATE/
│   └── PULL_REQUEST_TEMPLATE.md
├── pyproject.toml
├── CITATION.cff
├── CONTRIBUTING.md
├── GOVERNANCE.md
├── CODE_OF_CONDUCT.md
├── CHANGELOG.md
├── README.md
├── LICENSE
└── .gitignore
```

## Architecture principles

MAHAM is organized by scientific concept rather than by experiment.

- Methods define how calculations are performed.
- Models represent named theoretical or phenomenological descriptions.
- Datasets represent published measurements, limits, sensitivities, observations, detector-response products, and other scientific releases.
- Validation reproduces published scientific results using MAHAM's public interfaces.
- Integrations provide adapters to external ecosystems without introducing new physics.
- Runtime package data are stored under `src/maham/data/`.
- Tests verify software behavior; validation verifies scientific reproduction.
- Published detector-response tables belong under `datasets/`; detector calculations belong under `detector/`.
- MAHAM does not define an experiment-specific event format.
- MAHAM does not silently convert neutrino flavor conventions. Physical assumptions required for a conversion must be explicit.
- Generic scientific concepts should not be placed in experiment-specific top-level namespaces.
- `utils` and `helpers` catch-all modules are avoided. Functionality belongs in the scientific concept that owns it.
- Published detector-response products such as effective areas, effective volumes, acceptances, and efficiencies are distinct dataset types and are not silently combined. Derived response quantities must be explicit and documented in metadata.
- Generic operations on published spectral limits and sensitivities belong under `physics/spectra/`; experiment-specific published products remain under their corresponding `datasets/` categories.
- Published differential limits and sensitivities preserve their native normalization and statistical conventions. Common comparison conventions are constructed explicitly from native metadata rather than inferred from plotted-point spacing.
- Limits and sensitivities are distinct scientific products and remain separate dataset categories.
- Pure counting-statistics constructions belong under `statistics/`. Physics-specific use of those statistical results belongs in the scientific module that consumes them.
- Fundamental physical constants belong in `physics/constants.py` and carry explicit units. Material properties and analysis assumptions, such as an ice density, are inputs or metadata rather than fundamental constants.
- Named interaction models, such as CTW neutrino-nucleon cross sections, belong under `models/`; generic transformations using those models, such as an interaction length, belong under `physics/`.
- Reusable detector-response transformations, such as `Veff -> Aeff`, belong under `detector/` and are kept independent of experiment-specific dataset loaders.
- A source's stated confidence level is preserved without inventing an unstated statistical construction. For example, a published 90% CL sensitivity is not labeled Feldman-Cousins unless the source supports that attribution.

## Scientific provenance

Every scientific dataset and model records how its numerical values entered MAHAM.

Supported provenance classes include:

- `OFFICIAL_RELEASE`
- `OFFICIAL_REPOSITORY`
- `HEPDATA`
- `ZENODO`
- `AUTHOR_PROVIDED`
- `CURATED_DATABASE`
- `PUBLISHED_TABLE`
- `DIGITIZED`
- `DERIVED`

`PUBLISHED_TABLE` is used when numerical values are transcribed directly from a published table.

`DIGITIZED` is reserved for values reconstructed from figures or other graphical material. This includes exact extraction of vector-path coordinates from a published figure when no machine-readable numerical release is available; metadata should state whether the extraction was vector-based or raster-based.

`CURATED_DATABASE` is used when MAHAM preserves numerical values from a recognized scientific compilation or curated release while retaining both the original scientific reference and the curated data reference.

`DERIVED` is used when MAHAM computes a scientific product from another source rather than reproducing directly released values.

## Scientific data storage

MAHAM supports three storage modes.

### BUNDLED

Small curated, transcribed, digitized, derived, or otherwise reproducibility-critical data distributed with the package.

Examples:

- IceCube 9.5-year through-going muon piece-wise flux
- Telescope Array combined-spectrum digitization
- KM3NeT-curated cosmogenic and source-environment neutrino model curves
- Reproducibly derived literature-model tables preserved with pinned provenance and checksums
- Figure-extracted literature-model curves preserved with explicit digitization provenance and source-figure checksums
- IceCube six-year cascade differential flux digitized from the published Figure 3
- PUEO, IceCube-Gen2 Radio, GRAND200k, and Trinity figure-extracted projected sensitivity curves
- RNO-G official effective-volume input and the reproducibly derived Figure 24 sensitivity curve
- CTW published parametrization coefficients required for reproducible neutrino-nucleon cross-section calculations

### REMOTE

Authoritative public data downloaded on demand and cached locally. Integrity is checked using pinned checksums where available.

Examples include:

- IceCube releases
- KM3NeT KM3-230213A release
- Fermi-LAT VizieR data
- Auger supplementary data

### EXTERNAL

Data managed outside MAHAM and supplied through a user-provided path.

This mode is appropriate for large files, private data, collaboration data, and other resources that MAHAM should not download or redistribute.

## Data and model design

MAHAM should not become a data warehouse.

The preferred hierarchy for numerical scientific information is:

1. official machine-readable release
2. authoritative repository or archival dataset
3. published numerical table
4. author-provided data
5. curated scientific database
6. careful figure extraction when no numerical release exists

Large scientific products should normally remain remote or external. Small tables necessary for reproducibility may be bundled.

A single scientific publication may produce more than one MAHAM object. For example, an event record, flux inference, effective-area release, effective-volume release, efficiency curve, sensitivity, and theoretical model are distinct scientific objects and should remain separate.

Models and datasets are also kept conceptually distinct. A model represents a named theoretical or phenomenological prediction. A dataset represents an observational, experimental, or released scientific product.

Bundled source tables should preserve the source values and be protected by checksums where appropriate. Standardization required for MAHAM's numerical interfaces, such as energy ordering, duplicate-energy handling, or model-specific support restriction, belongs in the loader rather than in silent modification of the bundled source file. Model-specific standardization must be explicit, scientifically justified, documented in metadata, and covered by tests.

Published detector response should remain as close as possible to its native scientific object. Effective volume, effective area, acceptance, and efficiency are not interchangeable dataset labels. If one is derived from another, the transformation belongs in a reusable calculation layer and the provenance chain must remain visible.

## Physical constants, interaction models, and detector response

Fundamental constants used by MAHAM calculations are centralized in `physics/constants.py`, are unit-bearing, and should be pinned to an explicit reference convention where reproducibility depends on the numerical value.

Material or environmental quantities are not promoted to fundamental constants merely because a calculation uses a conventional value. For example, an ice density used in an interaction-length calculation remains an explicit input or dataset assumption.

Named cross-section parametrizations are models. The CTW 2011 neutrino-nucleon parametrization therefore belongs under `models/cross_sections/neutrino/`, with its published coefficients stored under `data/models/cross_sections/neutrino/`.

Generic physics relations built from a model belong under `physics/`. For example,

```text
cross-section model
        |
        v
interaction_length()
```

is a neutrino-interaction calculation and belongs in `physics/neutrino/interactions.py`.

Generic detector-response transformations belong under `detector/`. The current effective-volume conversion is conceptually:

```text
Veff
  |
  v
Aeff = Veff / Lint
```

The transformation is reusable and does not encode RNO-G-specific assumptions.

## Spectral representation

MAHAM separates the underlying physical differential intensity from its plotted energy weighting.

Supported representations include:

- `phi`
- `Ephi`
- `E2phi`
- `E3phi`
- `J`
- `EJ`
- `E2J`
- `E3J`

Energy weighting is reversible.

Cross-family `J <-> phi` conversion is permitted only when the dataset or model explicitly represents a differential intensity.

Neutrino flavor conventions are handled independently of spectral weighting. Conversions requiring physical assumptions, such as equal flavor composition, must be requested explicitly.

## Differential-limit normalization

MAHAM preserves the native normalization convention of published differential upper limits.

For limits defined using an explicit logarithmic energy width, the native width is recorded with:

- `limit_normalization_convention = "log10_energy_width"`
- `log10_energy_width_decades`

For experiment-specific historical conventions, the native convention and its parameters are recorded explicitly rather than translated into a fictitious energy-bin width.

Conversions to a common comparison convention are performed by reusable functions in `physics/spectra/limits.py`. Converted tables retain metadata describing the native convention, target convention, and applied normalization scale factor.

The spacing of tabulated or plotted energy points is not assumed to define the statistical width of a differential limit.

Generic arithmetic is named for the mathematical operation rather than an experiment. For example, decade-width and bandwidth-factor rescaling are reusable primitives even when the native convention originated with ANITA.

## Projected-sensitivity normalization and statistics

Projected sensitivities preserve their native statistical and spectral conventions just as upper limits do.

Sensitivity-specific transformations belong in `physics/spectra/sensitivities.py`. Pure Poisson confidence constructions belong in `statistics/poisson.py`.

A single-event sensitivity is a native one-expected-event quantity. It must remain identifiable as such in metadata. Converting it to a confidence-level sensitivity is an explicit transformation and records the statistical method, confidence level, assumed observed events, assumed background, and count scale factor.

For zero observed events and zero expected background, MAHAM distinguishes between:

- the conventional one-sided Poisson upper mean, `-ln(1-CL)`;
- the Feldman-Cousins confidence-belt upper endpoint.

These are not interchangeable. At 90% CL they are approximately `2.302585` and `2.435915`, respectively. A publication using a rounded value such as `2.44` retains that published value in its dataset metadata, while the generic statistics implementation may reproduce the unrounded construction independently.

If a source gives a confidence level but does not identify the confidence-interval construction, MAHAM records the confidence level and leaves the statistical method unspecified rather than inferring one.

For sensitivity products normalized over a logarithmic energy width, metadata use:

- `sensitivity_normalization_convention = "log10_energy_width"`
- `log10_energy_width_decades`

For SES products using a historical bandwidth convention, metadata preserve that convention and its factor explicitly. Conversion to a common decade-width comparison is performed only when requested.

The spacing of plotted vertices is never used as a substitute for the statistical energy width. This applies equally to raster digitizations, vector-path extractions, tabulated points, and smooth display curves.

## Response level and analysis efficiency

Projected detector sensitivities should record what level of detector response they represent whenever the source supports that distinction.

Useful metadata include:

- `response_level`
- `analysis_efficiency_included`
- `reconstruction_requirements_included`

Trigger-level sensitivity, detector-response sensitivity, and final post-selection sensitivity are not silently treated as identical scientific objects.

When a paper discusses analysis efficiency separately but does not fold it into the published projection, MAHAM records that distinction rather than upgrading the curve to an analysis-level sensitivity.

## Comparison conventions

A comparison plot may construct a common convention from heterogeneous native products, but the transformation chain must remain explicit and reversible.

The current diffuse-neutrino comparison uses:

- all-flavor neutrino flux;
- one-decade differential normalization where a conversion is required;
- current 90% CL upper limits as solid curves;
- projected 90% CL sensitivities as dashed curves;
- native confidence-level products directly when they already match the comparison convention;
- explicit SES-to-confidence-level conversion only when the native source is actually an SES.

Experiment-specific historical conventions remain in the native dataset metadata even after a converted comparison table is constructed.

Derived comparison objects are not replacements for the native scientific datasets.
