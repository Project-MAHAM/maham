import numpy as np

from maham.datasets import get_dataset
from maham.physics.spectra import convert_sensitivity_normalization_to_decade_width, convert_single_event_sensitivity_to_confidence_level


def test_pueo_native_ses_metadata():
    dataset = get_dataset("pueo.diffuse_sensitivity.2025")
    table = dataset.load(quantity="Ephi", flavor="all_flavor")
    assert dataset.metadata.source.provenance.value == "digitized"
    assert len(table) == 35
    assert table.meta["sensitivity_type"] == "single_event_sensitivity"
    assert table.meta["response_level"] == "trigger_level"
    assert table.meta["analysis_efficiency_included"] is False
    assert table.meta["flavor_convention"] == "all_flavor"
    assert np.isclose(table.meta["projection_days"], 30.0)
    assert np.isclose(table.meta["native_expected_signal_count"], 1.0)
    assert table.meta["sensitivity_normalization_convention"] == "bandwidth_factor"
    assert np.isclose(table.meta["sensitivity_bandwidth_factor"], 4.0)
    assert np.isclose(table["energy"][0].value, 4.168693834703e8)
    assert np.isclose(table["energy"][-1].value, 1.0e12)


def test_pueo_ephi_to_e2phi_is_explicit_spectral_conversion():
    native = get_dataset("pueo.diffuse_sensitivity.2025").load(quantity="Ephi", flavor="all_flavor")
    e2phi = get_dataset("pueo.diffuse_sensitivity.2025").load(quantity="E2phi", flavor="all_flavor")
    np.testing.assert_allclose(e2phi["E2phi"].value, native["Ephi"].value * native["energy"].value)
    assert e2phi.meta["native_quantity"] == "Ephi"
    assert e2phi.meta["quantity"] == "E2phi"


def test_pueo_one_decade_normalization_factor():
    native = get_dataset("pueo.diffuse_sensitivity.2025").load(quantity="E2phi", flavor="all_flavor")
    converted = convert_sensitivity_normalization_to_decade_width(native, target_width_decades=1.0)
    expected = 4.0 / np.log(10.0)
    assert converted.meta["native_sensitivity_normalization_convention"] == "bandwidth_factor"
    assert np.isclose(converted.meta["native_sensitivity_bandwidth_factor"], 4.0)
    assert converted.meta["sensitivity_normalization_convention"] == "log10_energy_width"
    assert np.isclose(converted.meta["log10_energy_width_decades"], 1.0)
    assert np.isclose(converted.meta["sensitivity_normalization_scale_factor"], expected)
    np.testing.assert_allclose(converted["E2phi"].value / native["E2phi"].value, expected)


def test_pueo_fc90_conversion():
    native = get_dataset("pueo.diffuse_sensitivity.2025").load(quantity="E2phi", flavor="all_flavor")
    decade = convert_sensitivity_normalization_to_decade_width(native, target_width_decades=1.0)
    fc90 = convert_single_event_sensitivity_to_confidence_level(decade, confidence_level=0.90, method="feldman_cousins")
    assert fc90.meta["native_sensitivity_type"] == "single_event_sensitivity"
    assert fc90.meta["sensitivity_type"] == "projected_confidence_level_sensitivity"
    assert np.isclose(fc90.meta["confidence_level"], 0.90)
    assert fc90.meta["statistical_method"] == "feldman_cousins"
    assert fc90.meta["assumed_observed_events"] == 0
    assert np.isclose(fc90.meta["assumed_background_events"], 0.0)
    assert np.isclose(fc90.meta["expected_signal_count_scale_factor"], 2.43591508865, atol=1e-9)
    expected_total = 4.0 / np.log(10.0) * fc90.meta["expected_signal_count_scale_factor"]
    np.testing.assert_allclose(fc90["E2phi"].value / native["E2phi"].value, expected_total)
