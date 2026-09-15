import astropy.units as u
import numpy as np

from astropy.table import QTable

from maham._core.metadata import ModelMetadata
from maham.models.flux.neutrino import NeutrinoFluxModel, build_envelope


UNIT = u.GeV / (u.cm**2 * u.s * u.sr)


class EnvelopeModelA(NeutrinoFluxModel):
    metadata = ModelMetadata(id="test.envelope.a", title="Envelope model A", messenger="neutrino", model_type="flux", family="test", quantity="E2phi", spectral_kind="differential_intensity", energy_unit="GeV", value_unit="GeV / (cm2 s sr)", flavor_convention="per_flavor", solid_angle_convention="diffuse")

    def load_native(self, cache: bool = True, show_progress: bool = True) -> QTable:
        table = QTable()
        table["energy"] = np.array([1e4, 1e6]) * u.GeV
        table["E2phi"] = np.array([1e-9, 1e-9]) * UNIT
        return table


class EnvelopeModelB(NeutrinoFluxModel):
    metadata = ModelMetadata(id="test.envelope.b", title="Envelope model B", messenger="neutrino", model_type="flux", family="test", quantity="E2phi", spectral_kind="differential_intensity", energy_unit="GeV", value_unit="GeV / (cm2 s sr)", flavor_convention="per_flavor", solid_angle_convention="diffuse")

    def load_native(self, cache: bool = True, show_progress: bool = True) -> QTable:
        table = QTable()
        table["energy"] = np.array([1e5, 1e7]) * u.GeV
        table["E2phi"] = np.array([1e-8, 1e-8]) * UNIT
        return table


def test_model_envelope():
    energy = np.array([1e4, 1e5, 1e6, 1e7]) * u.GeV
    table = build_envelope((EnvelopeModelA(), EnvelopeModelB()), energy=energy)

    assert np.array_equal(table["n_models"], [1, 2, 2, 1])
    assert u.allclose(table["E2phi_lower"], np.array([1e-9, 1e-9, 1e-9, 1e-8]) * UNIT)
    assert u.allclose(table["E2phi_upper"], np.array([1e-9, 1e-8, 1e-8, 1e-8]) * UNIT)


def test_model_envelope_all_flavor():
    energy = np.array([1e5, 1e6]) * u.GeV
    table = build_envelope((EnvelopeModelA(), EnvelopeModelB()), energy=energy, flavor="all_flavor", flavor_assumption="equal")

    assert table.meta["flavor_convention"] == "all_flavor"
    assert u.allclose(table["E2phi_lower"], np.array([3e-9, 3e-9]) * UNIT)
    assert u.allclose(table["E2phi_upper"], np.array([3e-8, 3e-8]) * UNIT)
