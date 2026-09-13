import pytest
import astropy.units as u
import numpy as np
from astropy.table import Table

from maham.datasets import get_dataset, list_datasets


def test_glashow_registered():
    assert "icecube.glashow.flux.2021" in [metadata.id for metadata in list_datasets()]


def test_glashow_metadata():
    dataset = get_dataset("icecube.glashow.flux.2021")
    assert dataset.metadata.experiment == "IceCube"
    assert dataset.metadata.messenger == "neutrino"
    assert dataset.metadata.data_type == "spectrum"
    assert dataset.metadata.quantity == "E2phi"
    assert dataset.metadata.flavor_convention == "per_flavor"
    assert dataset.metadata.confidence_level == 0.683
    assert dataset.metadata.source.provenance.value == "official_release"


def test_glashow_standardization():
    dataset = get_dataset("icecube.glashow.flux.2021")
    raw = Table({"E_min": [4.0e6], "E_max": [9.0e6], "y": [2.0], "y_lower": [1.0], "y_upper": [3.0]})
    table = dataset.standardize(raw)
    assert np.isclose(table["energy"][0].to_value(u.GeV), 6.0e6)
    assert np.isclose(table["E2phi"][0].to_value(u.GeV / (u.cm**2 * u.s * u.sr)), 2.0e-8)
    assert np.isclose(table["E2phi_lower"][0].to_value(u.GeV / (u.cm**2 * u.s * u.sr)), 1.0e-8)
    assert np.isclose(table["E2phi_upper"][0].to_value(u.GeV / (u.cm**2 * u.s * u.sr)), 3.0e-8)


def test_glashow_quantity_views(monkeypatch):
    dataset = get_dataset("icecube.glashow.flux.2021")
    raw = Table({"E_min": [4.0e6], "E_max": [9.0e6], "y": [2.0], "y_lower": [1.0], "y_upper": [3.0]})
    monkeypatch.setattr(dataset, "load_raw", lambda cache=True, show_progress=True: raw)
    E2phi = dataset.load_e2phi()
    Ephi = dataset.load_ephi()
    phi = dataset.load_phi()
    assert E2phi.meta["quantity"] == "E2phi"
    assert Ephi.meta["quantity"] == "Ephi"
    assert phi.meta["quantity"] == "phi"
    assert "E2phi" in E2phi.colnames
    assert "Ephi" in Ephi.colnames
    assert "phi" in phi.colnames
    assert u.allclose(E2phi["E2phi"][0], 2e-8 * u.GeV / (u.cm**2 * u.s * u.sr))
    assert u.allclose(Ephi["Ephi"][0], (2e-8 / 6e6) / (u.cm**2 * u.s * u.sr))
    assert u.allclose(phi["phi"][0], (2e-8 / 6e6**2) / (u.GeV * u.cm**2 * u.s * u.sr))


def test_glashow_upper_limit_flag():
    dataset = get_dataset("icecube.glashow.flux.2021")
    raw = Table({"E_min": [4.0e6, 5.0e6], "E_max": [5.0e6, 6.0e6], "y": [0.0, 1.0], "y_lower": [0.0, 0.5], "y_upper": [2.0, 1.5]})
    table = dataset.standardize(raw)
    assert table["is_upper_limit"].tolist() == [True, False]


def test_glashow_all_flavor_view(monkeypatch):
    dataset = get_dataset("icecube.glashow.flux.2021")
    raw = Table({"E_min": [4.0e6], "E_max": [9.0e6], "y": [2.0], "y_lower": [1.0], "y_upper": [3.0]})
    monkeypatch.setattr(dataset, "load_raw", lambda cache=True, show_progress=True: raw)
    table = dataset.load_e2phi(flavor="all_flavor", flavor_assumption="equal")
    assert table.meta["native_flavor_convention"] == "per_flavor"
    assert table.meta["flavor_convention"] == "all_flavor"
    assert table.meta["flavor_assumption"] == "equal"
    assert u.allclose(table["E2phi"][0], 6e-8 * u.GeV / (u.cm**2 * u.s * u.sr))
    assert u.allclose(table["E2phi_lower"][0], 3e-8 * u.GeV / (u.cm**2 * u.s * u.sr))
    assert u.allclose(table["E2phi_upper"][0], 9e-8 * u.GeV / (u.cm**2 * u.s * u.sr))


def test_glashow_all_flavor_requires_assumption(monkeypatch):
    dataset = get_dataset("icecube.glashow.flux.2021")
    raw = Table({"E_min": [4.0e6], "E_max": [9.0e6], "y": [2.0], "y_lower": [1.0], "y_upper": [3.0]})
    monkeypatch.setattr(dataset, "load_raw", lambda cache=True, show_progress=True: raw)
    with pytest.raises(ValueError):
        dataset.load_e2phi(flavor="all_flavor")
