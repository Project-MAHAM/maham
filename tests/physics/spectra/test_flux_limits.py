import astropy.units as u
import numpy as np
import pytest

from maham.physics.spectra import centered_log_energy_bounds, differential_flux_limit


def test_centered_log_energy_bounds_one_decade():
    energy = np.array([1e8, 1e9]) * u.GeV
    lower, upper = centered_log_energy_bounds(energy, 1.0)
    np.testing.assert_allclose((lower / energy).value, 1.0 / np.sqrt(10.0))
    np.testing.assert_allclose((upper / energy).value, np.sqrt(10.0))


def test_differential_flux_limit_definition():
    result = differential_flux_limit(1 * u.cm**2, 1 * u.GeV, 2 * u.GeV, 2.44, 1 * u.s, 1 * u.sr)
    assert np.isclose(result.to_value(1 / (u.GeV * u.cm**2 * u.s * u.sr)), 2.44)


def test_differential_flux_limit_vectorized():
    result = differential_flux_limit(np.array([1.0, 2.0]) * u.cm**2, np.array([1.0, 2.0]) * u.GeV, np.array([2.0, 4.0]) * u.GeV, 2.44, 1 * u.s, 1 * u.sr)
    np.testing.assert_allclose(result.to_value(1 / (u.GeV * u.cm**2 * u.s * u.sr)), [2.44, 0.61])


def test_differential_flux_limit_rejects_invalid_bounds():
    with pytest.raises(ValueError, match="energy_max"):
        differential_flux_limit(1 * u.cm**2, 2 * u.GeV, 1 * u.GeV, 2.44, 1 * u.s, 1 * u.sr)
