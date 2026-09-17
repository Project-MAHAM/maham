import astropy.units as u
import numpy as np
from astropy.table import QTable, Table

from maham._core.metadata import DataSource, DatasetMetadata, ProvenanceType, Reference, StorageMode
from maham.datasets.effective_area.base import EffectiveAreaDataset
from maham.datasets.registry import register_dataset


@register_dataset
class ANITAIVAcceptance2019(EffectiveAreaDataset):
    metadata = DatasetMetadata(
        id="anita.iv.acceptance.2019",
        title="ANITA-IV neutrino acceptance",
        experiment="ANITA",
        messenger="neutrino",
        data_type="effective_area",
        description="ANITA-IV neutrino acceptance printed in the Figure 6 table of the ANITA-IV diffuse-neutrino publication.",
        year=2019,
        quantity="acceptance",
        energy_unit="GeV",
        value_unit="km2 sr",
        paper=Reference(title="Constraints on the ultrahigh-energy cosmic neutrino flux from the fourth flight of ANITA", authors=("ANITA Collaboration",), year=2019, doi="10.1103/PhysRevD.99.122001", url="https://arxiv.org/abs/1902.04005"),
        dataset_reference=Reference(title="Figure 6 acceptance table of Constraints on the ultrahigh-energy cosmic neutrino flux from the fourth flight of ANITA", authors=("ANITA Collaboration",), year=2019, doi="10.1103/PhysRevD.99.122001", url="https://doi.org/10.1103/PhysRevD.99.122001"),
        source=DataSource(provenance=ProvenanceType.PUBLISHED_TABLE, storage=StorageMode.BUNDLED, path="data/datasets/effective_area/neutrino/anita_iv_acceptance_2019.csv", sha256="d095d0a7ce8f925539d9b3cdcc9c6eab761556351af182bbbf0e5ddbfaffbf6b"),
        notes=(
            "The Figure 6 table prints seven exact values of A in km2 sr at log10(E/eV)=18, 18.5, ..., 21.",
            "The publication calls A the ANITA-IV effective area, but its km2 sr unit includes solid angle; MAHAM stores the standardized quantity as acceptance to avoid conflating it with an area-only response.",
            "The Figure 6 caption explicitly states that the tabulated acceptance does not include analysis efficiency.",
            "The paper states that the flux limit uses analysis efficiency as a function of neutrino energy, but no numerical energy-dependent efficiency curve is published; scalar model-weighted efficiencies are therefore not registered as an energy-dependent MAHAM response.",
            "This response is ANITA-IV only, whereas the separate upper-limit dataset is the combined ANITA I-IV result.",
        ),
        tags=("ANITA", "ANITA-IV", "acceptance", "effective area", "radio", "detector response", "published table"),
    )

    def load_raw(self, cache: bool = True, show_progress: bool = True) -> Table:
        return Table.read(self.fetch(cache=cache, show_progress=show_progress), format="ascii.csv")

    def standardize(self, raw: Table) -> QTable:
        table = QTable()
        table["energy"] = np.asarray(raw["energy_GeV"], dtype=float) * u.GeV
        table["acceptance"] = np.asarray(raw["acceptance_km2_sr"], dtype=float) * u.km**2 * u.sr
        table.meta["dataset_id"] = self.metadata.id
        table.meta["quantity"] = self.metadata.quantity
        table.meta["includes_analysis_efficiency"] = False
        table.meta["flight"] = "ANITA-IV"
        table.meta["provenance"] = self.metadata.source.provenance.value
        return table
