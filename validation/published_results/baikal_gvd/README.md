# Baikal-GVD published-result validation

This directory validates MAHAM's Baikal-GVD 2025 very-high-energy neutrino datasets against the published result and its official ancillary effective-area release.

## Datasets

### Diffuse multi-PeV neutrino upper limit

MAHAM dataset:

`baikal_gvd.diffuse_neutrino_limit.2025`

The native result is the 90% CL `E2phi` upper limit listed in Table I of the 2025 Baikal-GVD diffuse high-energy cascade analysis. The table gives the flux per one flavor, summed over neutrinos and antineutrinos, assuming an isotropic flux and flavor equipartition.

The eight limits use overlapping decade-wide energy bins and a `1/E` spectrum within each bin. MAHAM stores the published per-flavor values natively and constructs an all-flavor view only through the explicit equal-flavor conversion.

### Very-high-energy cascade effective area

MAHAM dataset:

`baikal_gvd.effective_area.2025`

The effective-area values come from the official `effarea.txt` ancillary file distributed with arXiv:2507.05769v2. The bundled MAHAM CSV preserves the released numerical values and changes only the text layout into named CSV columns.

The source defines the response as an exposure-weighted average over the upper hemisphere (`2pi` solid angle) for the Baikal-GVD 2023 detector configuration. The released `nue`, `numu`, `nutau`, and total effective areas are retained in `m2`.

This response is not silently converted into the different exposure-weighted full-sky flavor-average convention used for the cross-experiment effective-area comparison in Figure 4 of the paper.

## Validation philosophy

The validation reproduces the result in its native convention. It checks:

- the eight published Table I limits
- 90% confidence level
- per-flavor and `nu+nubar` conventions
- decade-wide overlapping bins and the within-bin `1/E` assumption
- explicit equal-flavor conversion to all flavor
- the 45 official ancillary effective-area points
- the upper-hemisphere `2pi` averaging convention
- consistency of the published total effective area with the flavor-resolved columns
- the electron-neutrino effective-area enhancement around the Glashow resonance

## Outputs

The published-result upper limit is drawn as a solid black line through the published bin centers. Point-style upper-limit arrows are reserved for spectral measurements that contain upper-limit bins. Plot labels use LaTeX neutrino notation, and validation figures retain the native published physical convention rather than pre-converting to the common comparison convention.

The validation generates:

- `baikal_gvd_diffuse_limit_2025.png`
- `baikal_gvd_diffuse_limit_2025.pdf`
- `baikal_gvd_effective_area_2025.png`
- `baikal_gvd_effective_area_2025.pdf`

Generated files are written under `outputs/` and are not normally committed.

## Running

From the MAHAM repository root:

```bash
python validation/published_results/baikal_gvd/validate.py
```
