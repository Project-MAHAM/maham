from pathlib import Path
from hashlib import sha256

from astropy.utils.data import download_file

from maham._core.metadata import ModelMetadata, StorageMode


class Model:
    metadata: ModelMetadata

    @property
    def id(self) -> str:
        return self.metadata.id

    def fetch(self, path: str | Path | None = None, cache: bool = True, show_progress: bool = True) -> Path:
        source = self.metadata.source
        if source is None:
            raise ValueError(f"Model '{self.id}' has no tabulated data source.")

        if source.storage == StorageMode.REMOTE:
            if source.url is None:
                raise ValueError(f"Remote model '{self.id}' has no source URL.")
            downloaded = Path(download_file(source.url, cache=cache, show_progress=show_progress))
            self._verify_checksum(downloaded)
            return downloaded

        if source.storage == StorageMode.BUNDLED:
            if source.path is None:
                raise ValueError(f"Bundled model '{self.id}' has no source path.")
            bundled = Path(__file__).resolve().parents[1] / source.path
            if not bundled.is_file():
                raise FileNotFoundError(f"Bundled source file for '{self.id}' does not exist: {bundled}")
            self._verify_checksum(bundled)
            return bundled

        if source.storage == StorageMode.EXTERNAL:
            if path is None:
                raise ValueError(f"Model '{self.id}' is external-only. Provide the local source file with path=...")
            local = Path(path).expanduser().resolve()
            if not local.is_file():
                raise FileNotFoundError(f"External source file for '{self.id}' does not exist: {local}")
            self._verify_checksum(local)
            return local

        raise RuntimeError(f"Unsupported storage mode for model '{self.id}': {source.storage}")

    def _verify_checksum(self, path: Path) -> None:
        source = self.metadata.source
        if source is None or source.sha256 is None:
            return

        digest = sha256()
        with path.open("rb") as f:
            for block in iter(lambda: f.read(1024 * 1024), b""):
                digest.update(block)

        actual = digest.hexdigest()
        if actual != source.sha256:
            raise RuntimeError(f"Checksum mismatch for '{self.id}'. Expected {source.sha256}, got {actual}.")
