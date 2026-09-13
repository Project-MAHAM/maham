import astropy.units as u
from astropy.units import Quantity


def apply_energy_weighting(energy: Quantity, values: Quantity, power: float) -> Quantity:
    """Multiply a spectrum by an arbitrary power of energy."""
    energy = u.Quantity(energy)
    values = u.Quantity(values)
    if energy.unit == u.dimensionless_unscaled:
        raise u.UnitsError("energy must have physical units.")
    if values.unit == u.dimensionless_unscaled:
        raise u.UnitsError("spectral values must have physical units.")
    return values * energy**power
