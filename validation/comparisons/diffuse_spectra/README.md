# Diffuse Spectrum Comparison

This validation compares supported diffuse particle spectra and flux constraints using a common MAHAM spectral representation.

Experiment-specific validation remains responsible for reproducing each release in its native convention. This comparison instead tests MAHAM's cross-dataset spectral conversions.

## Supported representations

The comparison quantity is selected in `compare.py` with:

```python
PLOT_QUANTITY = "E2phi"
