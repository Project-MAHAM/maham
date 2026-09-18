# Trinity ICRC2025 sensitivity validation

The native dataset is the ten-year all-flavor differential 90% CL sensitivity of the full Trinity Neutrino Observatory from Figure 2 of PoS(ICRC2025)1188.

The 2025 status proceedings state that the Figure 2 differential flux sensitivity is a 90% CL upper-limit sensitivity and assume a 20% duty cycle. The full observatory design contains 18 wide-angle Cherenkov telescopes distributed over at least three sites, with the plotted Observatory sensitivity corresponding to ten years.

The Trinity differential-sensitivity construction integrates the acceptance over one order of magnitude in energy, so MAHAM records a native one-decade normalization.

The 2021 Trinity sensitivity paper defined sensitivity as the flux yielding one detected neutrino. The 2025 status figure instead explicitly presents the displayed differential curve as a 90% CL upper-limit sensitivity and is adapted from the Snowmass comparison of decade-wide 90% CL projected sensitivities. MAHAM therefore preserves the 2025 product directly and does not apply another SES-to-confidence-level conversion.

The 2025 source does not explicitly identify the confidence-interval construction used for this diffuse curve. MAHAM records `statistical_method="not_specified_in_source"` rather than inferring Feldman-Cousins.

Figure 2 is vector graphics. MAHAM extracts the exact dark-green `Trinity Observatory, 10 yrs` path, giving five vertices at `1e6` through `1e10 GeV`.

Pinned provenance:

- source PDF SHA256: `9877781b0d05fecfadb05d4f241537adb7c30fccec93a6c73fe8e877ccb51277`
- extracted CSV SHA256: `83b5be480f37ebcd76512f67abc61288c4a4f12ee94f644b342ca0201fa53038`
