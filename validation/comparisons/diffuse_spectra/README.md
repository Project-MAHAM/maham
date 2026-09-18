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

### RNO-G 2021 projected sensitivity

The comparison includes the RNO-G 35-station, five-year design-study projected sensitivity as a dashed curve in a separate projected-sensitivity legend. The bundled curve is derived from the official public effective-volume release using the collaboration's Figure 24 approximate prescription. It is native all-flavor and is not passed through the upper-limit normalization conversion applied to observed limits.

### PUEO 2025 projected sensitivity

The PUEO curve is stored natively as the digitized 30-day trigger-level single-event sensitivity from ICRC2025 Figure 3. For this comparison MAHAM converts the native `Ephi` curve to `E2phi`, converts the PUEO/ANITA `Delta=4` bandwidth convention to one decade, and scales one expected event to a 90% Feldman-Cousins sensitivity for `n=0`, `b=0`. The plotted curve therefore shares the 90% CL comparison convention while retaining the native SES provenance in metadata.

### IceCube-Gen2 Radio 2021 projected sensitivity

The IceCube-Gen2 Radio curve is the native ten-year trigger-level all-flavor differential 90% CL sensitivity of the 313-station ICRC2021 benchmark array. The source explicitly uses decade-wide energy bins and a zero-background hypothesis, so MAHAM applies no flavor, confidence-level, or decade-width conversion. The eight plotted vertices were extracted directly from the vector path in Figure 2 and are spaced by 0.5 decade; that display sampling is not interpreted as the statistical energy width.

### GRAND200k 2021 projected sensitivity

The GRAND200k curve is the native ten-year all-flavor differential 90% CL sensitivity from ICRC2021 Figure 1. It uses the GRAND background-free Feldman-Cousins construction with 2.44 events per decade for no candidates and null background. The simulation is trigger-level, and the 200k sensitivity is obtained by scaling the simulated 10,000 km2 array response by a factor of 20. No flavor, confidence-level, or decade-width conversion is applied. The plotted curve was extracted directly from the vector PDF and independently cross-checked against the matching 2024 GRAND status figure.

### Trinity 2025 projected sensitivity

The Trinity curve is the native ten-year all-flavor differential 90% CL sensitivity from ICRC2025 Figure 2. The source assumes a 20% duty cycle and the full 18-telescope observatory. The Trinity differential-sensitivity construction uses one order of magnitude in energy, so the native normalization is one decade. The 2025 source already labels the displayed curve as a 90% CL upper-limit sensitivity; MAHAM therefore applies no additional SES-to-CL conversion. The source does not explicitly name the confidence-interval construction for this diffuse curve, so no statistical method is inferred. The five plotted vertices were extracted directly from the vector PDF.
