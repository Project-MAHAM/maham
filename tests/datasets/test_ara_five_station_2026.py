import astropy.units as u
import numpy as np
import pytest

from maham.datasets import get_dataset, list_datasets


E2PHI_UNIT = u.GeV / (u.cm**2 * u.s * u.sr)


def test_ara_five_station_diffuse_limit_2026_registry_and_native_data():
    dataset_id = "ara.five_station.diffuse_neutrino_limit.2026"
    ids = [metadata.id for metadata in list_datasets(experiment="ARA", messenger="neutrino", data_type="limit")]
    assert dataset_id in ids
    dataset = get_dataset(dataset_id)
    table = dataset.load_e2phi()
    assert dataset.metadata.source.provenance.value == "digitized"
    assert len(table) == 10
    assert table.meta["flavor_convention"] == "all_flavor"
    assert np.isclose(table.meta["confidence_level"], 0.90)
    assert np.isclose(table.meta["array_wide_livetime_years"], 10.6)
    assert np.all(np.asarray(table["is_upper_limit"], dtype=bool))
    assert np.all(np.diff(table["energy"].to_value(u.GeV)) > 0)
    assert u.allclose(table["energy"][0], 10**7.5 * u.GeV)
    assert u.allclose(table["E2phi"][3], 2.23906122e-7 * E2PHI_UNIT)
    assert u.allclose(table["E2phi"][-1], 3.47761864e-7 * E2PHI_UNIT)


def test_ara_five_station_diffuse_limit_2026_flavor_conversion_is_explicit():
    dataset = get_dataset("ara.five_station.diffuse_neutrino_limit.2026")
    native = dataset.load_e2phi()
    with pytest.raises(ValueError, match="flavor_assumption='equal'"):
        dataset.load_e2phi(flavor="per_flavor")
    per_flavor = dataset.load_e2phi(flavor="per_flavor", flavor_assumption="equal")
    assert per_flavor.meta["flavor_convention"] == "per_flavor"
    assert per_flavor.meta["flavor_assumption"] == "equal"
    np.testing.assert_allclose(per_flavor["E2phi"].value, native["E2phi"].value / 3.0)


def test_ara_five_station_trigger_acceptance_2026_registry_and_derived_area():
    dataset_id = "ara.five_station.trigger_acceptance.2026"
    ids = [metadata.id for metadata in list_datasets(experiment="ARA", messenger="neutrino", data_type="effective_area")]
    assert dataset_id in ids
    dataset = get_dataset(dataset_id)
    table = dataset.load()
    assert dataset.metadata.source.provenance.value == "digitized"
    assert len(table) == 11
    assert table.meta["quantity"] == "acceptance"
    assert table.meta["response_level"] == "trigger"
    assert table.meta["neutrino_type_convention"] == "average_over_six_nu_nubar_types"
    assert table.meta["livetime_averaged"] is True
    assert u.allclose(table["acceptance"][4], 1.09668728e-2 * u.km**2 * u.sr)
    expected_area = (table["acceptance"] / (4 * np.pi * u.sr)).to(u.km**2)
    assert u.allclose(table["sky_averaged_effective_area"], expected_area)
    assert u.allclose(table["sky_averaged_effective_area"][4], 8.72716009e-4 * u.km**2, rtol=2e-7)


def test_ara_five_station_signal_efficiency_2026_registry_and_native_data():
    dataset_id = "ara.five_station.signal_efficiency.2026"
    ids = [metadata.id for metadata in list_datasets(experiment="ARA", messenger="neutrino", data_type="efficiency")]
    assert dataset_id in ids
    dataset = get_dataset(dataset_id)
    table = dataset.load()
    assert dataset.metadata.source.provenance.value == "digitized"
    assert len(table) == 11
    assert table.meta["quantity"] == "efficiency"
    assert table.meta["averaging"] == "exposure_weighted_array_wide"
    assert table.meta["response_stage"] == "after_event_selection"
    assert np.all((table["efficiency"].value >= 0) & (table["efficiency"].value <= 1))
    assert np.all(np.diff(table["energy"].to_value(u.GeV)) > 0)
    assert np.isclose(table["efficiency"][4].value, 0.14344520)
    assert np.isclose(table["efficiency"][-1].value, 0.32752763)
