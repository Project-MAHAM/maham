# IceCube Validation

This validation checks MAHAM implementations of currently supported published IceCube datasets.

## Included results

### IceCube Glashow 2021

MAHAM dataset:

`icecube.glashow.flux.2021`

The native published result is a per-flavor piecewise astrophysical neutrino flux with three energy bins.

The validation checks the native published representation and also constructs an explicit `1:1:1` all-flavor view for comparison with all-flavor EHE results.

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
- upper-limit classification
- selected published numerical values
- explicit per-flavor to all-flavor conversion
- effective-area flavor summation
- the local electron-neutrino effective-area enhancement near the Glashow resonance

## Outputs

The validation generates:

- `icecube_flux_results.png`
- `icecube_flux_results.pdf`
- `icecube_ehe_2025_effective_area.png`
- `icecube_ehe_2025_effective_area.pdf`

Generated files are written under `outputs/` and are not normally committed.

## Running

From the MAHAM repository root:

```bash
python validation/published_results/icecube/validate.py

A successful validation ends with:

Validation passed.
