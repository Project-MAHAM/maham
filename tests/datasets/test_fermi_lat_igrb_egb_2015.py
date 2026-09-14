import astropy.units as u
import numpy as np

from maham.datasets import get_dataset, list_datasets


PHI_UNIT = 1 / (u.MeV * u.cm**2 * u.s * u.sr)


def test_fermi_lat_datasets_registered():
    ids = [metadata.id for metadata in list_datasets()]
    assert "fermi_lat.igrb.2015" in ids
    assert "fermi_lat.egb.2015" in ids


def test_fermi_lat_igrb_raw():
    dataset = get_dataset("fermi_lat.igrb.2015")
    raw = dataset.load_raw()

    assert len(raw) == 26
    assert np.all(np.asarray(raw["model"]) == "A")
    assert np.isclose(raw["energy_min"][0], 100.0)
    assert np.isclose(raw["energy_max"][-1], 819200.0)
    assert np.isclose(raw["igrb"][-1], 4.206e-14)


def test_fermi_lat_igrb_standardized():
    dataset = get_dataset("fermi_lat.igrb.2015")
    table = dataset.load()

    assert len(table) == 26
    assert table.meta["quantity"] == "phi"
    assert table.meta["foreground_model"] == "A"
    assert u.allclose(table["energy"][0], 118.91173196955799 * u.MeV)
    assert u.allclose(table["phi"][0], 6.688405797101448e-8 * PHI_UNIT)
    assert np.count_nonzero(table["is_upper_limit"]) == 1
    assert bool(table["is_upper_limit"][-1])


def test_fermi_lat_igrb_final_upper_limit():
    dataset = get_dataset("fermi_lat.igrb.2015")
    table = dataset.load()

    expected = 2.3e-12 / (819200.0 - 579261.9)
    assert u.allclose(table["integrated_flux"][-1], 2.3e-12 / (u.cm**2 * u.s * u.sr))
    assert u.allclose(table["phi"][-1], expected * PHI_UNIT)
    assert np.isnan(table["phi_lower"][-1].value)
    assert np.isnan(table["phi_upper"][-1].value)


def test_fermi_lat_egb_standardized():
    dataset = get_dataset("fermi_lat.egb.2015")
    table = dataset.load()

    assert len(table) == 26
    assert np.count_nonzero(table["is_upper_limit"]) == 0
    assert np.isclose(table["integrated_flux"][0].value, 3.674e-6)
    assert np.isclose(table["integrated_flux"][-1].value, 9.663e-12)


def test_fermi_lat_foreground_uncertainty():
    dataset = get_dataset("fermi_lat.igrb.2015")
    table = dataset.load()

    expected_lower = 9.082e-7 / (141.4 - 100.0)
    expected_upper = 1.279e-7 / (141.4 - 100.0)

    assert u.allclose(table["phi_foreground_err_lower"][0], expected_lower * PHI_UNIT)
    assert u.allclose(table["phi_foreground_err_upper"][0], expected_upper * PHI_UNIT)


def test_fermi_lat_e2phi_conversion():
    dataset = get_dataset("fermi_lat.igrb.2015")
    table = dataset.load_e2phi()

    assert table.meta["native_quantity"] == "phi"
    assert table.meta["quantity"] == "E2phi"
    assert "E2phi" in table.colnames
    assert "E2phi_lower" in table.colnames
    assert "E2phi_upper" in table.colnames
    assert "E2phi_foreground_err_lower" in table.colnames
    assert "E2phi_foreground_err_upper" in table.colnames
    assert bool(table["is_upper_limit"][-1])
