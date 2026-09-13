# MAHAM Architecture

MAHAM is organized around scientific concepts rather than experiments or individual messengers.

The project separates scientific content into three principal categories:

## Methods

Methods are general equations, algorithms, and scientific operations.

Examples include:

- kinematic calculations
- spectral transformations
- statistical intervals and hypothesis tests
- exposure and event-rate calculations
- astronomical coordinate calculations
- coincidence and association methods
- detector-response calculations

Methods should not depend on a particular experiment or published physical model.

## Models

Models are specific theoretical or phenomenological prescriptions.

Examples include:

- neutrino, cosmic-ray, and gamma-ray flux models
- interaction cross-section models
- source spectra
- attenuation models
- background models
- source-population models

Models may be analytical, numerical, or tabulated.

Each model should preserve its scientific provenance, including its reference, parameters, assumptions, units, conventions, and validity range.

## Datasets

Datasets are published experimental or observational results.

Examples include:

- measured spectra
- flux measurements
- upper limits
- experimental sensitivities
- published effective areas and other detector-response products
- selected event measurements

Each dataset should preserve its source, reference, units, conventions, confidence level where applicable, and provenance.

Official machine-readable data should be preferred over digitized data whenever available.

Published detector-response products such as effective areas belong under `datasets/` because they are experiment-specific published results. General calculations involving detector response belong under `detector/`.

A single official release may contain several scientifically distinct products. These should be exposed as separate MAHAM datasets when their scientific meanings differ. For example, an observed upper limit, expected sensitivity, and effective area may come from the same release while remaining separate MAHAM dataset objects.

## Dataset interface conventions

Dataset interfaces separate the source representation from the standardized MAHAM representation.

`load_raw()` returns the published source data as close as practical to the authoritative representation.

`load()` returns a standardized MAHAM representation with explicit units, metadata, conventions, and scientifically meaningful column names.

Spectrum datasets may additionally provide standardized representations such as:

- `load_phi()`
- `load_ephi()`
- `load_e2phi()`

or equivalently:

- `load(quantity="phi")`
- `load(quantity="Ephi")`
- `load(quantity="E2phi")`

These representations are derived on demand rather than stored as duplicate copies of the same scientific result.

Upper-limit datasets should explicitly identify upper-limit values, for example through an `is_upper_limit` column when appropriate.

## Scientific data files

Small redistributable numerical tables required by MAHAM are stored under `src/maham/data/` and distributed with the package.

The Python interfaces to those files remain under `models/` or `datasets/`.

Large datasets or data that should remain at their authoritative source may be retrieved externally and cached rather than stored in the MAHAM repository.

MAHAM should not become a general-purpose scientific data warehouse. Remote authoritative releases should remain at their official source whenever practical.

## Remote data integrity

Remote scientific data should be verified whenever a stable integrity reference is available.

For ordinary static files, MAHAM may verify the checksum of the downloaded file.

For dynamically generated archives, such as archives assembled by external data repositories at request time, the archive checksum itself may not be stable. In those cases MAHAM should verify the checksum and, where useful, the byte size of the specific scientific file contained inside the archive.

Integrity verification should protect the scientific source content without assuming that transport containers or archive metadata remain byte-for-byte identical indefinitely.

## Validation

Software testing and scientific validation have different purposes.

`tests/` asks:

> Does the software behave as implemented?

`validation/` asks:

> Does the implementation reproduce the expected physics or published result?

Scientific validation may reproduce analytical results, tables, benchmark calculations, or published figures.

## Integrations

Integrations are adapters to external software and data formats.

They should contain no new scientific physics.

Examples may include interfaces to NuRadioMC/NuRadioReco, ROOT, and HEALPix software.

## Core architectural rules

1. Organize scientific functionality by concept, not by experiment.
2. General calculations belong in scientific method modules.
3. Specific theoretical or phenomenological prescriptions belong in `models/`.
4. Published measurements, limits, sensitivities, effective areas, and other published detector-response products belong in `datasets/`.
5. Experiment-specific adapters belong in `integrations/`, not in the scientific core.
6. General detector-response calculations belong in `detector/`; published detector-response tables belong in `datasets/`.
7. Do not duplicate functionality already provided well by established scientific packages without a clear scientific reason.
8. Avoid generic dumping-ground modules such as `utils.py`, `helpers.py`, and `misc.py`.
9. Tests verify software behavior; validation verifies scientific correctness.
10. Data provenance, units, conventions, assumptions, and citations are part of the scientific result and must not be hidden in plotting or analysis code.
11. Distinct scientific products from the same published release should remain distinct dataset interfaces even when they share one source file or archive.
12. New top-level modules should be introduced only when the functionality cannot naturally belong to an existing scientific concept.

## Planned package structure

The following structure describes the intended organization of MAHAM. Not every module is expected to contain implemented functionality during the early stages of development.

```text
maham/
│
├── src/
│   └── maham/
│       ├── __init__.py
│       ├── citations.py
│       ├── _core/
│       │   ├── __init__.py
│       │   ├── metadata.py
│       │   ├── units.py
│       │   └── typing.py
│       ├── physics/
│       │   ├── __init__.py
│       │   ├── particles.py
│       │   ├── kinematics.py
│       │   ├── interactions.py
│       │   └── propagation.py
│       ├── spectra/
│       │   ├── __init__.py
│       │   ├── conversions.py
│       │   ├── flavor.py
│       │   ├── integration.py
│       │   └── weighting.py
│       ├── statistics/
│       │   ├── __init__.py
│       │   ├── counting.py
│       │   ├── intervals.py
│       │   ├── likelihood.py
│       │   └── hypothesis.py
│       ├── detector/
│       │   ├── __init__.py
│       │   ├── response.py
│       │   ├── exposure.py
│       │   ├── rates.py
│       │   └── sensitivity.py
│       ├── astronomy/
│       │   ├── __init__.py
│       │   ├── coordinates.py
│       │   ├── time.py
│       │   ├── visibility.py
│       │   └── skymap.py
│       ├── multimessenger/
│       │   ├── __init__.py
│       │   ├── coincidence.py
│       │   ├── association.py
│       │   └── transients.py
│       ├── radio/
│       │   ├── __init__.py
│       │   ├── antenna.py
│       │   ├── transmission.py
│       │   ├── polarization.py
│       │   └── noise.py
│       ├── models/
│       │   ├── __init__.py
│       │   ├── base.py
│       │   ├── registry.py
│       │   ├── flux/
│       │   │   ├── __init__.py
│       │   │   ├── neutrino/
│       │   │   │   └── __init__.py
│       │   │   ├── cosmic_ray/
│       │   │   │   └── __init__.py
│       │   │   └── gamma_ray/
│       │   │       └── __init__.py
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
│       │   │   │   └── icecube_glashow_2021.py
│       │   │   ├── cosmic_ray/
│       │   │   │   └── __init__.py
│       │   │   └── gamma_ray/
│       │   │       └── __init__.py
│       │   ├── limits/
│       │   │   ├── __init__.py
│       │   │   ├── neutrino/
│       │   │   │   ├── __init__.py
│       │   │   │   └── icecube_ehe_2025.py
│       │   │   ├── cosmic_ray/
│       │   │   │   └── __init__.py
│       │   │   └── gamma_ray/
│       │   │       └── __init__.py
│       │   ├── sensitivities/
│       │   │   ├── __init__.py
│       │   │   ├── neutrino/
│       │   │   │   ├── __init__.py
│       │   │   │   └── icecube_ehe_2025.py
│       │   │   ├── cosmic_ray/
│       │   │   │   └── __init__.py
│       │   │   └── gamma_ray/
│       │   │       └── __init__.py
│       │   ├── effective_area/
│       │   │   ├── __init__.py
│       │   │   ├── base.py
│       │   │   ├── neutrino/
│       │   │   │   ├── __init__.py
│       │   │   │   └── icecube_ehe_2025.py
│       │   │   ├── cosmic_ray/
│       │   │   │   └── __init__.py
│       │   │   └── gamma_ray/
│       │   │       └── __init__.py
│       │   └── events/
│       │       └── __init__.py
│       ├── data/
│       │   ├── __init__.py
│       │   ├── models/
│       │   │   ├── README.md
│       │   │   ├── flux/
│       │   │   │   ├── neutrino/
│       │   │   │   ├── cosmic_ray/
│       │   │   │   └── gamma_ray/
│       │   │   ├── cross_sections/
│       │   │   ├── sources/
│       │   │   ├── attenuation/
│       │   │   ├── backgrounds/
│       │   │   └── populations/
│       │   └── datasets/
│       │       ├── README.md
│       │       ├── spectra/
│       │       │   ├── neutrino/
│       │       │   ├── cosmic_ray/
│       │       │   └── gamma_ray/
│       │       ├── limits/
│       │       │   ├── neutrino/
│       │       │   ├── cosmic_ray/
│       │       │   └── gamma_ray/
│       │       ├── sensitivities/
│       │       │   ├── neutrino/
│       │       │   ├── cosmic_ray/
│       │       │   └── gamma_ray/
│       │       ├── effective_area/
│       │       │   ├── neutrino/
│       │       │   ├── cosmic_ray/
│       │       │   └── gamma_ray/
│       │       └── events/
│       ├── integrations/
│       │   ├── __init__.py
│       │   ├── nuradio.py
│       │   ├── root.py
│       │   └── healpy.py
│       └── plotting/
│           ├── __init__.py
│           ├── style.py
│           ├── spectra.py
│           ├── limits.py
│           ├── detector.py
│           └── sky.py
│
├── tests/
│   ├── physics/
│   ├── spectra/
│   │   ├── test_conversions.py
│   │   └── test_flavor.py
│   ├── statistics/
│   ├── detector/
│   ├── astronomy/
│   ├── multimessenger/
│   ├── radio/
│   ├── models/
│   ├── datasets/
│   │   ├── test_icecube_glashow.py
│   │   └── test_icecube_ehe_2025.py
│   ├── integrations/
│   └── plotting/
│
├── validation/
│   ├── README.md
│   └── published_results/
│       └── icecube/
│           ├── README.md
│           ├── validate.py
│           └── outputs/
│               └── .gitignore
│
├── examples/
│   ├── physics/
│   ├── spectra/
│   ├── statistics/
│   ├── detector/
│   ├── astronomy/
│   ├── multimessenger/
│   ├── radio/
│   ├── models/
│   └── datasets/
│
├── benchmarks/
│   └── README.md
│
├── docs/
│   ├── architecture.md
│   ├── getting_started/
│   ├── user_guide/
│   ├── models/
│   ├── datasets/
│   ├── validation/
│   └── api/
│
├── .github/
│   ├── workflows/
│   ├── ISSUE_TEMPLATE/
│   └── PULL_REQUEST_TEMPLATE.md
│
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

The tree above describes the intended organization of MAHAM. It defines where future functionality belongs but does not imply that every planned module is already implemented.

Python modules contain scientific interfaces, calculations, and metadata logic.

Numerical tables distributed with MAHAM are stored separately under `src/maham/data/`.

The same conceptual hierarchy is used for code and data where practical so that the relationship between an implementation and its associated numerical data remains clear.

## Scientific naming conventions

MAHAM uses plain ASCII notation for scientific quantity names in code, documentation, metadata, and text labels where practical.

Examples include:

- `E2phi` for energy-squared weighted flux
- `Ephi` for energy-weighted flux
- `phi` for differential flux
- `nu` for neutrino
- `nubar` for antineutrino
- `nue` for electron neutrino
- `numu` for muon neutrino
- `nutau` for tau neutrino

Unicode mathematical symbols are not required to identify scientific quantities in the MAHAM API.

## Neutrino flavor conventions

MAHAM does not silently convert between per-flavor and all-flavor neutrino quantities.

A conversion between `per_flavor` and `all_flavor` requires an explicit physical assumption. The currently supported assumption is `equal`, corresponding to equal fluxes in the three neutrino flavors at Earth.

For example:

`per_flavor -> all_flavor` uses a factor of 3 only when `flavor_assumption="equal"` is explicitly requested.

The original flavor convention of every published dataset is retained in its metadata.

Flavor sums and particle/antiparticle conventions in detector-response datasets must also be explicit. For example, an effective area that is summed across `nue`, `numu`, and `nutau`, or averaged between `nu` and `nubar`, should record those conventions in metadata rather than relying on column names alone.
