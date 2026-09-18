import astropy.units as u
import numpy as np

from maham.datasets import get_dataset


UNIT = u.GeV / (u.cm**2 * u.s * u.sr)


def test_gen2_radio_native_metadata():
    dataset = get_dataset("icecube_gen2.radio.diffuse_sensitivity.2021")
    table = dataset.load(quantity="E2phi", flavor="all_flavor")
    assert dataset.metadata.source.provenance.value == "digitized"
    assert len(table) == 8
    assert table.meta["sensitivity_type"] == "projected_confidence_level_sensitivity"
    assert table.meta["response_level"] == "trigger_level"
    assert table.meta["analysis_efficiency_included"] is False
    assert table.meta["flavor_convention"] == "all_flavor"
    assert np.isclose(table.meta["confidence_level"], 0.90)
    assert np.isclose(table.meta["projection_years"], 10.0)
    assert table.meta["benchmark_stations"] == 313
    assert np.isclose(table.meta["assumed_background_events"], 0.0)
    assert table.meta["statistical_method"] == "not_specified_in_source"
    assert table.meta["sensitivity_normalization_convention"] == "log10_energy_width"
    assert np.isclose(table.meta["log10_energy_width_decades"], 1.0)
    assert np.isclose(table.meta["plot_point_spacing_decades"], 0.5)


def test_gen2_radio_vector_extracted_points():
    table = get_dataset("icecube_gen2.radio.diffuse_sensitivity.2021").load(quantity="E2phi")
    expected_energy = np.array([
        3.162277604160e7,
        9.999999645769e7,
        3.162277492142e8,
        9.999999291538e8,
        3.162277492142e9,
        9.999999291538e9,
        3.162277380124e10,
        9.999999291538e10,
    ])

    expected_flux = np.array([
        2.120535310567e-9,
        5.723884680840e-10,
        2.870329783985e-10,
        2.365309976840e-10,
        2.764543506936e-10,
        4.104233156754e-10,
        7.094275857264e-10,
        1.335514545218e-9,
    ])
    np.testing.assert_allclose(table["energy"].to_value(u.GeV), expected_energy, rtol=1e-12)
    np.testing.assert_allclose(table["E2phi"].to_value(UNIT), expected_flux, rtol=1e-12)


def test_gen2_radio_plot_sampling_is_half_decade():
    table = get_dataset("icecube_gen2.radio.diffuse_sensitivity.2021").load()
    spacing = np.diff(np.log10(table["energy"].to_value(u.GeV)))
    np.testing.assert_allclose(spacing, 0.5, atol=2e-7)
