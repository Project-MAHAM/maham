from io import BytesIO
from zipfile import ZipFile

from astropy.table import Table

from maham._core.metadata import DataSource, DatasetMetadata, ProvenanceType, Reference, StorageMode
from maham.datasets.base import Dataset
from maham.datasets.registry import register_dataset


@register_dataset
class IceCubeGlashowFlux2021(Dataset):
    metadata = DatasetMetadata(
        id="icecube.glashow.flux.2021",
        title="IceCube Glashow resonance piecewise astrophysical neutrino flux",
        experiment="IceCube",
        messenger="neutrino",
        data_type="spectrum",
        description="Measured per-flavor astrophysical neutrino flux in three neutrino-energy bins accompanying the first Glashow resonance candidate.",
        year=2021,
        confidence_level=0.683,
        paper=Reference(
            title="Detection of a particle shower at the Glashow resonance with IceCube",
            authors=("IceCube Collaboration",),
            year=2021,
            doi="10.1038/s41586-021-03256-1",
        ),
        dataset_reference=Reference(
            title="IceCube data for the first Glashow resonance candidate",
            authors=("IceCube Collaboration",),
            year=2021,
            doi="10.21234/gr2021",
        ),
        source=DataSource(
            provenance=ProvenanceType.OFFICIAL_RELEASE,
            storage=StorageMode.REMOTE,
            url="https://icecube.wisc.edu/data-releases/20210310_IceCube_data_for_the_first_Glashow_resonance_candidate.zip",
            sha256="64c31773fe21b1dc6268da69f2f5427a8d22663b44fc4514a368385c1e455c88",
        ),
        tags=("IceCube", "Glashow resonance", "astrophysical neutrinos", "flux"),
    )

    archive_member = "piecewise.csv"

    def load(self, cache: bool = True, show_progress: bool = True) -> Table:
        archive = self.fetch(cache=cache, show_progress=show_progress)

        with ZipFile(archive) as zf:
            names = zf.namelist()
            matches = [name for name in names if name.endswith(self.archive_member)]

            if len(matches) != 1:
                raise RuntimeError(
                    f"Expected one '{self.archive_member}' in archive, found {len(matches)}."
                )

            data = zf.read(matches[0])

        clean = b"\n".join(
            line for line in data.splitlines()
            if line.strip() and not line.lstrip().startswith(b"#")
        )

        return Table.read(BytesIO(clean), format="ascii.csv")
