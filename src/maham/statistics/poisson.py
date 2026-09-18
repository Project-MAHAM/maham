import math

import numpy as np
from scipy.stats import poisson


def _confidence_level(value):
    try:
        value = float(value)
    except (TypeError, ValueError) as exc:
        raise ValueError("confidence_level must satisfy 0 < confidence_level < 1.") from exc
    if not np.isfinite(value) or not 0.0 < value < 1.0:
        raise ValueError("confidence_level must satisfy 0 < confidence_level < 1.")
    return value


def poisson_zero_count_upper_limit(confidence_level=0.90):
    """Return the conventional one-sided Poisson upper mean for zero observed events and zero background."""
    confidence_level = _confidence_level(confidence_level)
    return -math.log1p(-confidence_level)


def _feldman_cousins_accepts(n_observed, signal_mean, confidence_level):
    mean = float(signal_mean)
    if mean < 0 or not np.isfinite(mean):
        raise ValueError("signal_mean must be finite and non-negative.")
    n_max = max(int(n_observed), 0 if mean == 0 else int(poisson.ppf(1.0 - 1e-12, mean)))
    n = np.arange(n_max + 1)
    probability = poisson.pmf(n, mean)
    best_probability = poisson.pmf(n, n.astype(float))
    ratio = np.divide(probability, best_probability, out=np.zeros_like(probability), where=best_probability > 0)
    order = np.argsort(-ratio, kind="stable")
    cumulative = 0.0
    accepted = set()
    for index in order:
        accepted.add(int(n[index]))
        cumulative += probability[index]
        if cumulative >= confidence_level:
            return int(n_observed) in accepted
    return False


def feldman_cousins_interval(n_observed, expected_background=0.0, confidence_level=0.90, scan_step=0.01, boundary_tolerance=1e-8):
    """Return a Feldman-Cousins interval for a Poisson signal with zero expected background.

    The current implementation intentionally supports expected_background=0 only. Nonzero-background
    support should be added with the original Feldman-Cousins background-compensation prescription
    rather than approximated silently.
    """
    if not isinstance(n_observed, (int, np.integer)) or n_observed < 0:
        raise ValueError("n_observed must be a non-negative integer.")
    background = float(expected_background)
    if not np.isfinite(background) or background < 0:
        raise ValueError("expected_background must be finite and non-negative.")
    if not np.isclose(background, 0.0):
        raise NotImplementedError("MAHAM Feldman-Cousins intervals currently support expected_background=0 only.")
    confidence_level = _confidence_level(confidence_level)
    scan_step = float(scan_step)
    boundary_tolerance = float(boundary_tolerance)
    if scan_step <= 0 or boundary_tolerance <= 0:
        raise ValueError("scan_step and boundary_tolerance must be positive.")

    signal_max = max(10.0, n_observed + 10.0 * math.sqrt(n_observed + 1.0) + 10.0)
    while True:
        grid = np.arange(0.0, signal_max + scan_step, scan_step)
        accepted = np.array([_feldman_cousins_accepts(n_observed, mu, confidence_level) for mu in grid], dtype=bool)
        indices = np.flatnonzero(accepted)
        if len(indices) == 0:
            raise RuntimeError("Could not construct a Feldman-Cousins interval.")
        if indices[-1] < len(grid) - 1:
            break
        signal_max *= 2.0

    first, last = int(indices[0]), int(indices[-1])
    lower = 0.0
    if first > 0:
        lo, hi = grid[first - 1], grid[first]
        while hi - lo > boundary_tolerance:
            mid = 0.5 * (lo + hi)
            if _feldman_cousins_accepts(n_observed, mid, confidence_level):
                hi = mid
            else:
                lo = mid
        lower = hi

    lo, hi = grid[last], grid[last + 1]
    while hi - lo > boundary_tolerance:
        mid = 0.5 * (lo + hi)
        if _feldman_cousins_accepts(n_observed, mid, confidence_level):
            lo = mid
        else:
            hi = mid
    return lower, lo


def feldman_cousins_upper_limit(n_observed=0, expected_background=0.0, confidence_level=0.90, **kwargs):
    """Return the upper endpoint of a Feldman-Cousins Poisson confidence interval."""
    return feldman_cousins_interval(n_observed, expected_background, confidence_level, **kwargs)[1]
