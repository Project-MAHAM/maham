import astropy.units as u
import numpy as np
from astropy.table import QTable, Table

from maham._core.metadata import DataSource, DatasetMetadata, ProvenanceType, Reference, StorageMode
from maham.datasets.registry import register_dataset
from maham.datasets.spectra.neutrino.base import NeutrinoSpectrumDataset


@register_dataset
class ANITAIIVDiffuseNeutrinoLimit2019(NeutrinoSpectrumDataset):
    metadata = DatasetMetadata(
        id="anita.i_iv_diffuse_neutrino_limit.2019",
        title="ANITA I-IV combined diffuse UHE neutrino upper limit",
        experiment="ANITA",
        messenger="neutrino",
        data_type="limit",
        description="Combined ANITA I-IV all-flavor 90% CL diffuse UHE neutrino upper limit digitized from Figure 6 of the ANITA-IV publication.",
        year=2019,
        confidence_level=0.90,
        quantity="Ephi",
        spectral_kind="differential_intensity",
        energy_unit="GeV",
        value_unit="cm-2 s-1 sr-1",
        flavor_convention="all_flavor",
        solid_angle_convention="per_sr",
        paper=Reference(title="Constraints on the ultrahigh-energy cosmic neutrino flux from the fourth flight of ANITA", authors=("ANITA Collaboration",), year=2019, doi="10.1103/PhysRevD.99.122001", url="https://arxiv.org/abs/1902.04005"),
        dataset_reference=Reference(title="Figure 6 of Constraints on the ultrahigh-energy cosmic neutrino flux from the fourth flight of ANITA", authors=("ANITA Collaboration",), year=2019, doi="10.1103/PhysRevD.99.122001", url="https://doi.org/10.1103/PhysRevD.99.122001"),
        source=DataSource(provenance=ProvenanceType.DIGITIZED, storage=StorageMode.BUNDLED, path="data/datasets/limits/neutrino/anita_i_iv_diffuse_neutrino_limit_2019.csv", sha256="280b15245573d0259c1f5b77f58f06fd391296cb1e2784ca5251bdd84440f4ba"),
        notes=(
            "Numerical values follow the cyan ANITA I-IV curve in Figure 6 and were extracted from the vector content of the published PDF rather than raster pixels.",
            "The native plotted quantity is Ephi = E dN/(dE dA dOmega dt) in cm-2 s-1 sr-1; MAHAM preserves that quantity and performs Ephi-to-E2phi conversion only when requested.",
            "The Figure 6 caption identifies this as the combined all-flavor diffuse UHE neutrino limit from ANITA flights I-IV.",
            "The combined I-IV result is the cyan Figure 6 vector path; the black curve is ANITA-IV only.",
            "As an independent cross-check, converting the corrected native Ephi values to E2phi and applying the 4/ln(10) comparison normalization reproduces the ARA sensitivity repository ANITA input point by point.",
            r"The ANITA differential-limit convention uses the historical bandwidth factor \(\Delta=4\); this is not an energy-bin width.",
            r"For a one-decade comparison, the native ANITA curve is multiplied by \(4/\ln(10)\simeq1.737\), because the native denominator uses \(\Delta=4\) while a one-decade logarithmic interval contributes \(\ln(10)\).",
            r"The 0.5-decade spacing of the seven Figure 6 vertices is only the tabulation grid and must not be interpreted as the statistical differential-limit width.",
            r"The ANITA differential-limit convention uses the historical bandwidth factor \(\Delta=4\). This \(\Delta\) is not an energy-bin width, not four bins per decade, and not \(\Delta\log_{10}E=0.25\).",
            r"For a one-decade comparison convention, \(\Phi_{\rm 1\,decade}=\Phi_{\rm ANITA}\,4/\ln(10)\), giving the scale factor \(4/\ln(10)\simeq1.737\). This normalization conversion is separate from flavor conversion; the combined ANITA I-IV limit is already all flavor.",
            r"The seven recovered vector vertices are spaced by 0.5 decades from \(10^{18}\) to \(10^{21}\,\mathrm{eV}\), but that spacing is only the tabulation/plot grid and must not be interpreted as the differential-limit width.",
            "The accompanying Figure 6 acceptance table is ANITA-IV only and is represented by a separate MAHAM detector-response dataset.",
            "Source PDF used for vector extraction had SHA256 5377f2b48f0ba89c1c49ccfdb7d95dc635bfeeae7a5af84f11e63b558072eeae.",
        ),
        tags=("ANITA", "UHE neutrinos", "diffuse neutrino flux", "upper limit", "radio", "digitized"),
    )

    def load_raw(self, cache: bool = True, show_progress: bool = True) -> Table:
        return Table.read(self.fetch(cache=cache, show_progress=show_progress), format="ascii.csv")

    def standardize(self, raw: Table) -> QTable:
        table = QTable()
        table["energy"] = np.asarray(raw["energy_GeV"], dtype=float) * u.GeV
        table["Ephi"] = np.asarray(raw["Ephi"], dtype=float) / (u.cm**2 * u.s * u.sr)
        table["confidence_level"] = np.asarray(raw["confidence_level"], dtype=float)
        upper_raw = np.asarray(raw["is_upper_limit"])
        table["is_upper_limit"] = np.char.lower(upper_raw.astype(str)) == "true" if upper_raw.dtype.kind in "USO" else upper_raw.astype(bool)
        table.meta["dataset_id"] = self.metadata.id
        table.meta["quantity"] = self.metadata.quantity
        table.meta["flavor_convention"] = self.metadata.flavor_convention
        table.meta["solid_angle_convention"] = self.metadata.solid_angle_convention
        table.meta["confidence_level"] = self.metadata.confidence_level
        table.meta["limit_type"] = "differential_upper_limit"
        table.meta["limit_normalization_convention"] = "anita_bandwidth"
        table.meta["limit_bandwidth_factor"] = 4.0
        table.meta["energy_definition"] = "vector_path_vertices"
        table.meta["provenance"] = self.metadata.source.provenance.value
        return table
