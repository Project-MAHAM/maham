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

def test_numu_nubar_to_all_flavor_equal():
    value = 2.0 * u.GeV
    result = convert_flavor_convention(value, "numu_nubar", "all_flavor", assumption="equal")
    assert u.allclose(result, 6.0 * u.GeV)


def test_numu_nubar_to_per_flavor_equal():
    value = 2.0 * u.GeV
    result = convert_flavor_convention(value, "numu_nubar", "per_flavor", assumption="equal")
    assert u.allclose(result, value)


def test_numu_nubar_conversion_requires_assumption():
    with pytest.raises(ValueError):
        convert_flavor_convention(2.0 * u.GeV, "numu_nubar", "all_flavor")
