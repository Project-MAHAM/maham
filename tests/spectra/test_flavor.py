import astropy.units as u
import pytest

from maham.spectra import convert_flavor_convention


def test_per_flavor_to_all_flavor():
    value = 2e-8 * u.GeV / (u.cm**2 * u.s * u.sr)
    result = convert_flavor_convention(value, "per_flavor", "all_flavor", assumption="equal")
    assert u.allclose(result, 6e-8 * u.GeV / (u.cm**2 * u.s * u.sr))


def test_all_flavor_to_per_flavor():
    value = 6e-8 * u.GeV / (u.cm**2 * u.s * u.sr)
    result = convert_flavor_convention(value, "all_flavor", "per_flavor", assumption="equal")
    assert u.allclose(result, 2e-8 * u.GeV / (u.cm**2 * u.s * u.sr))


def test_flavor_conversion_requires_assumption():
    value = 2e-8 * u.GeV / (u.cm**2 * u.s * u.sr)
    with pytest.raises(ValueError):
        convert_flavor_convention(value, "per_flavor", "all_flavor")


def test_same_flavor_requires_no_assumption():
    value = 2e-8 * u.GeV / (u.cm**2 * u.s * u.sr)
    assert u.allclose(convert_flavor_convention(value, "per_flavor", "per_flavor"), value)
