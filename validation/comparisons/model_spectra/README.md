# Diffuse model spectra comparison

This validation comparison visualizes the literature flux models registered in MAHAM in the common `E2phi` representation.

The plot contains three model families:

- gamma-ray source-environment models;
- neutrino source-environment models, converted to all-flavor with the explicit equal-flavor assumption where required;
- neutrino cosmogenic models, converted to all-flavor with the explicit equal-flavor assumption where required.

Every registered model is shown as an individual line. Lines use continuously sampled shades from a class-specific sequential colormap, so colors do not repeat after 10 or 20 models. The shaded region for each class is the pointwise family envelope over the available model support.

The Ajello et al. 2015 gamma-ray model contains an internal published model band. This cross-model comparison uses its representative centerline when constructing the gamma-ray family envelope, matching the central-curve treatment used for the other literature models.

Run from the repository root:

```bash
python validation/comparisons/model_spectra/compare.py
```

Outputs are written to `validation/comparisons/model_spectra/outputs/`.
