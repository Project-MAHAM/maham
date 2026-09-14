from astropy.table import QTable

from maham.datasets.spectra.base import SpectrumDataset
from maham.spectra.flavor import convert_flavor_convention, normalize_flavor_convention


class NeutrinoSpectrumDataset(SpectrumDataset):
    """Base class for published neutrino spectral datasets."""

    def load(self, quantity: str | None = None, flavor: str | None = None, flavor_assumption: str | None = None, cache: bool = True, show_progress: bool = True) -> QTable:
        table = super().load(quantity=quantity, cache=cache, show_progress=show_progress)
        native_flavor = self._native_flavor_convention()
        table.meta["native_flavor_convention"] = native_flavor
        table.meta["flavor_convention"] = native_flavor
        return table if flavor is None else self._convert_flavor(table, flavor, flavor_assumption)

    def load_phi(self, flavor: str | None = None, flavor_assumption: str | None = None, cache: bool = True, show_progress: bool = True) -> QTable:
        return self.load("phi", flavor, flavor_assumption, cache, show_progress)

    def load_ephi(self, flavor: str | None = None, flavor_assumption: str | None = None, cache: bool = True, show_progress: bool = True) -> QTable:
        return self.load("Ephi", flavor, flavor_assumption, cache, show_progress)

    def load_e2phi(self, flavor: str | None = None, flavor_assumption: str | None = None, cache: bool = True, show_progress: bool = True) -> QTable:
        return self.load("E2phi", flavor, flavor_assumption, cache, show_progress)

    def load_e3phi(self, flavor: str | None = None, flavor_assumption: str | None = None, cache: bool = True, show_progress: bool = True) -> QTable:
        return self.load("E3phi", flavor, flavor_assumption, cache, show_progress)

    def load_j(self, flavor: str | None = None, flavor_assumption: str | None = None, cache: bool = True, show_progress: bool = True) -> QTable:
        return self.load("J", flavor, flavor_assumption, cache, show_progress)

    def load_ej(self, flavor: str | None = None, flavor_assumption: str | None = None, cache: bool = True, show_progress: bool = True) -> QTable:
        return self.load("EJ", flavor, flavor_assumption, cache, show_progress)

    def load_e2j(self, flavor: str | None = None, flavor_assumption: str | None = None, cache: bool = True, show_progress: bool = True) -> QTable:
        return self.load("E2J", flavor, flavor_assumption, cache, show_progress)

    def load_e3j(self, flavor: str | None = None, flavor_assumption: str | None = None, cache: bool = True, show_progress: bool = True) -> QTable:
        return self.load("E3J", flavor, flavor_assumption, cache, show_progress)

    def _native_flavor_convention(self) -> str:
        if self.metadata.flavor_convention is None:
            raise ValueError(f"Neutrino spectrum dataset '{self.id}' has no flavor convention defined.")
        return normalize_flavor_convention(self.metadata.flavor_convention)

    def _convert_flavor(self, table: QTable, flavor: str, flavor_assumption: str | None) -> QTable:
        source = table.meta.get("flavor_convention", self._native_flavor_convention())
        target = normalize_flavor_convention(flavor)
        result = table.copy(copy_data=True)
        result.meta["native_flavor_convention"] = self._native_flavor_convention()

        if target == source:
            result.meta["flavor_convention"] = target
            return result

        quantity = result.meta["quantity"]
        for suffix in ("", "_lower", "_upper", "_90_lower", "_90_upper", "_2sigma_lower", "_2sigma_upper", "_3sigma_lower", "_3sigma_upper", "_stat_err_lower", "_stat_err_upper", "_sys_err_lower", "_sys_err_upper",):
            column = f"{quantity}{suffix}"
            if column in result.colnames:
                result[column] = convert_flavor_convention(result[column], source, target, flavor_assumption)

        result.meta["flavor_convention"] = target
        result.meta["flavor_assumption"] = "equal"
        return result
