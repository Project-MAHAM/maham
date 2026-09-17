import astropy.units as u
import numpy as np
import pytest
from astropy.table import QTable

from maham.physics.spectra import convert_limit_normalization_to_decade_width, rescale_anita_bandwidth_to_decade_width, rescale_differential_limit_decade_width


UNIT = u.GeV / (u.cm**2 * u.s * u.sr)


def make_limit(value=2.0):
    table = QTable()
    table["energy"] = [1e9] * u.GeV
    table["E2phi"] = [value] * UNIT
    table.meta["quantity"] = "E2phi"
    table.meta["limit_type"] = "differential_upper_limit"
    return table


def test_half_decade_to_one_decade():
    values = np.array([2.0, 4.0])
    np.testing.assert_allclose(rescale_differential_limit_decade_width(values, 0.5, 1.0), [1.0, 2.0])


def test_one_decade_to_half_decade():
    values = np.array([2.0, 4.0])
    np.testing.assert_allclose(rescale_differential_limit_decade_width(values, 1.0, 0.5), [4.0, 8.0])


def test_anita_bandwidth_to_one_decade():
    values = np.array([2.0, 4.0])
    np.testing.assert_allclose(rescale_anita_bandwidth_to_decade_width(values), values * 4.0 / np.log(10.0))


def test_log10_limit_table_conversion_preserves_native_provenance():
    table = make_limit()
    table.meta["limit_normalization_convention"] = "log10_energy_width"
    table.meta["log10_energy_width_decades"] = 0.5
    converted = convert_limit_normalization_to_decade_width(table, target_width_decades=1.0)
    assert u.allclose(converted["E2phi"], [1.0] * UNIT)
    assert converted.meta["native_limit_normalization_convention"] == "log10_energy_width"
    assert np.isclose(converted.meta["native_log10_energy_width_decades"], 0.5)
    assert converted.meta["limit_normalization_convention"] == "log10_energy_width"
    assert np.isclose(converted.meta["log10_energy_width_decades"], 1.0)
    assert np.isclose(converted.meta["limit_normalization_scale_factor"], 0.5)
    assert converted.meta["limit_normalization_rescaled"] is True


def test_anita_limit_table_conversion_preserves_native_provenance():
    table = make_limit()
    table.meta["limit_normalization_convention"] = "anita_bandwidth"
    table.meta["limit_bandwidth_factor"] = 4.0
    converted = convert_limit_normalization_to_decade_width(table, target_width_decades=1.0)
    assert u.allclose(converted["E2phi"], [2.0 * 4.0 / np.log(10.0)] * UNIT)
    assert converted.meta["native_limit_normalization_convention"] == "anita_bandwidth"
    assert np.isclose(converted.meta["native_limit_bandwidth_factor"], 4.0)
    assert converted.meta["limit_normalization_convention"] == "log10_energy_width"
    assert np.isclose(converted.meta["log10_energy_width_decades"], 1.0)
    assert np.isclose(converted.meta["limit_normalization_scale_factor"], 4.0 / np.log(10.0))


def test_limit_conversion_is_idempotent_at_same_target():
    table = make_limit()
    table.meta["limit_normalization_convention"] = "anita_bandwidth"
    table.meta["limit_bandwidth_factor"] = 4.0
    once = convert_limit_normalization_to_decade_width(table, target_width_decades=1.0)
    twice = convert_limit_normalization_to_decade_width(once, target_width_decades=1.0)
    assert u.allclose(twice["E2phi"], once["E2phi"])
    assert twice.meta["native_limit_normalization_convention"] == "anita_bandwidth"
    assert np.isclose(twice.meta["limit_normalization_scale_factor"], 4.0 / np.log(10.0))


@pytest.mark.parametrize("native,target", [(0, 1), (-0.5, 1), (0.5, 0), (0.5, -1)])
def test_decade_width_must_be_positive(native, target):
    with pytest.raises(ValueError, match="finite positive"):
        rescale_differential_limit_decade_width(np.array([1.0]), native, target)


def test_unknown_limit_normalization_convention_rejected():
    table = make_limit()
    table.meta["limit_normalization_convention"] = "unknown"
    with pytest.raises(ValueError, match="Unsupported differential-limit normalization convention"):
        convert_limit_normalization_to_decade_width(table)
