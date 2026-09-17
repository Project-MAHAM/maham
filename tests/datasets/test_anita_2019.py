import astropy.units as u
import numpy as np

from maham.datasets import get_dataset, list_datasets


EPHI_UNIT = 1 / (u.cm**2 * u.s * u.sr)
E2PHI_UNIT = u.GeV / (u.cm**2 * u.s * u.sr)


def test_anita_i_iv_diffuse_neutrino_limit_2019_registry_and_native_data():
    dataset_id = "anita.i_iv_diffuse_neutrino_limit.2019"
    ids = [metadata.id for metadata in list_datasets(experiment="ANITA", messenger="neutrino", data_type="limit")]
    assert dataset_id in ids
    dataset = get_dataset(dataset_id)
    table = dataset.load_ephi()
    assert dataset.metadata.source.provenance.value == "digitized"
    assert dataset.metadata.paper.doi == "10.1103/PhysRevD.99.122001"
    assert len(table) == 7
    assert table.meta["quantity"] == "Ephi"
    assert table.meta["flavor_convention"] == "all_flavor"
    assert table.meta["limit_normalization_convention"] == "anita_bandwidth"
    assert np.isclose(table.meta["limit_bandwidth_factor"], 4.0)
    assert np.isclose(table.meta["confidence_level"], 0.90)
    assert np.all(np.asarray(table["is_upper_limit"], dtype=bool))
    assert np.all(np.diff(table["energy"].to_value(u.GeV)) > 0)
    assert u.allclose(table["energy"][0], 1e9 * u.GeV)
    assert u.allclose(table["energy"][-1], 1e12 * u.GeV)
    assert u.allclose(table["Ephi"][0], 3.0371962350353715e-14 * EPHI_UNIT)
    assert u.allclose(table["Ephi"][3], 7.8167335261561550e-18 * EPHI_UNIT)
    assert u.allclose(table["Ephi"][-1], 2.0057984927391944e-19 * EPHI_UNIT)


def test_anita_i_iv_diffuse_neutrino_limit_2019_e2phi_conversion():
    dataset = get_dataset("anita.i_iv_diffuse_neutrino_limit.2019")
    native = dataset.load_ephi()
    converted = dataset.load_e2phi(flavor="all_flavor")
    assert converted.meta["native_quantity"] == "Ephi"
    assert converted.meta["quantity"] == "E2phi"
    assert converted.meta["flavor_convention"] == "all_flavor"
    expected = (native["Ephi"] * native["energy"]).to(E2PHI_UNIT)
    assert u.allclose(converted["E2phi"], expected)


def test_anita_iv_acceptance_2019_registry_and_native_data():
    dataset_id = "anita.iv.acceptance.2019"
    ids = [metadata.id for metadata in list_datasets(experiment="ANITA", messenger="neutrino", data_type="effective_area")]
    assert dataset_id in ids
    dataset = get_dataset(dataset_id)
    table = dataset.load()
    assert dataset.metadata.source.provenance.value == "published_table"
    assert dataset.metadata.paper.doi == "10.1103/PhysRevD.99.122001"
    assert len(table) == 7
    assert table.meta["quantity"] == "acceptance"
    assert table.meta["includes_analysis_efficiency"] is False
    assert table.meta["flight"] == "ANITA-IV"
    assert np.all(np.diff(table["energy"].to_value(u.GeV)) > 0)
    assert u.allclose(table["acceptance"][0], 0.0032 * u.km**2 * u.sr)
    assert u.allclose(table["acceptance"][3], 3.1 * u.km**2 * u.sr)
    assert u.allclose(table["acceptance"][-1], 167.0 * u.km**2 * u.sr)
