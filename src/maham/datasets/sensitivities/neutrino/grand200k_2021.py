import astropy.units as u
import numpy as np
from astropy.table import QTable, Table

from maham._core.metadata import DataSource, DatasetMetadata, ProvenanceType, Reference, StorageMode
from maham.datasets.registry import register_dataset
from maham.datasets.spectra.neutrino.base import NeutrinoSpectrumDataset


@register_dataset
class GRAND200kDiffuseSensitivity2021(NeutrinoSpectrumDataset):
    metadata = DatasetMetadata(
        id="grand200k.diffuse_sensitivity.2021",
        title="GRAND200k ten-year diffuse neutrino sensitivity",
        experiment="GRAND200k",
        messenger="neutrino",
        data_type="sensitivity",
        description="Ten-year all-flavor differential 90% CL projected sensitivity of GRAND200k.",
        year=2021,
        confidence_level=0.90,
        quantity="E2phi",
        spectral_kind="differential_intensity",
        energy_unit="GeV",
        value_unit="GeV cm-2 s-1 sr-1",
        flavor_convention="all_flavor",
        solid_angle_convention="per_sr",
        paper=Reference(
            title="The Giant Radio Array for Neutrino Detection (GRAND) Project",
            authors=("GRAND Collaboration",),
            year=2021,
            doi="10.22323/1.395.1181",
            url="https://arxiv.org/abs/2108.00032",
        ),
        dataset_reference=Reference(
            title="Figure 1: GRAND200k ten-year differential neutrino sensitivity",
            authors=("GRAND Collaboration",),
            year=2021,
            doi="10.22323/1.395.1181",
            url="https://arxiv.org/abs/2108.00032",
        ),
        source=DataSource(
            provenance=ProvenanceType.DIGITIZED,
            storage=StorageMode.BUNDLED,
            path="data/datasets/sensitivities/neutrino/grand200k_2021_10yr_sensitivity_vector_extracted.csv",
            sha256="a0f7dea93ff43c58585e2fc110e0799c0df954324683a6a51ddb13b287206d80",
        ),
        notes=(
            "Extracted from the exact maroon GRAND200k (10 yr) vector path in Figure 1 of PoS(ICRC2021)1181; no raster digitization was used.",
            "Source ICRC2021 PDF SHA256: e3dd4ba3279230dee52774465ca7e2992053493d9b2f5e8824c3e3ebcaaea5d3.",
            "The 2024 GRAND status proceedings reproduce the same ten-year differential curve; source PDF SHA256: 90b4da43ca5f996e24813e2d7f9709b2c464594b553493c9024a55cf263ef63f.",
            "The ICRC2021 source states that the ten-year GRAND sensitivity is 90% CL and is obtained by scaling the simulated 10,000 km2 region to 200,000 km2.",
            "The underlying GRAND sensitivity construction uses a background-free Feldman-Cousins upper count of 2.44 events per decade in energy for no candidate events.",
            "The simulation chain ends with detector trigger simulation; no post-trigger analysis-efficiency curve is folded into this projected sensitivity.",
            "The source figure presents an all-flavor flux with nu_e:nu_mu:nu_tau=1:1:1.",
            "The vector-path vertex spacing is plotting geometry only and is not interpreted as the statistical energy width.",
        ),
        tags=("GRAND", "GRAND200k", "neutrino", "sensitivity", "projection", "trigger level", "vector extracted"),
    )

    def load_raw(self, cache: bool = True, show_progress: bool = True) -> Table:
        return Table.read(self.fetch(cache=cache, show_progress=show_progress), format="ascii.csv")

    def standardize(self, raw: Table) -> QTable:
        unit = u.GeV / (u.cm**2 * u.s * u.sr)
        table = QTable()
        table["energy"] = np.asarray(raw["energy_GeV"], dtype=float) * u.GeV
        table["E2phi"] = np.asarray(raw["E2phi"], dtype=float) * unit
        table.meta["dataset_id"] = self.metadata.id
        table.meta["quantity"] = self.metadata.quantity
        table.meta["flavor_convention"] = self.metadata.flavor_convention
        table.meta["solid_angle_convention"] = self.metadata.solid_angle_convention
        table.meta["confidence_level"] = self.metadata.confidence_level
        table.meta["sensitivity_type"] = "projected_confidence_level_sensitivity"
        table.meta["response_level"] = "trigger_level"
        table.meta["analysis_efficiency_included"] = False
        table.meta["projection_years"] = 10.0
        table.meta["array_antennas"] = 200000
        table.meta["simulated_antennas"] = 10000
        table.meta["simulated_area_km2"] = 10000.0
        table.meta["extrapolation_factor"] = 20.0
        table.meta["statistical_method"] = "feldman_cousins"
        table.meta["assumed_observed_events"] = 0
        table.meta["assumed_background_events"] = 0.0
        table.meta["feldman_cousins_upper_count"] = 2.44
        table.meta["sensitivity_normalization_convention"] = "log10_energy_width"
        table.meta["log10_energy_width_decades"] = 1.0
        table.meta["provenance"] = self.metadata.source.provenance.value
        return table
