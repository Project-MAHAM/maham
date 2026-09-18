# PUEO ICRC2025 sensitivity validation

MAHAM preserves the Figure 3 `PUEO Total (30d SES)` curve as a native digitized single-event sensitivity and constructs the common comparison curve explicitly.

Native product:

- trigger-level diffuse all-flavor single-event sensitivity
- 30-day projection
- native spectral representation `Ephi`
- PUEO/ANITA bandwidth factor `Delta=4`
- no post-trigger analysis efficiency or background estimate folded in

Comparison transformation:

1. convert `Ephi -> E2phi`;
2. convert `Delta=4` bandwidth normalization to one decade with `4/ln(10)`;
3. convert one expected event to a 90% Feldman-Cousins projected sensitivity for `n=0`, `b=0`.

Pinned digitization provenance:

- source PDF SHA256: `915abf343474a914661e60c3d0af8a60e91b8c944cbd08203b37ad5de5d5e88a`
- digitized CSV SHA256: `b683db1e2f3cd478eb408dcf4c24d18a893c448052f922a487fb44e68d08d8c6`

The source curve is rasterized in the proceedings PDF, so MAHAM records `DIGITIZED` provenance.
