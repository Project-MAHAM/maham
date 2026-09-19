import astropy.units as u
import numpy as np
from astropy.table import QTable, Table

from maham._core.metadata import DataSource, DatasetMetadata, ProvenanceType, Reference, StorageMode
from maham.datasets.registry import register_dataset
from maham.datasets.spectra.neutrino.base import NeutrinoSpectrumDataset


@register_dataset
class RETNDiffuseSensitivity2022(NeutrinoSpectrumDataset):
    metadata = DatasetMetadata(
        id="ret_n.diffuse_sensitivity.2022",
        title="RET-N ten-year diffuse neutrino sensitivity",
        experiment="RET-N",
        messenger="neutrino",
        data_type="sensitivity",
        description="Ten-year all-flavor differential 90% CL projected sensitivity of the ten-station RET-N benchmark.",
        year=2022,
        confidence_level=0.90,
        quantity="E2phi",
        spectral_kind="differential_intensity",
        energy_unit="GeV",
        value_unit="GeV cm-2 s-1 sr-1",
        flavor_convention="all_flavor",
        solid_angle_convention="per_sr",
        paper=Reference(
            title="High-energy and ultra-high-energy neutrinos: A Snowmass white paper",
            authors=("M. Ackermann et al.",),
            year=2022,
            doi="10.1016/j.jheap.2022.08.001",
            url="https://doi.org/10.1016/j.jheap.2022.08.001",
        ),
        dataset_reference=Reference(
            title="Figure 18: expected differential 90% CL all-flavor diffuse neutrino sensitivities",
            authors=("M. Ackermann et al.",),
            year=2022,
            doi="10.1016/j.jheap.2022.08.001",
            url="https://doi.org/10.1016/j.jheap.2022.08.001",
        ),
        source=DataSource(
            provenance=ProvenanceType.DIGITIZED,
            storage=StorageMode.BUNDLED,
            path="data/datasets/sensitivities/neutrino/ret_n_diffuse_neutrino_sensitivity_2022.csv",
            sha256="7bbbb8497c09248378c0576d844c009614ed3763895b2b1f4fdc157fa4ad1686",
        ),
        notes=(
            "Vector-derived from the RET-N 10 x 100 kW Preliminary dashed curve in Figure 18 of the 2022 Snowmass white paper; the publisher PDF stores the dashed stroke as filled vector outlines, so MAHAM samples the center of each of the 55 dash polygons. No raster digitization was used.",
            "Source Snowmass PDF SHA256: 08f67525199766ff9970b52c70ddc06efa1f3a4a1ba695f134ebb28769d7dfb8.",
            "Figure 18 explicitly defines the comparison as differential 90% CL sensitivity to an all-flavor diffuse neutrino flux in decade-wide energy bins, with ten-year integration unless otherwise noted.",
            "The Figure 18 RET-N benchmark contains ten stations with a 100 kW transmitter at each station.",
            "The supporting RET ARENA2022 proceedings describe the simulated station as one transmitter 1.5 km below the surface surrounded by 27 receivers and state that the ten-station, ten-year sensitivity assumes efficient triggering at 0 dB relative to thermal noise over a 50 MHz bandwidth.",
            "RET-N uses active radar echo detection of the ionization plasma left by an in-ice particle cascade, distinct from passive Askaryan radio detection.",
            "The source does not identify the confidence-interval construction for the Figure 18 RET-N curve, so MAHAM does not infer Feldman-Cousins or another method.",
            "No flavor, confidence-level, decade-width, or exposure conversion is applied to this dataset for the MAHAM diffuse comparison.",
        ),
        tags=("RET-N", "Radar Echo Telescope", "neutrino", "sensitivity", "projection", "radar", "active radar", "vector extracted", "Snowmass2022"),
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
        table.meta["projection_years"] = 10.0
        table.meta["benchmark_stations"] = 10
        table.meta["transmitter_power_kw_per_station"] = 100.0
        table.meta["receivers_per_station"] = 27
        table.meta["transmitter_depth_km"] = 1.5
        table.meta["response_level"] = "trigger_level"
        table.meta["trigger_snr_db"] = 0.0
        table.meta["trigger_noise_bandwidth_mhz"] = 50.0
        table.meta["analysis_efficiency_included"] = False
        table.meta["statistical_method"] = "not_specified_in_source"
        table.meta["sensitivity_normalization_convention"] = "log10_energy_width"
        table.meta["log10_energy_width_decades"] = 1.0
        table.meta["source_curve_label"] = "RET-N 10 x 100 kW Preliminary"
        table.meta["provenance"] = self.metadata.source.provenance.value
        return table
