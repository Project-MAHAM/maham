import pytest

from maham._core.metadata import ModelMetadata
from maham.models.base import Model
from maham.models.registry import get_model, list_models, register_model


@register_model
class RegistryTestModel(Model):
    metadata = ModelMetadata(id="test.registry.model", title="Registry test model", messenger="neutrino", model_type="flux", family="test")


def test_model_registry_lookup():
    model = get_model("test.registry.model")
    assert model.id == "test.registry.model"


def test_model_registry_filter():
    models = list_models(messenger="neutrino", model_type="flux", family="test")
    assert any(model.id == "test.registry.model" for model in models)


def test_unknown_model():
    with pytest.raises(KeyError):
        get_model("test.does.not.exist")
