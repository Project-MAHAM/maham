from dataclasses import dataclass
from enum import Enum


class ProvenanceType(str, Enum):
    OFFICIAL_RELEASE = "official_release"
    OFFICIAL_REPOSITORY = "official_repository"
    HEPDATA = "hepdata"
    ZENODO = "zenodo"
    AUTHOR_PROVIDED = "author_provided"
    DIGITIZED = "digitized"
    DERIVED = "derived"
    CURATED_DATABASE = "curated_database"


class StorageMode(str, Enum):
    BUNDLED = "bundled"
    REMOTE = "remote"
    EXTERNAL = "external"


@dataclass(frozen=True)
class Reference:
    title: str
    authors: tuple[str, ...] = ()
    year: int | None = None
    doi: str | None = None
    url: str | None = None
    citation: str | None = None


@dataclass(frozen=True)
class DataSource:
    provenance: ProvenanceType
    storage: StorageMode
    url: str | None = None
    path: str | None = None
    sha256: str | None = None
    archive_member: str | None = None
    archive_member_sha256: str | None = None
    archive_member_size: int | None = None


@dataclass(frozen=True)
class DatasetMetadata:
    id: str
    title: str
    experiment: str
    messenger: str
    data_type: str
    source: DataSource
    description: str = ""
    year: int | None = None
    paper: Reference | None = None
    dataset_reference: Reference | None = None
    confidence_level: float | None = None
    quantity: str | None = None
    spectral_kind: str | None = None
    energy_unit: str | None = None
    value_unit: str | None = None
    flavor_convention: str | None = None
    solid_angle_convention: str | None = None
    notes: tuple[str, ...] = ()
    tags: tuple[str, ...] = ()
