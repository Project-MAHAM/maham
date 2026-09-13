import astropy.units as u
import numpy as np
import pytest

from maham.spectra import apply_energy_weighting, convert_differential_intensity, convert_spectral_quantity


def test_phi_to_Ephi():
    energy = 1e6 * u.GeV
    phi = 2e-20 / (u.GeV * u.cm**2 * u.s * u.sr)
    result = convert_spectral_quantity(energy, phi, "phi", "Ephi")
    expected = 2e-14 / (u.cm**2 * u.s * u.sr)
    assert u.allclose(result, expected)


def test_phi_to_E2phi():
    energy = 1e6 * u.GeV
    phi = 2e-20 / (u.GeV * u.cm**2 * u.s * u.sr)
    result = convert_spectral_quantity(energy, phi, "phi", "E2phi")
    expected = 2e-8 * u.GeV / (u.cm**2 * u.s * u.sr)
    assert u.allclose(result, expected)


def test_E2phi_to_phi():
    energy = 1e6 * u.GeV
    E2phi = 2e-8 * u.GeV / (u.cm**2 * u.s * u.sr)
    result = convert_spectral_quantity(energy, E2phi, "E2phi", "phi")
    expected = 2e-20 / (u.GeV * u.cm**2 * u.s * u.sr)
    assert u.allclose(result, expected)


def test_round_trip():
    energy = np.array([1e3, 1e6, 1e9]) * u.GeV
    phi = np.array([1e-15, 2e-20, 3e-25]) / (u.GeV * u.cm**2 * u.s * u.sr)
    E2phi = convert_spectral_quantity(energy, phi, "phi", "E2phi")
    recovered = convert_spectral_quantity(energy, E2phi, "E2phi", "phi")
    assert u.allclose(recovered, phi)


def test_quantity_names_are_case_insensitive():
    energy = 1e6 * u.GeV
    phi = 2e-20 / (u.GeV * u.cm**2 * u.s * u.sr)
    lower = convert_spectral_quantity(energy, phi, "phi", "e2phi")
    upper = convert_spectral_quantity(energy, phi, "phi", "E2phi")
    assert u.allclose(lower, upper)


def test_energy_requires_units():
    phi = 1e-20 / (u.GeV * u.cm**2 * u.s * u.sr)
    with pytest.raises(u.UnitsError):
        convert_spectral_quantity(1e6, phi, "phi", "E2phi")


def test_J_to_E3J():
    energy = 1e18 * u.eV
    J = 2e-18 / (u.km**2 * u.sr * u.yr * u.eV)
    result = convert_spectral_quantity(energy, J, "J", "E3J")
    expected = 2e36 * u.eV**2 / (u.km**2 * u.sr * u.yr)
    assert u.allclose(result, expected)


def test_J_round_trip():
    energy = np.array([1e17, 1e18, 1e19]) * u.eV
    J = np.array([1e-14, 1e-18, 1e-22]) / (u.km**2 * u.sr * u.yr * u.eV)
    E3J = convert_spectral_quantity(energy, J, "J", "E3J")
    recovered = convert_spectral_quantity(energy, E3J, "E3J", "J")
    assert u.allclose(recovered, J)


def test_cross_family_conversion_rejected():
    energy = 1e18 * u.eV
    J = 1e-18 / (u.km**2 * u.sr * u.yr * u.eV)
    with pytest.raises(ValueError):
        convert_spectral_quantity(energy, J, "J", "E2phi")

def test_E3phi_support():
    energy = 1e6 * u.GeV
    phi = 2e-20 / (u.GeV * u.cm**2 * u.s * u.sr)
    result = convert_spectral_quantity(energy, phi, "phi", "E3phi")
    expected = phi * energy**3
    assert u.allclose(result, expected)


def test_J_to_phi_requires_explicit_intensity_conversion():
    energy = 1e18 * u.eV
    J = 2e-18 / (u.eV * u.km**2 * u.yr * u.sr)
    with pytest.raises(ValueError):
        convert_spectral_quantity(energy, J, "J", "phi")


def test_J_to_phi_differential_intensity():
    energy = 1e18 * u.eV
    J = 2e-18 / (u.eV * u.km**2 * u.yr * u.sr)
    phi = convert_differential_intensity(energy, J, "J", "phi")
    assert u.allclose(phi, J)


def test_E3J_to_E2phi():
    energy = 1e18 * u.eV
    J = 2e-18 / (u.eV * u.km**2 * u.yr * u.sr)
    E3J = convert_spectral_quantity(energy, J, "J", "E3J")
    E2phi = convert_differential_intensity(energy, E3J, "E3J", "E2phi")
    assert u.allclose(E2phi, J * energy**2)


def test_fractional_energy_weighting():
    energy = 1e18 * u.eV
    J = 2e-18 / (u.eV * u.km**2 * u.yr * u.sr)
    weighted = apply_energy_weighting(energy, J, 2.6)
    assert u.allclose(weighted, J * energy**2.6)
