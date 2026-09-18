import numpy as np

from maham.physics.spectra.limits import LOG10_ENERGY_WIDTH, rescale_bandwidth_factor_to_decade_width, rescale_differential_decade_width

from maham.statistics import feldman_cousins_upper_limit, poisson_zero_count_upper_limit


def _positive_float(value, name):
    try:
        value = float(value)
    except (TypeError, ValueError) as exc:
        raise ValueError(f"{name} must be a finite positive number.") from exc
    if not np.isfinite(value) or value <= 0:
        raise ValueError(f"{name} must be a finite positive number.")
    return value


def rescale_single_event_sensitivity(values, expected_signal_count):
    """Scale a single-event sensitivity to a target expected signal count."""
    return values * _positive_float(expected_signal_count, "expected_signal_count")


def single_event_sensitivity_to_upper_limit(values, confidence_level=0.90, method="feldman_cousins", n_observed=0, expected_background=0.0):
    """Convert a single-event sensitivity to a Poisson upper-limit normalization."""
    key = str(method).strip().lower().replace("-", "_").replace(" ", "_")
    if key in {"feldman_cousins", "fc"}:
        count = feldman_cousins_upper_limit(n_observed=n_observed, expected_background=expected_background, confidence_level=confidence_level)
    elif key in {"classical", "one_sided_poisson"}:
        if n_observed != 0 or not np.isclose(expected_background, 0.0):
            raise NotImplementedError("The classical MAHAM SES conversion currently supports n_observed=0 and expected_background=0 only.")
        count = poisson_zero_count_upper_limit(confidence_level)
    else:
        raise ValueError("method must be 'feldman_cousins' or 'classical'.")
    return rescale_single_event_sensitivity(values, count)


def convert_sensitivity_normalization_to_decade_width(table, target_width_decades=1.0):
    """Return a copy of a differential sensitivity in a common decade-width normalization."""
    result = table.copy(copy_data=True)
    quantity = result.meta.get("quantity")
    if not quantity or quantity not in result.colnames:
        raise ValueError("The table metadata quantity must name a column in the table.")

    convention = result.meta.get("sensitivity_normalization_convention")
    native_recorded = "native_sensitivity_normalization_convention" in result.meta
    if not native_recorded:
        result.meta["native_sensitivity_normalization_convention"] = convention

    if convention == LOG10_ENERGY_WIDTH:
        current_width = result.meta.get("log10_energy_width_decades")
        factor = rescale_differential_decade_width(1.0, current_width, target_width_decades)
        if not native_recorded:
            result.meta["native_log10_energy_width_decades"] = float(current_width)
    elif convention == "bandwidth_factor":
        bandwidth = result.meta.get("sensitivity_bandwidth_factor")
        factor = rescale_bandwidth_factor_to_decade_width(1.0, bandwidth, target_width_decades)
        if not native_recorded:
            result.meta["native_sensitivity_bandwidth_factor"] = float(bandwidth)
    else:
        raise ValueError(f"Unsupported sensitivity normalization convention: {convention!r}.")

    for column in (quantity, f"{quantity}_lower", f"{quantity}_upper"):
        if column in result.colnames:
            result[column] = result[column] * factor
    previous = float(result.meta.get("sensitivity_normalization_scale_factor", 1.0))
    result.meta["sensitivity_normalization_convention"] = LOG10_ENERGY_WIDTH
    result.meta["log10_energy_width_decades"] = float(target_width_decades)
    result.meta["sensitivity_normalization_scale_factor"] = previous * factor
    return result


def convert_single_event_sensitivity_to_confidence_level(table, confidence_level=0.90, method="feldman_cousins", n_observed=0, expected_background=0.0):
    """Convert a single-event sensitivity table to a confidence-level projected sensitivity."""
    if table.meta.get("sensitivity_type") != "single_event_sensitivity":
        raise ValueError("Only single-event sensitivity tables can be converted with this function.")
    result = table.copy(copy_data=True)
    quantity = result.meta.get("quantity")
    if not quantity or quantity not in result.colnames:
        raise ValueError("The table metadata quantity must name a column in the table.")
    factor = single_event_sensitivity_to_upper_limit(1.0, confidence_level=confidence_level, method=method, n_observed=n_observed, expected_background=expected_background)
    for column in (quantity, f"{quantity}_lower", f"{quantity}_upper"):
        if column in result.colnames:
            result[column] = result[column] * factor
    key = str(method).strip().lower().replace("-", "_").replace(" ", "_")
    result.meta["native_sensitivity_type"] = "single_event_sensitivity"
    result.meta["sensitivity_type"] = "projected_confidence_level_sensitivity"
    result.meta["confidence_level"] = float(confidence_level)
    result.meta["statistical_method"] = "feldman_cousins" if key in {"feldman_cousins", "fc"} else "classical_one_sided_poisson"
    result.meta["assumed_observed_events"] = int(n_observed)
    result.meta["assumed_background_events"] = float(expected_background)
    result.meta["expected_signal_count_scale_factor"] = float(factor)
    return result

