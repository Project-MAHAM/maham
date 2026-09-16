import astropy.units as u
import numpy as np
import pytest

from maham.datasets import get_dataset, list_datasets


def test_icecube_cascade_piecewise_2020_registry_and_native_data():
    dataset_id = "icecube.cascade_piecewise_flux.2020"
    assert dataset_id in [metadata.id for metadata in list_datasets(experiment="IceCube", messenger="neutrino", data_type="spectrum")]
    dataset = get_dataset(dataset_id)
    table = dataset.load_e2phi()
    assert dataset.metadata.source.provenance.value == "digitized"
    assert dataset.metadata.paper.doi == "10.1103/PhysRevLett.125.121104"
    assert len(table) == 13
    assert table.meta["flavor_convention"] == "per_flavor"
    assert np.isclose(table.meta["confidence_level"], 0.68)
    assert table.meta["interval_method"] == "digitized_68_percent_simultaneous_coverage"
    assert np.all(np.diff(table["energy"].to_value(u.GeV)) > 0)
    upper = np.asarray(table["is_upper_limit"], dtype=bool)
    measured = ~upper
    assert np.array_equal(np.flatnonzero(upper), [5, 8, 9, 10, 11, 12])
    assert np.count_nonzero(measured) == 7
    assert np.all(table["E2phi"][measured] > 0)
    assert np.all(table["E2phi_lower"][measured] <= table["E2phi"][measured])
    assert np.all(table["E2phi"][measured] <= table["E2phi_upper"][measured])
    assert np.all(table["E2phi"][upper] == 0)
    assert np.all(table["E2phi_lower"][upper] == 0)
    assert np.all(table["E2phi_upper"][upper] > 0)
    assert np.allclose(table.meta["sensitive_energy_range_GeV"], [1.6e4, 2.6e6])


def test_icecube_cascade_piecewise_2020_all_flavor_conversion():
    dataset = get_dataset("icecube.cascade_piecewise_flux.2020")
    native = dataset.load_e2phi()
    with pytest.raises(ValueError, match="flavor_assumption='equal'"):
        dataset.load_e2phi(flavor="all_flavor")
    converted = dataset.load_e2phi(flavor="all_flavor", flavor_assumption="equal")
    assert converted.meta["flavor_convention"] == "all_flavor"
    assert converted.meta["flavor_assumption"] == "equal"
    np.testing.assert_allclose(converted["E2phi"].value, 3.0 * native["E2phi"].value)
    np.testing.assert_allclose(converted["E2phi_lower"].value, 3.0 * native["E2phi_lower"].value)
    np.testing.assert_allclose(converted["E2phi_upper"].value, 3.0 * native["E2phi_upper"].value)
