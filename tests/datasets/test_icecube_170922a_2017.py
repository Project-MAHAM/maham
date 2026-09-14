import astropy.units as u
import numpy as np

from maham.datasets import get_dataset


def test_icecube_170922a_metadata():
    dataset = get_dataset("icecube.170922a.2017")
    assert dataset.metadata.experiment == "IceCube"
    assert dataset.metadata.messenger == "neutrino"
    assert dataset.metadata.data_type == "event"
    assert dataset.metadata.source.sha256 == "11bf57cc70ef36799a4ba90ba2b44f7849d7ed45fe268ace16b30aa6a816049a"


def test_icecube_170922a_raw():
    raw = get_dataset("icecube.170922a.2017").load_raw()
    assert raw["event_name"] == "IceCube-170922A"
    assert raw["time_utc"] == "2017-09-22T20:54:30.43"
    assert np.isclose(raw["mjd_catalog"], 58018.871)
    assert raw["topology"] == "track"
    assert raw["selection"] == "EHE"
    assert np.isclose(raw["ra_deg"], 77.43)
    assert np.isclose(raw["dec_deg"], 5.72)
    assert np.isclose(raw["signalness"], 0.565)


def test_icecube_170922a_standardized():
    table = get_dataset("icecube.170922a.2017").load()
    assert len(table) == 1
    assert table["event_name"][0] == "IceCube-170922A"
    assert table["instrument"][0] == "IceCube"
    assert u.allclose(table["energy"][0], 290.0 * u.TeV)
    assert u.allclose(table["energy_lower"][0], 183.0 * u.TeV)
    assert u.allclose(table["energy_upper"][0], 4.3 * u.PeV)
    assert u.allclose(table["ra"][0], 77.43 * u.deg)
    assert u.allclose(table["dec"][0], 5.72 * u.deg)
    assert table["associated_source"][0] == "TXS 0506+056"


def test_icecube_170922a_directional_uncertainty():
    table = get_dataset("icecube.170922a.2017").load()
    assert u.allclose(table["ra_error_minus"][0], 0.65 * u.deg)
    assert u.allclose(table["ra_error_plus"][0], 0.95 * u.deg)
    assert u.allclose(table["dec_error_minus"][0], 0.30 * u.deg)
    assert u.allclose(table["dec_error_plus"][0], 0.50 * u.deg)


def test_icecube_170922a_energy_provenance():
    table = get_dataset("icecube.170922a.2017").load()
    assert u.allclose(table["deposited_muon_energy"][0], 23.7 * u.TeV)
    assert u.allclose(table["deposited_muon_energy_error"][0], 2.8 * u.TeV)
    assert table.meta["energy_definition"] == "most_probable_parent_neutrino_energy"
    assert np.isclose(table.meta["energy_confidence_level"], 0.90)
    assert table.meta["energy_spectral_assumption"] == "E^-2.13"
