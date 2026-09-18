import astropy.units as u
import numpy as np
from astropy.table import QTable, Table

from maham._core.metadata import DataSource, DatasetMetadata, ProvenanceType, Reference, StorageMode
from maham.datasets.registry import register_dataset
from maham.datasets.spectra.neutrino.base import NeutrinoSpectrumDataset


@register_dataset
class IceCubeGen2RadioDiffuseSensitivity2021(NeutrinoSpectrumDataset):
    metadata = DatasetMetadata(
        id="icecube_gen2.radio.diffuse_sensitivity.2021",
        title="IceCube-Gen2 Radio ten-year diffuse neutrino sensitivity",
        experiment="IceCube-Gen2 Radio",
        messenger="neutrino",
        data_type="sensitivity",
        description="Ten-year trigger-level all-flavor differential 90% CL sensitivity of the 313-station IceCube-Gen2 Radio benchmark array.",
        year=2021,
        confidence_level=0.90,
        quantity="E2phi",
        spectral_kind="differential_intensity",
        energy_unit="GeV",
        value_unit="GeV cm-2 s-1 sr-1",
        flavor_convention="all_flavor",
        solid_angle_convention="per_sr",
        paper=Reference(
            title="Sensitivity studies for the IceCube-Gen2 radio array",
            authors=("IceCube-Gen2 Collaboration",),
            year=2021,
            doi="10.22323/1.395.1183",
            url="https://pos.sissa.it/395/1183/",
        ),
        dataset_reference=Reference(
            title="Figure 2: ten-year expected differential IceCube-Gen2 Radio sensitivity",
            authors=("IceCube-Gen2 Collaboration",),
            year=2021,
            url="https://pos.sissa.it/395/1183/",
        ),
        source=DataSource(
            provenance=ProvenanceType.DIGITIZED,
            storage=StorageMode.BUNDLED,
            path="data/datasets/sensitivities/neutrino/icecube_gen2_radio_2021_10yr_sensitivity_vector_extracted.csv",
            sha256="68fce5381d48c0b04c09d917c7a2981b139f6e60cacdc7b7e136fe99de663838",
        ),
        notes=(
            "Extracted from the exact dashed-blue vector path of Figure 2 in PoS(ICRC2021)1183; no raster digitization was used.",
            "Source proceedings PDF SHA256: 76fded41e91cab3efc18bcd8c6fe2f7b0c6f3e70ea77fe325ac97fa27a3e64dc.",
            "The source defines the curve as a ten-year expected differential 90% CL trigger-level sensitivity for a zero-background hypothesis.",
            "The sensitivity is for a diffuse all-flavor neutrino flux and decade-wide energy bins.",
            "The simulated benchmark detector contains 313 stations: 144 hybrid plus 169 shallow-only stations.",
            "The plotted curve contains eight half-decade-spaced vertices from 10^16.5 to 10^20 eV; this plotting-point spacing is not the statistical decade width.",
            "The proceedings do not state the confidence-interval construction used to obtain the quoted 90% CL, so MAHAM does not infer Feldman-Cousins or another method.",
            "Analysis efficiency and background-rejection performance are discussed separately from this trigger-level sensitivity.",
        ),
        tags=("IceCube-Gen2", "radio", "neutrino", "sensitivity", "projection", "trigger level", "vector extracted"),
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
        table.meta["benchmark_stations"] = 313
        table.meta["assumed_background_events"] = 0.0
        table.meta["statistical_method"] = "not_specified_in_source"
        table.meta["sensitivity_normalization_convention"] = "log10_energy_width"
        table.meta["log10_energy_width_decades"] = 1.0
        table.meta["plot_point_spacing_decades"] = 0.5
        table.meta["provenance"] = self.metadata.source.provenance.value
        return table
