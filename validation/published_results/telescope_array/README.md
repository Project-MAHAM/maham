# Telescope Array Validation

This validation checks the Project MAHAM digitization of the 2023 Telescope Array combined cosmic-ray energy spectrum.

## Dataset

MAHAM dataset:

`telescope_array.combined_spectrum.2023`

The source figure is Figure 7, right panel, of *Highlights from the Telescope Array Experiment*, presented at ICRC 2023.

The spectrum combines:

- 14 years of Telescope Array surface-detector data;
- 3 years of TAx4 surface-detector data.

The MAHAM table is an independent digitization of the published figure and is not an official Telescope Array machine-readable data release.

## Native convention

The native plotted quantity is:

`E3J`

with the figure convention:

`E3J x 1e-24 [m^-2 s^-1 sr^-1 eV^2]`

The digitized dataset contains:

- 20 measured spectrum points;
- 1 upper-limit point;
- visually resolved vertical uncertainties for 11 measurements.

For points where the vertical uncertainty cannot be resolved from the source raster, MAHAM stores `NaN`. This means unresolved, not zero uncertainty.

## Validation

The validation checks:

- total number of digitized points;
- measurement and upper-limit counts;
- placement of the final upper limit;
- number of resolved vertical uncertainties;
- increasing energy grid;
- native `E3J` convention;
- digitized provenance;
- source-figure metadata;
- reconstruction of the logarithmic energy-bin widths.

## Outputs

Running:

```bash
python validation/published_results/telescope_array/validate.py
