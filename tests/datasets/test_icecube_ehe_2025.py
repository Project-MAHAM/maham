import astropy.units as u
from astropy.table import Table

from maham.datasets import get_dataset, list_datasets


def test_ehe_datasets_registered():
    ids = [metadata.id for metadata in list_datasets()]
    assert "icecube.ehe.differential_limit.2025" in ids
    assert "icecube.ehe.effective_area.2025" in ids
    assert "icecube.ehe.sensitivity.2025" in ids

def test_ehe_limit_metadata():
    dataset = get_dataset("icecube.ehe.differential_limit.2025")
    assert dataset.metadata.data_type == "limit"
    assert dataset.metadata.quantity == "E2phi"
    assert dataset.metadata.confidence_level == 0.90
    assert dataset.metadata.flavor_convention == "all_flavor"
    assert dataset.metadata.source.archive_member_sha256 == "b4d107c3cdd73c994e8399f6d8672bfe8a96c875b55cd46b7abe1522e30dd859"


def test_ehe_limit_standardization():
    dataset = get_dataset("icecube.ehe.differential_limit.2025")
    raw = Table({"energy_GeV": [1e8], "limit_E2phi": [5.743e-9], "sensitivity_E2phi": [5.142e-9]})
    table = dataset.standardize(raw)
    unit = u.GeV / (u.cm**2 * u.s * u.sr)
    assert u.allclose(table["energy"][0], 1e8 * u.GeV)
    assert u.allclose(table["E2phi"][0], 5.743e-9 * unit)
    assert table["is_upper_limit"][0]


def test_ehe_effective_area_metadata():
    dataset = get_dataset("icecube.ehe.effective_area.2025")
    assert dataset.metadata.data_type == "effective_area"
    assert dataset.metadata.quantity == "effective_area"
    assert dataset.metadata.source.archive_member_sha256 == "614d4f235880c08dfbcde66b054c261d3ae8cf2bcc16cecbdf425d8e589af88d"


def test_ehe_effective_area_standardization():
    dataset = get_dataset("icecube.ehe.effective_area.2025")
    raw = Table({"energy_GeV": [1.06e6], "effective_area_total_m2": [1.27], "effective_area_nue_m2": [0.106], "effective_area_numu_m2": [1.04], "effective_area_nutau_m2": [0.131]})
    table = dataset.standardize(raw)
    assert u.allclose(table["energy"][0], 1.06e6 * u.GeV)
    assert u.allclose(table["effective_area_total"][0], 1.27 * u.m**2)
    assert u.allclose(table["effective_area_nue"][0], 0.106 * u.m**2)
    assert u.allclose(table["effective_area_numu"][0], 1.04 * u.m**2)
    assert u.allclose(table["effective_area_nutau"][0], 0.131 * u.m**2)


def test_ehe_sensitivity_metadata():
    dataset = get_dataset("icecube.ehe.sensitivity.2025")
    assert dataset.metadata.data_type == "sensitivity"
    assert dataset.metadata.quantity == "E2phi"
    assert dataset.metadata.confidence_level == 0.90
    assert dataset.metadata.flavor_convention == "all_flavor"
    assert dataset.metadata.source.archive_member_sha256 == "b4d107c3cdd73c994e8399f6d8672bfe8a96c875b55cd46b7abe1522e30dd859"


def test_ehe_sensitivity_standardization():
    dataset = get_dataset("icecube.ehe.sensitivity.2025")
    raw = Table({"energy_GeV": [1e8], "limit_E2phi": [5.743e-9], "sensitivity_E2phi": [5.142e-9]})
    table = dataset.standardize(raw)
    unit = u.GeV / (u.cm**2 * u.s * u.sr)
    assert u.allclose(table["energy"][0], 1e8 * u.GeV)
    assert u.allclose(table["E2phi"][0], 5.142e-9 * unit)
    assert "is_upper_limit" not in table.colnames
    assert table.meta["sensitivity_type"] == "null_observation_expected_limit"


def test_ehe_sensitivity_flavor_view(monkeypatch):
    dataset = get_dataset("icecube.ehe.sensitivity.2025")
    raw = Table({"energy_GeV": [1e8], "limit_E2phi": [6e-9], "sensitivity_E2phi": [3e-9]})
    monkeypatch.setattr(dataset, "load_raw", lambda cache=True, show_progress=True: raw)
    table = dataset.load_e2phi(flavor="per_flavor", flavor_assumption="equal")
    unit = u.GeV / (u.cm**2 * u.s * u.sr)
    assert table.meta["native_flavor_convention"] == "all_flavor"
    assert table.meta["flavor_convention"] == "per_flavor"
    assert table.meta["flavor_assumption"] == "equal"
    assert u.allclose(table["E2phi"][0], 1e-9 * unit)
