import json

import astropy.units as u
import numpy as np
from astropy.table import QTable, Table

from maham._core.metadata import DataSource, DatasetMetadata, ProvenanceType, Reference, StorageMode
from maham.datasets.effective_volume.base import EffectiveVolumeDataset
from maham.datasets.registry import register_dataset


_PAPER = Reference(title="Design and Sensitivity of the Radio Neutrino Observatory in Greenland (RNO-G)", authors=("RNO-G Collaboration",), year=2021, doi="10.1088/1748-0221/16/03/P03025", url="https://arxiv.org/abs/2010.12279")
_REPOSITORY = Reference(title="RNO-G public data for Design and Sensitivity of the Radio Neutrino Observatory in Greenland (RNO-G)", authors=("RNO-G Collaboration",), year=2023, url="https://github.com/RNO-G/rno-g_public_data/tree/c7913a3fc3a0a48b0e6689200bf1f4d4e8cf57a0/2010.12279_RNO-G_Design_And_Sensitivity")
_THRESHOLDS = ("1.50sigma", "1.75sigma", "2.00sigma", "2.25sigma", "2.50sigma", "all_triggers")


@register_dataset
class RNOGEffectiveVolume2021(EffectiveVolumeDataset):
    metadata = DatasetMetadata(
        id="rno_g.design.effective_volume.2021",
        title="RNO-G design-study effective volume",
        experiment="RNO-G",
        messenger="neutrino",
        data_type="effective_volume",
        description="Official effective-volume arrays underlying the RNO-G 2021 design-study sensitivity projection.",
        year=2021,
        quantity="effective_volume",
        energy_unit="GeV",
        value_unit="m3",
        paper=_PAPER,
        dataset_reference=_REPOSITORY,
        source=DataSource(provenance=ProvenanceType.OFFICIAL_REPOSITORY, storage=StorageMode.BUNDLED, url="https://raw.githubusercontent.com/RNO-G/rno-g_public_data/c7913a3fc3a0a48b0e6689200bf1f4d4e8cf57a0/2010.12279_RNO-G_Design_And_Sensitivity/data/effective_volumes/Veff_dipole_array_Bastille_secondaries.json", path="data/datasets/effective_volume/neutrino/rno_g_effective_volume_2021.json", sha256="8ec29a23489114d39c9163ed94adce4b0ea04fb4e6c135115e0fdd5e0b0df7c6"),
        notes=(
            "Bundled byte-for-byte from the official RNO-G public-data repository at commit c7913a3fc3a0a48b0e6689200bf1f4d4e8cf57a0.",
            "Official source filename: data/effective_volumes/Veff_dipole_array_Bastille_secondaries.json.",
            "The source provides Veff and Veff uncertainty for trigger thresholds 1.50, 1.75, 2.00, 2.25, and 2.50 sigma_noise plus all_triggers.",
            "The official Figure 24 projection uses the 2.00 sigma_noise Veff and uncertainty arrays.",
            "The source values are effective volumes in m3 and energies in eV.",
        ),
        tags=("RNO-G", "effective volume", "neutrino", "detector response", "design study"),
    )

    def load_raw(self, cache: bool = True, show_progress: bool = True) -> Table:
        with self.fetch(cache=cache, show_progress=show_progress).open("r", encoding="utf-8") as f:
            data = json.load(f)
        columns = {"energy_eV": np.asarray(data["energies"], dtype=float)}
        for threshold in _THRESHOLDS:
            key = threshold.replace(".", "p")
            columns[f"effective_volume_{key}_m3"] = np.asarray(data[threshold]["Veffs"], dtype=float)
            columns[f"effective_volume_uncertainty_{key}_m3"] = np.asarray(data[threshold]["Veffs_uncertainty"], dtype=float)
        return Table(columns)

    def standardize(self, raw: Table) -> QTable:
        table = QTable()
        table["energy"] = np.asarray(raw["energy_eV"], dtype=float) * u.eV
        for threshold in _THRESHOLDS:
            key = threshold.replace(".", "p")
            table[f"effective_volume_{key}"] = np.asarray(raw[f"effective_volume_{key}_m3"], dtype=float) * u.m**3
            table[f"effective_volume_uncertainty_{key}"] = np.asarray(raw[f"effective_volume_uncertainty_{key}_m3"], dtype=float) * u.m**3
        table.meta["dataset_id"] = self.metadata.id
        table.meta["quantity"] = self.metadata.quantity
        table.meta["figure24_nominal_trigger"] = "2.00sigma"
        table.meta["source_repository_commit"] = "c7913a3fc3a0a48b0e6689200bf1f4d4e8cf57a0"
        table.meta["provenance"] = self.metadata.source.provenance.value
        return table
