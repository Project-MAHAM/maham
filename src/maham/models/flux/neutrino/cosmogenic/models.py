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

_KPS_REPOSITORY = Reference(
    title="KM3-230213A_UHECR_TA: code and simulation data for Ultra-High Energy Event KM3-230213A as a Cosmogenic Neutrino in Light of Minimal UHECR Flux Models",
    authors=("M. Yu. Kuznetsov", "N. A. Petrov", "Y. S. Savchenko"),
    year=2025,
    url="https://github.com/82492749123082/KM3-230213A_UHECR_TA",
)

_ENERGY_COLUMN = "Energy [GeV]"
_VALUE_COLUMN = "log10(E^2 F(E) [GeV.cm^-2.s^-1.sr^-1])"
_ROOT = "data/models/flux/neutrino/cosmogenic"


class _CosmogenicModel(TabulatedNeutrinoFluxModel):
    energy_column = _ENERGY_COLUMN
    value_column = _VALUE_COLUMN
    values_are_log10 = True


class _KPSCosmogenicModel(TabulatedNeutrinoFluxModel):
    energy_column = "Energy"
    value_column = "FluxE2"
    values_are_log10 = False
    nonpositive_flux_policy = "truncate_at_first"


class _YoshidaMeier2026CosmogenicModel(TabulatedNeutrinoFluxModel):
    energy_column = "Energy"
    value_column = "FluxE2"
    values_are_log10 = False


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


def _kps_metadata(model_id, title, filename, sha256, variant, support_note, extra_notes=()):
    return ModelMetadata(
        id=model_id,
        title=title,
        messenger="neutrino",
        model_type="flux",
        family="cosmogenic",
        description="Cosmogenic neutrino flux prediction from minimal Telescope Array UHECR models, reproduced from the authors' public analysis code.",
        year=2026,
        variant=variant,
        source=DataSource(provenance=ProvenanceType.DERIVED, storage=StorageMode.BUNDLED, path=f"{_ROOT}/{filename}", sha256=sha256),
        paper=Reference(
            title="Ultra-High Energy Event KM3-230213A as a Cosmogenic Neutrino in Light of Minimal UHECR Flux Models",
            authors=("M. Yu. Kuznetsov", "N. A. Petrov", "Y. S. Savchenko"),
            year=2026,
            doi="10.1134/S0021364025610061",
            url="https://arxiv.org/abs/2509.09590",
        ),
        data_reference=_KPS_REPOSITORY,
        quantity="E2phi",
        spectral_kind="differential_intensity",
        energy_unit="GeV",
        value_unit="GeV / (cm2 s sr)",
        flavor_convention="per_flavor",
        solid_angle_convention="diffuse",
        notes=(
            "Numerical table was reproduced from the authors' public repository at commit 774174d9faaa5df40b67af5fa42b4191f09d38c6 by running papermain.py.",
            "The authors' calc_fluxes() CSV output is preserved byte-for-byte after renaming for MAHAM.",
            "The export uses the z<4 CRPropa model normalized to the Telescope Array spectrum and samples a smoothing spline at 1000 log-spaced energies from 1e5 to 1e12 GeV.",
            "Native representation is per-flavor E2phi for nu+nubar under neutrino equipartition.",
            "The authors' high-energy smoothing spline becomes non-positive and later oscillates around zero; these values are nonphysical and incompatible with log-log flux interpolation.",
            support_note,
            "MAHAM therefore restricts the standardized support to the leading contiguous positive part of the unchanged source export.",
            "MAHAM does not extrapolate beyond this standardized positive support.",
            *extra_notes,
        ),
        tags=("neutrino", "cosmogenic", "UHECR", "Telescope Array", "KM3-230213A", "derived"),
    )



def _yoshida_meier_metadata(model_id, title, filename, sha256, variant, extra_notes=()):
    return ModelMetadata(
        id=model_id,
        title=title,
        messenger="neutrino",
        model_type="flux",
        family="cosmogenic",
        description="High-redshift cosmogenic neutrino flux prediction from ultrahigh-energy proton emission by the early AGN population observed by JWST.",
        year=2026,
        variant=variant,
        source=DataSource(provenance=ProvenanceType.DIGITIZED, storage=StorageMode.BUNDLED, path=f"{_ROOT}/{filename}", sha256=sha256),
        paper=Reference(
            title="Ultrahigh-energy cosmogenic neutrino emissions in the high-redshift universe",
            authors=("Shigeru Yoshida", "Maximilian Meier"),
            year=2026,
            doi="10.1103/ljz7-phzv",
            url="https://arxiv.org/abs/2604.14535",
        ),
        data_reference=Reference(
            title="arXiv source package for Ultrahigh-energy cosmogenic neutrino emissions in the high-redshift universe",
            authors=("Shigeru Yoshida", "Maximilian Meier"),
            year=2026,
            url="https://arxiv.org/src/2604.14535",
        ),
        quantity="E2phi",
        spectral_kind="differential_intensity",
        energy_unit="GeV",
        value_unit="GeV / (cm2 s sr)",
        flavor_convention="all_flavor",
        solid_angle_convention="diffuse",
        notes=(
            "Numerical curve was extracted from the vector content of the authors' nu_energy_distribution_units_gf_allflavor.pdf figure because the arXiv source package contains no machine-readable flux table.",
            "The source figure PDF has SHA256 b4bbaed45392ed7efaedf7283012a4d96a63e3fba312e12c7eab357d32b06435.",
            "Native representation is all-flavor E2phi diffuse intensity with neutrino flavor mixing included.",
            "The nominal CRPropa curve assumes maximum proton energy E_p,max=1e10 GeV and L_CR=1e45 erg/s.",
            "MAHAM does not extrapolate beyond the digitized energy support.",
            *extra_notes,
        ),
        tags=("neutrino", "cosmogenic", "UHECR", "high-redshift", "AGN", "JWST", "digitized"),
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


@register_model
class KuznetsovPetrovSavchenko2026BestFitCosmogenic(_KPSCosmogenicModel):
    metadata = _kps_metadata(
        "neutrino.cosmogenic.kuznetsov_petrov_savchenko_2026_best_fit",
        "Kuznetsov, Petrov and Savchenko 2026 cosmogenic neutrino flux: best fit",
        "kuznetsov_petrov_savchenko_2026_best_fit.csv",
        "163f0d1ce47d77eafd3797a4e16f24587d9d283a4f5fabef44a48f08db71e2e0",
        "best-fit Telescope Array UHECR solution",
        "The leading positive support contains 919 points from 1e5 to 2.707e11 GeV.",
        extra_notes=("Source configuration: Rmax=182 EeV, spectral slope -2.06, injected composition 99.2% He and 0.8% Fe.",),
    )


@register_model
class KuznetsovPetrovSavchenko2026LocalMinCosmogenic(_KPSCosmogenicModel):
    metadata = _kps_metadata(
        "neutrino.cosmogenic.kuznetsov_petrov_savchenko_2026_local_min",
        "Kuznetsov, Petrov and Savchenko 2026 cosmogenic neutrino flux: local minimum",
        "kuznetsov_petrov_savchenko_2026_local_min.csv",
        "141a9dce1707a8ce112ede580523a5c0bd070eed9bac1916a66f63a9c3853c7a",
        "local-minimum Telescope Array UHECR solution",
        "The leading positive support contains 787 points from 1e5 to 3.217e10 GeV.",
        extra_notes=("Source configuration: Rmax=15.8 EeV, spectral slope -0.78, injected composition 97.1% protons and 2.9% Fe.",),
    )


@register_model
class YoshidaMeier2026NoEvolutionCosmogenic(_YoshidaMeier2026CosmogenicModel):
    metadata = _yoshida_meier_metadata(
        "neutrino.cosmogenic.yoshida_meier_2026_no_evolution",
        "Yoshida and Meier 2026 high-redshift cosmogenic neutrino flux: no evolution",
        "yoshida_meier_2026_no_evolution.csv",
        "62ad7db9ffa53eac6d792cfbfe68d8a544a046bb796394808bc8b9003e04246f",
        "no source-density evolution",
        extra_notes=("The baseline source density is n0=1e-5 Mpc^-3.",),
    )


@register_model
class YoshidaMeier2026LogNormalCosmogenic(_YoshidaMeier2026CosmogenicModel):
    metadata = _yoshida_meier_metadata(
        "neutrino.cosmogenic.yoshida_meier_2026_log_normal",
        "Yoshida and Meier 2026 high-redshift cosmogenic neutrino flux: log-normal evolution",
        "yoshida_meier_2026_log_normal.csv",
        "4a78c22a8a9a0fa40f307e3db5ac9802bbc84b97599dbad64b1f209991d0a40b",
        "log-normal source-density evolution",
        extra_notes=("The source-density evolution follows the log-normal high-redshift evolution considered in the paper.",),
    )
