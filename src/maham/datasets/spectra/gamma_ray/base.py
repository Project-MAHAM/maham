from maham.datasets.spectra.base import SpectrumDataset


class GammaRaySpectrumDataset(SpectrumDataset):
    def load_phi(self, cache: bool = True, show_progress: bool = True):
        return self.load(quantity="phi", cache=cache, show_progress=show_progress)

    def load_ephi(self, cache: bool = True, show_progress: bool = True):
        return self.load(quantity="Ephi", cache=cache, show_progress=show_progress)

    def load_e2phi(self, cache: bool = True, show_progress: bool = True):
        return self.load(quantity="E2phi", cache=cache, show_progress=show_progress)

    def load_e3phi(self, cache: bool = True, show_progress: bool = True):
        return self.load(quantity="E3phi", cache=cache, show_progress=show_progress)
