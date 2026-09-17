import astropy.units as u
import numpy as np
from astropy.table import QTable, Table

from maham._core.metadata import DataSource, DatasetMetadata, ProvenanceType, Reference, StorageMode
from maham.datasets.efficiencies.base import EfficiencyDataset
from maham.datasets.registry import register_dataset


@register_dataset
class ARAFiveStationSignalEfficiency2026(EfficiencyDataset):
    metadata = DatasetMetadata(
        id="ara.five_station.signal_efficiency.2026",
        title="ARA five-station exposure-averaged signal efficiency",
        experiment="ARA",
        messenger="neutrino",
        data_type="efficiency",
        description="Exposure-averaged array-wide signal efficiency after event selection from Figure 14 of the 10.6-year five-station ARA analysis.",
        year=2026,
        quantity="efficiency",
        energy_unit="eV",
        value_unit="1",
        paper=Reference(title="Search for Ultrahigh Energy Neutrinos using 10.6 Years of Askaryan Radio Array Data", authors=("ARA Collaboration",), year=2026),
        dataset_reference=Reference(title="Figure 14 of Search for Ultrahigh Energy Neutrinos using 10.6 Years of Askaryan Radio Array Data", authors=("ARA Collaboration",), year=2026),
        source=DataSource(provenance=ProvenanceType.DIGITIZED, storage=StorageMode.BUNDLED, path="data/datasets/efficiencies/neutrino/ara_five_station_signal_efficiency_2026.csv", sha256="fbdef16d7c9f1b93fed3e4ea74dd7cb68ee8de065cbd398193ceb127c7f587f1"),
        notes=(
            "Numerical values were extracted from the vector content of the black solid exposure-averaged efficiency curve in Figure 14.",
            "The gray configuration-by-configuration curves and previous ARA analysis curves shown for comparison in Figure 14 are not part of this dataset.",
            "The native efficiency is dimensionless and is stored separately from the trigger-level acceptance.",
            "The manuscript also quotes a flux-model-weighted overall analysis efficiency of about 28%; MAHAM retains the energy-dependent Figure 14 curve instead of replacing it with that scalar summary.",
            "Source manuscript dated September 16, 2026 had SHA256 2e3447416516020ea42f529d9f2c6eb8613c78b502c3e56a07e0f885f32dac65.",
        ),
        tags=("ARA", "five station", "signal efficiency", "analysis efficiency", "radio", "digitized"),
    )

    def load_raw(self, cache: bool = True, show_progress: bool = True) -> Table:
        return Table.read(self.fetch(cache=cache, show_progress=show_progress), format="ascii.csv")

    def standardize(self, raw: Table) -> QTable:
        table = QTable()
        table["energy"] = (np.asarray(raw["energy_eV"], dtype=float) * u.eV).to(u.GeV)
        table["efficiency"] = np.asarray(raw["efficiency"], dtype=float) * u.one
        table.meta["dataset_id"] = self.metadata.id
        table.meta["quantity"] = self.metadata.quantity
        table.meta["averaging"] = "exposure_weighted_array_wide"
        table.meta["response_stage"] = "after_event_selection"
        table.meta["provenance"] = self.metadata.source.provenance.value
        return table
