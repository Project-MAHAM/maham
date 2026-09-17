import astropy.units as u
import numpy as np
from astropy.table import QTable, Table

from maham._core.metadata import DataSource, DatasetMetadata, ProvenanceType, Reference, StorageMode
from maham.datasets.effective_area.base import EffectiveAreaDataset
from maham.datasets.registry import register_dataset


@register_dataset
class ARAFiveStationTriggerAcceptance2026(EffectiveAreaDataset):
    metadata = DatasetMetadata(
        id="ara.five_station.trigger_acceptance.2026",
        title="ARA five-station trigger-level neutrino acceptance",
        experiment="ARA",
        messenger="neutrino",
        data_type="effective_area",
        description="Livetime-averaged full-array trigger-level neutrino acceptance from Figure 4 of the 10.6-year five-station ARA analysis.",
        year=2026,
        quantity="acceptance",
        energy_unit="eV",
        value_unit="km2 sr",
        paper=Reference(title="Search for Ultrahigh Energy Neutrinos using 10.6 Years of Askaryan Radio Array Data", authors=("ARA Collaboration",), year=2026),
        dataset_reference=Reference(title="Figure 4 of Search for Ultrahigh Energy Neutrinos using 10.6 Years of Askaryan Radio Array Data", authors=("ARA Collaboration",), year=2026),
        source=DataSource(provenance=ProvenanceType.DIGITIZED, storage=StorageMode.BUNDLED, path="data/datasets/effective_area/neutrino/ara_five_station_trigger_acceptance_2026.csv", sha256="696bb308d108a339bbbfaba341b9e8ccaef46436a50630e5d2864b3dd3caf5ab"),
        notes=(
            "Numerical values were extracted from the vector content of the red ARA5 trigger-level curve in Figure 4.",
            "The native published quantity is trigger-level acceptance in km2 sr, averaged over all six neutrino and antineutrino types and averaged over the livetime of the full array.",
            "The bundled CSV preserves only the native trigger-level acceptance.",
            "The standardized table additionally exposes sky_averaged_effective_area = acceptance/(4*pi sr) in km2 as an explicit derived convenience for future cross-experiment response comparisons.",
            "This is a trigger-level response and must not be treated as an analysis-level effective area without applying the event-selection efficiency consistently.",
            "Source manuscript dated September 16, 2026 had SHA256 2e3447416516020ea42f529d9f2c6eb8613c78b502c3e56a07e0f885f32dac65.",
        ),
        tags=("ARA", "five station", "acceptance", "effective area", "trigger level", "radio", "digitized"),
    )

    def load_raw(self, cache: bool = True, show_progress: bool = True) -> Table:
        return Table.read(self.fetch(cache=cache, show_progress=show_progress), format="ascii.csv")

    def standardize(self, raw: Table) -> QTable:
        table = QTable()
        table["energy"] = (np.asarray(raw["energy_eV"], dtype=float) * u.eV).to(u.GeV)
        table["acceptance"] = np.asarray(raw["trigger_acceptance_km2_sr"], dtype=float) * u.km**2 * u.sr
        table["sky_averaged_effective_area"] = (table["acceptance"] / (4 * np.pi * u.sr)).to(u.km**2)
        table.meta["dataset_id"] = self.metadata.id
        table.meta["quantity"] = self.metadata.quantity
        table.meta["response_level"] = "trigger"
        table.meta["neutrino_type_convention"] = "average_over_six_nu_nubar_types"
        table.meta["livetime_averaged"] = True
        table.meta["sky_averaged_effective_area_definition"] = "acceptance/(4*pi*sr)"
        table.meta["provenance"] = self.metadata.source.provenance.value
        return table
