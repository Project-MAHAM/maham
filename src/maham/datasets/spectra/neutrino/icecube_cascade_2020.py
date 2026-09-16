import astropy.units as u
import numpy as np
from astropy.table import QTable, Table

from maham._core.metadata import DataSource, DatasetMetadata, ProvenanceType, Reference, StorageMode
from maham.datasets.registry import register_dataset
from maham.datasets.spectra.neutrino.base import NeutrinoSpectrumDataset


@register_dataset
class IceCubeCascadePiecewiseFlux2020(NeutrinoSpectrumDataset):
    metadata = DatasetMetadata(
        id="icecube.cascade_piecewise_flux.2020",
        title="IceCube six-year cascade differential astrophysical neutrino flux",
        experiment="IceCube",
        messenger="neutrino",
        data_type="spectrum",
        description="Differential astrophysical neutrino flux per flavor from the 2010-2015 IceCube high-energy cascade analysis, digitized from Figure 3.",
        year=2020,
        confidence_level=0.68,
        quantity="E2phi",
        spectral_kind="differential_intensity",
        energy_unit="GeV",
        value_unit="GeV cm-2 s-1 sr-1",
        flavor_convention="per_flavor",
        solid_angle_convention="per_sr",
        paper=Reference(title="Characteristics of the Diffuse Astrophysical Electron and Tau Neutrino Flux with Six Years of IceCube High Energy Cascade Data", authors=("IceCube Collaboration",), year=2020, doi="10.1103/PhysRevLett.125.121104", url="https://arxiv.org/abs/2001.09520"),
        dataset_reference=Reference(title="Figure 3 of Characteristics of the Diffuse Astrophysical Electron and Tau Neutrino Flux with Six Years of IceCube High Energy Cascade Data", authors=("IceCube Collaboration",), year=2020, doi="10.1103/PhysRevLett.125.121104", url="https://doi.org/10.1103/PhysRevLett.125.121104"),
        source=DataSource(provenance=ProvenanceType.DIGITIZED, storage=StorageMode.BUNDLED, path="data/datasets/spectra/neutrino/icecube_cascade_piecewise_2020.csv", sha256="dfc34adf678f68fdb2134c2cabad430b16d3ee10a043d4cfa14ac8c224dff166"),
        notes=(
            "Numerical values were extracted from the vector content of Figure 3 in the published PDF rather than from raster pixels.",
            "Black crosses are the differential-flux best fits; downward arrows are stored as upper limits with E2phi=0, E2phi_lower=0, and the plotted limit in E2phi_upper.",
            "The Figure 3 horizontal bin extents form one-third-decade energy bins; MAHAM stores those bin edges and uses their geometric means as representative energies.",
            "The published Figure 3 quantity is E2phi for nu+nubar per neutrino flavor. Equal nue, numu, and nutau contributions at Earth are assumed for conversion to all-flavor.",
            "The paper states that the 1-sigma data uncertainties and data limits correspond to 68% CL simultaneous coverage for the unbroken single-power-law flux.",
            "The analysis sensitive energy range is 1.6e4 to 2.6e6 GeV; Figure 3 also displays differential bins outside that range, which are retained here.",
            "Source PDF used for vector extraction had SHA256 c64c11681e5c139fd4f6c936568595ffe05828f35d45750cc537ba3c08065998.",
        ),
        tags=("IceCube", "cascades", "astrophysical neutrinos", "differential spectrum", "piecewise flux", "digitized"),
    )

    def load_raw(self, cache: bool = True, show_progress: bool = True) -> Table:
        return Table.read(self.fetch(cache=cache, show_progress=show_progress), format="ascii.csv")

    def standardize(self, raw: Table) -> QTable:
        energy_min = np.asarray(raw["energy_min_GeV"], dtype=float)
        energy_max = np.asarray(raw["energy_max_GeV"], dtype=float)
        unit = u.GeV / (u.cm**2 * u.s * u.sr)
        table = QTable()
        table["energy_min"] = energy_min * u.GeV
        table["energy_max"] = energy_max * u.GeV
        table["energy"] = np.sqrt(energy_min * energy_max) * u.GeV
        for column in ("E2phi", "E2phi_lower", "E2phi_upper"):
            table[column] = np.asarray(raw[column], dtype=float) * unit
        table["confidence_level"] = np.asarray(raw["confidence_level"], dtype=float)
        upper_raw = np.asarray(raw["is_upper_limit"])
        table["is_upper_limit"] = np.char.lower(upper_raw.astype(str)) == "true" if upper_raw.dtype.kind in "USO" else upper_raw.astype(bool)
        table.meta["dataset_id"] = self.metadata.id
        table.meta["quantity"] = self.metadata.quantity
        table.meta["flavor_convention"] = self.metadata.flavor_convention
        table.meta["solid_angle_convention"] = self.metadata.solid_angle_convention
        table.meta["confidence_level"] = self.metadata.confidence_level
        table.meta["energy_definition"] = "geometric_mean_of_bin_edges"
        table.meta["interval_method"] = "digitized_68_percent_simultaneous_coverage"
        table.meta["sensitive_energy_range_GeV"] = (1.6e4, 2.6e6)
        table.meta["provenance"] = self.metadata.source.provenance.value
        return table
