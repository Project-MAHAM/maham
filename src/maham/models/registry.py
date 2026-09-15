from maham._core.metadata import ModelMetadata
from maham.models.base import Model


_REGISTRY: dict[str, type[Model]] = {}


def register_model(cls: type[Model]) -> type[Model]:
    model_id = cls.metadata.id
    if model_id in _REGISTRY:
        raise ValueError(f"Model '{model_id}' is already registered.")
    _REGISTRY[model_id] = cls
    return cls


def get_model(model_id: str) -> Model:
    try:
        cls = _REGISTRY[model_id]
    except KeyError as exc:
        available = ", ".join(sorted(_REGISTRY))
        raise KeyError(f"Unknown model '{model_id}'. Available models: {available or 'none'}") from exc
    return cls()


def list_models(messenger: str | None = None, model_type: str | None = None, family: str | None = None) -> tuple[ModelMetadata, ...]:
    models = [cls.metadata for cls in _REGISTRY.values()]
    if messenger is not None:
        models = [m for m in models if m.messenger.lower() == messenger.lower()]
    if model_type is not None:
        models = [m for m in models if m.model_type.lower() == model_type.lower()]
    if family is not None:
        models = [m for m in models if m.family.lower() == family.lower()]
    return tuple(sorted(models, key=lambda m: m.id))


def get_models(messenger: str | None = None, model_type: str | None = None, family: str | None = None) -> tuple[Model, ...]:
    return tuple(get_model(metadata.id) for metadata in list_models(messenger=messenger, model_type=model_type, family=family))
