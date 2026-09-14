import astropy.units as u
import numpy as np
import pytest

from maham.datasets import get_dataset


def test_ngc1068_metadata():
    dataset = get_dataset("icecube.ngc1068_flux.2022")
    assert dataset.metadata.spectral_kind == "differential_flux"
    assert dataset.metadata.flavor_convention == "numu_nubar"
    assert dataset.metadata.solid_angle_convention == "point_source"


def test_ngc1068_native_flux():
    dataset = get_dataset("icecube.ngc1068_flux.2022")
    table = dataset.load()

    assert table.meta["quantity"] == "phi"
    assert table.meta["source_name"] == "NGC 1068"
    assert table.meta["spectral_index"] == pytest.approx(3.2)
    assert table.meta["phi0_TeV_inv_cm2_s"] == pytest.approx(5.0e-11)
    assert table["energy"][0].to_value(u.TeV) == pytest.approx(1.5)
    assert table["energy"][-1].to_value(u.TeV) == pytest.approx(15.0)
    assert table["phi"].unit == 1 / (u.GeV * u.cm**2 * u.s)

    ratio = (table["phi"][-1] / table["phi"][0]).to_value(u.dimensionless_unscaled)
    expected = (table["energy"][-1] / table["energy"][0]).to_value(u.dimensionless_unscaled) ** -3.2
    assert ratio == pytest.approx(expected)


def test_ngc1068_e2phi_conversion():
    dataset = get_dataset("icecube.ngc1068_flux.2022")
    table = dataset.load(quantity="E2phi")
    assert table.meta["quantity"] == "E2phi"
    assert table["E2phi"].unit == u.GeV / (u.cm**2 * u.s)


def test_ngc1068_all_flavor_conversion():
    dataset = get_dataset("icecube.ngc1068_flux.2022")
    native = dataset.load()
    all_flavor = dataset.load(flavor="all_flavor", flavor_assumption="equal")
    np.testing.assert_allclose(all_flavor["phi"].value, 3.0 * native["phi"].value)
    assert all_flavor.meta["flavor_convention"] == "all_flavor"


def test_ngc1068_rejects_intensity_notation():
    dataset = get_dataset("icecube.ngc1068_flux.2022")
    with pytest.raises(ValueError, match="does not permit conversion"):
        dataset.load(quantity="J")
