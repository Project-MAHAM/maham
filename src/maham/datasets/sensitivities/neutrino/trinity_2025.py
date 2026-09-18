import astropy.units as u
import numpy as np
from astropy.table import QTable, Table

from maham._core.metadata import DataSource, DatasetMetadata, ProvenanceType, Reference, StorageMode
from maham.datasets.registry import register_dataset
from maham.datasets.spectra.neutrino.base import NeutrinoSpectrumDataset


@register_dataset
class TrinityDiffuseSensitivity2025(NeutrinoSpectrumDataset):
    metadata = DatasetMetadata(
        id="trinity.diffuse_sensitivity.2025",
        title="Trinity Observatory ten-year diffuse neutrino sensitivity",
        experiment="Trinity",
        messenger="neutrino",
        data_type="sensitivity",
        description="Ten-year all-flavor differential 90% CL projected sensitivity of the full Trinity Neutrino Observatory.",
        year=2025,
        confidence_level=0.90,
        quantity="E2phi",
        spectral_kind="differential_intensity",
        energy_unit="GeV",
        value_unit="GeV cm-2 s-1 sr-1",
        flavor_convention="all_flavor",
        solid_angle_convention="per_sr",
        paper=Reference(
            title="Status of the Trinity PeV Neutrino Observatory",
            authors=("Sofia Stepanoff", "Trinity Collaboration"),
            year=2025,
            doi="10.22323/1.501.1188",
            url="https://pos.sissa.it/501/1188/",
        ),
        dataset_reference=Reference(
            title="Figure 2: Trinity Observatory ten-year differential flux sensitivity",
            authors=("Trinity Collaboration",),
            year=2025,
            doi="10.22323/1.501.1188",
            url="https://pos.sissa.it/501/1188/",
        ),
        source=DataSource(
            provenance=ProvenanceType.DIGITIZED,
            storage=StorageMode.BUNDLED,
            path="data/datasets/sensitivities/neutrino/trinity_diffuse_neutrino_sensitivity_2025.csv",
            sha256="83b5be480f37ebcd76512f67abc61288c4a4f12ee94f644b342ca0201fa53038",
        ),
        notes=(
            "Extracted from the exact dark-green 'Trinity Observatory, 10 yrs' vector path in Figure 2 of PoS(ICRC2025)1188; no raster digitization was used.",
            "Source proceedings PDF SHA256: 9877781b0d05fecfadb05d4f241537adb7c30fccec93a6c73fe8e877ccb51277.",
            "Figure 2 explicitly labels the displayed differential sensitivity as a 90% CL upper-limit sensitivity and assumes a 20% duty cycle.",
            "The source presents a diffuse all-flavor flux with nu_e:nu_mu:nu_tau=1:1:1.",
            "The full Trinity design uses 18 wide-angle Cherenkov telescopes distributed across at least three sites and the plotted Observatory curve assumes ten years.",
            "The Trinity differential-sensitivity construction integrates over one order of magnitude in energy, so MAHAM records a native one-decade normalization.",
            "The 2021 Trinity sensitivity paper defined its native sensitivity as the flux yielding one detected neutrino. The 2025 status figure instead explicitly presents the plotted curve as a 90% CL upper-limit sensitivity; MAHAM therefore uses the 2025 product directly and applies no additional SES-to-CL scaling.",
            "The 2025 source does not explicitly identify the confidence-interval construction used for this diffuse curve, so MAHAM does not infer Feldman-Cousins.",
            "The detector-response calculation includes light-yield and reconstruction requirements but no final background-rejection analysis efficiency is supplied for this design projection.",
        ),
        tags=("Trinity", "neutrino", "sensitivity", "projection", "Cherenkov", "vector extracted", "ICRC2025"),
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
        table.meta["duty_cycle"] = 0.20
        table.meta["observatory_telescopes"] = 18
        table.meta["observatory_sites_minimum"] = 3
        table.meta["response_level"] = "detector_response"
        table.meta["reconstruction_requirements_included"] = True
        table.meta["analysis_efficiency_included"] = False
        table.meta["statistical_method"] = "not_specified_in_source"
        table.meta["sensitivity_normalization_convention"] = "log10_energy_width"
        table.meta["log10_energy_width_decades"] = 1.0
        table.meta["provenance"] = self.metadata.source.provenance.value
        return table
