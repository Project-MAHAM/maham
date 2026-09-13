from io import BytesIO

import astropy.units as u
import numpy as np
from astropy.table import QTable, Table

from maham._core.metadata import DataSource, DatasetMetadata, ProvenanceType, Reference, StorageMode
from maham.datasets.effective_area.base import EffectiveAreaDataset
from maham.datasets.registry import register_dataset


@register_dataset
class IceCubeEHEEffectiveArea2025(EffectiveAreaDataset):
    metadata = DatasetMetadata(
        id="icecube.ehe.effective_area.2025",
        title="IceCube 12.6-year EHE neutrino effective area",
        experiment="IceCube",
        messenger="neutrino",
        data_type="effective_area",
        description="Published effective area of the IceCube 12.6-year extremely-high-energy neutrino event selection.",
        year=2025,
        quantity="effective_area",
        energy_unit="GeV",
        value_unit="m2",
        paper=Reference(title="Search for Extremely-High-Energy Neutrinos and First Constraints on the Ultrahigh-Energy Cosmic-Ray Proton Fraction with IceCube", authors=("IceCube Collaboration",), year=2025, doi="10.1103/PhysRevLett.135.031001"),
        dataset_reference=Reference(title="Data release for A search for extremely-high-energy neutrinos and first constraints on the ultra-high-energy cosmic-ray proton fraction with IceCube", authors=("IceCube Collaboration",), year=2025, doi="10.7910/DVN/JHK49D"),
        source=DataSource(provenance=ProvenanceType.OFFICIAL_RELEASE, storage=StorageMode.REMOTE, url="https://dataverse.harvard.edu/api/access/dataset/:persistentId/versions/1.0?persistentId=doi:10.7910/DVN/JHK49D", archive_member="effective_area.csv", archive_member_sha256="614d4f235880c08dfbcde66b054c261d3ae8cf2bcc16cecbdf425d8e589af88d", archive_member_size=4639),
        notes=("The total effective area is summed across neutrino flavors and averaged across neutrinos and antineutrinos.", "The nue, numu, and nutau columns are each averaged over the corresponding neutrino and antineutrino.", "Effective areas are published in m2."),
        tags=("IceCube", "EHE", "effective area", "neutrino", "detector response"),
    )

    def load_raw(self, cache: bool = True, show_progress: bool = True) -> Table:
        data = self._read_archive_member(self.fetch(cache=cache, show_progress=show_progress))
        values = np.loadtxt(BytesIO(data), delimiter=",", comments="#")
        return Table({"energy_GeV": values[:, 0], "effective_area_total_m2": values[:, 1], "effective_area_nue_m2": values[:, 2], "effective_area_numu_m2": values[:, 3], "effective_area_nutau_m2": values[:, 4]})

    def standardize(self, raw: Table) -> QTable:
        table = QTable()
        table["energy"] = np.asarray(raw["energy_GeV"], dtype=float) * u.GeV
        table["effective_area_total"] = np.asarray(raw["effective_area_total_m2"], dtype=float) * u.m**2
        table["effective_area_nue"] = np.asarray(raw["effective_area_nue_m2"], dtype=float) * u.m**2
        table["effective_area_numu"] = np.asarray(raw["effective_area_numu_m2"], dtype=float) * u.m**2
        table["effective_area_nutau"] = np.asarray(raw["effective_area_nutau_m2"], dtype=float) * u.m**2
        table.meta["dataset_id"] = self.metadata.id
        table.meta["quantity"] = self.metadata.quantity
        table.meta["particle_convention"] = "nu_nubar_average"
        table.meta["total_flavor_convention"] = "sum_nue_numu_nutau"
        table.meta["provenance"] = self.metadata.source.provenance.value
        return table
