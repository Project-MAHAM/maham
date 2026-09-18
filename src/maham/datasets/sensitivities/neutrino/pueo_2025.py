import astropy.units as u
import numpy as np
from astropy.table import QTable, Table

from maham._core.metadata import DataSource, DatasetMetadata, ProvenanceType, Reference, StorageMode
from maham.datasets.registry import register_dataset
from maham.datasets.spectra.neutrino.base import NeutrinoSpectrumDataset


@register_dataset
class PUEODiffuseSensitivity2025(NeutrinoSpectrumDataset):
    metadata = DatasetMetadata(
        id="pueo.diffuse_sensitivity.2025",
        title="PUEO 30-day trigger-level diffuse neutrino single-event sensitivity",
        experiment="PUEO",
        messenger="neutrino",
        data_type="sensitivity",
        description="Digitized PUEO Total 30-day single-event sensitivity from Figure 3 of the PUEO ICRC2025 proceedings.",
        year=2025,
        quantity="Ephi",
        spectral_kind="differential_intensity",
        energy_unit="GeV",
        value_unit="cm-2 s-1 sr-1",
        flavor_convention="all_flavor",
        solid_angle_convention="per_sr",
        paper=Reference(
            title="Searching for Ultrahigh Energy Neutrinos with PUEO",
            authors=("Q. Abarr", "PUEO Collaboration"),
            year=2025,
            doi="10.22323/1.501.0976",
            url="https://pos.sissa.it/501/976/",
        ),
        dataset_reference=Reference(
            title="Figure 3: predicted PUEO Total 30-day single-event sensitivity",
            authors=("PUEO Collaboration",),
            year=2025,
            url="https://pos.sissa.it/501/976/",
        ),
        source=DataSource(
            provenance=ProvenanceType.DIGITIZED,
            storage=StorageMode.BUNDLED,
            path="data/datasets/sensitivities/neutrino/pueo_diffuse_neutrino_ses_2025.csv",
            sha256="b683db1e2f3cd478eb408dcf4c24d18a893c448052f922a487fb44e68d08d8c6",
        ),
        notes=(
            "Digitized from the rasterized black 'PUEO Total (30d SES)' curve in Figure 3 of PoS(ICRC2025)976.",
            "Source proceedings PDF SHA256: 915abf343474a914661e60c3d0af8a60e91b8c944cbd08203b37ad5de5d5e88a.",
            "The native plotted quantity is Ephi single-event sensitivity in cm^-2 s^-1 sr^-1.",
            "The source projection assumes a 30-day flight with an ANITA-IV-like trajectory and uses nicemc/pueoSim detector simulations.",
            "PUEO defines the diffuse SES at trigger level using SES=1/(T*Delta*AOmega_eff) with bandwidth factor Delta=4.",
            "The associated diffuse detector response is all-flavor.",
            "Post-trigger analysis efficiency and background are not folded into this trigger-level projection.",
            "MAHAM preserves the native SES and performs decade-width and confidence-level conversions explicitly for comparisons.",
            "The visible Figure 3 curve enters the plotting range near 4.2e17 eV; MAHAM does not extrapolate below the digitized support.",
        ),
        tags=("PUEO", "neutrino", "sensitivity", "SES", "trigger level", "digitized", "ICRC2025"),
    )

    def load_raw(self, cache: bool = True, show_progress: bool = True) -> Table:
        return Table.read(self.fetch(cache=cache, show_progress=show_progress), format="ascii.csv")

    def standardize(self, raw: Table) -> QTable:
        table = QTable()
        table["energy"] = np.asarray(raw["energy_GeV"], dtype=float) * u.GeV
        table["Ephi"] = np.asarray(raw["Ephi_SES"], dtype=float) / (u.cm**2 * u.s * u.sr)
        table.meta["dataset_id"] = self.metadata.id
        table.meta["quantity"] = self.metadata.quantity
        table.meta["flavor_convention"] = self.metadata.flavor_convention
        table.meta["solid_angle_convention"] = self.metadata.solid_angle_convention
        table.meta["sensitivity_type"] = "single_event_sensitivity"
        table.meta["response_level"] = "trigger_level"
        table.meta["analysis_efficiency_included"] = False
        table.meta["projection_days"] = 30.0
        table.meta["native_expected_signal_count"] = 1.0
        table.meta["sensitivity_normalization_convention"] = "bandwidth_factor"
        table.meta["sensitivity_bandwidth_factor"] = 4.0
        table.meta["provenance"] = self.metadata.source.provenance.value
        return table
