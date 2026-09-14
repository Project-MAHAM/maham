import xml.etree.ElementTree as ET

import astropy.units as u
from astropy.table import QTable
from astropy.time import Time

from maham._core.metadata import DataSource, DatasetMetadata, ProvenanceType, Reference, StorageMode
from maham.datasets.base import Dataset
from maham.datasets.registry import register_dataset


SOURCE_URL = "https://raw.githubusercontent.com/KM3NeT/KM3-230213A-data/main/data/event/KM3-230213A_voevent.xml"
SOURCE_SHA256 = "f4671f968770dfde51933601e9db133170b0c18d2fd4602aca21607b7169eb92"
PAPER_DOI = "10.1038/s41586-024-08543-1"
DATA_DOI = "10.5281/zenodo.14860165"

@register_dataset
class KM3NeT230213A2025(Dataset):
    metadata = DatasetMetadata(
        id="km3net.km3_230213a.2025",
        title="KM3NeT ultra-high-energy neutrino event KM3-230213A",
        experiment="KM3NeT",
        messenger="neutrino",
        data_type="event",
        source=DataSource(
            provenance=ProvenanceType.OFFICIAL_REPOSITORY,
            storage=StorageMode.REMOTE,
            url=SOURCE_URL,
            sha256=SOURCE_SHA256,
        ),
        description="Event metadata for KM3-230213A from the official KM3NeT VOEvent.",
        year=2025,
        paper=Reference(title="Observation of an ultra-high-energy cosmic neutrino with KM3NeT", doi=PAPER_DOI),
        dataset_reference=Reference(title="Data for the KM3-230213A high energy event observation", doi=DATA_DOI),
        notes=("The VOEvent reports an energy of 120 PeV.",
            "Sky coordinates are provided in the ICRS frame.",
            "Directional containment radii are provided at 50%, 68%, 90%, and 99%.",
            "Detector coordinates correspond to the ARCA021 detector location.",
        ), tags=("KM3NeT", "KM3-230213A", "neutrino", "event", "ARCA"),)

    def load_raw(self, cache: bool = True, show_progress: bool = True) -> dict:
        path = self.fetch(cache=cache, show_progress=show_progress)
        root = ET.parse(path).getroot()

        params = {param.attrib["name"]: param.attrib["value"] for param in root.findall(".//What/Param")}
        observation = root.find(".//ObservationLocation")
        observatory = root.find(".//ObservatoryLocation")
        position2d = observation.find(".//Position2D")
        position3d = observatory.find(".//Position3D")

        return {
            "event_name": params["Identifier"],
            "instrument": params["Instrument"],
            "energy_pev": float(params["Energy"]),
            "time_utc": observation.findtext(".//ISOTime"),
            "ra_deg": float(position2d.findtext("Value2/C1")),
            "dec_deg": float(position2d.findtext("Value2/C2")),
            "angular_error_50_deg": float(position2d.findtext("Error2Radius50")),
            "angular_error_68_deg": float(position2d.findtext("Error2Radius68")),
            "angular_error_90_deg": float(position2d.findtext("Error2Radius90")),
            "angular_error_99_deg": float(position2d.findtext("Error2Radius99")),
            "detector_longitude_deg": float(position3d.findtext("Value3/C1")),
            "detector_latitude_deg": float(position3d.findtext("Value3/C2")),
            "detector_elevation_m": float(position3d.findtext("Value3/C3")),
        }

    def load(self, cache: bool = True, show_progress: bool = True) -> QTable:
        return self.standardize(self.load_raw(cache=cache, show_progress=show_progress))

    def standardize(self, raw: dict) -> QTable:
        table = QTable()
        table["event_name"] = [raw["event_name"]]
        table["instrument"] = [raw["instrument"]]
        table["time"] = Time([raw["time_utc"]], format="isot", scale="utc")
        table["energy"] = [raw["energy_pev"]] * u.PeV
        table["ra"] = [raw["ra_deg"]] * u.deg
        table["dec"] = [raw["dec_deg"]] * u.deg
        table["angular_error_50"] = [raw["angular_error_50_deg"]] * u.deg
        table["angular_error_68"] = [raw["angular_error_68_deg"]] * u.deg
        table["angular_error_90"] = [raw["angular_error_90_deg"]] * u.deg
        table["angular_error_99"] = [raw["angular_error_99_deg"]] * u.deg
        table["detector_longitude"] = [raw["detector_longitude_deg"]] * u.deg
        table["detector_latitude"] = [raw["detector_latitude_deg"]] * u.deg
        table["detector_elevation"] = [raw["detector_elevation_m"]] * u.m
        table.meta["dataset_id"] = self.metadata.id
        table.meta["coordinate_frame"] = "ICRS"
        table.meta["time_scale"] = "UTC"
        table.meta["event_role"] = "observation"
        table.meta["energy_source"] = "VOEvent"
        return table
