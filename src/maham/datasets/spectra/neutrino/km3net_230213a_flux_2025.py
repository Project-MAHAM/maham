import json
import re

import astropy.units as u
from astropy.table import QTable, Table

from maham._core.metadata import DataSource, DatasetMetadata, ProvenanceType, Reference, StorageMode
from maham.datasets.registry import register_dataset
from maham.datasets.spectra.neutrino.base import NeutrinoSpectrumDataset


SOURCE_URL = "https://raw.githubusercontent.com/KM3NeT/KM3-230213A-data/main/notebooks/Astrophysical%20flux%20comparisons.ipynb"
SOURCE_SHA256 = "37b88c0c7d78f08779cde21172d1d8011804a801c979b7f14b89ef0da7fd46ab"


@register_dataset
class KM3NeT230213AFlux2025(NeutrinoSpectrumDataset):
    metadata = DatasetMetadata(
        id="km3net.km3_230213a_flux.2025",
        title="KM3NeT KM3-230213A inferred astrophysical neutrino flux",
        experiment="KM3NeT",
        messenger="neutrino",
        data_type="spectrum",
        source=DataSource(
            provenance=ProvenanceType.OFFICIAL_REPOSITORY,
            storage=StorageMode.REMOTE,
            url=SOURCE_URL,
            sha256=SOURCE_SHA256,
        ),
        description="Per-flavor E2phi inferred from the single KM3-230213A event over its central 90% neutrino-energy range.",
        year=2025,
        paper=Reference(
            title="Observation of an ultra-high-energy cosmic neutrino with KM3NeT",
            authors=("KM3NeT Collaboration",),
            year=2025,
            doi="10.1038/s41586-024-08543-1",
        ),
        dataset_reference=Reference(
            title="Data for the KM3-230213A high energy event observation",
            authors=("KM3NeT Collaboration",),
            year=2025,
            doi="10.5281/zenodo.14860165",
        ),
        confidence_level=0.6827,
        quantity="E2phi",
        spectral_kind="differential_intensity",
        energy_unit="GeV",
        value_unit="GeV cm-2 s-1 sr-1",
        flavor_convention="per_flavor",
        solid_angle_convention="per_sr",
        notes=(
            "The flux assumes an E^-2 incident neutrino spectrum.",
            "The horizontal range is the central 90% inferred neutrino-energy interval for KM3-230213A.",
            "The representative energy is the median of the inferred neutrino-energy distribution.",
            "The central interval stored as E2phi_lower and E2phi_upper is the 1-sigma Feldman-Cousins interval.",
            "Additional 2-sigma and 3-sigma Feldman-Cousins intervals are preserved explicitly.",
            "The published flux is per flavor under equal flavor composition at Earth.",
            "The official calculation uses 335 days of ARCA livetime.",
        ),
        tags=("KM3NeT", "KM3-230213A", "astrophysical neutrinos", "flux", "UHE neutrino"),
    )

    def load_raw(self, cache: bool = True, show_progress: bool = True) -> Table:
        path = self.fetch(cache=cache, show_progress=show_progress)
        with open(path, encoding="utf-8") as f:
            notebook = json.load(f)

        source = "\n".join("".join(cell.get("source", [])) for cell in notebook["cells"])
        output = "\n".join(
            "".join(item.get("text", [])) for cell in notebook["cells"] for item in cell.get("outputs", [])
        )

        energy_match = re.search(
            r"energy5_evt,\s*energy50_evt,\s*energy95_evt\s*=\s*([0-9.eE+-]+),\s*([0-9.eE+-]+),\s*([0-9.eE+-]+)",
            source,
        )
        flux_match = re.search(r"Phi\(1 GeV, evt range\)\s*=\s*([0-9.eE+-]+)", output)
        sigma1_match = re.search(r"1 sigma interval\s*=\s*([0-9.eE+-]+)\s*--\s*([0-9.eE+-]+)", output)
        sigma2_match = re.search(r"2 sigma interval\s*=\s*([0-9.eE+-]+)\s*--\s*([0-9.eE+-]+)", output)
        sigma3_match = re.search(r"3 sigma interval\s*=\s*([0-9.eE+-]+)\s*--\s*([0-9.eE+-]+)", output)

        if not all((energy_match, flux_match, sigma1_match, sigma2_match, sigma3_match)):
            raise RuntimeError("Could not locate the KM3-230213A flux result in the official notebook.")

        return Table(
            {
                "energy_min": [float(energy_match.group(1))],
                "energy": [float(energy_match.group(2))],
                "energy_max": [float(energy_match.group(3))],
                "E2phi": [float(flux_match.group(1))],
                "E2phi_lower": [float(sigma1_match.group(1))],
                "E2phi_upper": [float(sigma1_match.group(2))],
                "E2phi_2sigma_lower": [float(sigma2_match.group(1))],
                "E2phi_2sigma_upper": [float(sigma2_match.group(2))],
                "E2phi_3sigma_lower": [float(sigma3_match.group(1))],
                "E2phi_3sigma_upper": [float(sigma3_match.group(2))],
            }
        )

    def standardize(self, raw: Table) -> QTable:
        energy_unit = u.GeV
        flux_unit = u.GeV / (u.cm**2 * u.s * u.sr)

        table = QTable()
        table["energy_min"] = raw["energy_min"] * energy_unit
        table["energy"] = raw["energy"] * energy_unit
        table["energy_max"] = raw["energy_max"] * energy_unit
        for column in ("E2phi", "E2phi_lower", "E2phi_upper", "E2phi_2sigma_lower", "E2phi_2sigma_upper", "E2phi_3sigma_lower", "E2phi_3sigma_upper"):
            table[column] = raw[column] * flux_unit
        table["is_upper_limit"] = [False]

        table.meta["dataset_id"] = self.metadata.id
        table.meta["quantity"] = self.metadata.quantity
        table.meta["flavor_convention"] = self.metadata.flavor_convention
        table.meta["solid_angle_convention"] = self.metadata.solid_angle_convention
        table.meta["confidence_level"] = self.metadata.confidence_level
        table.meta["energy_definition"] = "median_of_inferred_neutrino_energy_distribution"
        table.meta["energy_interval"] = "central_90_percent"
        table.meta["interval_method"] = "Feldman-Cousins"
        table.meta["spectral_assumption"] = "E^-2"
        table.meta["provenance"] = self.metadata.source.provenance.value
        return table
