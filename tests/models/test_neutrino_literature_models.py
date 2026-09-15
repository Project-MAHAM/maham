import astropy.units as u
import numpy as np
import pytest

from maham.models import get_model, list_models


COSMOGENIC = {
    "neutrino.cosmogenic.aloisio_2015": 45,
    "neutrino.cosmogenic.berat_2024": 44,
    "neutrino.cosmogenic.boncioli_2019": 60,
    "neutrino.cosmogenic.condorelli_2023": 45,
    "neutrino.cosmogenic.ehlert_2024": 57,
    "neutrino.cosmogenic.muzio_farrar_2023": 31,
    "neutrino.cosmogenic.muzio_unger_wissel_2023": 61,
    "neutrino.cosmogenic.auger_2023": 65,
    "neutrino.cosmogenic.heinze_2019": 22,
    "neutrino.cosmogenic.zhang_murase_2019": 72,
}

SOURCE_ENVIRONMENT = {
    "neutrino.source_environment.boncioli_llgrb_2019": 70,
    "neutrino.source_environment.fang_pulsar_2014": 86,
    "neutrino.source_environment.rodrigues_agn_2021": 161,
    "neutrino.source_environment.rodrigues_bllac_2024": 59,
    "neutrino.source_environment.rodrigues_fsrq_2024": 62,
    "neutrino.source_environment.tamborra_llgrb_2015": 86,
    "neutrino.source_environment.tamborra_sgrb_2015": 77,
    "neutrino.source_environment.winter_tde_2023": 75,
}


@pytest.mark.parametrize(("model_id", "n_points"), {**COSMOGENIC, **SOURCE_ENVIRONMENT}.items())
def test_literature_model_native_data(model_id, n_points):
    model = get_model(model_id)
    table = model.load()

    assert len(table) == n_points
    assert table.meta["quantity"] == "E2phi"
    assert table.meta["flavor_convention"] == "per_flavor"
    assert table.meta["spectral_kind"] == "differential_intensity"
    assert table.meta["solid_angle_convention"] == "diffuse"
    assert np.all(np.diff(table["energy"].to_value(u.GeV)) > 0)
    assert np.all(np.isfinite(table["E2phi"].value))
    assert np.all(table["E2phi"].value > 0)


def test_cosmogenic_registry_membership():
    models = list_models(messenger="neutrino", model_type="flux", family="cosmogenic")
    assert len(models) == 10
    assert {model.id for model in models} == set(COSMOGENIC)


def test_source_environment_registry_membership():
    models = list_models(messenger="neutrino", model_type="flux", family="source_environment")
    assert len(models) == 8
    assert {model.id for model in models} == set(SOURCE_ENVIRONMENT)


@pytest.mark.parametrize("family", ("cosmogenic", "source_environment"))
def test_family_models_have_curated_provenance(family):
    models = list_models(messenger="neutrino", model_type="flux", family=family)

    for model in models:
        assert model.source.provenance.value == "curated_database"
        assert model.data_reference.doi == "10.5281/zenodo.14860165"


def test_literature_model_all_flavor_conversion():
    model = get_model("neutrino.cosmogenic.aloisio_2015")
    native = model.load_e2phi()
    all_flavor = model.load_e2phi(flavor="all_flavor", flavor_assumption="equal")
    assert u.allclose(all_flavor["E2phi"], 3.0 * native["E2phi"])


def test_ehlert_duplicate_energy_is_collapsed_in_native_log_space():
    model = get_model("neutrino.cosmogenic.ehlert_2024")
    table = model.load_e2phi()
    energy = 12918150998.348774 * u.GeV
    index = np.flatnonzero(np.isclose(table["energy"].to_value(u.GeV), energy.to_value(u.GeV), rtol=1e-12, atol=0.0))
    assert len(index) == 1
    expected = 10.0 ** ((-10.8373857391 - 10.6597490987) / 2.0) * u.GeV / (u.cm**2 * u.s * u.sr)
    assert u.isclose(table["E2phi"][index[0]], expected, rtol=1e-12)
