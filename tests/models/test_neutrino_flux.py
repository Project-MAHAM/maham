import astropy.units as u
import numpy as np

from astropy.table import QTable

from maham._core.metadata import ModelMetadata
from maham.models.flux.neutrino import NeutrinoFluxModel


class SyntheticFluxModel(NeutrinoFluxModel):
    metadata = ModelMetadata(
        id="test.synthetic.neutrino_flux",
        title="Synthetic neutrino flux",
        messenger="neutrino",
        model_type="flux",
        family="test",
        quantity="E2phi",
        spectral_kind="differential_intensity",
        energy_unit="GeV",
        value_unit="GeV / (cm2 s sr)",
        flavor_convention="per_flavor",
        solid_angle_convention="diffuse",
    )

    def load_native(self, cache: bool = True, show_progress: bool = True) -> QTable:
        table = QTable()
        table["energy"] = np.array([1e3, 1e4, 1e5]) * u.GeV
        table["E2phi"] = np.array([1e-8, 1e-9, 1e-10]) * u.GeV / (u.cm**2 * u.s * u.sr)
        return table


def test_native_neutrino_flux():
    table = SyntheticFluxModel().load()
    assert table.meta["quantity"] == "E2phi"
    assert table.meta["flavor_convention"] == "per_flavor"
    assert u.allclose(table["E2phi"], [1e-8, 1e-9, 1e-10] * u.GeV / (u.cm**2 * u.s * u.sr))


def test_neutrino_flux_quantity_conversion():
    table = SyntheticFluxModel().load_phi()
    expected = np.array([1e-14, 1e-17, 1e-20]) / (u.GeV * u.cm**2 * u.s * u.sr)
    assert u.allclose(table["phi"], expected)


def test_neutrino_flux_flavor_conversion():
    table = SyntheticFluxModel().load_e2phi(flavor="all_flavor", flavor_assumption="equal")
    expected = np.array([3e-8, 3e-9, 3e-10]) * u.GeV / (u.cm**2 * u.s * u.sr)
    assert u.allclose(table["E2phi"], expected)


def test_neutrino_flux_loglog_interpolation():
    value = SyntheticFluxModel().evaluate(np.sqrt(1e3 * 1e4) * u.GeV)
    expected = np.sqrt(1e-8 * 1e-9) * u.GeV / (u.cm**2 * u.s * u.sr)
    assert u.allclose(value, expected)


def test_neutrino_flux_does_not_extrapolate():
    values = SyntheticFluxModel().evaluate(np.array([1e2, 1e6]) * u.GeV)
    assert np.all(np.isnan(values.value))
