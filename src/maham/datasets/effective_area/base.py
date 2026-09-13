from abc import abstractmethod

from astropy.table import QTable, Table

from maham.datasets.base import Dataset


class EffectiveAreaDataset(Dataset):
    """Base class for published detector effective-area datasets."""

    @abstractmethod
    def load_raw(self, cache: bool = True, show_progress: bool = True) -> Table:
        pass

    @abstractmethod
    def standardize(self, raw: Table) -> QTable:
        pass

    def load(self, cache: bool = True, show_progress: bool = True) -> QTable:
        return self.standardize(self.load_raw(cache=cache, show_progress=show_progress))
