import astropy.units as u
import numpy as np
from astropy.units import Quantity


def effective_area_from_effective_volume(effective_volume: Quantity, interaction_length: Quantity) -> Quantity:
    """Convert effective volume to effective area using Aeff = Veff / Lint."""
    volume = u.Quantity(effective_volume)
    length = u.Quantity(interaction_length)
    if volume.unit == u.dimensionless_unscaled or length.unit == u.dimensionless_unscaled:
        raise u.UnitsError("effective_volume and interaction_length must have physical units.")
    if np.any(~np.isfinite(volume.value)) or np.any(volume.value < 0):
        raise ValueError("effective_volume must contain finite non-negative values.")
    if np.any(~np.isfinite(length.value)) or np.any(length.value <= 0):
        raise ValueError("interaction_length must contain finite positive values.")
    return (volume / length).to(u.m**2)
