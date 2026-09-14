import astropy.units as u
import numpy as np
from astropy.table import QTable, Table

from maham._core.metadata import DataSource, DatasetMetadata, ProvenanceType, Reference, StorageMode
from maham.datasets.registry import register_dataset
from maham.datasets.spectra.neutrino.base import NeutrinoSpectrumDataset


@register_dataset
class IceCubeThroughgoingMuonPiecewiseFlux2022(NeutrinoSpectrumDataset):
    metadata = DatasetMetadata(
        id="icecube.throughgoing_muon_piecewise_flux.2022",
        title="IceCube 9.5-year through-going muon-neutrino piece-wise flux",
        experiment="IceCube",
        messenger="neutrino",
        data_type="spectrum",
        description="Five-piece astrophysical nu_mu + nubar_mu flux from 9.5 years of northern-sky through-going muon data.",
        year=2022,
        quantity="E2phi",
        spectral_kind="differential_intensity",
        energy_unit="GeV",
        value_unit="GeV cm-2 s-1 sr-1",
        flavor_convention="numu_nubar",
        solid_angle_convention="per_sr",
        paper=Reference(
            title="Improved Characterization of the Astrophysical Muon-Neutrino Flux with 9.5 Years of IceCube Data",
            authors=("IceCube Collaboration",),
            year=2022,
            doi="10.3847/1538-4357/ac4d29",
        ),
        source=DataSource(
            provenance=ProvenanceType.PUBLISHED_TABLE,
            storage=StorageMode.BUNDLED,
            path="data/datasets/spectra/neutrino/icecube_throughgoing_muon_piecewise_2022.csv",
            sha256="2df5b1d88498d693b0e8c992f67ce8779db4ec1698099e6b3c9aebe40e41b992",
        ),
        notes=(
            "Values are transcribed directly from Table 5 of the publication, not digitized from a figure.",
            "Each piece has fixed spectral index gamma=2.0 and normalization defined at 100 TeV.",
            "C_units = 1e-18 GeV-1 cm-2 s-1 sr-1.",
            "Pieces 2-4 quote 68.27% profile-likelihood intervals.",
            "Pieces 1 and 5 quote 90% CL upper limits.",
            "All five piece normalizations are fitted simultaneously and therefore are correlated.",
        ),
        tags=("IceCube", "through-going muons", "astrophysical neutrinos", "numu", "piecewise flux"),
    )

    def load_raw(self, cache: bool = True, show_progress: bool = True) -> Table:
        return Table.read(self.fetch(cache=cache, show_progress=show_progress), format="ascii.csv")

    def standardize(self, raw: Table) -> QTable:
        energy_min = np.asarray(raw["energy_min_GeV"], dtype=float)
        energy_max = np.asarray(raw["energy_max_GeV"], dtype=float)
        scale = 1e-8 * u.GeV / (u.cm**2 * u.s * u.sr)

        table = QTable()
        table["energy_min"] = energy_min * u.GeV
        table["energy_max"] = energy_max * u.GeV
        table["energy"] = np.sqrt(energy_min * energy_max) * u.GeV
        table["E2phi"] = np.asarray(raw["phi_piece_Cunits"], dtype=float) * scale
        table["E2phi_lower"] = np.asarray(raw["phi_piece_lower_Cunits"], dtype=float) * scale
        table["E2phi_upper"] = np.asarray(raw["phi_piece_upper_Cunits"], dtype=float) * scale
        table["confidence_level"] = np.asarray(raw["confidence_level"], dtype=float)

        upper_raw = np.asarray(raw["is_upper_limit"])
        table["is_upper_limit"] = np.char.lower(upper_raw.astype(str)) == "true" if upper_raw.dtype.kind in "USO" else upper_raw.astype(bool)

        table.meta["dataset_id"] = self.metadata.id
        table.meta["quantity"] = self.metadata.quantity
        table.meta["flavor_convention"] = self.metadata.flavor_convention
        table.meta["solid_angle_convention"] = self.metadata.solid_angle_convention
        table.meta["confidence_level"] = None
        table.meta["confidence_level_column"] = "confidence_level"
        table.meta["energy_definition"] = "geometric_mean_of_bin_edges"
        table.meta["reference_energy"] = "100 TeV"
        table.meta["spectral_index_per_piece"] = 2.0
        table.meta["interval_method"] = "profile_likelihood"
        table.meta["provenance"] = self.metadata.source.provenance.value
        return table
