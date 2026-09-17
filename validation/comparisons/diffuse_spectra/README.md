## Current datasets

The comparison currently includes:

- Fermi-LAT 2015 isotropic gamma-ray background (IGRB);
- Fermi-LAT 2015 total extragalactic gamma-ray background (EGB);
- Pierre Auger Observatory 2021 combined cosmic-ray spectrum;
- Telescope Array 2023 combined TA SD + TAx4 SD cosmic-ray spectrum;
- IceCube 2021 Glashow-resonance flux measurement and upper limits;
- IceCube 2025 EHE differential limit;
- IceCube 2025 EHE sensitivity.

The Fermi-LAT spectra use Galactic foreground model A. The final IGRB energy bin is represented as the published upper limit.

The Telescope Array dataset is an independent Project MAHAM digitization of the published combined spectrum and includes its final upper-limit point.

Neutrino results are displayed using the all-flavor comparison convention.

## Common upper-limit normalization

The upper-limit comparison uses a common all-flavor, one-decade differential-limit convention. Native published datasets remain unchanged; the comparison creates transformed table copies and preserves the native normalization metadata.

- IceCube EHE 2025: native all flavor and one decade, so no normalization rescaling.
- Baikal-GVD 2025: native per flavor and one decade, so only the explicit equal-flavor conversion contributes a factor of 3.
- Pierre Auger 2023: native single flavor and \(\Delta\log_{10}E=0.5\). The equal-flavor conversion contributes a factor of 3 and the half-decade to one-decade conversion contributes a factor of 0.5, for a net factor of 1.5 relative to the published native curve.
- ARA five-station 2026: native all flavor and one decade, so no normalization rescaling. The half-decade simulation-energy grid is not treated as the differential-limit width.
- ANITA I-IV: native all flavor with the historical ANITA bandwidth factor \(\Delta=4\). It is converted to the one-decade convention with \(4/\ln(10)\), not with a half-decade bin-width factor.

Feldman-Cousins count factors such as 2.44 belong to constructing a limit from event counts and exposure. They are never applied as an additional conversion factor to an already-published 90% CL flux limit.

### Curated standalone-limit set

Baikal-GVD remains registered and validated in MAHAM, but is intentionally omitted from this overview comparison plot. Its dataset, tests, and published-result validation remain untouched.

The plotted standalone 90% CL limits are IceCube EHE, Auger, ARA, and ANITA I-IV.

ANTARES may be added later as a complementary lower-energy constraint, but it should not be placed under the same `90% CL UL` heading without an explicit convention note because the commonly plotted ANTARES result is a 95% CL spectral-envelope constraint rather than the same one-decade 90% CL differential-limit construction.
