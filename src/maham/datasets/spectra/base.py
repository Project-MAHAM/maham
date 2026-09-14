from abc import abstractmethod
from pathlib import Path

from astropy.table import QTable, Table

from maham.datasets.base import Dataset
from maham.physics.spectra import convert_differential_intensity, convert_spectral_quantity, normalize_spectral_quantity, spectral_quantity_info


class SpectrumDataset(Dataset):
    """Base class for published spectral datasets."""

    @abstractmethod
    def load_raw(self, cache: bool = True, show_progress: bool = True) -> Table:
        pass

    @abstractmethod
    def standardize(self, raw: Table) -> QTable:
        pass

    def load(self, quantity: str | None = None, cache: bool = True, show_progress: bool = True, path: str | Path | None = None) -> QTable:
        raw = self.load_raw(cache=cache, show_progress=show_progress) if path is None else self.load_raw(path=path, cache=cache, show_progress=show_progress)
        table = self.standardize(raw)
        native_quantity = self._native_quantity()
        table.meta["native_quantity"] = native_quantity
        table.meta["quantity"] = native_quantity
        return table if quantity is None else self._convert_quantity(table, quantity)

    def _native_quantity(self) -> str:
        if self.metadata.quantity is None:
            raise ValueError(f"Spectrum dataset '{self.id}' has no native quantity defined.")
        return normalize_spectral_quantity(self.metadata.quantity)

    def _convert_quantity(self, table: QTable, quantity: str) -> QTable:
        source = self._native_quantity()
        target = normalize_spectral_quantity(quantity)
        source_family, _ = spectral_quantity_info(source)
        target_family, _ = spectral_quantity_info(target)
        result = table.copy(copy_data=True)
        result.meta["native_quantity"] = source

        if target == source:
            result.meta["quantity"] = target
            return result

        if "energy" not in result.colnames:
            raise ValueError(f"Spectrum dataset '{self.id}' has no standardized 'energy' column.")

        if source_family == target_family:
            converter = convert_spectral_quantity
        elif self.metadata.spectral_kind == "differential_intensity":
            converter = convert_differential_intensity
        else:
            raise ValueError(f"Spectrum dataset '{self.id}' does not permit conversion between '{source_family}' and '{target_family}' notation.")

        suffixes = ("", "_lower", "_upper", "_90_lower", "_90_upper", "_2sigma_lower", "_2sigma_upper", "_3sigma_lower", "_3sigma_upper", "_stat_err_lower", "_stat_err_upper", "_sys_err_lower", "_sys_err_upper", "_foreground_err_lower", "_foreground_err_upper")

        for suffix in suffixes:
            source_column = f"{source}{suffix}"
            if source_column not in result.colnames:
                continue
            target_column = f"{target}{suffix}"
            index = result.colnames.index(source_column)
            converted = converter(result["energy"], result[source_column], source, target)
            result.remove_column(source_column)
            result.add_column(converted, name=target_column, index=index)

        if target not in result.colnames:
            raise ValueError(f"Spectrum dataset '{self.id}' does not contain the expected native column '{source}'.")

        result.meta["quantity"] = target
        return result
