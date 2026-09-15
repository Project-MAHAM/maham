import astropy.units as u
import numpy as np

from maham.models.flux.neutrino import family_envelope


def test_cosmogenic_family_envelope():
    table = family_envelope("cosmogenic")
    assert table.meta["family"] == "cosmogenic"
    assert len(table.meta["model_ids"]) == 10
    assert np.max(table["n_models"]) > 1
    assert np.max(table["n_models"]) <= 10
    assert np.all(table["E2phi_lower"][table["n_models"] > 0] <= table["E2phi_upper"][table["n_models"] > 0])


def test_source_environment_family_envelope():
    table = family_envelope("source_environment")
    assert table.meta["family"] == "source_environment"
    assert len(table.meta["model_ids"]) == 8
    assert np.max(table["n_models"]) > 1
    assert np.max(table["n_models"]) <= 8
    assert np.all(table["E2phi_lower"][table["n_models"] > 0] <= table["E2phi_upper"][table["n_models"] > 0])


def test_cosmogenic_all_flavor_envelope():
    native = family_envelope("cosmogenic")
    all_flavor = family_envelope("cosmogenic", flavor="all_flavor", flavor_assumption="equal")

    assert all_flavor.meta["flavor_convention"] == "all_flavor"
    assert u.allclose(all_flavor["E2phi_lower"], 3.0 * native["E2phi_lower"], equal_nan=True)
    assert u.allclose(all_flavor["E2phi_upper"], 3.0 * native["E2phi_upper"], equal_nan=True)
