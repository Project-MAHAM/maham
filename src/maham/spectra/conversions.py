import astropy.units as u
from astropy.units import Quantity


_QUANTITY_POWERS = {"phi": 0, "Ephi": 1, "E2phi": 2}


def normalize_spectral_quantity(quantity: str) -> str:
    """Return the canonical MAHAM name for a spectral quantity."""
    aliases = {"phi": "phi", "ephi": "Ephi", "e2phi": "E2phi"}
    try:
        return aliases[quantity.strip().lower()]
    except (AttributeError, KeyError) as exc:
        raise ValueError("Spectral quantity must be one of: 'phi', 'Ephi', or 'E2phi'.") from exc


def convert_spectral_quantity(energy: Quantity, values: Quantity, from_quantity: str, to_quantity: str) -> Quantity:
    """Convert between phi, Ephi, and E2phi."""
    energy = u.Quantity(energy)
    values = u.Quantity(values)
    if energy.unit == u.dimensionless_unscaled:
        raise u.UnitsError("energy must have physical units.")
    if values.unit == u.dimensionless_unscaled:
        raise u.UnitsError("spectral values must have physical units.")
    source = normalize_spectral_quantity(from_quantity)
    target = normalize_spectral_quantity(to_quantity)
    power = _QUANTITY_POWERS[target] - _QUANTITY_POWERS[source]
    return values * energy**power
