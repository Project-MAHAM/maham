import astropy.units as u
import numpy as np
from astropy.table import QTable, Table

from maham._core.metadata import DataSource, DatasetMetadata, ProvenanceType, Reference, StorageMode
from maham.datasets.registry import register_dataset
from maham.datasets.spectra.cosmic_ray.base import CosmicRaySpectrumDataset


@register_dataset
class AugerCombinedSpectrum2021(CosmicRaySpectrumDataset):
    metadata = DatasetMetadata(
        id="auger.combined_spectrum.2021",
        title="Pierre Auger combined cosmic-ray energy spectrum",
        experiment="Pierre Auger Observatory",
        messenger="cosmic_ray",
        data_type="spectrum",
        description="Combined SD-750 and SD-1500 all-particle cosmic-ray energy spectrum from the Pierre Auger Observatory.",
        year=2021,
        quantity="J",
        spectral_kind="differential_intensity",
        energy_unit="eV",
        value_unit="km-2 sr-1 yr-1 eV-1",
        paper=Reference(title="The energy spectrum of cosmic rays beyond the turn-down around 10^17 eV as measured with the surface detector of the Pierre Auger Observatory", authors=("Pierre Auger Collaboration",), year=2021, doi="10.1140/epjc/s10052-021-09700-w"),
        dataset_reference=Reference(title="Electronic supplementary material: combined spectrum, Table 10", authors=("Pierre Auger Collaboration",), year=2021, doi="10.1140/epjc/s10052-021-09700-w"),
        source=DataSource(provenance=ProvenanceType.OFFICIAL_RELEASE, storage=StorageMode.REMOTE, url="https://media.springernature.com/original/springer-static/esm/art%3A10.1140%2Fepjc%2Fs10052-021-09700-w/MediaObjects/10052_2021_9700_MOESM5_ESM.txt", sha256="cea1620b28252ab63a789102b9c6ad3bb48a80184e6c1a6f3d39441b91e6e218"),
        notes=("The native spectral quantity is J.", "Energy is published as lg(E/eV) with logarithmic bin half-widths.", "Statistical and systematic uncertainties are retained separately.", "The source corresponds to the combined spectrum in Table 10."),
        tags=("Pierre Auger Observatory", "cosmic rays", "spectrum", "SD-750", "SD-1500"),
    )

    def load_raw(self, cache: bool = True, show_progress: bool = True) -> Table:
        values = np.loadtxt(self.fetch(cache=cache, show_progress=show_progress), comments="#")
        return Table({"lgE_eV": values[:, 0], "lgE_halfwidth": values[:, 1], "J": values[:, 2], "J_stat_err_lower": values[:, 3], "J_stat_err_upper": values[:, 4], "J_sys_err_lower": values[:, 5], "J_sys_err_upper": values[:, 6]})

    def standardize(self, raw: Table) -> QTable:
        lgE = np.asarray(raw["lgE_eV"], dtype=float)
        halfwidth = np.asarray(raw["lgE_halfwidth"], dtype=float)
        J_unit = 1 / (u.km**2 * u.sr * u.yr * u.eV)

        table = QTable()
        table["energy_min"] = 10 ** (lgE - halfwidth) * u.eV
        table["energy_max"] = 10 ** (lgE + halfwidth) * u.eV
        table["energy"] = 10**lgE * u.eV
        table["J"] = np.asarray(raw["J"], dtype=float) * J_unit
        table["J_stat_err_lower"] = np.asarray(raw["J_stat_err_lower"], dtype=float) * J_unit
        table["J_stat_err_upper"] = np.asarray(raw["J_stat_err_upper"], dtype=float) * J_unit
        table["J_sys_err_lower"] = np.asarray(raw["J_sys_err_lower"], dtype=float) * J_unit
        table["J_sys_err_upper"] = np.asarray(raw["J_sys_err_upper"], dtype=float) * J_unit
        table.meta["dataset_id"] = self.metadata.id
        table.meta["quantity"] = self.metadata.quantity
        table.meta["spectrum_type"] = "all_particle"
        table.meta["provenance"] = self.metadata.source.provenance.value
        return table
