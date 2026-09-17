import astropy.units as u
import numpy as np
import pytest

from maham.datasets import get_dataset, list_datasets


E2PHI_UNIT = u.GeV / (u.cm**2 * u.s * u.sr)


def test_auger_diffuse_neutrino_limit_2023_registry_and_native_data():
    dataset_id = "auger.diffuse_neutrino_limit.2023"
    ids = [metadata.id for metadata in list_datasets(experiment="Pierre Auger Observatory", messenger="neutrino", data_type="limit")]
    assert dataset_id in ids
    dataset = get_dataset(dataset_id)
    table = dataset.load_e2phi()
    assert dataset.metadata.source.provenance.value == "digitized"
    assert dataset.metadata.paper.doi == "10.22323/1.444.1488"
    assert len(table) == 8
    assert table.meta["flavor_convention"] == "per_flavor"
    assert np.isclose(table.meta["confidence_level"], 0.90)
    assert table.meta["limit_normalization_convention"] == "log10_energy_width"
    assert np.isclose(table.meta["log10_energy_width_decades"], 0.5)
    assert table.meta["observation_period"] == "2004-01-01/2021-12-31"
    assert np.all(np.asarray(table["is_upper_limit"], dtype=bool))
    assert np.all(np.diff(table["energy"].to_value(u.GeV)) > 0)
    assert u.allclose(table["energy_min"][0], 10**7.5 * u.GeV)
    assert u.allclose(table["energy_max"][-1], 10**11.5 * u.GeV)
    assert u.allclose(table["E2phi"][0], 7.583e-8 * E2PHI_UNIT)
    assert u.allclose(table["E2phi"][2], 1.151e-8 * E2PHI_UNIT)
    assert u.allclose(table["E2phi"][-1], 3.468e-7 * E2PHI_UNIT)


def test_auger_diffuse_neutrino_limit_2023_all_flavor_conversion():
    dataset = get_dataset("auger.diffuse_neutrino_limit.2023")
    native = dataset.load_e2phi()
    with pytest.raises(ValueError, match="flavor_assumption='equal'"):
        dataset.load_e2phi(flavor="all_flavor")
    converted = dataset.load_e2phi(flavor="all_flavor", flavor_assumption="equal")
    assert converted.meta["flavor_convention"] == "all_flavor"
    assert converted.meta["flavor_assumption"] == "equal"
    np.testing.assert_allclose(converted["E2phi"].value, 3.0 * native["E2phi"].value)
