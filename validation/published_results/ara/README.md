# ARA Validation

This validation reproduces the native published results used for the 10.6-year five-station Askaryan Radio Array analysis.

## ARA Five-Station Diffuse Neutrino Upper Limit 2026

MAHAM dataset:

`ara.five_station.diffuse_neutrino_limit.2026`

The native result is the thick red curve in Figure 13. It is an all-flavor 90% CL differential upper limit in `E2phi`. MAHAM digitizes the vector content of the manuscript figure and preserves the native energy coordinate in eV in the bundled CSV.

The first recoverable vector point is at `10^16.5 eV`; the lower-energy part of the curve is clipped by the Figure 13 plotting range, so MAHAM does not invent a `10^16 eV` upper-limit value.

Standalone upper-limit validation plots are drawn as solid black lines. Point-style upper-limit arrows are reserved for spectral measurements containing upper-limit bins.

## ARA Five-Station Trigger-Level Acceptance 2026

MAHAM dataset:

`ara.five_station.trigger_acceptance.2026`

Figure 4 gives the trigger-level acceptance of the full array in `km^2 sr`, averaged over all six neutrino and antineutrino types and averaged over the full-array livetime. This native acceptance is what is bundled and plotted in published-result validation.

For future cross-experiment detector-response comparisons, the standardized table also exposes the explicitly derived quantity

`sky_averaged_effective_area = acceptance / (4*pi sr)`

in `km^2`. This derived convenience is not written into the native source CSV and is not plotted as though it were the published Figure 4 quantity.

## ARA Five-Station Signal Efficiency 2026

MAHAM dataset:

`ara.five_station.signal_efficiency.2026`

Figure 14 gives the array-wide signal efficiency after event selection. MAHAM stores the black exposure-averaged curve as a separate dimensionless efficiency dataset. The gray individual-configuration curves and older ARA comparison curves are not included.

The manuscript quotes an overall efficiency near 28% for a flux corresponding to current experimental upper limits, but that scalar summary does not replace the energy-dependent Figure 14 result.

## Outputs

Running:

```bash
python validation/published_results/ara/validate.py
```

writes:

- `ara_five_station_diffuse_neutrino_limit_2026.png`
- `ara_five_station_diffuse_neutrino_limit_2026.pdf`
- `ara_five_station_trigger_acceptance_2026.png`
- `ara_five_station_trigger_acceptance_2026.pdf`
- `ara_five_station_signal_efficiency_2026.png`
- `ara_five_station_signal_efficiency_2026.pdf`
