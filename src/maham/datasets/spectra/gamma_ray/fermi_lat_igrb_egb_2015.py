import astropy.units as u
import numpy as np
from astropy.table import QTable, Table

from maham._core.metadata import DataSource, DatasetMetadata, ProvenanceType, Reference, StorageMode
from maham.datasets.registry import register_dataset
from maham.datasets.spectra.gamma_ray.base import GammaRaySpectrumDataset


SOURCE_URL = "https://cdsarc.cds.unistra.fr/ftp/J/ApJ/799/86/table3.dat"
SOURCE_SHA256 = "438ba07ab0feeb1430e4266ad556532abe25f99647f04cb34087b61b8e59c032"
PAPER_DOI = "10.1088/0004-637X/799/1/86"
VIZIER_DOI = "10.26093/cds/vizier.17990086"
IGRB_FINAL_UPPER_LIMIT = 2.3e-12

RAW_COLUMNS = (
    "model",
    "energy_min",
    "energy_max",
    "igrb",
    "igrb_err_upper",
    "igrb_err_lower",
    "igrb_foreground_err_upper",
    "igrb_foreground_err_lower",
    "egb",
    "egb_err_upper",
    "egb_err_lower",
    "egb_foreground_err_upper",
    "egb_foreground_err_lower",
    "resolved_sources",
    "resolved_sources_err_upper",
    "resolved_sources_err_lower",
)


class _FermiLATDiffuseGamma2015(GammaRaySpectrumDataset):
    component: str

    def load_raw(self, cache: bool = True, show_progress: bool = True) -> Table:
        path = self.fetch(cache=cache, show_progress=show_progress)
        rows = []

        with path.open() as f:
            for line in f:
                fields = line.split()
                if not fields:
                    continue
                rows.append([fields[0], *map(float, fields[1:])])

        table = Table(rows=rows, names=RAW_COLUMNS)
        return table[np.asarray(table["model"]) == "A"]

    def standardize(self, raw: Table) -> QTable:
        energy_min = np.asarray(raw["energy_min"], dtype=float)
        energy_max = np.asarray(raw["energy_max"], dtype=float)
        energy = np.sqrt(energy_min * energy_max)
        width = energy_max - energy_min

        flux = np.asarray(raw[self.component], dtype=float).copy()
        err_upper = np.asarray(raw[f"{self.component}_err_upper"], dtype=float).copy()
        err_lower = np.asarray(raw[f"{self.component}_err_lower"], dtype=float).copy()
        foreground_err_upper = np.asarray(raw[f"{self.component}_foreground_err_upper"], dtype=float).copy()
        foreground_err_lower = np.asarray(raw[f"{self.component}_foreground_err_lower"], dtype=float).copy()

        is_upper_limit = np.zeros(len(raw), dtype=bool)

        if self.component == "igrb":
            is_upper_limit[-1] = True
            flux[-1] = IGRB_FINAL_UPPER_LIMIT
            err_upper[-1] = np.nan
            err_lower[-1] = np.nan
            foreground_err_upper[-1] = np.nan
            foreground_err_lower[-1] = np.nan

        phi = flux / width
        phi_err_upper = err_upper / width
        phi_err_lower = err_lower / width
        phi_foreground_err_upper = foreground_err_upper / width
        phi_foreground_err_lower = foreground_err_lower / width

        energy_unit = u.MeV
        flux_unit = 1 / (u.cm**2 * u.s * u.sr)
        phi_unit = 1 / (u.MeV * u.cm**2 * u.s * u.sr)

        table = QTable()
        table["energy_min"] = energy_min * energy_unit
        table["energy_max"] = energy_max * energy_unit
        table["energy"] = energy * energy_unit
        table["phi"] = phi * phi_unit
        table["phi_lower"] = np.where(np.isfinite(phi_err_lower), phi - phi_err_lower, np.nan) * phi_unit
        table["phi_upper"] = np.where(np.isfinite(phi_err_upper), phi + phi_err_upper, np.nan) * phi_unit
        table["phi_foreground_err_lower"] = phi_foreground_err_lower * phi_unit
        table["phi_foreground_err_upper"] = phi_foreground_err_upper * phi_unit
        table["integrated_flux"] = flux * flux_unit
        table["is_upper_limit"] = is_upper_limit

        table.meta["dataset_id"] = self.metadata.id
        table.meta["quantity"] = "phi"
        table.meta["native_published_quantity"] = "band_integrated_flux"
        table.meta["foreground_model"] = "A"
        table.meta["energy_representative"] = "geometric_mean"
        table.meta["differential_conversion"] = "integrated_flux / (energy_max - energy_min)"
        return table


@register_dataset
class FermiLATIGRB2015(_FermiLATDiffuseGamma2015):
    component = "igrb"

    metadata = DatasetMetadata(
        id="fermi_lat.igrb.2015",
        title="Fermi-LAT isotropic gamma-ray background spectrum",
        experiment="Fermi-LAT",
        messenger="gamma_ray",
        data_type="spectrum",
        description="Fermi-LAT isotropic gamma-ray background measured from 100 MeV to 820 GeV using Galactic foreground model A.",
        year=2015,
        quantity="phi",
        spectral_kind="differential_intensity",
        energy_unit="MeV",
        value_unit="MeV-1 cm-2 s-1 sr-1",
        paper=Reference(
            title="The spectrum of isotropic diffuse gamma-ray emission between 100 MeV and 820 GeV",
            authors=("Fermi-LAT Collaboration",),
            year=2015,
            doi=PAPER_DOI,
        ),
        dataset_reference=Reference(
            title="VizieR J/ApJ/799/86",
            authors=("Ackermann et al.",),
            year=2015,
            doi=VIZIER_DOI,
        ),
        source=DataSource(
            provenance=ProvenanceType.CURATED_DATABASE,
            storage=StorageMode.REMOTE,
            url=SOURCE_URL,
            sha256=SOURCE_SHA256,
        ),
        notes=(
            "Uses Galactic foreground model A, the baseline model in the publication.",
            "Published values are band-integrated intensities; MAHAM derives bin-averaged differential intensity by dividing by the bin width.",
            "Representative energy is the geometric mean of each energy bin.",
            "Primary uncertainties combine statistical and instrument-related systematic uncertainties.",
            "Galactic foreground-model uncertainties are retained separately.",
            "The final 580-820 GeV IGRB bin is represented as the published upper limit of 2.3e-12 cm-2 s-1 sr-1.",
        ),
        tags=("Fermi-LAT", "gamma ray", "IGRB", "diffuse", "spectrum"),
    )


@register_dataset
class FermiLATEGB2015(_FermiLATDiffuseGamma2015):
    component = "egb"

    metadata = DatasetMetadata(
        id="fermi_lat.egb.2015",
        title="Fermi-LAT total extragalactic gamma-ray background spectrum",
        experiment="Fermi-LAT",
        messenger="gamma_ray",
        data_type="spectrum",
        description="Fermi-LAT total extragalactic gamma-ray background, defined as IGRB plus resolved sources, using Galactic foreground model A.",
        year=2015,
        quantity="phi",
        spectral_kind="differential_intensity",
        energy_unit="MeV",
        value_unit="MeV-1 cm-2 s-1 sr-1",
        paper=Reference(
            title="The spectrum of isotropic diffuse gamma-ray emission between 100 MeV and 820 GeV",
            authors=("Fermi-LAT Collaboration",),
            year=2015,
            doi=PAPER_DOI,
        ),
        dataset_reference=Reference(
            title="VizieR J/ApJ/799/86",
            authors=("Ackermann et al.",),
            year=2015,
            doi=VIZIER_DOI,
        ),
        source=DataSource(
            provenance=ProvenanceType.CURATED_DATABASE,
            storage=StorageMode.REMOTE,
            url=SOURCE_URL,
            sha256=SOURCE_SHA256,
        ),
        notes=(
            "Uses Galactic foreground model A, the baseline model in the publication.",
            "Total EGB is the IGRB plus resolved sources.",
            "Published values are band-integrated intensities; MAHAM derives bin-averaged differential intensity by dividing by the bin width.",
            "Representative energy is the geometric mean of each energy bin.",
            "Primary uncertainties combine statistical and instrument-related systematic uncertainties.",
            "Galactic foreground-model uncertainties are retained separately.",
        ),
        tags=("Fermi-LAT", "gamma ray", "EGB", "extragalactic", "diffuse", "spectrum"),
    )
