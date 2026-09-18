import numpy as np
import pytest

from maham.statistics import feldman_cousins_interval, feldman_cousins_upper_limit, poisson_zero_count_upper_limit


def test_zero_count_classical_90_percent():
    assert np.isclose(poisson_zero_count_upper_limit(0.90), -np.log(0.1), rtol=1e-14)


@pytest.mark.parametrize(
    ("n_observed", "lower", "upper"),
    [(0, 0.00, 2.44), (1, 0.11, 4.36), (2, 0.53, 5.91), (3, 1.10, 7.42), (4, 1.47, 8.60), (5, 1.84, 9.99)],
)
def test_feldman_cousins_matches_published_90_percent_table(n_observed, lower, upper):
    actual_lower, actual_upper = feldman_cousins_interval(n_observed, confidence_level=0.90)
    assert np.isclose(actual_lower, lower, atol=0.006)
    assert np.isclose(actual_upper, upper, atol=0.006)


def test_feldman_cousins_zero_count_95_percent():
    assert np.isclose(feldman_cousins_upper_limit(0, confidence_level=0.95), 3.09, atol=0.006)


def test_nonzero_background_is_not_silently_approximated():
    with pytest.raises(NotImplementedError, match="expected_background=0"):
        feldman_cousins_upper_limit(0, expected_background=0.1)
