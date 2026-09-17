# ANITA Validation

This validation reproduces the ANITA I-IV combined diffuse UHE-neutrino upper limit and the ANITA-IV detector acceptance in their native published conventions.

## Combined ANITA I-IV Diffuse Neutrino Upper Limit 2019

MAHAM dataset:

`anita.i_iv_diffuse_neutrino_limit.2019`

The native result is the cyan `ANITA I-IV` curve in Figure 6 of the ANITA-IV publication. MAHAM digitizes the vector content of the published PDF and preserves the native plotted quantity `Ephi = E dN/(dE dA dOmega dt)` in `cm^-2 s^-1 sr^-1`.

The Figure 6 caption identifies the result as an all-flavor diffuse UHE-neutrino limit. The published-result validation therefore remains in native all-flavor `Ephi`. MAHAM's spectral conversion machinery is separately checked by constructing an `E2phi` view for later cross-experiment comparison.

Standalone published upper limits are plotted as solid black lines. Upper-limit arrows are reserved for spectra containing a mixture of measured bins and upper-limit bins.

## ANITA-IV Acceptance 2019

MAHAM dataset:

`anita.iv.acceptance.2019`

Figure 6 prints seven exact values of `A` in `km^2 sr` at half-decade energies from `1e18` through `1e21 eV`. The paper calls this the ANITA-IV effective area, but because the native quantity contains solid angle, MAHAM stores it as `acceptance`.

The Figure 6 caption explicitly states that these acceptance values do not include analysis efficiency. The paper says that the flux limit uses analysis efficiency as a function of neutrino energy, but it does not provide that energy-dependent efficiency numerically. MAHAM therefore does not register the scalar 71% or 82% model-weighted efficiencies as an energy-dependent response.

The acceptance belongs to ANITA-IV only; the flux upper-limit dataset is the combined ANITA I-IV result.

## Outputs

Running:

```bash
python validation/published_results/anita/validate.py
```

writes:

- `anita_i_iv_diffuse_neutrino_limit_2019.png`
- `anita_i_iv_diffuse_neutrino_limit_2019.pdf`
- `anita_iv_acceptance_2019.png`
- `anita_iv_acceptance_2019.pdf`

## Differential-limit normalization convention

ANITA's published differential-limit convention uses the historical bandwidth factor \(\Delta=4\). This is not an energy-bin width. In particular, it does not mean four bins per decade and it does not mean \(\Delta\log_{10}E=0.25\).

For a standard one-decade logarithmic normalization, the denominator associated with the energy interval is \(\ln(10)\). Therefore the conversion used only for cross-experiment comparison is

\[
\Phi_{\rm 1\,decade}=\Phi_{\rm ANITA}\frac{4}{\ln(10)}.
\]

Thus the native ANITA I-IV curve is multiplied by \(4/\ln(10)\simeq1.737\) when constructing MAHAM's common one-decade comparison view. No flavor factor is applied because the combined ANITA I-IV result is already all flavor.

The half-decade spacing of the seven Figure 6 vertices is only the tabulation and plotting grid. It is not the statistical differential-limit width. MAHAM therefore stores `limit_normalization_convention="anita_bandwidth"` and `limit_bandwidth_factor=4.0` rather than assigning a fictitious `log10_energy_width_decades` value to the native ANITA dataset.

### Differential-limit normalization

ANITA's native differential-limit formula contains the historical bandwidth factor \(\Delta=4\). This is not a logarithmic bin width and must not be interpreted as four bins per decade. For a common one-decade comparison convention,

\[
(E\Phi)_{\rm 1\,decade}=(E\Phi)_{\rm ANITA}\frac{4}{\ln(10)}.
\]

Thus the MAHAM comparison view uses the factor \(4/\ln(10)\simeq1.737\). The combined ANITA I-IV curve is already all flavor, so no flavor factor is applied. The half-decade spacing of the plotted Figure 6 vertices is only the tabulation grid.

### Vector-path correction

Figure 6 contains separate ANITA-IV and combined ANITA I-IV curves. The combined I-IV result is the cyan curve; the black curve is ANITA-IV only. An earlier MAHAM extraction accidentally followed the ANITA-IV-only path.

The bundled I-IV CSV now follows the cyan vector path directly. The existing 4/ln(10) one-decade comparison conversion remains unchanged.
