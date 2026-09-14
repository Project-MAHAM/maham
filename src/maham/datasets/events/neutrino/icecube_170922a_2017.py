import astropy.units as u
import pandas as pd

from astropy.table import QTable
from astropy.time import Time

from maham._core.metadata import DataSource, DatasetMetadata, ProvenanceType, Reference, StorageMode
from maham.datasets.base import Dataset
from maham.datasets.registry import register_dataset


DATA_PATH = "data/datasets/events/neutrino/icecube_170922a_2017.csv"
DATA_SHA256 = "11bf57cc70ef36799a4ba90ba2b44f7849d7ed45fe268ace16b30aa6a816049a"
PAPER_DOI = "10.1126/science.aat1378"
DATA_DOI = "10.21234/B4KS6S"


@register_dataset
class IceCube170922A2017(Dataset):
    metadata = DatasetMetadata(
        id="icecube.170922a.2017",
        title="IceCube high-energy neutrino alert IceCube-170922A",
        experiment="IceCube",
        messenger="neutrino",
        data_type="event",
        source=DataSource(provenance=ProvenanceType.PUBLISHED_TABLE, storage=StorageMode.BUNDLED, path=DATA_PATH, sha256=DATA_SHA256),
        description="Single-event record for IceCube-170922A, the 2017 high-energy track associated with TXS 0506+056.",
        year=2017,
        paper=Reference(title="Multimessenger observations of a flaring blazar coincident with high-energy neutrino IceCube-170922A", doi=PAPER_DOI),
        dataset_reference=Reference(title="IceCube catalog of alert events up through IceCube-170922A", doi=DATA_DOI),
        notes=(
            "The event was selected by the IceCube extremely-high-energy track alert stream.",
            "The reconstructed direction is RA=77.43 deg and Dec=5.72 deg in J2000/ICRS coordinates.",
            "Directional uncertainties are asymmetric 90% containment ranges.",
            "The traversing muon deposited 23.7 +/- 2.8 TeV in IceCube.",
            "The most-probable parent-neutrino energy is 290 TeV for an assumed E^-2.13 astrophysical nu_mu spectrum.",
            "The corresponding 90% neutrino-energy interval is 183 TeV to 4.3 PeV.",
            "The reported signalness is 56.5%.",
            "TXS 0506+056 lies within the directional uncertainty region and is retained as the associated source.",
            "This dataset represents an event, not a source-flux measurement.",
        ),
        tags=("IceCube", "IceCube-170922A", "TXS 0506+056", "neutrino", "event", "EHE", "track"),
    )

    def load_raw(self, cache: bool = True, show_progress: bool = True) -> dict:
        path = self.fetch(cache=cache, show_progress=show_progress)
        row = pd.read_csv(path).iloc[0]
        return {
            "event_name": row["event_name"],
            "time_utc": row["time_utc"],
            "mjd_catalog": float(row["mjd_catalog"]),
            "topology": row["topology"],
            "selection": row["selection"],
            "ra_deg": float(row["ra_deg"]),
            "ra_err_minus_deg": float(row["ra_err_minus_deg"]),
            "ra_err_plus_deg": float(row["ra_err_plus_deg"]),
            "dec_deg": float(row["dec_deg"]),
            "dec_err_minus_deg": float(row["dec_err_minus_deg"]),
            "dec_err_plus_deg": float(row["dec_err_plus_deg"]),
            "deposited_muon_energy_TeV": float(row["deposited_muon_energy_TeV"]),
            "deposited_muon_energy_err_TeV": float(row["deposited_muon_energy_err_TeV"]),
            "neutrino_energy_mode_TeV": float(row["neutrino_energy_mode_TeV"]),
            "neutrino_energy_90_lower_TeV": float(row["neutrino_energy_90_lower_TeV"]),
            "neutrino_energy_90_upper_TeV": float(row["neutrino_energy_90_upper_TeV"]),
            "neutrino_spectral_index": float(row["neutrino_spectral_index"]),
            "signalness": float(row["signalness"]),
            "associated_source": row["associated_source"],
        }

    def load(self, cache: bool = True, show_progress: bool = True) -> QTable:
        return self.standardize(self.load_raw(cache=cache, show_progress=show_progress))

    def standardize(self, raw: dict) -> QTable:
        table = QTable()
        table["event_name"] = [raw["event_name"]]
        table["instrument"] = ["IceCube"]
        table["time"] = Time([raw["time_utc"]], format="isot", scale="utc")
        table["mjd_catalog"] = [raw["mjd_catalog"]]
        table["topology"] = [raw["topology"]]
        table["selection"] = [raw["selection"]]
        table["energy"] = [raw["neutrino_energy_mode_TeV"]] * u.TeV
        table["energy_lower"] = [raw["neutrino_energy_90_lower_TeV"]] * u.TeV
        table["energy_upper"] = [raw["neutrino_energy_90_upper_TeV"]] * u.TeV
        table["ra"] = [raw["ra_deg"]] * u.deg
        table["ra_error_minus"] = [raw["ra_err_minus_deg"]] * u.deg
        table["ra_error_plus"] = [raw["ra_err_plus_deg"]] * u.deg
        table["dec"] = [raw["dec_deg"]] * u.deg
        table["dec_error_minus"] = [raw["dec_err_minus_deg"]] * u.deg
        table["dec_error_plus"] = [raw["dec_err_plus_deg"]] * u.deg
        table["deposited_muon_energy"] = [raw["deposited_muon_energy_TeV"]] * u.TeV
        table["deposited_muon_energy_error"] = [raw["deposited_muon_energy_err_TeV"]] * u.TeV
        table["signalness"] = [raw["signalness"]]
        table["associated_source"] = [raw["associated_source"]]
        table.meta["dataset_id"] = self.metadata.id
        table.meta["coordinate_frame"] = "ICRS"
        table.meta["time_scale"] = "UTC"
        table.meta["event_role"] = "observation"
        table.meta["energy_definition"] = "most_probable_parent_neutrino_energy"
        table.meta["energy_confidence_level"] = 0.90
        table.meta["energy_spectral_assumption"] = "E^-2.13"
        return table
