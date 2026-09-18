# RNO-G 2021 design sensitivity validation

This validation reproduces the nominal 2 sigma_noise differential sensitivity from Figure 24 of the RNO-G design paper using MAHAM's public scientific interfaces.

Pinned provenance:

- RNO-G public-data repository commit: `c7913a3fc3a0a48b0e6689200bf1f4d4e8cf57a0`
- effective-volume JSON SHA256: `8ec29a23489114d39c9163ed94adce4b0ea04fb4e6c135115e0fdd5e0b0df7c6`
- official `figure_24_diffuse_sensitivity.py` SHA256: `ca2e905991bf7c6cd2056ff7c09fc5036c112411ab7f54ae5267b77c287ccc90`

The official plotting script uses `mode="approximate"` and `decade_bin="full"`. On the released 1/6-decade energy grid it multiplies effective area by `decade_factor=5`, uses Feldman-Cousins `N90=2.44`, livetime `(2/3)*5 years`, `4pi` solid angle, and CTW neutrino total cross sections. MAHAM reproduces that prescription explicitly. The factor 5 remains an RNO-G Figure 24 approximation detail rather than a generic decade-width conversion.

The validation also plots a central-Aeff one-decade diagnostic. That diagnostic is not labeled as the published RNO-G sensitivity.
