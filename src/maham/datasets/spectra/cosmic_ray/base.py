from astropy.table import QTable

from maham.datasets.spectra.base import SpectrumDataset


class CosmicRaySpectrumDataset(SpectrumDataset):
    """Base class for published cosmic-ray spectral datasets."""

    def load_j(self, cache: bool = True, show_progress: bool = True) -> QTable:
        return self.load("J", cache=cache, show_progress=show_progress)

    def load_ej(self, cache: bool = True, show_progress: bool = True) -> QTable:
        return self.load("EJ", cache=cache, show_progress=show_progress)

    def load_e2j(self, cache: bool = True, show_progress: bool = True) -> QTable:
        return self.load("E2J", cache=cache, show_progress=show_progress)

    def load_e3j(self, cache: bool = True, show_progress: bool = True) -> QTable:
        return self.load("E3J", cache=cache, show_progress=show_progress)

    def load_phi(self, cache: bool = True, show_progress: bool = True) -> QTable:
        return self.load("phi", cache=cache, show_progress=show_progress)

    def load_ephi(self, cache: bool = True, show_progress: bool = True) -> QTable:
        return self.load("Ephi", cache=cache, show_progress=show_progress)

    def load_e2phi(self, cache: bool = True, show_progress: bool = True) -> QTable:
        return self.load("E2phi", cache=cache, show_progress=show_progress)

    def load_e3phi(self, cache: bool = True, show_progress: bool = True) -> QTable:
        return self.load("E3phi", cache=cache, show_progress=show_progress)
