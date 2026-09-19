# RET-N 2022 projected sensitivity validation

The native MAHAM dataset is the RET-N `10 x 100 kW Preliminary` projected curve from Figure 18 of the Snowmass white paper, *High-energy and ultra-high-energy neutrinos*.

Figure 18 defines the comparison as an expected differential 90% CL sensitivity to an all-flavor diffuse neutrino flux, computed in decade-wide energy bins and assuming ten years unless otherwise noted. The RET-N legend specifies ten stations, each with a 100 kW transmitter.

The supporting RET ARENA2022 proceedings describe the simulated station as one transmitter 1.5 km below the surface surrounded by 27 receivers. The ten-station, ten-year sensitivity assumes an efficient trigger at 0 dB relative to thermal noise over a 50 MHz bandwidth.

The Snowmass publisher PDF is vector graphics, but its dashed RET-N curve is stored as filled stroke-outline geometry rather than a centerline path. MAHAM therefore reconstructs the plotted centerline by taking the geometric center of each of the 55 RET-N dash polygons. This is vector-derived digitization; no raster digitization is used.

No flavor, confidence-level, decade-width, or exposure transformation is applied in the MAHAM diffuse comparison. The Snowmass source does not identify the confidence-interval construction, so MAHAM records `statistical_method="not_specified_in_source"`.

Pinned provenance:

- Snowmass source PDF SHA256: `08f67525199766ff9970b52c70ddc06efa1f3a4a1ba695f134ebb28769d7dfb8`
- extracted CSV SHA256: `7bbbb8497c09248378c0576d844c009614ed3763895b2b1f4fdc157fa4ad1686`
