import astropy.units as u
import numpy as np
from astropy.table import QTable, Table

from maham._core.metadata import DataSource, DatasetMetadata, ProvenanceType, Reference, StorageMode
from maham.datasets.registry import register_dataset
from maham.datasets.spectra.neutrino.base import NeutrinoSpectrumDataset


@register_dataset
class ARAFiveStationDiffuseNeutrinoLimit2026(NeutrinoSpectrumDataset):
    metadata = DatasetMetadata(
        id="ara.five_station.diffuse_neutrino_limit.2026",
        title="ARA five-station diffuse UHE neutrino upper limit",
        experiment="ARA",
        messenger="neutrino",
        data_type="limit",
        description="All-flavor 90% CL diffuse UHE neutrino upper limit from the 10.6-year five-station ARA analysis, digitized from Figure 13.",
        year=2026,
        confidence_level=0.90,
        quantity="E2phi",
        spectral_kind="differential_intensity",
        energy_unit="eV",
        value_unit="GeV cm-2 s-1 sr-1",
        flavor_convention="all_flavor",
        solid_angle_convention="per_sr",
        paper=Reference(title="Search for Ultrahigh Energy Neutrinos using 10.6 Years of Askaryan Radio Array Data", authors=("ARA Collaboration",), year=2026),
        dataset_reference=Reference(title="Figure 13 of Search for Ultrahigh Energy Neutrinos using 10.6 Years of Askaryan Radio Array Data", authors=("ARA Collaboration",), year=2026),
        source=DataSource(provenance=ProvenanceType.DIGITIZED, storage=StorageMode.BUNDLED, path="data/datasets/limits/neutrino/ara_five_station_diffuse_neutrino_limit_2026.csv", sha256="a7e8c1bac11cf90615ac8ecd43d30ad8d67484cbe778069f10bf6f30c8a37346"),
        notes=(
            "Numerical values were extracted from the vector content of the thick red Figure 13 curve rather than raster pixels.",
            "The native result is an all-flavor 90% CL differential upper limit in E2phi.",
            r"The differential upper limit is normalized to decade-wide energy intervals, \(\Delta\log_{10}E=1\). The half-decade simulated-energy grid and plotted point spacing do not define the statistical limit width.",
            "The manuscript uses neutrino energy in eV; the bundled CSV preserves that native energy unit and the standardized table converts energy to GeV.",
            "The first recoverable vector point is at 10^16.5 eV because the lower-energy curve is clipped by the published Figure 13 plotting range; no 10^16 eV value is invented.",
            "The analysis uses data from all five ARA stations collected from January 2013 through December 2023, corresponding to 10.6 years of array-wide livetime.",
            "The manuscript reports zero neutrino candidates on an expected background of 0.13 +/- 0.01 (stat.) +0.05/-0.06 (syst.) events.",
            "Source manuscript dated September 16, 2026 had SHA256 2e3447416516020ea42f529d9f2c6eb8613c78b502c3e56a07e0f885f32dac65.",
        ),
        tags=("ARA", "five station", "UHE neutrinos", "diffuse neutrino flux", "upper limit", "radio", "digitized"),
    )

    def load_raw(self, cache: bool = True, show_progress: bool = True) -> Table:
        return Table.read(self.fetch(cache=cache, show_progress=show_progress), format="ascii.csv")

    def standardize(self, raw: Table) -> QTable:
        unit = u.GeV / (u.cm**2 * u.s * u.sr)
        table = QTable()
        table["energy"] = (np.asarray(raw["energy_eV"], dtype=float) * u.eV).to(u.GeV)
        table["E2phi"] = np.asarray(raw["E2phi"], dtype=float) * unit
        table["confidence_level"] = np.asarray(raw["confidence_level"], dtype=float)
        upper_raw = np.asarray(raw["is_upper_limit"])
        table["is_upper_limit"] = np.char.lower(upper_raw.astype(str)) == "true" if upper_raw.dtype.kind in "USO" else upper_raw.astype(bool)
        table.meta["dataset_id"] = self.metadata.id
        table.meta["quantity"] = self.metadata.quantity
        table.meta["flavor_convention"] = self.metadata.flavor_convention
        table.meta["solid_angle_convention"] = self.metadata.solid_angle_convention
        table.meta["confidence_level"] = self.metadata.confidence_level
        table.meta["limit_type"] = "differential_upper_limit"
        table.meta["limit_normalization_convention"] = "log10_energy_width"
        table.meta["log10_energy_width_decades"] = 1.0
        table.meta["observation_period"] = "2013-01 to 2023-12"
        table.meta["array_wide_livetime_years"] = 10.6
        table.meta["provenance"] = self.metadata.source.provenance.value
        return table
