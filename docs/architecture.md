# MAHAM Architecture

MAHAM is organized around scientific concepts rather than experiments or
individual messengers.

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

Methods should not depend on a particular experiment or published physical
model.

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

Each model should preserve its scientific provenance, including its reference,
parameters, assumptions, units, conventions, and validity range.

## Datasets

Datasets are published experimental or observational results.

Examples include:

- measured spectra
- flux measurements
- upper limits
- experimental sensitivities
- selected event measurements

Each dataset should preserve its source, reference, units, conventions,
confidence level where applicable, and provenance.

Official machine-readable data should be preferred over digitized data whenever
available.

## Scientific data files

Small redistributable numerical tables required by MAHAM are stored under

`src/maham/data/`

and distributed with the package.

The Python interfaces to those files remain under `models/` or `datasets/`.

Large datasets or data that should remain at their authoritative source may be
retrieved externally and cached rather than stored in the MAHAM repository.

## Validation

Software testing and scientific validation have different purposes.

`tests/` asks:

> Does the software behave as implemented?

`validation/` asks:

> Does the implementation reproduce the expected physics or published result?

Scientific validation may reproduce analytical results, tables, benchmark
calculations, or published figures.

## Integrations

Integrations are adapters to external software and data formats.

They should contain no new scientific physics.

Examples may include interfaces to NuRadioMC/NuRadioReco, ROOT, and HEALPix
software.

## Core architectural rules

1. Organize scientific functionality by concept, not by experiment.
2. General calculations belong in scientific method modules.
3. Specific theoretical or phenomenological prescriptions belong in `models/`.
4. Published measurements, limits, and sensitivities belong in `datasets/`.
5. Experiment-specific adapters belong in `integrations/`, not in the scientific core.
6. Do not duplicate functionality already provided well by established scientific packages without a clear scientific reason.
7. Avoid generic dumping-ground modules such as `utils.py`, `helpers.py`, and `misc.py`.
8. Tests verify software behavior; validation verifies scientific correctness.
9. Data provenance, units, conventions, and citations are part of the scientific result and must not be hidden in plotting or analysis code.
10. New top-level modules should be introduced only when the functionality cannot naturally belong to an existing scientific concept.

## Planned package structure

The following structure describes the intended organization of MAHAM. Not every
module is expected to contain implemented functionality during the early stages
of development.

maham/
│
├── src/
│   └── maham/
│       │
│       ├── __init__.py
│       ├── citations.py
│       │
│       ├── _core/
│       │   ├── __init__.py
│       │   ├── metadata.py
│       │   ├── units.py
│       │   └── typing.py
│       │
│       ├── physics/
│       │   ├── __init__.py
│       │   ├── particles.py
│       │   ├── kinematics.py
│       │   ├── interactions.py
│       │   └── propagation.py
│       │
│       ├── spectra/
│       │   ├── __init__.py
│       │   ├── conversions.py
│       │   ├── integration.py
│       │   └── weighting.py
│       │
│       ├── statistics/
│       │   ├── __init__.py
│       │   ├── counting.py
│       │   ├── intervals.py
│       │   ├── likelihood.py
│       │   └── hypothesis.py
│       │
│       ├── detector/
│       │   ├── __init__.py
│       │   ├── response.py
│       │   ├── exposure.py
│       │   ├── rates.py
│       │   └── sensitivity.py
│       │
│       ├── astronomy/
│       │   ├── __init__.py
│       │   ├── coordinates.py
│       │   ├── time.py
│       │   ├── visibility.py
│       │   └── skymap.py
│       │
│       ├── multimessenger/
│       │   ├── __init__.py
│       │   ├── coincidence.py
│       │   ├── association.py
│       │   └── transients.py
│       │
│       ├── radio/
│       │   ├── __init__.py
│       │   ├── antenna.py
│       │   ├── transmission.py
│       │   ├── polarization.py
│       │   └── noise.py
│       │
│       ├── models/
│       │   ├── __init__.py
│       │   ├── base.py
│       │   ├── registry.py
│       │   │
│       │   ├── flux/
│       │   │   ├── __init__.py
│       │   │   ├── neutrino/
│       │   │   │   └── __init__.py
│       │   │   ├── cosmic_ray/
│       │   │   │   └── __init__.py
│       │   │   └── gamma_ray/
│       │   │       └── __init__.py
│       │   │
│       │   ├── cross_sections/
│       │   │   └── __init__.py
│       │   │
│       │   ├── sources/
│       │   │   └── __init__.py
│       │   │
│       │   ├── attenuation/
│       │   │   └── __init__.py
│       │   │
│       │   ├── backgrounds/
│       │   │   └── __init__.py
│       │   │
│       │   └── populations/
│       │       └── __init__.py
│       │
│       ├── datasets/
│       │   ├── __init__.py
│       │   ├── base.py
│       │   ├── registry.py
│       │   │
│       │   ├── spectra/
│       │   │   ├── __init__.py
│       │   │   ├── neutrino/
│       │   │   │   └── __init__.py
│       │   │   ├── cosmic_ray/
│       │   │   │   └── __init__.py
│       │   │   └── gamma_ray/
│       │   │       └── __init__.py
│       │   │
│       │   ├── limits/
│       │   │   ├── __init__.py
│       │   │   ├── neutrino/
│       │   │   │   └── __init__.py
│       │   │   ├── cosmic_ray/
│       │   │   │   └── __init__.py
│       │   │   └── gamma_ray/
│       │   │       └── __init__.py
│       │   │
│       │   ├── sensitivities/
│       │   │   ├── __init__.py
│       │   │   ├── neutrino/
│       │   │   │   └── __init__.py
│       │   │   ├── cosmic_ray/
│       │   │   │   └── __init__.py
│       │   │   └── gamma_ray/
│       │   │       └── __init__.py
│       │   │
│       │   └── events/
│       │       └── __init__.py
│       │
│       ├── data/
│       │   ├── __init__.py
│       │   │
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
│       │   │
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
│       │       └── events/
│       │
│       ├── integrations/
│       │   ├── __init__.py
│       │   ├── nuradio.py
│       │   ├── root.py
│       │   └── healpy.py
│       │
│       └── plotting/
│           ├── __init__.py
│           ├── spectra.py
│           ├── limits.py
│           ├── detector.py
│           └── sky.py
│
├── tests/
│   ├── physics/
│   ├── spectra/
│   ├── statistics/
│   ├── detector/
│   ├── astronomy/
│   ├── multimessenger/
│   ├── radio/
│   ├── models/
│   ├── datasets/
│   ├── integrations/
│   └── plotting/
│
├── validation/
│   ├── README.md
│   └── published_results/
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

The tree above describes the intended organization of MAHAM. It defines where
future functionality belongs but does not imply that every planned module is
already implemented.

Python modules contain scientific interfaces, calculations, and metadata logic.
Numerical tables distributed with MAHAM are stored separately under
`src/maham/data/`.

The same conceptual hierarchy is used for code and data where practical so that
the relationship between an implementation and its associated numerical data
remains clear.
