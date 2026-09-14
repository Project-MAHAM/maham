# Fermi-LAT Diffuse Gamma-Ray Validation

This validation checks the Project MAHAM implementation of the 2015 Fermi-LAT isotropic gamma-ray background (IGRB) and total extragalactic gamma-ray background (EGB).

## Datasets

MAHAM datasets:

`fermi_lat.igrb.2015`

`fermi_lat.egb.2015`

The data are obtained from the machine-readable VizieR catalog associated with the publication *The spectrum of isotropic diffuse gamma-ray emission between 100 MeV and 820 GeV*.

Both datasets use Galactic foreground model A.

Model A is used as the baseline model for quoted results in the publication but is not assumed by MAHAM to be uniquely preferred over the alternative foreground models.

## Published quantities

The source table provides band-integrated intensities in units of:

`ph cm-2 s-1 sr-1`

MAHAM converts each bin to a bin-averaged differential intensity using:

`phi = integrated_flux / (Emax - Emin)`

with representative energy:

`E = sqrt(Emin * Emax)`

The resulting differential spectrum can then use the standard MAHAM spectral representations:

`phi`, `Ephi`, `E2phi`, and `E3phi`.

## Uncertainties

The source provides two uncertainty classes:

- the primary measurement uncertainty;
- uncertainty associated with Galactic foreground modeling.

MAHAM retains these separately.

The foreground-model uncertainty is not silently combined in quadrature with the primary uncertainty.

## IGRB upper limit

The final IGRB energy bin, 579.2619-819.2 GeV, is represented using the published upper limit:

`2.3e-12 ph cm-2 s-1 sr-1`

rather than the very small unconstrained best-fit central value stored in the electronic table.

The total EGB value in that energy bin remains a measurement.

## Validation

The validation checks:

- 26 energy bins;
- foreground model A selection;
- 100 MeV to 819.2 GeV energy coverage;
- one final IGRB upper limit;
- no EGB upper-limit bins;
- preservation of foreground uncertainties;
- increasing and correctly bounded energy bins;
- conversion to `E2phi`.

The validation plot displays both IGRB and EGB as `E2phi`, with foreground-model uncertainties shown as shaded regions.

## Outputs

Running:

```bash
python validation/published_results/fermi_lat/validate.py
