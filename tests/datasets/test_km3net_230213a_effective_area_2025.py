import astropy.units as u
import numpy as np

from maham.datasets import get_dataset


def test_km3net_230213a_effective_area_metadata():
    dataset = get_dataset("km3net.km3_230213a_effective_area.2025")
    assert dataset.metadata.experiment == "KM3NeT"
    assert dataset.metadata.data_type == "effective_area"
    assert dataset.metadata.quantity == "effective_area"
    assert dataset.metadata.source.sha256 == "5a321e65a708c1d746ab5605b37deea4dc84aa230a17c0b8967034f651ce8f9f"


def test_km3net_230213a_effective_area_values():
    table = get_dataset("km3net.km3_230213a_effective_area.2025").load()

    assert len(table) == 60
    assert u.allclose(table["energy"][0], 112201.845 * u.GeV)
    assert u.allclose(table["energy"][-1], 89125093800.0 * u.GeV)
    assert u.allclose(table["effective_area_total"][0], 0.0 * u.cm**2)
    assert u.allclose(table["effective_area_total"][6], 45.9646734 * u.cm**2)
    assert u.allclose(table["effective_area_total"][30], 2267036.58 * u.cm**2)
    assert u.allclose(table["effective_area_total"][-1], 35343948.1 * u.cm**2)


def test_km3net_230213a_effective_area_grid():
    table = get_dataset("km3net.km3_230213a_effective_area.2025").load()
    energy = table["energy"].to_value(u.GeV)
    area = table["effective_area_total"].to_value(u.cm**2)

    assert np.all(np.diff(energy) > 0)
    assert np.all(area >= 0)
    assert np.count_nonzero(area[:6]) == 0
    assert np.all(area[6:] > 0)


def test_km3net_230213a_effective_area_metadata_conventions():
    table = get_dataset("km3net.km3_230213a_effective_area.2025").load()

    assert table.meta["flavor_convention"] == "all_flavor"
    assert table.meta["particle_convention"] == "nu_plus_nubar"
    assert table.meta["sky_averaging"] == "all_sky"
