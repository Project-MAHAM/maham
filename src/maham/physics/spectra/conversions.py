import astropy.units as u
from astropy.units import Quantity


_QUANTITY_INFO = {
    "phi": ("phi", 0),
    "Ephi": ("phi", 1),
    "E2phi": ("phi", 2),
    "E3phi": ("phi", 3),
    "J": ("J", 0),
    "EJ": ("J", 1),
    "E2J": ("J", 2),
    "E3J": ("J", 3),
}

_ALIASES = {name.lower(): name for name in _QUANTITY_INFO}


def normalize_spectral_quantity(quantity: str) -> str:
    """Return the canonical MAHAM name for a spectral quantity."""
    try:
        return _ALIASES[quantity.strip().lower()]
    except (AttributeError, KeyError) as exc:
        raise ValueError(f"Spectral quantity must be one of: {', '.join(_QUANTITY_INFO)}.") from exc


def spectral_quantity_info(quantity: str) -> tuple[str, int]:
    """Return the notation family and energy power of a spectral quantity."""
    return _QUANTITY_INFO[normalize_spectral_quantity(quantity)]


def convert_spectral_quantity(energy: Quantity, values: Quantity, from_quantity: str, to_quantity: str) -> Quantity:
    """Convert energy weighting within one spectral notation family."""
    energy = u.Quantity(energy)
    values = u.Quantity(values)
    if energy.unit == u.dimensionless_unscaled:
        raise u.UnitsError("energy must have physical units.")
    if values.unit == u.dimensionless_unscaled:
        raise u.UnitsError("spectral values must have physical units.")

    source_family, source_power = spectral_quantity_info(from_quantity)
    target_family, target_power = spectral_quantity_info(to_quantity)

    if source_family != target_family:
        raise ValueError(f"Cannot convert spectral notation '{source_family}' to '{target_family}' without an explicit differential-intensity conversion.")

    return values * energy ** (target_power - source_power)


def convert_differential_intensity(energy: Quantity, values: Quantity, from_quantity: str, to_quantity: str) -> Quantity:
    """Convert between J and phi representations of a differential intensity."""
    energy = u.Quantity(energy)
    values = u.Quantity(values)
    if energy.unit == u.dimensionless_unscaled:
        raise u.UnitsError("energy must have physical units.")
    if values.unit == u.dimensionless_unscaled:
        raise u.UnitsError("spectral values must have physical units.")

    source_family, source_power = spectral_quantity_info(from_quantity)
    target_family, target_power = spectral_quantity_info(to_quantity)

    if source_family not in {"J", "phi"} or target_family not in {"J", "phi"}:
        raise ValueError("Differential-intensity notation conversion supports only J and phi families.")

    return values * energy ** (target_power - source_power)
