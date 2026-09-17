import math

import numpy as np


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


def rescale_differential_limit_decade_width(values, native_width_decades, target_width_decades):
    """Rescale a differential limit between logarithmic energy widths measured in decades."""
    native = _positive_float(native_width_decades, "native_width_decades")
    target = _positive_float(target_width_decades, "target_width_decades")
    return values * native / target


def rescale_anita_bandwidth_to_decade_width(values, bandwidth_factor=4.0, target_width_decades=1.0):
    """Convert the historical ANITA bandwidth normalization to a log10-energy-width convention."""
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
        factor = current_width / target
    elif convention == ANITA_BANDWIDTH:
        bandwidth = _positive_float(result.meta.get("limit_bandwidth_factor"), "limit_bandwidth_factor")
        if not native_recorded:
            result.meta["native_limit_bandwidth_factor"] = bandwidth
        factor = bandwidth / (math.log(10.0) * target)
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
