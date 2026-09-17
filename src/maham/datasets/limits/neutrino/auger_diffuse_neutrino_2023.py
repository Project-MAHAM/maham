import astropy.units as u
import numpy as np
from astropy.table import QTable, Table

from maham._core.metadata import DataSource, DatasetMetadata, ProvenanceType, Reference, StorageMode
from maham.datasets.registry import register_dataset
from maham.datasets.spectra.neutrino.base import NeutrinoSpectrumDataset


@register_dataset
class AugerDiffuseNeutrinoLimit2023(NeutrinoSpectrumDataset):
    metadata = DatasetMetadata(
        id="auger.diffuse_neutrino_limit.2023",
        title="Pierre Auger diffuse UHE neutrino differential upper limit",
        experiment="Pierre Auger Observatory",
        messenger="neutrino",
        data_type="limit",
        description="Single-flavor 90% CL differential upper limit on the diffuse UHE neutrino flux from the combined Pierre Auger neutrino search channels, digitized from Figure 4 of the ICRC2023 proceedings.",
        year=2023,
        confidence_level=0.90,
        quantity="E2phi",
        spectral_kind="differential_intensity",
        energy_unit="GeV",
        value_unit="GeV cm-2 s-1 sr-1",
        flavor_convention="per_flavor",
        solid_angle_convention="per_sr",
        paper=Reference(title="Latest results from the searches for ultra-high-energy photons and neutrinos at the Pierre Auger Observatory", authors=("Pierre Auger Collaboration",), year=2023, doi="10.22323/1.444.1488", url="https://pos.sissa.it/444/1488/"),
        dataset_reference=Reference(title="Figure 4 of Latest results from the searches for ultra-high-energy photons and neutrinos at the Pierre Auger Observatory", authors=("Pierre Auger Collaboration",), year=2023, doi="10.22323/1.444.1488", url="https://pos.sissa.it/444/1488/pdf"),
        source=DataSource(provenance=ProvenanceType.DIGITIZED, storage=StorageMode.BUNDLED, path="data/datasets/limits/neutrino/auger_diffuse_neutrino_limit_2023.csv", sha256="26e3738266484bb886ccd6f9f6029a952e53374218db0c96c5aa47c67fca786c"),
        notes=(
            "Numerical values were extracted from the vector content of Figure 4 in the proceedings PDF rather than from raster pixels.",
            "The published differential result is labeled single flavor; MAHAM maps this native convention to per_flavor.",
            r"The published differential limit uses \(\Delta\log_{10}(E_\nu/\mathrm{eV})=0.5\), so its native normalization is half a decade. This is a limit-normalization convention, not merely the spacing of plotted points.",
            r"Under the equal-flavor assumption, conversion from the native single-flavor, half-decade result to the MAHAM all-flavor, one-decade comparison convention gives the net factor \(3\times0.5=1.5\).",
            "The combined neutrino search uses data from 1 January 2004 through 31 December 2021 and reports no neutrino candidates in any search channel.",
            "The paper also quotes a single-flavor integral E^-2 normalization limit of 3.5e-9 GeV cm-2 s-1 sr-1 over 1e17 to 2.5e19 eV; that integral constraint is not mixed into this differential dataset.",
            "Figure 4 labels the displayed Auger result as Auger (2022) and PRELIMINARY; the MAHAM dataset year identifies the ICRC2023 source used for the digitization.",
            "Source PDF used for vector extraction had SHA256 75431a97b0583ca0ed3ea37f5d37a2e6186060ef5d15030f26f2ce738d68b9b0.",
        ),
        tags=("Pierre Auger Observatory", "UHE neutrinos", "diffuse neutrino flux", "differential upper limit", "digitized"),
    )

    def load_raw(self, cache: bool = True, show_progress: bool = True) -> Table:
        return Table.read(self.fetch(cache=cache, show_progress=show_progress), format="ascii.csv")

    def standardize(self, raw: Table) -> QTable:
        energy_min = np.asarray(raw["energy_min_GeV"], dtype=float)
        energy_max = np.asarray(raw["energy_max_GeV"], dtype=float)
        unit = u.GeV / (u.cm**2 * u.s * u.sr)
        table = QTable()
        table["energy_min"] = energy_min * u.GeV
        table["energy_max"] = energy_max * u.GeV
        table["energy"] = np.sqrt(energy_min * energy_max) * u.GeV
        table["E2phi"] = np.asarray(raw["E2phi"], dtype=float) * unit
        table["confidence_level"] = np.asarray(raw["confidence_level"], dtype=float)
        upper_raw = np.asarray(raw["is_upper_limit"])
        table["is_upper_limit"] = np.char.lower(upper_raw.astype(str)) == "true" if upper_raw.dtype.kind in "USO" else upper_raw.astype(bool)
        table.meta["dataset_id"] = self.metadata.id
        table.meta["quantity"] = self.metadata.quantity
        table.meta["flavor_convention"] = self.metadata.flavor_convention
        table.meta["solid_angle_convention"] = self.metadata.solid_angle_convention
        table.meta["confidence_level"] = self.metadata.confidence_level
        table.meta["limit_type"] = "differential_upper_limit"
        table.meta["energy_definition"] = "geometric_mean_of_bin_edges"
        table.meta["limit_normalization_convention"] = "log10_energy_width"
        table.meta["log10_energy_width_decades"] = 0.5
        table.meta["observation_period"] = "2004-01-01/2021-12-31"
        table.meta["provenance"] = self.metadata.source.provenance.value
        return table
