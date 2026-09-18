# GRAND200k ICRC2021 sensitivity validation

The native dataset is the GRAND200k ten-year differential all-flavor neutrino sensitivity from Figure 1 of PoS(ICRC2021)1181.

The 2021 proceedings state that the ten-year GRAND sensitivity is at 90% CL and is obtained by scaling the simulated 10,000 km2 region to 200,000 km2. The underlying GRAND design calculation uses a background-free Feldman-Cousins upper count of 2.44 events per decade in energy for no candidate events.

The figure is vector graphics. MAHAM extracts the exact maroon `GRAND200k (10 yr)` path rather than raster-digitizing it. The curve extends beyond the right plot boundary in the PDF; MAHAM preserves all visible source vertices and adds the exact linearly clipped endpoint at `1e11 GeV`.

The vector-path sampling is a plotting representation and is not interpreted as the statistical energy width. The native statistical normalization is one decade.

The 2024 GRAND status proceedings reproduce the same ten-year differential GRAND200k curve; the independently extracted vector coordinates agree with the 2021 curve to approximately `1e-4 dex`.

Pinned provenance:

- ICRC2021 source PDF SHA256: `e3dd4ba3279230dee52774465ca7e2992053493d9b2f5e8824c3e3ebcaaea5d3`
- ARENA2024 status PDF SHA256: `90b4da43ca5f996e24813e2d7f9709b2c464594b553493c9024a55cf263ef63f`
- extracted CSV SHA256: `a0f7dea93ff43c58585e2fc110e0799c0df954324683a6a51ddb13b287206d80`
