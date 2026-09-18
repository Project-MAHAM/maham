import astropy.units as u
import numpy as np
from astropy.units import Quantity

from maham.physics.constants import PROTON_MASS


def interaction_length(cross_section: Quantity, density: Quantity, target_mass: Quantity = PROTON_MASS) -> Quantity:
    """Return the interaction length for a cross section and target mass density."""
    sigma = u.Quantity(cross_section)
    rho = u.Quantity(density)
    mass = u.Quantity(target_mass)
    if sigma.unit == u.dimensionless_unscaled or rho.unit == u.dimensionless_unscaled or mass.unit == u.dimensionless_unscaled:
        raise u.UnitsError("cross_section, density, and target_mass must have physical units.")

    sigma = sigma.to(u.cm**2)
    rho = rho.to(u.g / u.cm**3)
    mass = mass.to(u.g)
    if np.any(~np.isfinite(sigma.value)) or np.any(sigma.value <= 0):
        raise ValueError("cross_section must contain finite positive values.")
    if np.any(~np.isfinite(rho.value)) or np.any(rho.value <= 0):
        raise ValueError("density must contain finite positive values.")
    if np.any(~np.isfinite(mass.value)) or np.any(mass.value <= 0):
        raise ValueError("target_mass must contain finite positive values.")
    return (mass / (sigma * rho)).to(u.cm)
