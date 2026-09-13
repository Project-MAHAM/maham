from abc import abstractmethod

from astropy.table import QTable, Table

from maham.datasets.base import Dataset
from maham.spectra.conversions import convert_spectral_quantity, normalize_spectral_quantity


class SpectrumDataset(Dataset):
    """Base class for published spectral datasets."""

    @abstractmethod
    def load_raw(self, cache: bool = True, show_progress: bool = True) -> Table:
        pass

    @abstractmethod
    def standardize(self, raw: Table) -> QTable:
        pass

    def load(self, quantity: str | None = None, cache: bool = True, show_progress: bool = True) -> QTable:
        raw = self.load_raw(cache=cache, show_progress=show_progress)
        table = self.standardize(raw)
        native_quantity = self._native_quantity()
        table.meta["native_quantity"] = native_quantity
        table.meta["quantity"] = native_quantity
        return table if quantity is None else self._convert_quantity(table, quantity)

    def load_phi(self, cache: bool = True, show_progress: bool = True) -> QTable:
        return self.load(quantity="phi", cache=cache, show_progress=show_progress)

    def load_ephi(self, cache: bool = True, show_progress: bool = True) -> QTable:
        return self.load(quantity="Ephi", cache=cache, show_progress=show_progress)

    def load_e2phi(self, cache: bool = True, show_progress: bool = True) -> QTable:
        return self.load(quantity="E2phi", cache=cache, show_progress=show_progress)

    def _native_quantity(self) -> str:
        if self.metadata.quantity is None:
            raise ValueError(f"Spectrum dataset '{self.id}' has no native quantity defined.")
        return normalize_spectral_quantity(self.metadata.quantity)

    def _convert_quantity(self, table: QTable, quantity: str) -> QTable:
        source = self._native_quantity()
        target = normalize_spectral_quantity(quantity)
        result = table.copy(copy_data=True)
        result.meta["native_quantity"] = source
        if target == source:
            result.meta["quantity"] = target
            return result
        if "energy" not in result.colnames:
            raise ValueError(f"Spectrum dataset '{self.id}' has no standardized 'energy' column.")
        for suffix in ("", "_lower", "_upper"):
            source_column = f"{source}{suffix}"
            if source_column not in result.colnames:
                continue
            target_column = f"{target}{suffix}"
            index = result.colnames.index(source_column)
            converted = convert_spectral_quantity(result["energy"], result[source_column], source, target)
            result.remove_column(source_column)
            result.add_column(converted, name=target_column, index=index)
        if target not in result.colnames:
            raise ValueError(f"Spectrum dataset '{self.id}' does not contain the expected native column '{source}'.")
        result.meta["quantity"] = target
        return result
