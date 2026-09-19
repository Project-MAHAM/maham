import astropy.units as u
import numpy as np

from maham.datasets import get_dataset


UNIT = u.GeV / (u.cm**2 * u.s * u.sr)


def test_ret_n_native_metadata():
    dataset = get_dataset("ret_n.diffuse_sensitivity.2022")
    table = dataset.load(quantity="E2phi", flavor="all_flavor")
    assert dataset.metadata.source.provenance.value == "digitized"
    assert len(table) == 55
    assert table.meta["sensitivity_type"] == "projected_confidence_level_sensitivity"
    assert table.meta["flavor_convention"] == "all_flavor"
    assert np.isclose(table.meta["confidence_level"], 0.90)
    assert np.isclose(table.meta["projection_years"], 10.0)
    assert table.meta["benchmark_stations"] == 10
    assert np.isclose(table.meta["transmitter_power_kw_per_station"], 100.0)
    assert table.meta["receivers_per_station"] == 27
    assert np.isclose(table.meta["transmitter_depth_km"], 1.5)
    assert table.meta["response_level"] == "trigger_level"
    assert np.isclose(table.meta["trigger_snr_db"], 0.0)
    assert np.isclose(table.meta["trigger_noise_bandwidth_mhz"], 50.0)
    assert table.meta["analysis_efficiency_included"] is False
    assert table.meta["statistical_method"] == "not_specified_in_source"
    assert table.meta["sensitivity_normalization_convention"] == "log10_energy_width"
    assert np.isclose(table.meta["log10_energy_width_decades"], 1.0)


def test_ret_n_vector_derived_curve_samples():
    table = get_dataset("ret_n.diffuse_sensitivity.2022").load(quantity="E2phi")
    energy = table["energy"].to_value(u.GeV)
    flux = table["E2phi"].to_value(UNIT)
    assert np.all(np.diff(energy) > 0)
    np.testing.assert_allclose(
        [energy[0], energy[37], energy[-1]],
        [1.990626798129e6, 1.982570657777e9, 4.852885817627e10],
        rtol=1e-12,
    )
    np.testing.assert_allclose(
        [flux[0], flux[37], flux[-1]],
        [1.000599101952e-8, 6.534334616736e-10, 2.003565167448e-9],
        rtol=1e-12,
    )


def test_ret_n_minimum_is_near_2e9_gev():
    table = get_dataset("ret_n.diffuse_sensitivity.2022").load(quantity="E2phi")
    energy = table["energy"].to_value(u.GeV)
    flux = table["E2phi"].to_value(UNIT)
    i_min = np.argmin(flux)
    assert np.isclose(energy[i_min], 1.982570657777e9, rtol=1e-12)
    assert np.isclose(flux[i_min], 6.534334616736e-10, rtol=1e-12)
