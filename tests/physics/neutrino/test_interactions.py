import astropy.units as u
import numpy as np
import pytest

from maham.physics.constants import PROTON_MASS
from maham.physics.neutrino.interactions import interaction_length


def test_interaction_length_matches_definition():
    sigma = 1e-33 * u.cm**2
    density = 0.917 * u.g / u.cm**3
    expected = PROTON_MASS / (sigma * density)
    result = interaction_length(sigma, density)
    assert result.unit.is_equivalent(u.cm)
    assert np.isclose(result.to_value(u.cm), expected.to_value(u.cm), rtol=1e-14)


def test_interaction_length_vectorized():
    sigma = np.array([1e-34, 1e-33, 1e-32]) * u.cm**2
    result = interaction_length(sigma, 0.917 * u.g / u.cm**3)
    assert result.shape == (3,)
    assert np.all(np.diff(result.to_value(u.km)) < 0)


def test_interaction_length_requires_positive_cross_section():
    with pytest.raises(ValueError, match="cross_section"):
        interaction_length(0 * u.cm**2, 0.917 * u.g / u.cm**3)
