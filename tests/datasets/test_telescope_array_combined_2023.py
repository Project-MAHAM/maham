import astropy.units as u
import numpy as np

from maham.datasets import get_dataset, list_datasets


def test_telescope_array_registered():
    assert "telescope_array.combined_spectrum.2023" in [metadata.id for metadata in list_datasets()]


def test_telescope_array_metadata():
    dataset = get_dataset("telescope_array.combined_spectrum.2023")
    assert dataset.metadata.experiment == "Telescope Array"
    assert dataset.metadata.messenger == "cosmic_ray"
    assert dataset.metadata.data_type == "spectrum"
    assert dataset.metadata.quantity == "E3J"
    assert dataset.metadata.spectral_kind == "differential_intensity"
    assert dataset.metadata.source.sha256 == "ef53895480c1990699a15ae30fc44d1588c50eb4cc5713191a6468edab87a393"


def test_telescope_array_raw():
    dataset = get_dataset("telescope_array.combined_spectrum.2023")
    raw = dataset.load_raw()
    assert len(raw) == 21
    assert np.count_nonzero(raw["is_upper_limit"]) == 1
    assert np.isclose(raw["log10_energy_eV"][0], 18.44960387828612)
    assert np.isclose(raw["log10_energy_eV"][-1], 20.449285287536043)
    assert bool(raw["is_upper_limit"][-1])


def test_telescope_array_standardized():
    dataset = get_dataset("telescope_array.combined_spectrum.2023")
    table = dataset.load()
    unit = u.eV**2 / (u.m**2 * u.s * u.sr)

    assert len(table) == 21
    assert table.meta["quantity"] == "E3J"
    assert table.meta["provenance"] == "digitized"
    assert u.allclose(table["energy"][0], 2.8158134450480763e18 * u.eV)
    assert u.allclose(table["E3J"][0], 1.652875551458479e24 * unit)
    assert np.isnan(table["E3J_lower"][0].value)
    assert not bool(table["has_resolved_vertical_error"][0])
    assert bool(table["is_upper_limit"][-1])


def test_telescope_array_digitized_error():
    dataset = get_dataset("telescope_array.combined_spectrum.2023")
    table = dataset.load()
    unit = u.eV**2 / (u.m**2 * u.s * u.sr)
    index = 9

    central = 2.2919815661075344e24
    lower_error = 1.0655741983547617e23
    upper_error = 1.0413611958671165e23

    assert bool(table["has_resolved_vertical_error"][index])
    assert u.allclose(table["E3J"][index], central * unit)
    assert u.allclose(table["E3J_lower"][index], (central - lower_error) * unit)
    assert u.allclose(table["E3J_upper"][index], (central + upper_error) * unit)


def test_telescope_array_upper_limit():
    dataset = get_dataset("telescope_array.combined_spectrum.2023")
    table = dataset.load()
    unit = u.eV**2 / (u.m**2 * u.s * u.sr)

    assert bool(table["is_upper_limit"][-1])
    assert u.allclose(table["E3J"][-1], 1.1168962538478597e24 * unit)
    assert np.isnan(table["E3J_lower"][-1].value)
    assert np.isnan(table["E3J_upper"][-1].value)


def test_telescope_array_common_flux_view():
    dataset = get_dataset("telescope_array.combined_spectrum.2023")
    table = dataset.load_e2phi()

    assert len(table) == 21
    assert table.meta["native_quantity"] == "E3J"
    assert table.meta["quantity"] == "E2phi"
    assert "E2phi" in table.colnames
    assert "E2phi_lower" in table.colnames
    assert "E2phi_upper" in table.colnames
    assert bool(table["is_upper_limit"][-1])
