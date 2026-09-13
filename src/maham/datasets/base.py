from abc import ABC, abstractmethod
from hashlib import sha256
from pathlib import Path
from zipfile import ZipFile

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

    def _read_archive_member(self, archive: Path) -> bytes:
        source = self.metadata.source
        member = source.archive_member
        if member is None:
            raise ValueError(f"Dataset '{self.id}' has no archive member defined.")
        with ZipFile(archive) as zf:
            matches = [name for name in zf.namelist() if name == member or name.endswith(f"/{member}")]
            if len(matches) != 1:
                raise RuntimeError(f"Expected one '{member}' in archive, found {len(matches)}.")
            data = zf.read(matches[0])
        expected_size = source.archive_member_size
        if expected_size is not None and len(data) != expected_size:
            raise RuntimeError(f"Archive member size mismatch for '{self.id}': expected {expected_size}, got {len(data)}.")
        expected_hash = source.archive_member_sha256
        if expected_hash is not None:
            actual_hash = sha256(data).hexdigest()
            if actual_hash != expected_hash:
                raise RuntimeError(f"Archive member checksum mismatch for '{self.id}'. Expected {expected_hash}, got {actual_hash}.")
        return data

    @abstractmethod
    def load(self, cache: bool = True, show_progress: bool = True):
        pass
