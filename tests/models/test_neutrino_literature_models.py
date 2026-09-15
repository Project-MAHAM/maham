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
    "neutrino.cosmogenic.kuznetsov_petrov_savchenko_2026_best_fit": 919,
    "neutrino.cosmogenic.kuznetsov_petrov_savchenko_2026_local_min": 787,
    "neutrino.cosmogenic.yoshida_meier_2026_no_evolution": 80,
    "neutrino.cosmogenic.yoshida_meier_2026_log_normal": 86,
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

DERIVED_COSMOGENIC = {
    "neutrino.cosmogenic.kuznetsov_petrov_savchenko_2026_best_fit",
    "neutrino.cosmogenic.kuznetsov_petrov_savchenko_2026_local_min",
}

DIGITIZED_COSMOGENIC = {
    "neutrino.cosmogenic.yoshida_meier_2026_no_evolution",
    "neutrino.cosmogenic.yoshida_meier_2026_log_normal",
}

ALL_FLAVOR_COSMOGENIC = DIGITIZED_COSMOGENIC


@pytest.mark.parametrize(("model_id", "n_points"), {**COSMOGENIC, **SOURCE_ENVIRONMENT}.items())
def test_literature_model_native_data(model_id, n_points):
    model = get_model(model_id)
    table = model.load()

    assert len(table) == n_points
    assert table.meta["quantity"] == "E2phi"
    expected_flavor = "all_flavor" if model_id in ALL_FLAVOR_COSMOGENIC else "per_flavor"
    assert table.meta["flavor_convention"] == expected_flavor
    assert table.meta["spectral_kind"] == "differential_intensity"
    assert table.meta["solid_angle_convention"] == "diffuse"
    assert np.all(np.diff(table["energy"].to_value(u.GeV)) > 0)
    assert np.all(np.isfinite(table["E2phi"].value))
    assert np.all(table["E2phi"].value > 0)


def test_cosmogenic_registry_membership():
    models = list_models(messenger="neutrino", model_type="flux", family="cosmogenic")
    assert len(models) == 14
    assert {model.id for model in models} == set(COSMOGENIC)


def test_source_environment_registry_membership():
    models = list_models(messenger="neutrino", model_type="flux", family="source_environment")
    assert len(models) == 8
    assert {model.id for model in models} == set(SOURCE_ENVIRONMENT)


def test_km3net_curated_models_have_curated_provenance():
    model_ids = (set(COSMOGENIC) - DERIVED_COSMOGENIC - DIGITIZED_COSMOGENIC) | set(SOURCE_ENVIRONMENT)
    for model_id in model_ids:
        model = get_model(model_id)
        assert model.metadata.source.provenance.value == "curated_database"
        assert model.metadata.data_reference.doi == "10.5281/zenodo.14860165"


@pytest.mark.parametrize("model_id", sorted(DERIVED_COSMOGENIC))
def test_recent_cosmogenic_models_have_derived_provenance(model_id):
    model = get_model(model_id)
    assert model.metadata.source.provenance.value == "derived"
    assert model.metadata.paper.doi == "10.1134/S0021364025610061"
    assert model.metadata.data_reference.url == "https://github.com/82492749123082/KM3-230213A_UHECR_TA"


@pytest.mark.parametrize("model_id", sorted(DIGITIZED_COSMOGENIC))
def test_yoshida_meier_2026_models_have_digitized_provenance(model_id):
    model = get_model(model_id)
    assert model.metadata.source.provenance.value == "digitized"
    assert model.metadata.source.storage.value == "bundled"
    assert model.metadata.paper.doi == "10.1103/ljz7-phzv"
    assert model.metadata.data_reference.url == "https://arxiv.org/src/2604.14535"
    assert model.metadata.flavor_convention == "all_flavor"


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


@pytest.mark.parametrize(
    ("model_id", "n_points", "last_energy", "first_flux", "last_flux"),
    [
        ("neutrino.cosmogenic.kuznetsov_petrov_savchenko_2026_best_fit", 919, 2.707e11, 4.369e-12, 2.052e-16),
        ("neutrino.cosmogenic.kuznetsov_petrov_savchenko_2026_local_min", 787, 3.217e10, 3.547e-13, 2.481e-14),
    ],
)
def test_kuznetsov_petrov_savchenko_2026_exports(model_id, n_points, last_energy, first_flux, last_flux):
    model = get_model(model_id)
    table = model.load_e2phi()
    flux_unit = u.GeV / (u.cm**2 * u.s * u.sr)

    assert len(table) == n_points
    assert u.isclose(table["energy"][0], 1.0e5 * u.GeV)
    assert u.isclose(table["energy"][-1], last_energy * u.GeV)
    assert u.isclose(table["E2phi"][0], first_flux * flux_unit, rtol=1e-12)
    assert u.isclose(table["E2phi"][-1], last_flux * flux_unit, rtol=1e-12)


@pytest.mark.parametrize(
    ("model_id", "outside_energy"),
    [
        ("neutrino.cosmogenic.kuznetsov_petrov_savchenko_2026_best_fit", 2.751e11),
        ("neutrino.cosmogenic.kuznetsov_petrov_savchenko_2026_local_min", 3.270e10),
    ],
)
def test_kuznetsov_petrov_savchenko_2026_does_not_expose_negative_spline_tail(model_id, outside_energy):
    model = get_model(model_id)
    value = model.evaluate(outside_energy * u.GeV)
    assert np.isnan(value.value)


@pytest.mark.parametrize(
    ("model_id", "n_points", "first_energy", "last_energy", "peak_energy", "peak_flux"),
    [
        ("neutrino.cosmogenic.yoshida_meier_2026_no_evolution", 80, 4.276428464384e3, 2.349859391796e8, 3.900036360406e7, 3.980585992125e-9),
        ("neutrino.cosmogenic.yoshida_meier_2026_log_normal", 86, 1.866502680028e3, 2.349859391796e8, 4.477350682291e7, 1.421221803347e-8),
    ],
)
def test_yoshida_meier_2026_digitized_curves(model_id, n_points, first_energy, last_energy, peak_energy, peak_flux):
    model = get_model(model_id)
    table = model.load_e2phi()
    flux_unit = u.GeV / (u.cm**2 * u.s * u.sr)
    peak = int(np.argmax(table["E2phi"]))

    assert len(table) == n_points
    assert table.meta["flavor_convention"] == "all_flavor"
    assert u.isclose(table["energy"][0], first_energy * u.GeV, rtol=1e-12)
    assert u.isclose(table["energy"][-1], last_energy * u.GeV, rtol=1e-12)
    assert u.isclose(table["energy"][peak], peak_energy * u.GeV, rtol=1e-12)
    assert u.isclose(table["E2phi"][peak], peak_flux * flux_unit, rtol=1e-12)


@pytest.mark.parametrize(
    ("model_id", "outside_energy"),
    [
        ("neutrino.cosmogenic.yoshida_meier_2026_no_evolution", 3.0e8),
        ("neutrino.cosmogenic.yoshida_meier_2026_log_normal", 3.0e8),
    ],
)
def test_yoshida_meier_2026_does_not_extrapolate(model_id, outside_energy):
    value = get_model(model_id).evaluate(outside_energy * u.GeV)
    assert np.isnan(value.value)
