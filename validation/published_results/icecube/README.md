# IceCube Validation

This validation checks MAHAM implementations of currently supported published IceCube datasets.

## Included results

### IceCube Glashow 2021

MAHAM dataset:

`icecube.glashow.flux.2021`

The native published result is a per-flavor piecewise astrophysical neutrino flux with three energy bins.

The validation checks the native published representation and also constructs an explicit `1:1:1` all-flavor view for comparison with all-flavor EHE results.

### IceCube Combined Astrophysical Spectrum 2015

MAHAM dataset:

`icecube.combined_astrophysical_flux.2015`

The official IceCube release provides a nine-bin all-flavor `E2phi` astrophysical neutrino spectrum spanning `1e4` to `1e7 GeV`.

MAHAM derives the 68% and 90% confidence intervals directly from the released profile-likelihood scans rather than using the approximate covariance-matrix errors. Bins 6, 8, and 9 have zero best-fit normalization and are represented as upper limits.

### IceCube Six-Year Cascade Differential Flux 2020

MAHAM dataset:

`icecube.cascade_piecewise_flux.2020`

The native result is the per-flavor differential astrophysical neutrino flux shown by the black crosses in Figure 3 of the 2020 six-year cascade analysis. MAHAM digitizes the vector content of the published figure and preserves the displayed one-third-decade energy bins.

The dataset contains 13 usable displayed bins: seven nonzero best-fit measurements and six upper limits. The paper states that the 1-sigma uncertainties and data limits correspond to 68% CL simultaneous coverage. The published sensitive energy range is `1.6e4` to `2.6e6 GeV`; Figure 3 also shows differential bins outside that range, which MAHAM retains.

The native quantity is per-flavor `E2phi` for `nu+nubar`. MAHAM provides an explicit equal-flavor conversion to all-flavor for multimessenger comparisons.

### IceCube 9.5-Year Through-Going Muon Flux 2022

MAHAM dataset:

`icecube.throughgoing_muon_piecewise_flux.2022`

The native result is a `nu_mu + nubar_mu` piece-wise astrophysical flux. Each segment has fixed spectral index `gamma=2.0`.

Pieces 2-4 have 68.27% profile-likelihood intervals. Pieces 1 and 5 are 90% CL upper limits. MAHAM preserves these mixed confidence levels per row and provides an explicit equal-flavor conversion for comparisons requiring an all-flavor view.

### IceCube NGC 1068 Point-Source Flux 2022

MAHAM dataset:

`icecube.ngc1068_flux.2022`

The dataset represents the published best-fit `nu_mu + nubar_mu` point-source flux from NGC 1068 as an unbroken power law.

The best-fit normalization is defined at `1 TeV` with spectral index `gamma=3.2`. The MAHAM representation spans the published characteristic energy range from `1.5` to `15 TeV`.

The validation checks the published normalization, spectral index, characteristic energy range, signal-event count, global significance, and reconstruction of the best-fit `E2phi` curve.

Because this is a point-source flux, the spectral quantity does not contain a `sr^-1` factor.

### IceCube TXS 0506+056 2014-2015 Flare

MAHAM dataset:

`icecube.txs0506_flare_flux.2018`

The dataset represents the average best-fit `nu_mu + nubar_mu` source flux during the published 158-day neutrino flare from TXS 0506+056.

The best-fit normalization is defined at `100 TeV` with spectral index `gamma=2.2`. MAHAM uses the published box-shaped flare window from MJD `56937.81` to `57096.21`.

The validation checks the published normalization and bounds, spectral index and uncertainty, flare duration, signal-event count, global significance, reconstruction of the best-fit `E2phi` curve, and consistency between the average flux and the published flare fluence.

Because this is a point-source flux, the spectral quantity does not contain a `sr^-1` factor.

### IceCube-170922A 2017

MAHAM dataset:

`icecube.170922a.2017`

IceCube-170922A is represented as an individual neutrino event rather than as a source-flux measurement.

The dataset preserves the event time, track topology, EHE alert selection, reconstructed direction, asymmetric directional uncertainties, deposited muon energy, signalness, and association with TXS 0506+056.

The parent-neutrino energy is an inferred quantity rather than a direct calorimetric energy measurement. MAHAM stores the published most-probable value of `290 TeV` together with the 90% interval from `183 TeV` to `4.3 PeV` and explicitly records the assumed `E^-2.13` astrophysical neutrino spectrum used for that inference.

The validation checks the event identity, topology, selection, direction, deposited muon energy, inferred parent-neutrino energy and interval, signalness, TXS 0506+056 association, and the spectral assumption used for the neutrino-energy inference.

IceCube-170922A is not plotted as an additional source-flux curve because it is an individual event, not a published point-source flux measurement.

### IceCube EHE 2025

MAHAM datasets:

- `icecube.ehe.differential_limit.2025`
- `icecube.ehe.sensitivity.2025`
- `icecube.ehe.effective_area.2025`

The EHE differential limit and sensitivity are all-flavor `E2phi` quantities.

The effective-area release contains total, `nue`, `numu`, and `nutau` effective areas. Each flavor-specific effective area is averaged over neutrinos and antineutrinos, while the total is summed across flavors.

## Validation philosophy

The validation uses MAHAM's public dataset APIs and checks both numerical values and scientific conventions.

It verifies:

- published dataset lengths and energy grids
- confidence levels
- native flavor conventions
- diffuse-intensity versus point-source-flux conventions
- upper-limit classification
- selected published numerical values
- explicit per-flavor to all-flavor conversion
- effective-area flavor summation
- the local electron-neutrino effective-area enhancement near the Glashow resonance
- combined-spectrum profile-likelihood intervals at 68% and 90%
- cascade Figure 3 digitization, 68% simultaneous-coverage intervals, and upper-limit classification
- physical-boundary treatment of zero-best-fit flux bins
- reconstruction of published NGC 1068 and TXS 0506+056 best-fit power laws
- TXS 0506+056 flare duration and fluence consistency
- IceCube-170922A event time, direction, topology, selection, and signalness
- IceCube-170922A deposited muon energy
- IceCube-170922A inferred parent-neutrino energy and 90% interval
- explicit retention of the spectral assumption used for the IceCube-170922A neutrino-energy inference

## Outputs

The validation generates:

- `icecube_flux_results.png`
- `icecube_flux_results.pdf`
- `icecube_combined_2015_spectrum.png`
- `icecube_combined_2015_spectrum.pdf`
- `icecube_cascade_2020_piecewise.png`
- `icecube_cascade_2020_piecewise.pdf`
- `icecube_throughgoing_muon_2022_piecewise.png`
- `icecube_throughgoing_muon_2022_piecewise.pdf`
- `icecube_ngc1068_flux_2022.png`
- `icecube_ngc1068_flux_2022.pdf`
- `icecube_txs0506_flare_2018.png`
- `icecube_txs0506_flare_2018.pdf`
- `icecube_ehe_2025_effective_area.png`
- `icecube_ehe_2025_effective_area.pdf`

IceCube-170922A is validated numerically but does not currently generate a standalone figure.

Generated files are written under `outputs/` and are not normally committed.

## Running

From the MAHAM repository root:

```bash
python validation/published_results/icecube/validate.py
