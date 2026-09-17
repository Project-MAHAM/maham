import astropy.units as u
import numpy as np
from astropy.table import QTable, Table

from maham._core.metadata import DataSource, DatasetMetadata, ProvenanceType, Reference, StorageMode
from maham.datasets.registry import register_dataset
from maham.datasets.spectra.neutrino.base import NeutrinoSpectrumDataset


@register_dataset
class BaikalGVDDiffuseNeutrinoLimit2025(NeutrinoSpectrumDataset):
    metadata = DatasetMetadata(
        id="baikal_gvd.diffuse_neutrino_limit.2025",
        title="Baikal-GVD diffuse multi-PeV neutrino upper limit",
        experiment="Baikal-GVD",
        messenger="neutrino",
        data_type="limit",
        description="Published 90% CL per-flavor diffuse neutrino upper limits from the Baikal-GVD high-energy cascade search using 2018-2024 data.",
        year=2025,
        confidence_level=0.90,
        quantity="E2phi",
        spectral_kind="differential_intensity",
        energy_unit="GeV",
        value_unit="GeV cm-2 s-1 sr-1",
        flavor_convention="per_flavor",
        solid_angle_convention="per_sr",
        paper=Reference(title="Constraints on the diffuse flux of multi-PeV astrophysical neutrinos obtained with the Baikal Gigaton Volume Detector", authors=("Baikal-GVD Collaboration",), year=2025, doi="10.1103/jlz3-26lw", url="https://arxiv.org/abs/2507.05769"),
        dataset_reference=Reference(title="Table I of Constraints on the diffuse flux of multi-PeV astrophysical neutrinos obtained with the Baikal Gigaton Volume Detector", authors=("Baikal-GVD Collaboration",), year=2025, doi="10.1103/jlz3-26lw", url="https://doi.org/10.1103/jlz3-26lw"),
        source=DataSource(provenance=ProvenanceType.PUBLISHED_TABLE, storage=StorageMode.BUNDLED, path="data/datasets/limits/neutrino/baikal_gvd_diffuse_neutrino_limit_2025.csv", sha256="85d52312ddfaacb1fdd257b5db84904aebe61bd4096fa83a954bf3d6138a52c7"),
        notes=(
            "Table I gives 90% CL upper limits on the diffuse astrophysical neutrino flux per one flavor, summed over neutrinos and antineutrinos, assuming an isotropic flux and flavor equipartition.",
            r"The published limits use overlapping decade-wide energy intervals, \(\Delta\log_{10}E=1\), and assume a \(1/E\) spectrum within each interval to account for the energy dependence of the exposure.",
            "No event was observed above 10^3.5 TeV; the expected atmospheric background is negligible and the analysis uses N90 approximately 2.3 for zero observed events.",
            "MAHAM stores the published E2phi limits in their native per-flavor convention. Conversion to all-flavor requires flavor_assumption='equal'.",
        ),
        tags=("Baikal-GVD", "cascade", "diffuse neutrinos", "upper limit", "multi-PeV", "published table"),
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
        table.meta["particle_convention"] = "nu_plus_nubar"
        table.meta["solid_angle_convention"] = self.metadata.solid_angle_convention
        table.meta["confidence_level"] = self.metadata.confidence_level
        table.meta["limit_type"] = "differential_upper_limit"
        table.meta["energy_definition"] = "geometric_mean_of_bin_edges"
        table.meta["limit_normalization_convention"] = "log10_energy_width"
        table.meta["log10_energy_width_decades"] = 1.0
        table.meta["limit_spectral_assumption"] = "E^-1"
        table.meta["interval_method"] = "poisson_zero_events_n90_approximately_2.3"
        table.meta["provenance"] = self.metadata.source.provenance.value
        return table
