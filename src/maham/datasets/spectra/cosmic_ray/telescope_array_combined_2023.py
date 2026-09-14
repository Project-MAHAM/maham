import csv

import astropy.units as u
import numpy as np
from astropy.table import QTable, Table

from maham._core.metadata import DataSource, DatasetMetadata, ProvenanceType, Reference, StorageMode
from maham.datasets.registry import register_dataset
from maham.datasets.spectra.cosmic_ray.base import CosmicRaySpectrumDataset


@register_dataset
class TelescopeArrayCombinedSpectrum2023(CosmicRaySpectrumDataset):
    metadata = DatasetMetadata(
        id="telescope_array.combined_spectrum.2023",
        title="Telescope Array combined TA SD + TAx4 SD cosmic-ray spectrum",
        experiment="Telescope Array",
        messenger="cosmic_ray",
        data_type="spectrum",
        description="Combined all-particle spectrum using 14 years of TA SD data and 3 years of TAx4 SD data, independently digitized by Project MAHAM from Figure 7 of the ICRC 2023 Telescope Array highlights.",
        year=2023,
        quantity="E3J",
        spectral_kind="differential_intensity",
        energy_unit="eV",
        value_unit="eV2 m-2 s-1 sr-1",
        paper=Reference(
            title="Highlights from the Telescope Array Experiment",
            authors=("Jihyun Kim for the Telescope Array Collaboration",),
            year=2023,
            doi="10.22323/1.444.0008",
        ),
        dataset_reference=Reference(
            title="Figure 7: combined TA SD and TAx4 SD energy spectrum",
            authors=("Telescope Array Collaboration",),
            year=2023,
            doi="10.22323/1.444.0008",
        ),
        source=DataSource(
            provenance=ProvenanceType.DIGITIZED,
            storage=StorageMode.BUNDLED,
            path="data/datasets/spectra/cosmic_ray/telescope_array_combined_2023_digitized.csv",
            sha256="ef53895480c1990699a15ae30fc44d1588c50eb4cc5713191a6468edab87a393",
        ),
        notes=(
            "Independent Project MAHAM digitization from Figure 7, right panel.",
            "The spectrum combines 14 years of TA SD data and 3 years of TAx4 SD data.",
            "The native plotted quantity is E3J.",
            "The digitized table contains 20 measurements and one upper limit.",
            "Vertical uncertainties are retained only where visually resolvable in the source raster.",
            "NaN uncertainty values mean unresolved in the source figure, not zero uncertainty.",
            "The final point is represented as an upper limit.",
            "This is not an official Telescope Array machine-readable data release.",
        ),
        tags=("Telescope Array", "TA", "TAx4", "cosmic rays", "spectrum", "digitized", "ICRC 2023"),
    )

    def load_raw(self, cache: bool = True, show_progress: bool = True) -> Table:
        path = self.fetch(cache=cache, show_progress=show_progress)
        with path.open(newline="") as f:
            rows = list(csv.DictReader(line for line in f if not line.startswith("#")))

        numeric_columns = (
            "log10_energy_eV",
            "energy_eV",
            "log10_energy_err_lower",
            "log10_energy_err_upper",
            "scaled_E3J",
            "scaled_E3J_err_lower",
            "scaled_E3J_err_upper",
            "E3J_eV2_m-2_s-1_sr-1",
            "E3J_err_lower_eV2_m-2_s-1_sr-1",
            "E3J_err_upper_eV2_m-2_s-1_sr-1",
        )

        table = Table()
        for column in numeric_columns:
            table[column] = np.array([float(row[column]) if row[column].strip() else np.nan for row in rows], dtype=float)
        table["is_upper_limit"] = np.array([row["is_upper_limit"].strip().lower() == "true" for row in rows], dtype=bool)
        return table

    def standardize(self, raw: Table) -> QTable:
        log_energy = np.asarray(raw["log10_energy_eV"], dtype=float)
        log_err_lower = np.asarray(raw["log10_energy_err_lower"], dtype=float)
        log_err_upper = np.asarray(raw["log10_energy_err_upper"], dtype=float)
        values = np.asarray(raw["E3J_eV2_m-2_s-1_sr-1"], dtype=float)
        err_lower = np.asarray(raw["E3J_err_lower_eV2_m-2_s-1_sr-1"], dtype=float)
        err_upper = np.asarray(raw["E3J_err_upper_eV2_m-2_s-1_sr-1"], dtype=float)
        unit = u.eV**2 / (u.m**2 * u.s * u.sr)

        table = QTable()
        table["energy_min"] = 10 ** (log_energy - log_err_lower) * u.eV
        table["energy_max"] = 10 ** (log_energy + log_err_upper) * u.eV
        table["energy"] = np.asarray(raw["energy_eV"], dtype=float) * u.eV
        table["E3J"] = values * unit
        table["E3J_lower"] = np.where(np.isfinite(err_lower), values - err_lower, np.nan) * unit
        table["E3J_upper"] = np.where(np.isfinite(err_upper), values + err_upper, np.nan) * unit
        table["is_upper_limit"] = np.asarray(raw["is_upper_limit"], dtype=bool)
        table["has_resolved_vertical_error"] = np.isfinite(err_lower) & np.isfinite(err_upper)
        table.meta["dataset_id"] = self.metadata.id
        table.meta["quantity"] = self.metadata.quantity
        table.meta["spectrum_type"] = "all_particle"
        table.meta["provenance"] = self.metadata.source.provenance.value
        table.meta["source_figure"] = "Figure 7, right panel"
        return table
