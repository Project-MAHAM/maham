# Pierre Auger Observatory Validation

This validation reproduces and checks the Pierre Auger Observatory combined cosmic-ray energy spectrum published in 2021.

## Dataset

MAHAM dataset:

`auger.combined_spectrum.2021`

The source is the official electronic supplementary material corresponding to the combined spectrum in Table 10 of the publication.

The native spectral quantity is `J`, with units:

`km^-2 yr^-1 sr^-1 eV^-1`

The published statistical and systematic uncertainties are retained separately.

## Validation

The validation checks:

- the number of published spectrum points;
- the first and last published energy bins and flux values;
- monotonicity of the energy grid;
- reconstruction of bin centers and edges from `lg(E/eV)` and the published logarithmic half-widths;
- non-negative statistical and systematic uncertainties;
- dataset metadata and native spectral convention.

The validation figure uses the publication convention `E^2.6 J(E)`.

## Outputs

Running:

```bash
python validation/published_results/auger/validate.py
