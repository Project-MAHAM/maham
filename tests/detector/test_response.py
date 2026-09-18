import astropy.units as u
import numpy as np
import pytest

from maham.detector.response import effective_area_from_effective_volume


def test_effective_area_from_effective_volume():
    result = effective_area_from_effective_volume(1 * u.km**3, 2 * u.km)
    assert np.isclose(result.to_value(u.km**2), 0.5)


def test_effective_area_vectorized():
    volume = np.array([1.0, 2.0, 3.0]) * u.km**3
    result = effective_area_from_effective_volume(volume, 2 * u.km)
    np.testing.assert_allclose(result.to_value(u.km**2), [0.5, 1.0, 1.5])


def test_effective_area_rejects_nonpositive_interaction_length():
    with pytest.raises(ValueError, match="interaction_length"):
        effective_area_from_effective_volume(1 * u.km**3, 0 * u.km)
