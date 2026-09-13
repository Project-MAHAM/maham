from abc import ABC, abstractmethod
from hashlib import sha256
from pathlib import Path

from astropy.utils.data import download_file

from maham._core.metadata import DatasetMetadata, StorageMode


class Dataset(ABC):
    metadata: DatasetMetadata

    @property
    def id(self) -> str:
        return self.metadata.id

    def fetch(self, cache: bool = True, show_progress: bool = True) -> Path:
        source = self.metadata.source
        if source.storage == StorageMode.REMOTE:
            if source.url is None:
                raise ValueError(f"Remote dataset '{self.id}' has no source URL.")
            path = Path(download_file(source.url, cache=cache, show_progress=show_progress))
            self._verify_checksum(path)
            return path
        if source.storage == StorageMode.BUNDLED:
            raise NotImplementedError("Bundled dataset loading will be implemented when the first bundled dataset is added.")
        raise RuntimeError(f"Dataset '{self.id}' is external-only and cannot be downloaded automatically.")

    def _verify_checksum(self, path: Path) -> None:
        expected = self.metadata.source.sha256
        if expected is None:
            return
        digest = sha256()
        with path.open("rb") as f:
            for block in iter(lambda: f.read(1024 * 1024), b""):
                digest.update(block)
        actual = digest.hexdigest()
        if actual != expected:
            raise RuntimeError(f"Checksum mismatch for '{self.id}'. Expected {expected}, got {actual}.")

    @abstractmethod
    def load(self, cache: bool = True, show_progress: bool = True):
        pass
