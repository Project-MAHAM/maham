# Point-Source Neutrino Flux Comparison

This validation comparison places published IceCube point-source neutrino flux results on a common spectral representation.

## Included datasets

- NGC 1068, IceCube 2022
- TXS 0506+056, 2014-2015 158-day neutrino flare

Both datasets are represented in their native `nu_mu + nubar_mu` flavor convention.

The default comparison quantity is `E2phi` in units of `GeV cm^-2 s^-1`. Unlike diffuse neutrino intensities, point-source fluxes do not carry a `sr^-1` factor.

## Scientific interpretation

NGC 1068 is represented by its published steady-source best-fit power law.

TXS 0506+056 is represented by the average best-fit flux during the published 158-day 2014-2015 flare window.

These curves are best-fit source fluxes and are not uncertainty bands. MAHAM does not construct energy-dependent uncertainty bands from independently quoted normalization and spectral-index uncertainties because those parameters are correlated.

IceCube-170922A is not included in this flux comparison. It is an individual 2017 neutrino event associated with TXS 0506+056 and is represented separately by the `icecube.170922a.2017` event dataset.

## Run

```bash
python validation/comparisons/point_source_neutrinos/compare.py
