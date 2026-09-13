import astropy.units as u
import numpy as np
import pytest

from maham.spectra import convert_spectral_quantity


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
