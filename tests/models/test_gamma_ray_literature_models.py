import astropy.units as u
import numpy as np
from maham.models import get_model, list_models

def test_gamma_ray_source_environment_registry():
    models = list_models(messenger="gamma_ray", model_type="flux", family="source_environment")
    assert {model.id for model in models} == {"gamma_ray.source_environment.km3net_blazar_population_2026_best_fit", "gamma_ray.source_environment.ajello_blazar_population_2015"}

def test_km3net_blazar_gamma_2026():
    model = get_model("gamma_ray.source_environment.km3net_blazar_population_2026_best_fit")
    table = model.load_e2phi()
    assert model.metadata.source.provenance.value == "digitized"
    assert model.metadata.paper.doi == "10.1088/1475-7516/2026/03/033"
    assert len(table) == 85
    assert np.all(np.diff(table["energy"].to_value(u.GeV)) > 0)
    assert np.all(table["E2phi"].value > 0)
    assert np.isnan(model.evaluate(1e5 * u.GeV).value)

def test_ajello_blazar_gamma_2015_band():
    model = get_model("gamma_ray.source_environment.ajello_blazar_population_2015")
    table = model.load_e2phi()
    assert model.metadata.source.provenance.value == "digitized"
    assert model.metadata.paper.doi == "10.1088/2041-8205/800/2/L27"
    assert len(table) == 15
    assert np.all(table["E2phi_lower"] <= table["E2phi"])
    assert np.all(table["E2phi"] <= table["E2phi_upper"])
