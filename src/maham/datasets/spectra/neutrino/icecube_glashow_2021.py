from io import BytesIO
from zipfile import ZipFile

import astropy.units as u
import numpy as np
from astropy.table import QTable, Table

from maham._core.metadata import DataSource, DatasetMetadata, ProvenanceType, Reference, StorageMode
from maham.datasets.registry import register_dataset
from maham.datasets.spectra.neutrino.base import NeutrinoSpectrumDataset


@register_dataset
class IceCubeGlashowFlux2021(NeutrinoSpectrumDataset):
    metadata = DatasetMetadata(
        id="icecube.glashow.flux.2021",
        title="IceCube Glashow resonance piecewise astrophysical neutrino flux",
        experiment="IceCube",
        messenger="neutrino",
        data_type="spectrum",
        description="Measured per-flavor astrophysical neutrino flux in three neutrino-energy bins accompanying the first Glashow resonance candidate.",
        year=2021,
        confidence_level=0.683,
        quantity="E2phi",
        energy_unit="GeV",
        value_unit="GeV cm-2 s-1 sr-1",
        flavor_convention="per_flavor",
        solid_angle_convention="per_sr",
        paper=Reference(title="Detection of a particle shower at the Glashow resonance with IceCube", authors=("IceCube Collaboration",), year=2021, doi="10.1038/s41586-021-03256-1"),
        dataset_reference=Reference(title="IceCube data for the first Glashow resonance candidate", authors=("IceCube Collaboration",), year=2021, doi="10.21234/gr2021"),
        source=DataSource(provenance=ProvenanceType.OFFICIAL_RELEASE, storage=StorageMode.REMOTE, url="https://icecube.wisc.edu/data-releases/20210310_IceCube_data_for_the_first_Glashow_resonance_candidate.zip", sha256="64c31773fe21b1dc6268da69f2f5427a8d22663b44fc4514a368385c1e455c88"),
        notes=("The official source gives energy in GeV.", "The official source gives per-flavor E2phi in units of 1e-8 GeV cm-2 s-1 sr-1.", "The standardized energy value is the geometric mean of the published bin edges.", "The official source defines bins with y=0.0 as upper limits."),
        tags=("IceCube", "Glashow resonance", "astrophysical neutrinos", "flux"),
    )

    archive_member = "piecewise.csv"

    def load_raw(self, cache: bool = True, show_progress: bool = True) -> Table:
        archive = self.fetch(cache=cache, show_progress=show_progress)
        with ZipFile(archive) as zf:
            matches = [name for name in zf.namelist() if name.endswith(self.archive_member)]
            if len(matches) != 1:
                raise RuntimeError(f"Expected one '{self.archive_member}' in archive, found {len(matches)}.")
            data = zf.read(matches[0])
        clean = b"\n".join(line for line in data.splitlines() if line.strip() and not line.lstrip().startswith(b"#"))
        return Table.read(BytesIO(clean), format="ascii.csv")

    def standardize(self, raw: Table) -> QTable:
        energy_unit = u.GeV
        E2phi_unit = u.GeV / (u.cm**2 * u.s * u.sr)
        energy_min = np.asarray(raw["E_min"], dtype=float)
        energy_max = np.asarray(raw["E_max"], dtype=float)
        table = QTable()
        table["energy_min"] = energy_min * energy_unit
        table["energy_max"] = energy_max * energy_unit
        table["energy"] = np.sqrt(energy_min * energy_max) * energy_unit
        table["E2phi"] = np.asarray(raw["y"], dtype=float) * 1e-8 * E2phi_unit
        table["E2phi_lower"] = np.asarray(raw["y_lower"], dtype=float) * 1e-8 * E2phi_unit
        table["E2phi_upper"] = np.asarray(raw["y_upper"], dtype=float) * 1e-8 * E2phi_unit
        table["is_upper_limit"] = np.asarray(raw["y"], dtype=float) == 0.0
        table.meta["dataset_id"] = self.metadata.id
        table.meta["quantity"] = self.metadata.quantity
        table.meta["flavor_convention"] = self.metadata.flavor_convention
        table.meta["solid_angle_convention"] = self.metadata.solid_angle_convention
        table.meta["confidence_level"] = self.metadata.confidence_level
        table.meta["energy_definition"] = "geometric_mean_of_bin_edges"
        table.meta["provenance"] = self.metadata.source.provenance.value
        return table
