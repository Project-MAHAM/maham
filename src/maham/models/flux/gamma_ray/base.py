from abc import abstractmethod
import astropy.units as u
import numpy as np
import pandas as pd
from astropy.table import QTable
from maham.models.base import Model
from maham.physics.spectra.conversions import convert_differential_intensity, convert_spectral_quantity, normalize_spectral_quantity, spectral_quantity_info

class GammaRayFluxModel(Model):
    @abstractmethod
    def load_native(self) -> QTable:
        pass

    def load(self, quantity: str | None = None) -> QTable:
        table = self.load_native()
        native = self._native_quantity()
        self._validate_native_table(table, native)
        table.meta.update(model_id=self.id, native_quantity=native, quantity=native, spectral_kind=self.metadata.spectral_kind, solid_angle_convention=self.metadata.solid_angle_convention, provenance=self.metadata.source.provenance.value)
        return table if quantity is None else self._convert_quantity(table, quantity)

    def load_phi(self): return self.load("phi")
    def load_ephi(self): return self.load("Ephi")
    def load_e2phi(self): return self.load("E2phi")
    def load_e3phi(self): return self.load("E3phi")

    def support(self):
        table = self.load()
        return table["energy"][0], table["energy"][-1]

    def evaluate(self, energy: u.Quantity, quantity: str = "E2phi") -> u.Quantity:
        table = self.load(quantity)
        energy = u.Quantity(energy).to(table["energy"].unit)
        scalar = energy.isscalar
        values_in = np.atleast_1d(energy.value)
        values = np.full(values_in.shape, np.nan, dtype=float)
        x = table["energy"].to_value(table["energy"].unit)
        y = table[quantity].to_value(table[quantity].unit)
        mask = (values_in >= x[0]) & (values_in <= x[-1])
        values[mask] = 10.0 ** np.interp(np.log10(values_in[mask]), np.log10(x), np.log10(y))
        result = values * table[quantity].unit
        return result[0] if scalar else result

    def _native_quantity(self):
        if self.metadata.quantity is None:
            raise ValueError(f"Gamma-ray model '{self.id}' has no native quantity defined.")
        return normalize_spectral_quantity(self.metadata.quantity)

    def _convert_quantity(self, table, quantity):
        source = self._native_quantity()
        target = normalize_spectral_quantity(quantity)
        source_family, _ = spectral_quantity_info(source)
        target_family, _ = spectral_quantity_info(target)
        result = table.copy(copy_data=True)
        if target == source:
            result.meta["quantity"] = target
            return result
        if source_family != target_family and self.metadata.spectral_kind != "differential_intensity":
            raise ValueError(f"Gamma-ray model '{self.id}' does not permit conversion between '{source_family}' and '{target_family}' notation.")
        converter = convert_spectral_quantity if source_family == target_family else convert_differential_intensity
        for suffix in ("", "_lower", "_upper"):
            source_column = f"{source}{suffix}"
            if source_column in result.colnames:
                result[f"{target}{suffix}"] = converter(result["energy"], result[source_column], source, target)
                result.remove_column(source_column)
        result.meta["quantity"] = target
        return result

    def _validate_native_table(self, table, quantity):
        energy = table["energy"].to_value(table["energy"].unit)
        values = table[quantity].to_value(table[quantity].unit)
        if len(table) < 2 or not np.all(np.isfinite(energy)) or np.any(energy <= 0) or np.any(np.diff(energy) <= 0):
            raise ValueError(f"Energy values for '{self.id}' must be finite, positive, and strictly increasing.")
        if not np.all(np.isfinite(values)) or np.any(values <= 0):
            raise ValueError(f"Flux values for '{self.id}' must be finite and positive.")

class TabulatedGammaRayFluxModel(GammaRayFluxModel):
    energy_column = "Energy"
    value_column = "FluxE2"
    lower_column = None
    upper_column = None

    def load_native(self):
        frame = pd.read_csv(self.fetch(), comment="#")
        unit_e = u.Unit(self.metadata.energy_unit)
        unit_f = u.Unit(self.metadata.value_unit)
        q = self._native_quantity()
        table = QTable()
        table["energy"] = np.asarray(frame[self.energy_column], dtype=float) * unit_e
        table[q] = np.asarray(frame[self.value_column], dtype=float) * unit_f
        if self.lower_column:
            table[f"{q}_lower"] = np.asarray(frame[self.lower_column], dtype=float) * unit_f
        if self.upper_column:
            table[f"{q}_upper"] = np.asarray(frame[self.upper_column], dtype=float) * unit_f
        return table
