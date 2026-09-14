import astropy.units as u
import numpy as np

from maham.datasets import get_dataset


def test_km3net_230213a_flux_metadata():
    dataset = get_dataset("km3net.km3_230213a_flux.2025")
    assert dataset.metadata.experiment == "KM3NeT"
    assert dataset.metadata.quantity == "E2phi"
    assert dataset.metadata.flavor_convention == "per_flavor"
    assert dataset.metadata.confidence_level == 0.6827


def test_km3net_230213a_flux_native_values():
    table = get_dataset("km3net.km3_230213a_flux.2025").load()
    unit = u.GeV / (u.cm**2 * u.s * u.sr)

    assert len(table) == 1
    assert u.allclose(table["energy_min"][0], 7.24e7 * u.GeV)
    assert u.allclose(table["energy"][0], 2.18e8 * u.GeV)
    assert u.allclose(table["energy_max"][0], 2.57e9 * u.GeV)
    assert u.allclose(table["E2phi"][0], 5.80e-8 * unit)
    assert u.allclose(table["E2phi_lower"][0], 2.13e-8 * unit)
    assert u.allclose(table["E2phi_upper"][0], 1.59e-7 * unit)
    assert u.allclose(table["E2phi_2sigma_lower"][0], 2.70e-9 * unit)
    assert u.allclose(table["E2phi_2sigma_upper"][0], 2.98e-7 * unit)
    assert u.allclose(table["E2phi_3sigma_lower"][0], 1.62e-10 * unit)
    assert u.allclose(table["E2phi_3sigma_upper"][0], 4.82e-7 * unit)
    assert not table["is_upper_limit"][0]


def test_km3net_230213a_flux_quantity_conversion():
    dataset = get_dataset("km3net.km3_230213a_flux.2025")
    native = dataset.load_e2phi()
    phi = dataset.load_phi()

    expected = native["E2phi"][0] / native["energy"][0] ** 2
    expected_2sigma_lower = native["E2phi_2sigma_lower"][0] / native["energy"][0] ** 2

    assert u.allclose(phi["phi"][0], expected)
    assert u.allclose(phi["phi_2sigma_lower"][0], expected_2sigma_lower)


def test_km3net_230213a_flux_all_flavor_conversion():
    dataset = get_dataset("km3net.km3_230213a_flux.2025")
    per_flavor = dataset.load_e2phi()
    all_flavor = dataset.load_e2phi(flavor="all_flavor", flavor_assumption="equal")

    assert u.allclose(all_flavor["E2phi"][0], 3 * per_flavor["E2phi"][0])
    assert u.allclose(all_flavor["E2phi_lower"][0], 3 * per_flavor["E2phi_lower"][0])
    assert u.allclose(all_flavor["E2phi_2sigma_lower"][0], 3 * per_flavor["E2phi_2sigma_lower"][0])
    assert u.allclose(all_flavor["E2phi_3sigma_upper"][0], 3 * per_flavor["E2phi_3sigma_upper"][0])
    assert all_flavor.meta["flavor_convention"] == "all_flavor"
    assert all_flavor.meta["flavor_assumption"] == "equal"


def test_km3net_230213a_flux_not_upper_limit():
    table = get_dataset("km3net.km3_230213a_flux.2025").load()
    assert np.count_nonzero(table["is_upper_limit"]) == 0
