from maham._core.metadata import DataSource, ModelMetadata, ProvenanceType, Reference, StorageMode
from maham.models.flux.neutrino.base import TabulatedNeutrinoFluxModel
from maham.models.registry import register_model


_RELEASE = Reference(
    title="Data for the KM3-230213A high energy event observation",
    authors=("KM3NeT Collaboration",),
    year=2025,
    doi="10.5281/zenodo.14860165",
    url="https://zenodo.org/records/14860165",
)

_ENERGY_COLUMN = "Energy [GeV]"
_VALUE_COLUMN = "log10(E^2 F(E) [GeV.cm^-2.s^-1.sr^-1])"
_ROOT = "data/models/flux/neutrino/cosmogenic"


class _CosmogenicModel(TabulatedNeutrinoFluxModel):
    energy_column = _ENERGY_COLUMN
    value_column = _VALUE_COLUMN
    values_are_log10 = True


def _metadata(model_id, title, filename, sha256, year, paper_title, authors, arxiv, doi, variant=None, extra_notes=()):
    return ModelMetadata(
        id=model_id,
        title=title,
        messenger="neutrino",
        model_type="flux",
        family="cosmogenic",
        description="Cosmogenic neutrino flux model curated in the KM3NeT KM3-230213A data release.",
        year=year,
        variant=variant,
        source=DataSource(provenance=ProvenanceType.CURATED_DATABASE, storage=StorageMode.BUNDLED, path=f"{_ROOT}/{filename}", sha256=sha256),
        paper=Reference(title=paper_title, authors=authors, year=year, doi=doi, url=f"https://arxiv.org/abs/{arxiv}"),
        data_reference=_RELEASE,
        quantity="E2phi",
        spectral_kind="differential_intensity",
        energy_unit="GeV",
        value_unit="GeV / (cm2 s sr)",
        flavor_convention="per_flavor",
        solid_angle_convention="diffuse",
        notes=(
            "Numerical curve is the KM3NeT-curated tabulation distributed with the 2025 KM3-230213A data release.",
            "Native representation is per-flavor E2phi diffuse intensity.",
            "MAHAM does not extrapolate this model beyond the tabulated energy support.",
            *extra_notes,
        ),
        tags=("neutrino", "cosmogenic", "UHECR", "KM3NeT-curated"),
    )


@register_model
class Aloisio2015Cosmogenic(_CosmogenicModel):
    metadata = _metadata(
        "neutrino.cosmogenic.aloisio_2015", "Aloisio et al. 2015 cosmogenic neutrino flux", "aloisio_2015.json",
        "6f9ebd48c9443528d587355a0f50ada7abd9f594e06b90541c24708fa935a76c", 2015,
        "Cosmogenic neutrinos and ultra-high energy cosmic ray models",
        ("R. Aloisio", "D. Boncioli", "A. di Matteo", "A. F. Grillo", "S. Petrera", "F. Salamida"),
        "1505.04020", "10.1088/1475-7516/2015/10/006",
    )


@register_model
class Berat2024Cosmogenic(_CosmogenicModel):
    metadata = _metadata(
        "neutrino.cosmogenic.berat_2024", "Berat et al. 2024 cosmogenic neutrino flux", "berat_2024.json",
        "3a056a57d776dc7d662daaefef884ad04c4d56c4c86c3fde22f097f0cbbe790a", 2024,
        "Floor of cosmogenic neutrino fluxes above 10^17 eV",
        ("Corinne Berat", "Antonio Condorelli", "Olivier Deligny", "Francois Montanet", "Zoe Torres"),
        "2402.04759", "10.3847/1538-4357/ad372a",
    )


@register_model
class Boncioli2019Cosmogenic(_CosmogenicModel):
    metadata = _metadata(
        "neutrino.cosmogenic.boncioli_2019", "Boncioli et al. 2019 cosmogenic neutrino flux", "boncioli_2019.json",
        "9178e8f62d7224d0375651466edd51ffd5d80966273abee7d4d70eed023d69bc", 2019,
        "On the common origin of cosmic rays across the ankle and diffuse neutrinos at the highest energies from low-luminosity Gamma-Ray Bursts",
        ("Denise Boncioli", "Daniel Biehl", "Walter Winter"), "1808.07481", "10.3847/1538-4357/aafda7",
        variant="cosmogenic component",
    )


@register_model
class Condorelli2023Cosmogenic(_CosmogenicModel):
    metadata = _metadata(
        "neutrino.cosmogenic.condorelli_2023", "Condorelli et al. 2023 cosmogenic neutrino flux", "condorelli_2023.json",
        "03b51326084833f1032162fb77268f28da7964254f0bb34b52ad00a488eed250", 2023,
        "Testing hadronic and photo-hadronic interactions as responsible for UHECR and neutrino fluxes from Starburst Galaxies",
        ("Antonio Condorelli", "Denise Boncioli", "Enrico Peretti", "Sergio Petrera"),
        "2209.08593", "10.1103/PhysRevD.107.083009",
    )


@register_model
class Ehlert2024Cosmogenic(_CosmogenicModel):
    duplicate_energy_policy = "mean_native"
    metadata = _metadata(
        "neutrino.cosmogenic.ehlert_2024", "Ehlert et al. 2024 cosmogenic neutrino flux", "ehlert_2024.json",
        "b482ae59d1dd25348a938c2f6dd346608616574b65223997cd77b896874f085b", 2024,
        "Constraints on the proton fraction of cosmic rays at the highest energies and the consequences for cosmogenic neutrinos and photons",
        ("Domenik Ehlert", "Arjen van Vliet", "Foteini Oikonomou", "Walter Winter"),
        "2304.07321", "10.1088/1475-7516/2024/02/022",
        extra_notes=("The KM3NeT-curated tabulation contains one duplicate energy coordinate; MAHAM collapses it by averaging the two native log10(E2phi) values before conversion to linear flux.",),
    )


@register_model
class MuzioFarrar2023Cosmogenic(_CosmogenicModel):
    metadata = _metadata(
        "neutrino.cosmogenic.muzio_farrar_2023", "Muzio and Farrar 2023 cosmogenic neutrino flux", "muzio_farrar_2023.json",
        "f1844873982220672fb899219920b2a38694beb85ffc1433be41c2533fe800b0", 2023,
        "Constraints on the hosts of UHECR accelerators", ("Marco Stein Muzio", "Glennys R. Farrar"),
        "2209.08068", "10.3847/2041-8213/acac93",
    )


@register_model
class MuzioUngerWissel2023Cosmogenic(_CosmogenicModel):
    metadata = _metadata(
        "neutrino.cosmogenic.muzio_unger_wissel_2023",
        "Muzio, Unger and Wissel 2023 cosmogenic neutrino flux",
        "muzio_unger_wissel_2023.json", "4f1ca46c0d15f10f60bce718854ea866c19b4ddf048983d8c2a26866f25432bb", 2023,
        "Prospects for joint cosmic ray and neutrino constraints on the evolution of trans-Greisen-Zatsepin-Kuzmin proton sources",
        ("Marco Stein Muzio", "Michael Unger", "Stephanie Wissel"),
        "2303.04170", "10.1103/PhysRevD.107.103030",
    )


@register_model
class Auger2023Cosmogenic(_CosmogenicModel):
    metadata = _metadata(
        "neutrino.cosmogenic.auger_2023", "Pierre Auger 2023 cosmogenic neutrino flux", "auger_2023.json",
        "d25312fb062ff229621012b29a15f810033b8ea169358d8356d5d08d1fa72740", 2023,
        "Constraining the sources of ultra-high-energy cosmic rays across and above the ankle with the spectrum and composition data measured at the Pierre Auger Observatory",
        ("Pierre Auger Collaboration",), "2211.02857", "10.1088/1475-7516/2023/05/024",
    )


@register_model
class Heinze2019Cosmogenic(_CosmogenicModel):
    metadata = _metadata(
        "neutrino.cosmogenic.heinze_2019", "Heinze et al. 2019 cosmogenic neutrino flux", "heinze_2019.json",
        "b6e6b4698887abd782f069763ec5854f768f193a88e89fa915888cc01b556fc0", 2019,
        "A new view on Auger data and cosmogenic neutrinos in light of different nuclear disintegration and air-shower models",
        ("Jonas Heinze", "Anatoli Fedynitch", "Denise Boncioli", "Walter Winter"),
        "1901.03338", "10.3847/1538-4357/ab05ce",
    )


@register_model
class ZhangMurase2019Cosmogenic(_CosmogenicModel):
    metadata = _metadata(
        "neutrino.cosmogenic.zhang_murase_2019", "Zhang and Murase 2019 cosmogenic neutrino flux", "zhang_murase_2019.json",
        "88f82bad09d4a4319eb0c90d9c50071b8ae74ea926e684be0ad7f5828c5bf109", 2019,
        "Ultrahigh-energy cosmic-ray nuclei and neutrinos from engine-driven supernovae",
        ("B. Theodore Zhang", "Kohta Murase"), "1812.10289", "10.1103/PhysRevD.100.103004",
        variant="cosmogenic component",
    )
