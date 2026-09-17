# Pierre Auger Observatory Validation

This validation reproduces and checks the Pierre Auger Observatory combined cosmic-ray spectrum and diffuse UHE-neutrino differential upper limit in their native published conventions.

## Combined Cosmic-Ray Spectrum 2021

MAHAM dataset:

`auger.combined_spectrum.2021`

The source is the official electronic supplementary material corresponding to the combined spectrum in Table 10 of the publication. The native spectral quantity is `J` in `km^-2 yr^-1 sr^-1 eV^-1`, with statistical and systematic uncertainties retained separately.

The validation checks the number of points, published endpoint values, monotonicity, reconstruction of logarithmic bin centers and edges, uncertainty signs, metadata, and native spectral convention. The validation figure uses the publication convention `E^2.6 J(E)`.

## Diffuse UHE Neutrino Differential Upper Limit 2023

MAHAM dataset:

`auger.diffuse_neutrino_limit.2023`

The native result is the curved differential upper limit in Figure 4 of PoS(ICRC2023)1488.
The native curve was re-extracted directly from the PDF vector path and cross-checked against Figure 4 of the Auger ICRC2025 proceedings; the two vector curves agree. The earlier MAHAM extraction used an incorrect logarithmic y-axis mapping and has been replaced. Numerical values are extracted from the vector content of the proceedings PDF. The paper labels the result as single flavor, which is represented by MAHAM's `per_flavor` convention, and states that the differential limits use bins of width `Delta log10(E_nu/eV)=0.5`.

The combined search uses data collected from 1 January 2004 through 31 December 2021 and reports no neutrino candidates. The differential result is at 90% CL. The separate integral `E^-2` normalization limit quoted in the paper is not mixed into this dataset.

The published-result validation plot remains in the native single-flavor `E2phi` convention and draws the standalone upper limit as a solid black line. Conversion to all flavor is tested explicitly with `flavor_assumption="equal"` but is reserved for cross-experiment comparison plots.

## Outputs

Running:

```bash
python validation/published_results/auger/validate.py
```

writes:

- `auger_combined_spectrum_2021.png`
- `auger_combined_spectrum_2021.pdf`
- `auger_diffuse_neutrino_limit_2023.png`
- `auger_diffuse_neutrino_limit_2023.pdf`
