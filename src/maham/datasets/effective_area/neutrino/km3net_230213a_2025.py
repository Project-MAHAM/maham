import json

import astropy.units as u
import numpy as np
from astropy.table import QTable, Table

from maham._core.metadata import DataSource, DatasetMetadata, ProvenanceType, Reference, StorageMode
from maham.datasets.effective_area.base import EffectiveAreaDataset
from maham.datasets.registry import register_dataset


SOURCE_URL = "https://raw.githubusercontent.com/KM3NeT/KM3-230213A-data/main/data/supplementary/simulations/effective_area_brighttrackselection_allflavour_skyavg.json"
SOURCE_SHA256 = "5a321e65a708c1d746ab5605b37deea4dc84aa230a17c0b8967034f651ce8f9f"


@register_dataset
class KM3NeT230213AEffectiveArea2025(EffectiveAreaDataset):
    metadata = DatasetMetadata(
        id="km3net.km3_230213a_effective_area.2025",
        title="KM3NeT KM3-230213A bright-track effective area",
        experiment="KM3NeT",
        messenger="neutrino",
        data_type="effective_area",
        description="Sky-averaged all-flavor effective area used for the KM3-230213A bright-track flux calculation.",
        year=2025,
        quantity="effective_area",
        energy_unit="GeV",
        value_unit="cm2",
        paper=Reference(
            title="Observation of an ultra-high-energy cosmic neutrino with KM3NeT",
            authors=("KM3NeT Collaboration",),
            year=2025,
            doi="10.1038/s41586-024-08543-1",
        ),
        dataset_reference=Reference(
            title="Data for the KM3-230213A high energy event observation",
            authors=("KM3NeT Collaboration",),
            year=2025,
            doi="10.5281/zenodo.14860165",
        ),
        source=DataSource(
            provenance=ProvenanceType.OFFICIAL_REPOSITORY,
            storage=StorageMode.REMOTE,
            url=SOURCE_URL,
            sha256=SOURCE_SHA256,
        ),
        notes=(
            "The official JSON provides energy in GeV and effective area in cm2.",
            "The effective area is sky averaged and all flavor.",
            "This response is used by the official KM3-230213A flux-comparison notebook.",
        ),
        tags=("KM3NeT", "KM3-230213A", "effective area", "neutrino", "detector response"),
    )

    def load_raw(self, cache: bool = True, show_progress: bool = True) -> Table:
        path = self.fetch(cache=cache, show_progress=show_progress)
        with open(path, encoding="utf-8") as f:
            data = json.load(f)

        energy = data["Energy [GeV]"]
        area = data["Aeff [cm^2]"]

        if set(energy) != set(area):
            raise RuntimeError("KM3NeT effective-area energy and response indices do not match.")

        indices = sorted(energy, key=int)
        return Table(
            {
                "energy_GeV": [energy[index] for index in indices],
                "effective_area_total_cm2": [area[index] for index in indices],
            }
        )

    def standardize(self, raw: Table) -> QTable:
        table = QTable()
        table["energy"] = np.asarray(raw["energy_GeV"], dtype=float) * u.GeV
        table["effective_area_total"] = np.asarray(raw["effective_area_total_cm2"], dtype=float) * u.cm**2
        table.meta["dataset_id"] = self.metadata.id
        table.meta["quantity"] = self.metadata.quantity
        table.meta["flavor_convention"] = "all_flavor"
        table.meta["particle_convention"] = "nu_plus_nubar"
        table.meta["sky_averaging"] = "all_sky"
        table.meta["provenance"] = self.metadata.source.provenance.value
        return table
