import astropy.units as u
import numpy as np
from astropy.table import QTable, Table

from maham._core.metadata import DataSource, DatasetMetadata, ProvenanceType, Reference, StorageMode
from maham.datasets.registry import register_dataset
from maham.datasets.spectra.neutrino.base import NeutrinoSpectrumDataset


@register_dataset
class IceCubeTXS0506FlareFlux2018(NeutrinoSpectrumDataset):
    metadata = DatasetMetadata(
        id="icecube.txs0506_flare_flux.2018",
        title="IceCube TXS 0506+056 2014-2015 neutrino flare flux",
        experiment="IceCube",
        messenger="neutrino",
        data_type="spectrum",
        description="Average nu_mu + nubar_mu point-source flux during the 158-day TXS 0506+056 neutrino flare.",
        year=2018,
        quantity="phi",
        spectral_kind="differential_flux",
        energy_unit="GeV",
        value_unit="GeV-1 cm-2 s-1",
        flavor_convention="numu_nubar",
        solid_angle_convention="point_source",
        paper=Reference(
            title="Neutrino emission from the direction of the blazar TXS 0506+056 prior to the IceCube-170922A alert",
            authors=("IceCube Collaboration",),
            year=2018,
            doi="10.1126/science.aat2890",
        ),
        dataset_reference=Reference(
            title="IceCube data from 2008 to 2017 related to analysis of TXS 0506+056",
            authors=("IceCube Collaboration",),
            year=2018,
            doi="10.21234/B4QG92",
        ),
        source=DataSource(
            provenance=ProvenanceType.DERIVED,
            storage=StorageMode.BUNDLED,
            path="data/datasets/spectra/neutrino/icecube_txs0506_flare_flux_2018.csv",
            sha256="bd4a9467bbe11ddcd7143eeb04b3fce19b12fdbd1621d63b1ebe4052201f54ea",
            url="https://icecube.wisc.edu/data-releases/2018/07/"
            "icecube-data-from-2008-to-2017-related-to-analysis-of-txs-0506056/",
        ),
        notes=(
            "This dataset uses the published 158-day box-shaped time-window result.",
            "The native flux is nu_mu + nubar_mu and is a point-source flux, so no sr^-1 factor is present.",
            "The average normalization is defined at 100 TeV: 1.6e-15 TeV-1 cm-2 s-1.",
            "The quoted normalization interval is +0.7/-0.6e-15 TeV-1 cm-2 s-1.",
            "The best-fit box-window spectral index is 2.2 +/- 0.2.",
            "The box window extends from MJD 56937.81 to 57096.21 and is reported as 158 days.",
            "The flare contains an estimated 13 +/- 5 signal events.",
            "The final trial-corrected significance is 3.5 sigma.",
            "No pointwise uncertainty band is constructed because flux normalization and spectral index are correlated.",
        ),
        tags=("IceCube", "TXS 0506+056", "point source", "blazar", "transient", "neutrino flare"),
    )

    def load_raw(self, cache: bool = True, show_progress: bool = True) -> Table:
        return Table.read(self.fetch(cache=cache, show_progress=show_progress), format="ascii.csv")

    def standardize(self, raw: Table) -> QTable:
        row = raw[0]
        reference_energy = float(row["reference_energy_TeV"]) * u.TeV
        phi100 = float(row["phi100_TeV_inv_cm2_s"]) / (u.TeV * u.cm**2 * u.s)
        gamma = float(row["spectral_index"])

        # IceCube quotes 32 TeV to 3.6 PeV as the central 68% sensitivity range for an E^-2.1 source.
        # We use that published interval only to delimit the displayed best-fit spectrum.
        energy = np.geomspace(32.0e3, 3.6e6, 64) * u.GeV
        phi = phi100 * (energy / reference_energy) ** (-gamma)

        table = QTable()
        table["energy"] = energy
        table["phi"] = phi.to(1 / (u.GeV * u.cm**2 * u.s))

        table.meta["dataset_id"] = self.metadata.id
        table.meta["quantity"] = self.metadata.quantity
        table.meta["spectral_kind"] = self.metadata.spectral_kind
        table.meta["flavor_convention"] = self.metadata.flavor_convention
        table.meta["solid_angle_convention"] = self.metadata.solid_angle_convention
        table.meta["source_name"] = "TXS 0506+056"
        table.meta["coordinate_frame"] = "ICRS"
        table.meta["ra_deg"] = float(row["ra_deg"])
        table.meta["dec_deg"] = float(row["dec_deg"])
        table.meta["spectral_model"] = "unbroken_power_law"
        table.meta["reference_energy_TeV"] = float(row["reference_energy_TeV"])
        table.meta["phi100_TeV_inv_cm2_s"] = float(row["phi100_TeV_inv_cm2_s"])
        table.meta["phi100_lower_TeV_inv_cm2_s"] = float(row["phi100_lower_TeV_inv_cm2_s"])
        table.meta["phi100_upper_TeV_inv_cm2_s"] = float(row["phi100_upper_TeV_inv_cm2_s"])
        table.meta["spectral_index"] = gamma
        table.meta["spectral_index_err"] = float(row["spectral_index_err"])
        table.meta["window_start_mjd"] = float(row["window_start_mjd"])
        table.meta["window_end_mjd"] = float(row["window_end_mjd"])
        table.meta["window_duration_days"] = float(row["window_duration_days"])
        table.meta["signal_events"] = int(row["signal_events"])
        table.meta["signal_events_err"] = int(row["signal_events_err"])
        table.meta["global_significance_sigma"] = float(row["global_significance_sigma"])
        table.meta["display_energy_min_TeV"] = 32.0
        table.meta["display_energy_max_TeV"] = 3600.0
        table.meta["display_energy_range_basis_gamma"] = 2.1
        table.meta["provenance"] = self.metadata.source.provenance.value
        return table
