import astropy.units as u
import numpy as np
from astropy.table import QTable, Table

from maham._core.metadata import DataSource, DatasetMetadata, ProvenanceType, Reference, StorageMode
from maham.datasets.effective_area.base import EffectiveAreaDataset
from maham.datasets.registry import register_dataset


@register_dataset
class BaikalGVDEffectiveArea2025(EffectiveAreaDataset):
    metadata = DatasetMetadata(
        id="baikal_gvd.effective_area.2025",
        title="Baikal-GVD very-high-energy cascade effective area",
        experiment="Baikal-GVD",
        messenger="neutrino",
        data_type="effective_area",
        description="Published Baikal-GVD effective area for very-high-energy neutrino-induced cascades in the 2023 detector configuration.",
        year=2025,
        quantity="effective_area",
        energy_unit="TeV",
        value_unit="m2",
        paper=Reference(title="Constraints on the diffuse flux of multi-PeV astrophysical neutrinos obtained with the Baikal Gigaton Volume Detector", authors=("Baikal-GVD Collaboration",), year=2025, doi="10.1103/jlz3-26lw", url="https://arxiv.org/abs/2507.05769"),
        dataset_reference=Reference(title="effarea.txt ancillary file for arXiv:2507.05769v2", authors=("Baikal-GVD Collaboration",), year=2025, url="https://arxiv.org/src/2507.05769v2/anc/effarea.txt"),
        source=DataSource(provenance=ProvenanceType.OFFICIAL_RELEASE, storage=StorageMode.BUNDLED, path="data/datasets/effective_area/neutrino/baikal_gvd_effective_area_2025.csv", sha256="21132e6eeea05f8467eb4d5a04ec55f0df4f620e2c7351573f844c3398c5c8b5"),
        notes=(
            "The bundled CSV preserves the numerical values of the official arXiv ancillary file effarea.txt; only the whitespace-delimited layout and header names were normalized to CSV.",
            "The ancillary file defines an exposure-weighted average over the upper hemisphere, 2pi solid angle, for the Baikal-GVD 2023 configuration.",
            "Flavor-resolved nue, numu, and nutau effective areas and the published total effective area are retained in m2.",
            "The electron-neutrino effective area contains the Glashow-resonance enhancement near 6.3 PeV and includes the high-energy LPM suppression described in the paper.",
            "This upper-hemisphere response must not be silently relabeled as the exposure-weighted full-sky 4pi flavor-average effective area used in the paper's cross-experiment Figure 4.",
        ),
        tags=("Baikal-GVD", "effective area", "cascade", "neutrino", "detector response", "official ancillary"),
    )

    def load_raw(self, cache: bool = True, show_progress: bool = True) -> Table:
        return Table.read(self.fetch(cache=cache, show_progress=show_progress), format="ascii.csv")

    def standardize(self, raw: Table) -> QTable:
        table = QTable()
        table["energy"] = (10 ** np.asarray(raw["log10_energy_TeV"], dtype=float) * u.TeV).to(u.GeV)
        table["effective_area_nue"] = np.asarray(raw["effective_area_nue_m2"], dtype=float) * u.m**2
        table["effective_area_numu"] = np.asarray(raw["effective_area_numu_m2"], dtype=float) * u.m**2
        table["effective_area_nutau"] = np.asarray(raw["effective_area_nutau_m2"], dtype=float) * u.m**2
        table["effective_area_total"] = np.asarray(raw["effective_area_total_m2"], dtype=float) * u.m**2
        table.meta["dataset_id"] = self.metadata.id
        table.meta["quantity"] = self.metadata.quantity
        table.meta["detector_configuration"] = "Baikal-GVD 2023"
        table.meta["solid_angle_convention"] = "upper_hemisphere_2pi_exposure_weighted_average"
        table.meta["flavor_structure"] = "nue_numu_nutau_and_published_total"
        table.meta["provenance"] = self.metadata.source.provenance.value
        return table
