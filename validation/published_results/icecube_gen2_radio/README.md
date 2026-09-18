# IceCube-Gen2 Radio ICRC2021 sensitivity validation

The native dataset is the ten-year expected differential 90% CL trigger-level sensitivity of the 313-station IceCube-Gen2 Radio benchmark array from Figure 2 of PoS(ICRC2021)1183.

The proceedings define the result as:

- diffuse all-flavor neutrino flux;
- 90% CL;
- zero-background hypothesis;
- trigger level;
- ten years of uptime;
- decade-wide energy bins.

The figure itself is vector graphics. MAHAM therefore extracts the exact eight vertices of the dashed-blue `Gen2 radio` path rather than raster-digitizing it. The path vertices are spaced by 0.5 decade from `10^16.5` to `10^20 eV`; this is the plotting-point spacing and is distinct from the native one-decade statistical width.

The proceedings do not specify which confidence-interval construction was used for the quoted 90% CL. MAHAM therefore records the confidence level and zero-background assumption but does not infer Feldman-Cousins.

Pinned provenance:

- source PDF SHA256: `76fded41e91cab3efc18bcd8c6fe2f7b0c6f3e70ea77fe325ac97fa27a3e64dc`
- extracted CSV SHA256: `68fce5381d48c0b04c09d917c7a2981b139f6e60cacdc7b7e136fe99de663838`
