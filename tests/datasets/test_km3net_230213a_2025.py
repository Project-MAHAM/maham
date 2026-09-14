import astropy.units as u
import numpy as np

from maham.datasets import get_dataset


def test_km3net_230213a_metadata():
    dataset = get_dataset("km3net.km3_230213a.2025")
    assert dataset.metadata.experiment == "KM3NeT"
    assert dataset.metadata.messenger == "neutrino"
    assert dataset.metadata.data_type == "event"
    assert dataset.metadata.source.sha256 == "f4671f968770dfde51933601e9db133170b0c18d2fd4602aca21607b7169eb92"


def test_km3net_230213a_raw():
    raw = get_dataset("km3net.km3_230213a.2025").load_raw()
    assert raw["event_name"] == "KM3-230213A"
    assert raw["instrument"] == "ARCA021"
    assert raw["time_utc"] == "2023-02-13T01:16:47"
    assert np.isclose(raw["energy_pev"], 120.0)
    assert np.isclose(raw["ra_deg"], 94.3)
    assert np.isclose(raw["dec_deg"], -7.8)


def test_km3net_230213a_standardized():
    table = get_dataset("km3net.km3_230213a.2025").load()
    assert len(table) == 1
    assert table["event_name"][0] == "KM3-230213A"
    assert table["instrument"][0] == "ARCA021"
    assert u.allclose(table["energy"][0], 120.0 * u.PeV)
    assert u.allclose(table["ra"][0], 94.3 * u.deg)
    assert u.allclose(table["dec"][0], -7.8 * u.deg)
    assert u.allclose(table["angular_error_50"][0], 1.2 * u.deg)
    assert u.allclose(table["angular_error_68"][0], 1.5 * u.deg)
    assert u.allclose(table["angular_error_90"][0], 2.2 * u.deg)
    assert u.allclose(table["angular_error_99"][0], 3.0 * u.deg)


def test_km3net_230213a_detector_location():
    table = get_dataset("km3net.km3_230213a.2025").load()
    assert u.allclose(table["detector_longitude"][0], 15.975552 * u.deg)
    assert u.allclose(table["detector_latitude"][0], 36.292201 * u.deg)
    assert u.allclose(table["detector_elevation"][0], -3450.0 * u.m)
