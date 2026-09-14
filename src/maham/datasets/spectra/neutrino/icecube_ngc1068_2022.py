import astropy.units as u
import numpy as np
from astropy.table import QTable, Table

from maham._core.metadata import DataSource, DatasetMetadata, ProvenanceType, Reference, StorageMode
from maham.datasets.registry import register_dataset
from maham.datasets.spectra.neutrino.base import NeutrinoSpectrumDataset


@register_dataset
class IceCubeNGC1068Flux2022(NeutrinoSpectrumDataset):
    metadata = DatasetMetadata(
        id="icecube.ngc1068_flux.2022",
        title="IceCube NGC 1068 steady point-source neutrino flux",
        experiment="IceCube",
        messenger="neutrino",
        data_type="spectrum",
        description="Best-fit steady nu_mu + nubar_mu point-source spectrum of NGC 1068.",
        year=2022,
        quantity="phi",
        spectral_kind="differential_flux",
        energy_unit="GeV",
        value_unit="GeV-1 cm-2 s-1",
        flavor_convention="numu_nubar",
        solid_angle_convention="point_source",
        paper=Reference(
            title="Evidence for neutrino emission from the nearby active galaxy NGC 1068",
            authors=("IceCube Collaboration",),
            year=2022,
            doi="10.1126/science.abg3395",
        ),
        dataset_reference=Reference(
            title="Evidence for neutrino emission from the nearby active galaxy NGC 1068",
            authors=("IceCube Collaboration",),
            year=2022,
            doi="10.21234/03fq-rh11",
        ),
        source=DataSource(
            provenance=ProvenanceType.DERIVED,
            storage=StorageMode.BUNDLED,
            path="data/datasets/spectra/neutrino/icecube_ngc1068_flux_2022.csv",
            sha256="5fd32e584d5b06f843afc3092ec2bd52d443d51a15af7e2485ee86346542c28c",
            url="https://icecube.wisc.edu/data-releases/2022/11/"
            "evidence-for-neutrino-emission-from-the-nearby-active-galaxy-ngc-1068/",
        ),
        notes=(
            "The bundled parameters reproduce the published best-fit unbroken power-law spectrum.",
            "The native flux is nu_mu + nubar_mu and is a point-source flux, so no sr^-1 factor is present.",
            "The normalization is defined at 1 TeV: 5.0e-11 TeV-1 cm-2 s-1.",
            "The published normalization uncertainties are +/-1.5e-11 statistical and +/-0.6e-11 systematic.",
            "The best-fit spectral index is 3.2 with +/-0.2 statistical and +/-0.07 systematic uncertainty.",
            "The 1.5-15 TeV interval contributes 68% of the total test statistic.",
            "No pointwise uncertainty band is constructed because normalization and spectral index are correlated.",
        ),
        tags=("IceCube", "NGC 1068", "point source", "AGN", "Seyfert", "steady neutrino source"),
    )

    def load_raw(self, cache: bool = True, show_progress: bool = True) -> Table:
        return Table.read(self.fetch(cache=cache, show_progress=show_progress), format="ascii.csv")

    def standardize(self, raw: Table) -> QTable:
        row = raw[0]
        reference_energy = float(row["reference_energy_TeV"]) * u.TeV
        phi0 = float(row["phi0_TeV_inv_cm2_s"]) / (u.TeV * u.cm**2 * u.s)
        gamma = float(row["spectral_index"])
        energy_min = float(row["energy_min_TeV"]) * u.TeV
        energy_max = float(row["energy_max_TeV"]) * u.TeV
        energy = np.geomspace(energy_min.to_value(u.GeV), energy_max.to_value(u.GeV), 64) * u.GeV
        phi = phi0 * (energy / reference_energy) ** (-gamma)

        table = QTable()
        table["energy"] = energy
        table["phi"] = phi.to(1 / (u.GeV * u.cm**2 * u.s))

        table.meta["dataset_id"] = self.metadata.id
        table.meta["quantity"] = self.metadata.quantity
        table.meta["spectral_kind"] = self.metadata.spectral_kind
        table.meta["flavor_convention"] = self.metadata.flavor_convention
        table.meta["solid_angle_convention"] = self.metadata.solid_angle_convention
        table.meta["source_name"] = "NGC 1068"
        table.meta["coordinate_frame"] = "ICRS"
        table.meta["ra_deg"] = float(row["ra_deg"])
        table.meta["dec_deg"] = float(row["dec_deg"])
        table.meta["spectral_model"] = "unbroken_power_law"
        table.meta["reference_energy_TeV"] = float(row["reference_energy_TeV"])
        table.meta["phi0_TeV_inv_cm2_s"] = float(row["phi0_TeV_inv_cm2_s"])
        table.meta["phi0_stat_err_TeV_inv_cm2_s"] = float(row["phi0_stat_err_TeV_inv_cm2_s"])
        table.meta["phi0_sys_err_TeV_inv_cm2_s"] = float(row["phi0_sys_err_TeV_inv_cm2_s"])
        table.meta["spectral_index"] = gamma
        table.meta["spectral_index_stat_err"] = float(row["spectral_index_stat_err"])
        table.meta["spectral_index_sys_err"] = float(row["spectral_index_sys_err"])
        table.meta["energy_min_TeV"] = float(row["energy_min_TeV"])
        table.meta["energy_max_TeV"] = float(row["energy_max_TeV"])
        table.meta["signal_events"] = int(row["signal_events"])
        table.meta["signal_events_lower"] = int(row["signal_events_lower"])
        table.meta["signal_events_upper"] = int(row["signal_events_upper"])
        table.meta["global_significance_sigma"] = float(row["global_significance_sigma"])
        table.meta["energy_range_definition"] = "68% of total test statistic"
        table.meta["provenance"] = self.metadata.source.provenance.value
        return table
