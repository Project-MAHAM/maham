from io import BytesIO

import astropy.units as u
import numpy as np
from astropy.table import QTable, Table

from maham._core.metadata import DataSource, DatasetMetadata, ProvenanceType, Reference, StorageMode
from maham.datasets.registry import register_dataset
from maham.datasets.spectra.neutrino.base import NeutrinoSpectrumDataset


@register_dataset
class IceCubeEHELimit2025(NeutrinoSpectrumDataset):
    metadata = DatasetMetadata(
        id="icecube.ehe.differential_limit.2025",
        title="IceCube 12.6-year EHE differential neutrino upper limit",
        experiment="IceCube",
        messenger="neutrino",
        data_type="limit",
        description="Observed all-flavor differential neutrino upper limit from the IceCube 12.6-year extremely-high-energy neutrino search.",
        year=2025,
        confidence_level=0.90,
        quantity="E2phi",
        spectral_kind="differential_intensity",
        energy_unit="GeV",
        value_unit="GeV cm-2 s-1 sr-1",
        flavor_convention="all_flavor",
        solid_angle_convention="per_sr",
        paper=Reference(title="Search for Extremely-High-Energy Neutrinos and First Constraints on the Ultrahigh-Energy Cosmic-Ray Proton Fraction with IceCube", authors=("IceCube Collaboration",), year=2025, doi="10.1103/PhysRevLett.135.031001"),
        dataset_reference=Reference(title="Data release for A search for extremely-high-energy neutrinos and first constraints on the ultra-high-energy cosmic-ray proton fraction with IceCube", authors=("IceCube Collaboration",), year=2025, doi="10.7910/DVN/JHK49D"),
        source=DataSource(provenance=ProvenanceType.OFFICIAL_RELEASE, storage=StorageMode.REMOTE, url="https://dataverse.harvard.edu/api/access/dataset/:persistentId/versions/1.0?persistentId=doi:10.7910/DVN/JHK49D", archive_member="differential_limit_and_sensitivity.csv", archive_member_sha256="b4d107c3cdd73c994e8399f6d8672bfe8a96c875b55cd46b7abe1522e30dd859", archive_member_size=393),
        notes=("The native result is an all-flavor differential upper limit at 90% CL.", "The official source file also contains the expected sensitivity in its third column.", "load_raw() preserves the sensitivity column; load() returns only the observed upper limit."),
        tags=("IceCube", "EHE", "upper limit", "neutrino", "flux"),
    )

    def load_raw(self, cache: bool = True, show_progress: bool = True) -> Table:
        data = self._read_archive_member(self.fetch(cache=cache, show_progress=show_progress))
        values = np.loadtxt(BytesIO(data), delimiter=",", comments="#")
        return Table({"energy_GeV": values[:, 0], "limit_E2phi": values[:, 1], "sensitivity_E2phi": values[:, 2]})

    def standardize(self, raw: Table) -> QTable:
        E2phi_unit = u.GeV / (u.cm**2 * u.s * u.sr)
        table = QTable()
        table["energy"] = np.asarray(raw["energy_GeV"], dtype=float) * u.GeV
        table["E2phi"] = np.asarray(raw["limit_E2phi"], dtype=float) * E2phi_unit
        table["is_upper_limit"] = np.ones(len(raw), dtype=bool)
        table.meta["dataset_id"] = self.metadata.id
        table.meta["quantity"] = self.metadata.quantity
        table.meta["flavor_convention"] = self.metadata.flavor_convention
        table.meta["solid_angle_convention"] = self.metadata.solid_angle_convention
        table.meta["confidence_level"] = self.metadata.confidence_level
        table.meta["limit_type"] = "differential_upper_limit"
        table.meta["provenance"] = self.metadata.source.provenance.value
        return table
