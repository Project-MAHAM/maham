from io import BytesIO
from zipfile import ZipFile

import astropy.units as u
import numpy as np
from astropy.table import QTable, Table

from maham._core.metadata import DataSource, DatasetMetadata, ProvenanceType, Reference, StorageMode
from maham.datasets.registry import register_dataset
from maham.datasets.spectra.neutrino.base import NeutrinoSpectrumDataset


SOURCE_URL = "https://icecube.wisc.edu/data-releases/20161115_A_combined_maximum-likelihood_analysis_of_the_astrophysical_neutrino_flux.zip"
SOURCE_SHA256 = "8e32d5c7aabe14c0b1f43e551c589f58cfeefc7c799b283e44f2eb376c814fd2"


def _loadtxt_member(zf, name):
    return np.loadtxt(BytesIO(zf.read(name)), skiprows=2)


def _crossing(x1, y1, x2, y2, target):
    return x1 + (target - y1) * (x2 - x1) / (y2 - y1)


def _profile_interval(normalization, nll, delta_threshold):
    normalization = np.asarray(normalization, dtype=float)
    nll = np.asarray(nll, dtype=float)
    minimum_index = int(np.argmin(nll))
    delta = nll - nll[minimum_index]

    if np.isclose(normalization[0], 0.0) and delta[0] <= delta_threshold:
        lower = normalization[0]
    else:
        lower = None
        for i in range(minimum_index - 1, -1, -1):
            if delta[i] >= delta_threshold and delta[i + 1] <= delta_threshold:
                lower = _crossing(normalization[i], delta[i], normalization[i + 1], delta[i + 1], delta_threshold)
                break
        if lower is None:
            raise RuntimeError("Profile likelihood scan does not bracket the lower confidence bound.")

    upper = None
    for i in range(minimum_index, len(normalization) - 1):
        if delta[i] <= delta_threshold and delta[i + 1] >= delta_threshold:
            upper = _crossing(normalization[i], delta[i], normalization[i + 1], delta[i + 1], delta_threshold)
            break
    if upper is None:
        raise RuntimeError("Profile likelihood scan does not bracket the upper confidence bound.")

    return lower, upper

@register_dataset
class IceCubeCombinedAstrophysicalFlux2015(NeutrinoSpectrumDataset):
    metadata = DatasetMetadata(
        id="icecube.combined_astrophysical_flux.2015",
        title="IceCube combined astrophysical neutrino spectrum",
        experiment="IceCube",
        messenger="neutrino",
        data_type="spectrum",
        description="Nine-bin all-flavor differential astrophysical neutrino spectrum from the combined IceCube maximum-likelihood analysis.",
        year=2015,
        confidence_level=0.6827,
        quantity="E2phi",
        spectral_kind="differential_intensity",
        energy_unit="GeV",
        value_unit="GeV cm-2 s-1 sr-1",
        flavor_convention="all_flavor",
        solid_angle_convention="per_sr",
        paper=Reference(
            title="A combined maximum-likelihood analysis of the high-energy astrophysical neutrino flux measured with IceCube",
            authors=("IceCube Collaboration",),
            year=2015,
            doi="10.1088/0004-637X/809/1/98",
        ),
        dataset_reference=Reference(
            title="A combined maximum-likelihood analysis of the astrophysical neutrino flux",
            authors=("IceCube Collaboration",),
            year=2016,
            doi="10.21234/B4WC7T",
        ),
        source=DataSource(
            provenance=ProvenanceType.OFFICIAL_RELEASE,
            storage=StorageMode.REMOTE,
            url=SOURCE_URL,
            sha256=SOURCE_SHA256,
        ),
        notes=(
            "The release contains nine logarithmically spaced energy bins between 1e4 and 1e7 GeV.",
            "The released normalization is all-flavor E2phi in units of 1e-8 GeV cm-2 s-1 sr-1.",
            "Equal nue, numu, and nutau contributions at Earth are assumed.",
            "The standardized energy is the geometric mean of each published energy bin.",
            "The 68% and 90% intervals are derived from the released profile likelihood scans.",
            "Bins with a zero best-fit normalization are marked as upper limits.",
        ),
        tags=("IceCube", "astrophysical neutrinos", "combined analysis", "differential spectrum", "flux"),
    )

    def load_raw(self, cache: bool = True, show_progress: bool = True) -> Table:
        archive = self.fetch(cache=cache, show_progress=show_progress)

        with ZipFile(archive) as zf:
            energy_edges = np.asarray(_loadtxt_member(zf, "energy_bins.txt"), dtype=float)
            bestfit = np.asarray(_loadtxt_member(zf, "bestfit.txt"), dtype=float)[:, 1]

            lower68, upper68, lower90, upper90 = [], [], [], []
            for bin_number in range(1, 10):
                scan = np.asarray(_loadtxt_member(zf, f"scan_{bin_number}.txt"), dtype=float)
                lo68, hi68 = _profile_interval(scan[:, 0], scan[:, 1], 1.0)
                lo90, hi90 = _profile_interval(scan[:, 0], scan[:, 1], 2.71)
                lower68.append(lo68)
                upper68.append(hi68)
                lower90.append(lo90)
                upper90.append(hi90)

        return Table(
            {
                "energy_min_GeV": energy_edges[:-1],
                "energy_max_GeV": energy_edges[1:],
                "E2phi": bestfit,
                "E2phi_lower": lower68,
                "E2phi_upper": upper68,
                "E2phi_90_lower": lower90,
                "E2phi_90_upper": upper90,
            }
        )

    def standardize(self, raw: Table) -> QTable:
        energy_min = np.asarray(raw["energy_min_GeV"], dtype=float)
        energy_max = np.asarray(raw["energy_max_GeV"], dtype=float)
        unit = 1e-8 * u.GeV / (u.cm**2 * u.s * u.sr)

        table = QTable()
        table["energy_min"] = energy_min * u.GeV
        table["energy_max"] = energy_max * u.GeV
        table["energy"] = np.sqrt(energy_min * energy_max) * u.GeV
        for column in ("E2phi", "E2phi_lower", "E2phi_upper", "E2phi_90_lower", "E2phi_90_upper"):
            table[column] = np.asarray(raw[column], dtype=float) * unit
        table["is_upper_limit"] = np.asarray(raw["E2phi"], dtype=float) == 0.0

        table.meta["dataset_id"] = self.metadata.id
        table.meta["quantity"] = self.metadata.quantity
        table.meta["flavor_convention"] = self.metadata.flavor_convention
        table.meta["solid_angle_convention"] = self.metadata.solid_angle_convention
        table.meta["confidence_level"] = self.metadata.confidence_level
        table.meta["energy_definition"] = "geometric_mean_of_bin_edges"
        table.meta["interval_method"] = "profile_likelihood"
        table.meta["provenance"] = self.metadata.source.provenance.value
        return table
