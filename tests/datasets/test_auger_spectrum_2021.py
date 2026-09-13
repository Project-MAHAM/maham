import astropy.units as u
from astropy.table import Table

from maham.datasets import get_dataset, list_datasets


def test_auger_registered():
    assert "auger.combined_spectrum.2021" in [metadata.id for metadata in list_datasets()]


def test_auger_metadata():
    dataset = get_dataset("auger.combined_spectrum.2021")
    assert dataset.metadata.experiment == "Pierre Auger Observatory"
    assert dataset.metadata.messenger == "cosmic_ray"
    assert dataset.metadata.data_type == "spectrum"
    assert dataset.metadata.quantity == "J"
    assert dataset.metadata.source.sha256 == "cea1620b28252ab63a789102b9c6ad3bb48a80184e6c1a6f3d39441b91e6e218"
    assert dataset.metadata.spectral_kind == "differential_intensity"


def test_auger_standardization():
    dataset = get_dataset("auger.combined_spectrum.2021")
    raw = Table({"lgE_eV": [17.05], "lgE_halfwidth": [0.05], "J": [6.341e-14], "J_stat_err_lower": [0.015e-14], "J_stat_err_upper": [0.015e-14], "J_sys_err_lower": [1.9e-14], "J_sys_err_upper": [2.1e-14]})
    table = dataset.standardize(raw)
    J_unit = 1 / (u.km**2 * u.sr * u.yr * u.eV)
    assert u.allclose(table["energy"][0], 10**17.05 * u.eV)
    assert u.allclose(table["energy_min"][0], 1e17 * u.eV)
    assert u.allclose(table["energy_max"][0], 10**17.1 * u.eV)
    assert u.allclose(table["J"][0], 6.341e-14 * J_unit)
    assert u.allclose(table["J_stat_err_lower"][0], 0.015e-14 * J_unit)
    assert u.allclose(table["J_sys_err_upper"][0], 2.1e-14 * J_unit)


def test_auger_E3J_view(monkeypatch):
    dataset = get_dataset("auger.combined_spectrum.2021")
    raw = Table({"lgE_eV": [18.0], "lgE_halfwidth": [0.05], "J": [2e-18], "J_stat_err_lower": [1e-19], "J_stat_err_upper": [1e-19], "J_sys_err_lower": [2e-19], "J_sys_err_upper": [3e-19]})
    monkeypatch.setattr(dataset, "load_raw", lambda cache=True, show_progress=True: raw)
    table = dataset.load_e3j()
    assert table.meta["quantity"] == "E3J"
    assert "E3J" in table.colnames
    assert "E3J_stat_err_lower" in table.colnames
    assert "E3J_sys_err_upper" in table.colnames


def test_auger_phi_view(monkeypatch):
    dataset = get_dataset("auger.combined_spectrum.2021")
    raw = Table({"lgE_eV": [18.0], "lgE_halfwidth": [0.05], "J": [2e-18], "J_stat_err_lower": [1e-19], "J_stat_err_upper": [1e-19], "J_sys_err_lower": [2e-19], "J_sys_err_upper": [3e-19]})
    monkeypatch.setattr(dataset, "load_raw", lambda cache=True, show_progress=True: raw)
    table = dataset.load_e2phi()
    assert table.meta["quantity"] == "E2phi"
    assert "E2phi" in table.colnames
    assert "E2phi_stat_err_lower" in table.colnames
    assert "E2phi_sys_err_upper" in table.colnames
