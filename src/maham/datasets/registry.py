from maham._core.metadata import DatasetMetadata
from maham.datasets.base import Dataset


_REGISTRY: dict[str, type[Dataset]] = {}


def register_dataset(cls: type[Dataset]) -> type[Dataset]:
    dataset_id = cls.metadata.id
    if dataset_id in _REGISTRY:
        raise ValueError(f"Dataset '{dataset_id}' is already registered.")
    _REGISTRY[dataset_id] = cls
    return cls


def get_dataset(dataset_id: str) -> Dataset:
    try:
        cls = _REGISTRY[dataset_id]
    except KeyError as exc:
        available = ", ".join(sorted(_REGISTRY))
        raise KeyError(f"Unknown dataset '{dataset_id}'. Available datasets: {available or 'none'}") from exc
    return cls()


def list_datasets(experiment: str | None = None, messenger: str | None = None, data_type: str | None = None) -> tuple[DatasetMetadata, ...]:
    datasets = [cls.metadata for cls in _REGISTRY.values()]
    if experiment is not None:
        datasets = [d for d in datasets if d.experiment.lower() == experiment.lower()]
    if messenger is not None:
        datasets = [d for d in datasets if d.messenger.lower() == messenger.lower()]
    if data_type is not None:
        datasets = [d for d in datasets if d.data_type.lower() == data_type.lower()]
    return tuple(sorted(datasets, key=lambda d: d.id))
