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
│       │   ├── particles/
│       │   │   └── __init__.py
│       │   ├── kinematics/
│       │   │   └── __init__.py
│       │   ├── interactions/
│       │   │   └── __init__.py
│       │   ├── propagation/
│       │   │   └── __init__.py
│       │   ├── spectra/
│       │   │   ├── __init__.py
│       │   │   ├── conversions.py
│       │   │   └── weighting.py
│       │   └── neutrino/
│       │       ├── __init__.py
│       │       └── flavor.py
│       ├── statistics/
│       │   ├── __init__.py
│       │   ├── counting/
│       │   │   └── __init__.py
│       │   ├── intervals/
│       │   │   └── __init__.py
│       │   ├── likelihood/
│       │   │   └── __init__.py
│       │   └── hypothesis/
│       │       └── __init__.py
│       ├── detector/
│       │   ├── __init__.py
│       │   ├── response/
│       │   │   └── __init__.py
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
│       │   │   └── __init__.py
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
│       │   │   │   ├── auger_combined_2021.py
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
│       │   │       └── icecube_ehe_2025.py
│       │   ├── sensitivities/
│       │   │   ├── __init__.py
│       │   │   ├── cosmic_ray/
│       │   │   │   └── __init__.py
│       │   │   ├── gamma_ray/
│       │   │   │   └── __init__.py
│       │   │   └── neutrino/
│       │   │       ├── __init__.py
│       │   │       └── icecube_ehe_2025.py
│       │   ├── effective_area/
│       │   │   ├── __init__.py
│       │   │   ├── base.py
│       │   │   └── neutrino/
│       │   │       ├── __init__.py
│       │   │       ├── icecube_ehe_2025.py
│       │   │       └── km3net_230213a_2025.py
│       │   └── events/
│       │       ├── __init__.py
│       │       └── neutrino/
│       │           ├── __init__.py
│       │           ├── icecube_170922a_2017.py
│       │           └── km3net_230213a_2025.py
│       ├── data/
│       │   ├── models/
│       │   │   ├── README.md
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
│       │       ├── sensitivities/
│       │       ├── effective_area/
│       │       │   └── neutrino/
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
│   │   │   └── test_conversions.py
│   │   └── neutrino/
│   │       └── test_flavor.py
│   ├── statistics/
│   ├── detector/
│   ├── astronomy/
│   ├── multimessenger/
│   ├── radio/
│   ├── models/
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
│   │   ├── test_auger_combined_2021.py
│   │   ├── test_telescope_array_combined_2023.py
│   │   ├── test_fermi_lat_igrb_egb_2015.py
│   │   ├── test_km3net_230213a_2025.py
│   │   ├── test_km3net_230213a_flux_2025.py
│   │   └── test_km3net_230213a_effective_area_2025.py
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
│   │   ├── auger/
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

`DIGITIZED` is reserved for values reconstructed from figures or other graphical material.

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
6. careful figure digitization when no numerical release exists

Large scientific products should normally remain remote or external. Small tables necessary for reproducibility may be bundled.

A single scientific publication may produce more than one MAHAM object. For example, an event record, flux inference, effective-area release, and theoretical model are distinct scientific objects and should remain separate.

Models and datasets are also kept conceptually distinct. A model represents a named theoretical or phenomenological prediction. A dataset represents an observational, experimental, or released scientific product.

Bundled source tables should preserve the source values and be protected by checksums where appropriate. Standardization required for MAHAM's numerical interfaces, such as energy ordering, duplicate-energy handling, or model-specific support restriction, belongs in the loader rather than in silent modification of the bundled source file. Model-specific standardization must be explicit, scientifically justified, documented in metadata, and covered by tests.

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

