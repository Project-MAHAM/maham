from abc import ABC, abstractmethod

from astropy.units import Quantity

from maham.models.base import Model


class NeutrinoCrossSectionModel(Model, ABC):
    """Base class for neutrino-nucleon cross-section models."""

    @abstractmethod
    def cross_section(self, energy: Quantity, particle: str = "nu", current: str = "total", variation: str = "central") -> Quantity:
        """Return the neutrino-nucleon cross section."""
        raise NotImplementedError
