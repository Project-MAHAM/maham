from abc import ABC, abstractmethod

import astropy.units as u
import numpy as np
import pandas as pd

from astropy.table import QTable
from astropy.units import Quantity

from maham.models.base import Model
from maham.physics.neutrino import convert_flavor_convention, normalize_flavor_convention
from maham.physics.spectra import convert_differential_intensity, convert_spectral_quantity, normalize_spectral_quantity, spectral_quantity_info


class NeutrinoFluxModel(Model, ABC):
    @abstractmethod
    def load_native(self, cache: bool = True, show_progress: bool = True) -> QTable:
        pass

    def load(self, quantity: str | None = None, flavor: str | None = None, flavor_assumption: str | None = None, cache: bool = True, show_progress: bool = True) -> QTable:
        table = self.load_native(cache=cache, show_progress=show_progress)
        native_quantity = self._native_quantity()
        native_flavor = self._native_flavor_convention()
        self._validate_native_table(table, native_quantity)

        table = table.copy(copy_data=True)
        table.meta["model_id"] = self.id
        table.meta["native_quantity"] = native_quantity
        table.meta["quantity"] = native_quantity
        table.meta["native_flavor_convention"] = native_flavor
        table.meta["flavor_convention"] = native_flavor
        table.meta["spectral_kind"] = self.metadata.spectral_kind
        table.meta["solid_angle_convention"] = self.metadata.solid_angle_convention

        target_quantity = native_quantity if quantity is None else normalize_spectral_quantity(quantity)
        if target_quantity != native_quantity:
            values = self._convert_quantity(table["energy"], table[native_quantity], native_quantity, target_quantity)
            table[target_quantity] = values
            table.remove_column(native_quantity)
            table.meta["quantity"] = target_quantity

        if flavor is not None:
            target_flavor = normalize_flavor_convention(flavor)
            source_flavor = table.meta["flavor_convention"]
            if target_flavor != source_flavor:
                table[target_quantity] = convert_flavor_convention(table[target_quantity], source_flavor, target_flavor, flavor_assumption)
                table.meta["flavor_convention"] = target_flavor
                table.meta["flavor_assumption"] = "equal"

        return table

    def load_phi(self, flavor: str | None = None, flavor_assumption: str | None = None, cache: bool = True, show_progress: bool = True) -> QTable:
        return self.load("phi", flavor, flavor_assumption, cache, show_progress)

    def load_ephi(self, flavor: str | None = None, flavor_assumption: str | None = None, cache: bool = True, show_progress: bool = True) -> QTable:
        return self.load("Ephi", flavor, flavor_assumption, cache, show_progress)

    def load_e2phi(self, flavor: str | None = None, flavor_assumption: str | None = None, cache: bool = True, show_progress: bool = True) -> QTable:
        return self.load("E2phi", flavor, flavor_assumption, cache, show_progress)

    def load_e3phi(self, flavor: str | None = None, flavor_assumption: str | None = None, cache: bool = True, show_progress: bool = True) -> QTable:
        return self.load("E3phi", flavor, flavor_assumption, cache, show_progress)

    def evaluate(self, energy: Quantity, quantity: str | None = None, flavor: str | None = None, flavor_assumption: str | None = None, cache: bool = True, show_progress: bool = True) -> Quantity:
        table = self.load(quantity=quantity, flavor=flavor, flavor_assumption=flavor_assumption, cache=cache, show_progress=show_progress)
        target_quantity = table.meta["quantity"]
        energy_unit = table["energy"].unit
        value_unit = table[target_quantity].unit
        x = np.log10(table["energy"].to_value(energy_unit))
        y = np.log10(table[target_quantity].to_value(value_unit))
        query = u.Quantity(energy).to(energy_unit)
        log_values = np.interp(np.log10(query.to_value(energy_unit)), x, y, left=np.nan, right=np.nan)
        return 10.0**log_values * value_unit

    def support(self, cache: bool = True, show_progress: bool = True) -> tuple[Quantity, Quantity]:
        table = self.load_native(cache=cache, show_progress=show_progress)
        native_quantity = self._native_quantity()
        self._validate_native_table(table, native_quantity)
        return table["energy"][0], table["energy"][-1]

    def _native_quantity(self) -> str:
        if self.metadata.quantity is None:
            raise ValueError(f"Neutrino flux model '{self.id}' has no native spectral quantity defined.")
        return normalize_spectral_quantity(self.metadata.quantity)

    def _native_flavor_convention(self) -> str:
        if self.metadata.flavor_convention is None:
            raise ValueError(f"Neutrino flux model '{self.id}' has no flavor convention defined.")
        return normalize_flavor_convention(self.metadata.flavor_convention)

    def _convert_quantity(self, energy: Quantity, values: Quantity, source: str, target: str) -> Quantity:
        source_family, _ = spectral_quantity_info(source)
        target_family, _ = spectral_quantity_info(target)
        if source_family == target_family:
            return convert_spectral_quantity(energy, values, source, target)
        if self.metadata.spectral_kind != "differential_intensity":
            raise ValueError(f"Model '{self.id}' cannot convert between spectral notation families because it is not a differential intensity.")
        return convert_differential_intensity(energy, values, source, target)

    def _validate_native_table(self, table: QTable, quantity: str) -> None:
        if "energy" not in table.colnames or quantity not in table.colnames:
            raise ValueError(f"Native table for '{self.id}' must contain 'energy' and '{quantity}' columns.")
        energy = table["energy"].to_value(table["energy"].unit)
        values = table[quantity].to_value(table[quantity].unit)
        if len(table) < 2:
            raise ValueError(f"Native table for '{self.id}' must contain at least two points.")
        if not np.all(np.isfinite(energy)) or np.any(energy <= 0) or np.any(np.diff(energy) <= 0):
            raise ValueError(f"Energy values for '{self.id}' must be finite, positive, and strictly increasing.")
        if not np.all(np.isfinite(values)) or np.any(values <= 0):
            raise ValueError(f"Flux values for '{self.id}' must be finite and positive.")


class TabulatedNeutrinoFluxModel(NeutrinoFluxModel):
    energy_column: str | None = None
    value_column: str | None = None
    values_are_log10: bool = False
    duplicate_energy_policy: str = "error"

    def load_native(self, cache: bool = True, show_progress: bool = True) -> QTable:
        if self.energy_column is None or self.value_column is None:
            raise ValueError(f"Tabulated model '{self.id}' must define energy_column and value_column.")
        if self.metadata.energy_unit is None or self.metadata.value_unit is None:
            raise ValueError(f"Tabulated model '{self.id}' must define energy_unit and value_unit.")

        path = self.fetch(cache=cache, show_progress=show_progress)
        if path.suffix.lower() == ".json":
            frame = pd.read_json(path)
        elif path.suffix.lower() == ".csv":
            frame = pd.read_csv(path)
        else:
            raise ValueError(f"Unsupported tabulated model format for '{self.id}': {path.suffix}")

        energy = frame[self.energy_column].to_numpy(dtype=float)
        values = frame[self.value_column].to_numpy(dtype=float)
        order = np.argsort(energy, kind="stable")
        energy = energy[order]
        values = values[order]
        energy, values = self._resolve_duplicate_energies(energy, values)
        if self.values_are_log10:
            values = 10.0**values

        quantity = self._native_quantity()
        table = QTable()
        table["energy"] = energy * u.Unit(self.metadata.energy_unit)
        table[quantity] = values * u.Unit(self.metadata.value_unit)
        return table

    def _resolve_duplicate_energies(self, energy: np.ndarray, values: np.ndarray) -> tuple[np.ndarray, np.ndarray]:
        if len(energy) < 2 or not np.any(np.diff(energy) == 0):
            return energy, values
        if self.duplicate_energy_policy == "error":
            raise ValueError(f"Tabulated model '{self.id}' contains duplicate energy values.")
        if self.duplicate_energy_policy != "mean_native":
            raise ValueError(f"Unsupported duplicate_energy_policy for '{self.id}': {self.duplicate_energy_policy}")
        unique_energy, inverse = np.unique(energy, return_inverse=True)
        counts = np.bincount(inverse)
        mean_values = np.bincount(inverse, weights=values) / counts
        return unique_energy, mean_values
