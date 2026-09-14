# KM3NeT KM3-230213A validation

This validation covers the MAHAM datasets associated with the KM3-230213A ultra-high-energy neutrino event reported by the KM3NeT Collaboration in 2025.

## References

Paper:

- KM3NeT Collaboration, "Observation of an ultra-high-energy cosmic neutrino with KM3NeT"
- Nature 638, 376-382 (2025)
- DOI: 10.1038/s41586-024-08543-1

Official data release:

- "Data for the KM3-230213A high energy event observation"
- DOI: 10.5281/zenodo.14860165
- Version v1.0

MAHAM datasets:

- `km3net.km3_230213a.2025`
- `km3net.km3_230213a_flux.2025`
- `km3net.km3_230213a_effective_area.2025`

## Flux reproduction

The official KM3NeT flux-comparison notebook computes the one-event astrophysical flux using:

- 335 days of ARCA livetime
- the released sky-averaged all-flavor neutrino-plus-antineutrino effective area
- an incident `E^-2` spectrum
- the central 90% inferred neutrino-energy interval, 7.24e7 to 2.57e9 GeV
- 200 logarithmically spaced integration points
- linear interpolation of the released effective area
- trapezoidal numerical integration

The executable notebook gives

`E2phi = 5.80e-8 GeV cm^-2 s^-1 sr^-1`

for the one-event normalization.

The validation independently reproduces this value from the MAHAM effective-area dataset and verifies the released 1-sigma, 2-sigma, and 3-sigma Feldman-Cousins intervals.

## Notebook normalization note

The explanatory markdown in the official notebook writes a factor `1/2` in the expected-event expression and therefore a factor `2` in the inferred normalization. The executable calculation does not apply this factor and instead evaluates

`1 / (4*pi*T*acceptance)`.

MAHAM reproduces the executable calculation and published numerical result. The discrepancy is documented here rather than silently modifying the released analysis.

## Outputs

Running `validate.py` produces:

- `outputs/km3net_230213a_effective_area.png`
- `outputs/km3net_230213a_effective_area.pdf`
