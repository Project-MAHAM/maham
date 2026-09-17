import astropy.units as u
import numpy as np
import pytest
from astropy.table import Table

from maham.datasets import get_dataset, list_datasets


def test_baikal_gvd_2025_datasets_registered():
    ids = [metadata.id for metadata in list_datasets(experiment="Baikal-GVD", messenger="neutrino")]
    assert "baikal_gvd.diffuse_neutrino_limit.2025" in ids
    assert "baikal_gvd.effective_area.2025" in ids


def test_baikal_gvd_limit_native_data():
    dataset = get_dataset("baikal_gvd.diffuse_neutrino_limit.2025")
    table = dataset.load_e2phi()
    unit = u.GeV / (u.cm**2 * u.s * u.sr)
    assert dataset.metadata.data_type == "limit"
    assert dataset.metadata.source.provenance.value == "published_table"
    assert dataset.metadata.paper.doi == "10.1103/jlz3-26lw"
    assert len(table) == 8
    assert table.meta["flavor_convention"] == "per_flavor"
    assert table.meta["particle_convention"] == "nu_plus_nubar"
    assert np.isclose(table.meta["confidence_level"], 0.90)
    assert table.meta["limit_normalization_convention"] == "log10_energy_width"
    assert np.isclose(table.meta["log10_energy_width_decades"], 1.0)
    assert table.meta["limit_spectral_assumption"] == "E^-1"
    assert np.all(table["is_upper_limit"])
    assert u.allclose(table["energy_min"][0], 10**6.5 * u.GeV)
    assert u.allclose(table["energy_max"][0], 10**7.5 * u.GeV)
    assert u.allclose(table["energy"][0], 1e7 * u.GeV)
    assert u.allclose(table["E2phi"][0], 0.78e-8 * unit)
    assert u.allclose(table["E2phi"][-1], 54e-8 * unit)


def test_baikal_gvd_limit_all_flavor_conversion():
    dataset = get_dataset("baikal_gvd.diffuse_neutrino_limit.2025")
    native = dataset.load_e2phi()
    with pytest.raises(ValueError, match="flavor_assumption='equal'"):
        dataset.load_e2phi(flavor="all_flavor")
    converted = dataset.load_e2phi(flavor="all_flavor", flavor_assumption="equal")
    assert converted.meta["native_flavor_convention"] == "per_flavor"
    assert converted.meta["flavor_convention"] == "all_flavor"
    assert converted.meta["flavor_assumption"] == "equal"
    np.testing.assert_allclose(converted["E2phi"].value, 3.0 * native["E2phi"].value)


def test_baikal_gvd_effective_area_native_data():
    dataset = get_dataset("baikal_gvd.effective_area.2025")
    table = dataset.load()
    assert dataset.metadata.data_type == "effective_area"
    assert dataset.metadata.source.provenance.value == "official_release"
    assert len(table) == 45
    assert table.meta["solid_angle_convention"] == "upper_hemisphere_2pi_exposure_weighted_average"
    assert np.all(np.diff(table["energy"].to_value(u.GeV)) > 0)
    assert u.allclose(table["energy"][0], 10**3.55 * u.TeV)
    assert u.allclose(table["effective_area_nue"][0], 38.80 * u.m**2)
    assert u.allclose(table["effective_area_total"][0], 57.03 * u.m**2)
    assert u.allclose(table["effective_area_total"][-1], 19026.19 * u.m**2)
    summed = table["effective_area_nue"] + table["effective_area_numu"] + table["effective_area_nutau"]
    assert np.allclose(table["effective_area_total"].to_value(u.m**2), summed.to_value(u.m**2), atol=0.011)


def test_baikal_gvd_effective_area_standardization():
    dataset = get_dataset("baikal_gvd.effective_area.2025")
    raw = Table({"log10_energy_TeV": [3.75], "effective_area_nue_m2": [396.00], "effective_area_numu_m2": [13.26], "effective_area_nutau_m2": [26.64], "effective_area_total_m2": [435.90]})
    table = dataset.standardize(raw)
    assert u.allclose(table["energy"][0], 10**3.75 * u.TeV)
    assert u.allclose(table["effective_area_nue"][0], 396.00 * u.m**2)
    assert u.allclose(table["effective_area_total"][0], 435.90 * u.m**2)
