import astropy.units as u
import numpy as np

from maham.datasets import get_dataset


def test_icecube_combined_metadata():
    dataset = get_dataset("icecube.combined_astrophysical_flux.2015")
    assert dataset.metadata.experiment == "IceCube"
    assert dataset.metadata.quantity == "E2phi"
    assert dataset.metadata.flavor_convention == "all_flavor"
    assert dataset.metadata.confidence_level == 0.6827
    assert dataset.metadata.source.sha256 == "8e32d5c7aabe14c0b1f43e551c589f58cfeefc7c799b283e44f2eb376c814fd2"


def test_icecube_combined_native_values():
    table = get_dataset("icecube.combined_astrophysical_flux.2015").load()
    unit = u.GeV / (u.cm**2 * u.s * u.sr)

    expected = np.array([9.31407260358, 22.5643864183, 5.63201177622, 3.20115983712, 4.25417119386, 0.0, 6.85816864131, 0.0, 0.0])

    assert len(table) == 9
    assert u.allclose(table["energy_min"][0], 1e4 * u.GeV)
    assert u.allclose(table["energy_max"][-1], 1e7 * u.GeV)
    assert np.allclose(table["E2phi"].to_value(unit), expected * 1e-8)


def test_icecube_combined_profile_intervals_match_paper():
    table = get_dataset("icecube.combined_astrophysical_flux.2015").load()
    unit = u.GeV / (u.cm**2 * u.s * u.sr)

    lower68 = np.round(table["E2phi_lower"].to_value(unit) / 1e-8, 1)
    upper68 = np.round(table["E2phi_upper"].to_value(unit) / 1e-8, 1)
    lower90 = np.round(table["E2phi_90_lower"].to_value(unit) / 1e-8, 1)
    upper90 = np.round(table["E2phi_90_upper"].to_value(unit) / 1e-8, 1)

    assert np.allclose(lower68, [1.7, 17.0, 2.4, 0.8, 2.0, 0.0, 4.5, 0.0, 0.0])
    assert np.allclose(upper68, [17.3, 28.5, 9.2, 5.9, 7.0, 1.5, 9.7, 1.5, 0.6])
    assert np.allclose(lower90, [0.0, 13.5, 0.5, 0.0, 0.8, 0.0, 3.1, 0.0, 0.0])
    assert np.allclose(upper90, [22.7, 32.5, 11.6, 7.9, 9.0, 3.5, 11.9, 3.8, 1.5])


def test_icecube_combined_upper_limit_bins():
    table = get_dataset("icecube.combined_astrophysical_flux.2015").load()
    assert np.array_equal(np.flatnonzero(table["is_upper_limit"]), [5, 7, 8])


def test_icecube_combined_per_flavor_conversion():
    dataset = get_dataset("icecube.combined_astrophysical_flux.2015")
    all_flavor = dataset.load_e2phi()
    per_flavor = dataset.load_e2phi(flavor="per_flavor", flavor_assumption="equal")

    assert u.allclose(per_flavor["E2phi"], all_flavor["E2phi"] / 3)
    assert u.allclose(per_flavor["E2phi_lower"], all_flavor["E2phi_lower"] / 3)
    assert u.allclose(per_flavor["E2phi_90_upper"], all_flavor["E2phi_90_upper"] / 3)


def test_icecube_combined_quantity_conversion():
    dataset = get_dataset("icecube.combined_astrophysical_flux.2015")
    native = dataset.load_e2phi()
    phi = dataset.load_phi()

    assert u.allclose(phi["phi"], native["E2phi"] / native["energy"] ** 2)
    assert u.allclose(phi["phi_90_upper"], native["E2phi_90_upper"] / native["energy"] ** 2)
