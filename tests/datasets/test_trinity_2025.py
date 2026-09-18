import astropy.units as u
import numpy as np

from maham.datasets import get_dataset


UNIT = u.GeV / (u.cm**2 * u.s * u.sr)


def test_trinity_native_metadata():
    dataset = get_dataset("trinity.diffuse_sensitivity.2025")
    table = dataset.load(quantity="E2phi", flavor="all_flavor")
    assert dataset.metadata.source.provenance.value == "digitized"
    assert len(table) == 5
    assert table.meta["sensitivity_type"] == "projected_confidence_level_sensitivity"
    assert table.meta["flavor_convention"] == "all_flavor"
    assert np.isclose(table.meta["confidence_level"], 0.90)
    assert np.isclose(table.meta["projection_years"], 10.0)
    assert np.isclose(table.meta["duty_cycle"], 0.20)
    assert table.meta["observatory_telescopes"] == 18
    assert table.meta["observatory_sites_minimum"] == 3
    assert table.meta["response_level"] == "detector_response"
    assert table.meta["reconstruction_requirements_included"] is True
    assert table.meta["analysis_efficiency_included"] is False
    assert table.meta["statistical_method"] == "not_specified_in_source"
    assert table.meta["sensitivity_normalization_convention"] == "log10_energy_width"
    assert np.isclose(table.meta["log10_energy_width_decades"], 1.0)


def test_trinity_vector_extracted_points():
    table = get_dataset("trinity.diffuse_sensitivity.2025").load(quantity="E2phi")
    expected_energy = np.array([1e6, 1e7, 1e8, 1e9, 1e10])
    expected_flux = np.array([
        2.276300661819e-8,
        1.803961242458e-9,
        8.697582027394e-10,
        1.803961242458e-9,
        1.277374757627e-8,
    ])
    np.testing.assert_allclose(table["energy"].to_value(u.GeV), expected_energy, rtol=1e-12)
    np.testing.assert_allclose(table["E2phi"].to_value(UNIT), expected_flux, rtol=1e-12)


def test_trinity_minimum_is_near_1e8_gev():
    table = get_dataset("trinity.diffuse_sensitivity.2025").load(quantity="E2phi")
    energy = table["energy"].to_value(u.GeV)
    flux = table["E2phi"].to_value(UNIT)
    i_min = np.argmin(flux)
    assert np.isclose(energy[i_min], 1e8)
    assert np.isclose(flux[i_min], 8.697582027394e-10, rtol=1e-12)
