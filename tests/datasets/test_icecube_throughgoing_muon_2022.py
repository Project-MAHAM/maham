import astropy.units as u
import numpy as np
import pytest

from maham.datasets import get_dataset


UNIT = u.GeV / (u.cm**2 * u.s * u.sr)


def test_throughgoing_muon_metadata():
    dataset = get_dataset("icecube.throughgoing_muon_piecewise_flux.2022")
    assert dataset.metadata.experiment == "IceCube"
    assert dataset.metadata.quantity == "E2phi"
    assert dataset.metadata.flavor_convention == "numu_nubar"
    assert dataset.metadata.confidence_level is None
    assert dataset.metadata.source.sha256 == "2df5b1d88498d693b0e8c992f67ce8779db4ec1698099e6b3c9aebe40e41b992"


def test_throughgoing_muon_native_values():
    table = get_dataset("icecube.throughgoing_muon_piecewise_flux.2022").load()

    assert len(table) == 5
    assert u.allclose(table["energy_min"], [100, 15000, 104000, 721000, 5000000] * u.GeV)
    assert u.allclose(table["energy_max"], [15000, 104000, 721000, 5000000, 100000000] * u.GeV)
    assert u.allclose(table["E2phi"], np.array([0.0, 2.22, 1.21, 0.33, 0.0]) * 1e-8 * UNIT)
    assert u.allclose(table["E2phi_lower"], np.array([0.0, 1.42, 0.90, 0.15, 0.0]) * 1e-8 * UNIT)
    assert u.allclose(table["E2phi_upper"], np.array([3.10, 3.02, 1.53, 0.55, 0.41]) * 1e-8 * UNIT)


def test_throughgoing_muon_mixed_confidence_levels():
    table = get_dataset("icecube.throughgoing_muon_piecewise_flux.2022").load()
    assert np.allclose(table["confidence_level"], [0.90, 0.6827, 0.6827, 0.6827, 0.90])
    assert np.array_equal(table["is_upper_limit"], [True, False, False, False, True])


def test_throughgoing_muon_all_flavor_conversion():
    dataset = get_dataset("icecube.throughgoing_muon_piecewise_flux.2022")
    native = dataset.load_e2phi()
    all_flavor = dataset.load_e2phi(flavor="all_flavor", flavor_assumption="equal")

    assert u.allclose(all_flavor["E2phi"], 3 * native["E2phi"])
    assert u.allclose(all_flavor["E2phi_lower"], 3 * native["E2phi_lower"])
    assert u.allclose(all_flavor["E2phi_upper"], 3 * native["E2phi_upper"])
    assert all_flavor.meta["flavor_convention"] == "all_flavor"


def test_throughgoing_muon_conversion_requires_equal_flavor_assumption():
    dataset = get_dataset("icecube.throughgoing_muon_piecewise_flux.2022")
    with pytest.raises(ValueError):
        dataset.load_e2phi(flavor="all_flavor")


def test_throughgoing_muon_quantity_conversion():
    dataset = get_dataset("icecube.throughgoing_muon_piecewise_flux.2022")
    native = dataset.load_e2phi()
    phi = dataset.load_phi()

    assert u.allclose(phi["phi"], native["E2phi"] / native["energy"] ** 2)
    assert u.allclose(phi["phi_upper"], native["E2phi_upper"] / native["energy"] ** 2)
