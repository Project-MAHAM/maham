import astropy.units as u
import numpy as np
import pytest

from maham.datasets import get_dataset


def test_txs0506_metadata():
    dataset = get_dataset("icecube.txs0506_flare_flux.2018")
    assert dataset.metadata.spectral_kind == "differential_flux"
    assert dataset.metadata.flavor_convention == "numu_nubar"
    assert dataset.metadata.solid_angle_convention == "point_source"


def test_txs0506_native_flux():
    dataset = get_dataset("icecube.txs0506_flare_flux.2018")
    table = dataset.load()

    assert table.meta["quantity"] == "phi"
    assert table.meta["source_name"] == "TXS 0506+056"
    assert table.meta["spectral_index"] == pytest.approx(2.2)
    assert table.meta["phi100_TeV_inv_cm2_s"] == pytest.approx(1.6e-15)
    assert table.meta["window_start_mjd"] == pytest.approx(56937.81)
    assert table.meta["window_end_mjd"] == pytest.approx(57096.21)
    assert table.meta["window_duration_days"] == pytest.approx(158.0)
    assert table["phi"].unit == 1 / (u.GeV * u.cm**2 * u.s)

    ratio = (table["phi"][-1] / table["phi"][0]).to_value(u.dimensionless_unscaled)
    expected = (table["energy"][-1] / table["energy"][0]).to_value(u.dimensionless_unscaled) ** -2.2
    assert ratio == pytest.approx(expected)


def test_txs0506_reference_normalization():
    dataset = get_dataset("icecube.txs0506_flare_flux.2018")
    table = dataset.load()

    phi100 = table.meta["phi100_TeV_inv_cm2_s"] / (u.TeV * u.cm**2 * u.s)
    gamma = table.meta["spectral_index"]
    energy = 100.0 * u.TeV
    expected = phi100 * (energy / (100.0 * u.TeV)) ** (-gamma)

    assert expected.to_value(1 / (u.TeV * u.cm**2 * u.s)) == pytest.approx(1.6e-15)


def test_txs0506_average_flux_reproduces_fluence():
    dataset = get_dataset("icecube.txs0506_flare_flux.2018")
    table = dataset.load()

    phi100 = table.meta["phi100_TeV_inv_cm2_s"] / (u.TeV * u.cm**2 * u.s)
    duration = table.meta["window_duration_days"] * u.day
    e2_fluence = ((100.0 * u.TeV) ** 2 * phi100 * duration).to(u.TeV / u.cm**2)

    assert e2_fluence.value == pytest.approx(2.18e-4, rel=0.02)


def test_txs0506_e2phi_conversion():
    dataset = get_dataset("icecube.txs0506_flare_flux.2018")
    table = dataset.load(quantity="E2phi")
    assert table.meta["quantity"] == "E2phi"
    assert table["E2phi"].unit == u.GeV / (u.cm**2 * u.s)


def test_txs0506_all_flavor_conversion():
    dataset = get_dataset("icecube.txs0506_flare_flux.2018")
    native = dataset.load()
    all_flavor = dataset.load(flavor="all_flavor", flavor_assumption="equal")

    np.testing.assert_allclose(all_flavor["phi"].value, 3.0 * native["phi"].value)
    assert all_flavor.meta["flavor_convention"] == "all_flavor"


def test_txs0506_rejects_intensity_notation():
    dataset = get_dataset("icecube.txs0506_flare_flux.2018")
    with pytest.raises(ValueError, match="does not permit conversion"):
        dataset.load(quantity="J")
