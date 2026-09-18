import astropy.units as u
import numpy as np
import pytest

from maham.models import get_model
from maham.models.cross_sections.neutrino import CTW2011CrossSection


@pytest.mark.parametrize(
    ("energy_GeV", "cc_cm2", "nc_cm2", "total_cm2"),
    [
        (1.0e4, 0.48e-34, 0.16e-34, 0.63e-34),
        (1.0e6, 0.72e-33, 0.27e-33, 0.98e-33),
        (1.0e8, 0.48e-32, 0.19e-32, 0.67e-32),
        (1.0e10, 0.22e-31, 0.90e-32, 0.31e-31),
    ],
)
def test_ctw_matches_published_nu_table(energy_GeV, cc_cm2, nc_cm2, total_cm2):
    model = CTW2011CrossSection()
    energy = energy_GeV * u.GeV
    assert np.isclose(model.cross_section(energy, current="cc").to_value(u.cm**2), cc_cm2, rtol=0.05)
    assert np.isclose(model.cross_section(energy, current="nc").to_value(u.cm**2), nc_cm2, rtol=0.05)
    assert np.isclose(model.cross_section(energy, current="total").to_value(u.cm**2), total_cm2, rtol=0.05)


def test_ctw_total_is_cc_plus_nc():
    model = CTW2011CrossSection()
    energy = np.logspace(6, 11, 12) * u.GeV
    total = model.cross_section(energy, current="total")
    summed = model.cross_section(energy, current="cc") + model.cross_section(energy, current="nc")
    np.testing.assert_allclose(total.to_value(u.cm**2), summed.to_value(u.cm**2), rtol=1e-14)


def test_ctw_uncertainty_variants_at_uhe():
    model = CTW2011CrossSection()
    energy = 1e10 * u.GeV
    lower = model.cross_section(energy, variation="lower")
    central = model.cross_section(energy)
    upper = model.cross_section(energy, variation="upper")
    assert lower < central < upper


def test_ctw_supports_antineutrinos():
    model = CTW2011CrossSection()
    energy = 1e6 * u.GeV
    assert model.cross_section(energy, particle="nubar") > 0 * u.cm**2
    assert model.cross_section(energy, particle="nubar") != model.cross_section(energy, particle="nu")


@pytest.mark.parametrize("energy", [1e3, 1e13])
def test_ctw_rejects_out_of_range_energy(energy):
    with pytest.raises(ValueError, match="supported only"):
        CTW2011CrossSection().cross_section(energy * u.GeV)


def test_ctw_is_registered():
    model = get_model("neutrino.cross_section.ctw_2011")
    assert isinstance(model, CTW2011CrossSection)
