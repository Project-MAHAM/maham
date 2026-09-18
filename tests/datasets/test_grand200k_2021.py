import astropy.units as u
import numpy as np

from maham.datasets import get_dataset
from maham.statistics import feldman_cousins_upper_limit


UNIT = u.GeV / (u.cm**2 * u.s * u.sr)


def test_grand200k_native_metadata():
    dataset = get_dataset("grand200k.diffuse_sensitivity.2021")
    table = dataset.load(quantity="E2phi", flavor="all_flavor")
    assert dataset.metadata.source.provenance.value == "digitized"
    assert len(table) == 24
    assert table.meta["sensitivity_type"] == "projected_confidence_level_sensitivity"
    assert table.meta["response_level"] == "trigger_level"
    assert table.meta["analysis_efficiency_included"] is False
    assert table.meta["flavor_convention"] == "all_flavor"
    assert np.isclose(table.meta["confidence_level"], 0.90)
    assert np.isclose(table.meta["projection_years"], 10.0)
    assert table.meta["array_antennas"] == 200000
    assert table.meta["simulated_antennas"] == 10000
    assert np.isclose(table.meta["extrapolation_factor"], 20.0)
    assert table.meta["statistical_method"] == "feldman_cousins"
    assert table.meta["assumed_observed_events"] == 0
    assert np.isclose(table.meta["assumed_background_events"], 0.0)
    assert np.isclose(table.meta["feldman_cousins_upper_count"], 2.44)
    assert table.meta["sensitivity_normalization_convention"] == "log10_energy_width"
    assert np.isclose(table.meta["log10_energy_width_decades"], 1.0)


def test_grand200k_vector_extraction_endpoints_and_minimum():
    table = get_dataset("grand200k.diffuse_sensitivity.2021").load(quantity="E2phi")
    energy = table["energy"].to_value(u.GeV)
    flux = table["E2phi"].to_value(UNIT)
    assert np.isclose(energy[0], 4.819670e7, rtol=2e-7)
    assert np.isclose(energy[-1], 1.0e11, rtol=1e-12)
    assert np.isclose(flux[0], 1.278806e-9, rtol=2e-7)
    assert np.isclose(flux[-1], 6.387042e-9, rtol=2e-7)
    i_min = np.argmin(flux)
    assert np.isclose(energy[i_min], 5.172055e8, rtol=2e-7)
    assert np.isclose(flux[i_min], 1.907897e-10, rtol=2e-7)


def test_grand200k_published_fc_count_matches_maham():
    table = get_dataset("grand200k.diffuse_sensitivity.2021").load()
    exact = feldman_cousins_upper_limit(0, expected_background=0.0, confidence_level=0.90)
    assert np.isclose(table.meta["feldman_cousins_upper_count"], exact, atol=0.005)
