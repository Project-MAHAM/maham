import math

import astropy.units as u
import numpy as np
from astropy.units import Quantity


LOG10_ENERGY_WIDTH = "log10_energy_width"
ANITA_BANDWIDTH = "anita_bandwidth"


def _positive_float(value, name):
    try:
        value = float(value)
    except (TypeError, ValueError) as exc:
        raise ValueError(f"{name} must be a finite positive number.") from exc
    if not np.isfinite(value) or value <= 0:
        raise ValueError(f"{name} must be a finite positive number.")
    return value


def rescale_differential_decade_width(values, native_width_decades, target_width_decades):
    """Rescale a differential quantity between logarithmic energy widths measured in decades."""
    native = _positive_float(native_width_decades, "native_width_decades")
    target = _positive_float(target_width_decades, "target_width_decades")
    return values * native / target


def rescale_bandwidth_factor_to_decade_width(values, bandwidth_factor, target_width_decades=1.0):
    """Convert a Delta-style bandwidth-factor normalization to a log10-energy-width convention."""
    bandwidth = _positive_float(bandwidth_factor, "bandwidth_factor")
    target = _positive_float(target_width_decades, "target_width_decades")
    return values * bandwidth / (math.log(10.0) * target)


def convert_limit_normalization_to_decade_width(table, target_width_decades=1.0):
    """Return a copy of a differential upper-limit table in a common decade-width normalization."""
    target = _positive_float(target_width_decades, "target_width_decades")
    result = table.copy(copy_data=True)
    if result.meta.get("limit_type") != "differential_upper_limit":
        raise ValueError("Only differential upper-limit tables can be decade-width normalized.")

    quantity = result.meta.get("quantity")
    if not quantity or quantity not in result.colnames:
        raise ValueError("The table metadata quantity must name a column in the table.")

    convention = result.meta.get("limit_normalization_convention")
    native_recorded = "native_limit_normalization_convention" in result.meta
    if not native_recorded:
        result.meta["native_limit_normalization_convention"] = convention

    if convention == LOG10_ENERGY_WIDTH:
        current_width = _positive_float(result.meta.get("log10_energy_width_decades"), "log10_energy_width_decades")
        if not native_recorded:
            result.meta["native_log10_energy_width_decades"] = current_width
        factor = rescale_differential_decade_width(1.0, current_width, target)
    elif convention == ANITA_BANDWIDTH:
        bandwidth = _positive_float(result.meta.get("limit_bandwidth_factor"), "limit_bandwidth_factor")
        if not native_recorded:
            result.meta["native_limit_bandwidth_factor"] = bandwidth
        factor = rescale_bandwidth_factor_to_decade_width(1.0, bandwidth, target)
    else:
        raise ValueError(f"Unsupported differential-limit normalization convention: {convention!r}.")

    for column in (quantity, f"{quantity}_lower", f"{quantity}_upper"):
        if column in result.colnames:
            result[column] = result[column] * factor

    previous_factor = _positive_float(result.meta.get("limit_normalization_scale_factor", 1.0), "limit_normalization_scale_factor")
    cumulative_factor = previous_factor * factor
    result.meta["limit_normalization_convention"] = LOG10_ENERGY_WIDTH
    result.meta["log10_energy_width_decades"] = target
    result.meta["limit_normalization_scale_factor"] = cumulative_factor
    result.meta["limit_normalization_rescaled"] = not np.isclose(cumulative_factor, 1.0)
    return result



def centered_log_energy_bounds(energy: Quantity, width_decades: float) -> tuple[Quantity, Quantity]:
    """Return logarithmically symmetric lower and upper energy bounds around bin centers."""
    energy = u.Quantity(energy)
    if energy.unit == u.dimensionless_unscaled:
        raise u.UnitsError("energy must have physical units.")
    values = np.asarray(energy.value, dtype=float)
    if np.any(~np.isfinite(values)) or np.any(values <= 0):
        raise ValueError("energy must contain finite positive values.")
    width = _positive_float(width_decades, "width_decades")
    factor = 10.0 ** (0.5 * width)
    return energy / factor, energy * factor


def differential_flux_limit(effective_area: Quantity, energy_min: Quantity, energy_max: Quantity, upper_count: float, livetime: Quantity, solid_angle: Quantity = 4.0 * math.pi * u.sr) -> Quantity:
    """Return a differential flux limit from effective area, exposure, and energy-bin bounds."""
    area, e_min, e_max = u.Quantity(effective_area), u.Quantity(energy_min), u.Quantity(energy_max)
    time, omega = u.Quantity(livetime), u.Quantity(solid_angle)
    if area.unit == u.dimensionless_unscaled or e_min.unit == u.dimensionless_unscaled or e_max.unit == u.dimensionless_unscaled or time.unit == u.dimensionless_unscaled or omega.unit == u.dimensionless_unscaled:
        raise u.UnitsError("effective_area, energy bounds, livetime, and solid_angle must have physical units.")
    area, e_min, e_max, time, omega = area.to(u.cm**2), e_min.to(u.GeV), e_max.to(u.GeV), time.to(u.s), omega.to(u.sr)
    count = _positive_float(upper_count, "upper_count")
    width = e_max - e_min
    if np.any(~np.isfinite(area.value)) or np.any(area.value <= 0):
        raise ValueError("effective_area must contain finite positive values.")
    if np.any(~np.isfinite(width.value)) or np.any(width.value <= 0):
        raise ValueError("energy_max must be greater than energy_min.")
    if np.any(~np.isfinite(time.value)) or np.any(time.value <= 0):
        raise ValueError("livetime must contain finite positive values.")
    if np.any(~np.isfinite(omega.value)) or np.any(omega.value <= 0):
        raise ValueError("solid_angle must contain finite positive values.")
    return (count / (area * time * omega * width)).to(1 / (u.GeV * u.cm**2 * u.s * u.sr))
