import astropy.units as u
import numpy as np
from maham.models.flux.neutrino import family_envelope


def test_cosmogenic_family_envelope():
    table = family_envelope("cosmogenic", flavor="all_flavor", flavor_assumption="equal")
    assert table.meta["family"] == "cosmogenic"
    assert table.meta["flavor_convention"] == "all_flavor"
    assert len(table.meta["model_ids"]) == 17
    assert np.max(table["n_models"]) > 1
    assert np.max(table["n_models"]) <= 17
    assert np.all(table["E2phi_lower"][table["n_models"] > 0] <= table["E2phi_upper"][table["n_models"] > 0])


def test_source_environment_family_envelope():
    table = family_envelope("source_environment", flavor="all_flavor", flavor_assumption="equal")
    assert table.meta["family"] == "source_environment"
    assert table.meta["flavor_convention"] == "all_flavor"
    assert len(table.meta["model_ids"]) == 9
    assert np.max(table["n_models"]) > 1
    assert np.max(table["n_models"]) <= 9
    assert np.all(table["E2phi_lower"][table["n_models"] > 0] <= table["E2phi_upper"][table["n_models"] > 0])


def test_cosmogenic_per_flavor_conversion():
    all_flavor = family_envelope("cosmogenic", flavor="all_flavor", flavor_assumption="equal")
    per_flavor = family_envelope("cosmogenic", flavor="per_flavor", flavor_assumption="equal")
    assert per_flavor.meta["flavor_convention"] == "per_flavor"
    assert u.allclose(all_flavor["E2phi_lower"], 3.0 * per_flavor["E2phi_lower"], equal_nan=True)
    assert u.allclose(all_flavor["E2phi_upper"], 3.0 * per_flavor["E2phi_upper"], equal_nan=True)
