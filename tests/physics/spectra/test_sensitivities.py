import astropy.units as u
import numpy as np

from maham.physics.spectra.sensitivities import rescale_single_event_sensitivity, single_event_sensitivity_to_upper_limit


def test_rescale_single_event_sensitivity():
    values = np.array([1.0, 2.0]) * u.GeV
    result = rescale_single_event_sensitivity(values, 2.5)
    np.testing.assert_allclose(result.to_value(u.GeV), [2.5, 5.0])


def test_ses_to_fc_90_percent_uses_244_count():
    result = single_event_sensitivity_to_upper_limit(1.0, confidence_level=0.90, method="feldman_cousins")
    assert np.isclose(result, 2.44, atol=0.006)


def test_ses_to_classical_90_percent_uses_log10_count():
    result = single_event_sensitivity_to_upper_limit(1.0, confidence_level=0.90, method="classical")
    assert np.isclose(result, np.log(10.0), rtol=1e-14)
