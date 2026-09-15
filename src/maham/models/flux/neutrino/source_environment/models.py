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
_ROOT = "data/models/flux/neutrino/source_environment"


class _SourceEnvironmentModel(TabulatedNeutrinoFluxModel):
    energy_column = _ENERGY_COLUMN
    value_column = _VALUE_COLUMN
    values_are_log10 = True


def _metadata(model_id, title, filename, sha256, year, paper_title, authors, arxiv, doi, variant):
    return ModelMetadata(
        id=model_id,
        title=title,
        messenger="neutrino",
        model_type="flux",
        family="source_environment",
        description="Astrophysical source-environment neutrino flux model curated in the KM3NeT KM3-230213A data release.",
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
        ),
        tags=("neutrino", "source_environment", "astrophysical_source", "KM3NeT-curated"),
    )


@register_model
class BoncioliLLGRB2019(_SourceEnvironmentModel):
    metadata = _metadata(
        "neutrino.source_environment.boncioli_llgrb_2019", "Boncioli et al. 2019 LL-GRB source neutrino flux",
        "boncioli_llgrb_2019.json", "ddfd4e4f1aaf55193b954120f220d8b756bac9ffc4ffd570a348b3d3b532f30c", 2019,
        "On the common origin of cosmic rays across the ankle and diffuse neutrinos at the highest energies from low-luminosity Gamma-Ray Bursts",
        ("Denise Boncioli", "Daniel Biehl", "Walter Winter"), "1808.07481", "10.3847/1538-4357/aafda7",
        "LL-GRB source component",
    )


@register_model
class FangPulsar2014(_SourceEnvironmentModel):
    metadata = _metadata(
        "neutrino.source_environment.fang_pulsar_2014", "Fang et al. 2014 newborn-pulsar neutrino flux",
        "fang_pulsar_2014.json", "451d5bd72ba6ee49bc66e719c5818fd248767dbbf710c4f074f85b6beeef82b3", 2014,
        "Testing the Newborn Pulsar Origin of Ultrahigh Energy Cosmic Rays with EeV Neutrinos",
        ("Ke Fang", "Kumiko Kotera", "Kohta Murase", "Angela V. Olinto"),
        "1311.2044", "10.1103/PhysRevD.90.103005", "newborn pulsars",
    )


@register_model
class RodriguesAGN2021(_SourceEnvironmentModel):
    metadata = _metadata(
        "neutrino.source_environment.rodrigues_agn_2021", "Rodrigues et al. 2021 AGN source neutrino flux",
        "rodrigues_agn_2021.json", "900f71cd8a470ca34594a04a9a4129158d46c33a9d2f23ea6f71926e089df988", 2021,
        "AGN jets as the origin of UHECRs and perspectives for the detection of astrophysical source neutrinos at EeV energies",
        ("Xavier Rodrigues", "Jonas Heinze", "Andrea Palladino", "Arjen van Vliet", "Walter Winter"),
        "2003.08392", "10.1103/PhysRevLett.126.191101", "AGN jets",
    )


@register_model
class RodriguesBLLac2024(_SourceEnvironmentModel):
    metadata = _metadata(
        "neutrino.source_environment.rodrigues_bllac_2024", "Rodrigues et al. 2024 BL Lac neutrino flux",
        "rodrigues_bllac_2024.json", "c5f3b76db35d8af1e8ff4800188634cf5c14905fb44818cc749f602b778c0ba2", 2024,
        "Leptohadronic Multimessenger Modeling of 324 Gamma-Ray Blazars",
        ("Xavier Rodrigues", "Vaidehi S. Paliya", "Simone Garrappa", "Anastasiia Omeliukh", "Anna Franckowiak", "Walter Winter"),
        "2307.13024", "10.1051/0004-6361/202347540", "BL Lac sample",
    )


@register_model
class RodriguesFSRQ2024(_SourceEnvironmentModel):
    metadata = _metadata(
        "neutrino.source_environment.rodrigues_fsrq_2024", "Rodrigues et al. 2024 FSRQ neutrino flux",
        "rodrigues_fsrq_2024.json", "9b65426fccf2c08cf8c2cb2515d54d0b729d5adaaae841edf788c425375e066b", 2024,
        "Leptohadronic Multimessenger Modeling of 324 Gamma-Ray Blazars",
        ("Xavier Rodrigues", "Vaidehi S. Paliya", "Simone Garrappa", "Anastasiia Omeliukh", "Anna Franckowiak", "Walter Winter"),
        "2307.13024", "10.1051/0004-6361/202347540", "FSRQ sample",
    )


@register_model
class TamborraLLGRB2015(_SourceEnvironmentModel):
    metadata = _metadata(
        "neutrino.source_environment.tamborra_llgrb_2015", "Tamborra and Ando 2015 LL-GRB neutrino flux",
        "tamborra_llgrb_2015.json", "486df080c1704f8c1a2a930fe9109053f5118fc8f25a65a58a32b83e783bc307", 2015,
        "Diffuse emission of high-energy neutrinos from gamma-ray burst fireballs",
        ("Irene Tamborra", "Shin'ichiro Ando"), "1504.00107", "10.1088/1475-7516/2015/09/036",
        "low-luminosity GRB",
    )


@register_model
class TamborraSGRB2015(_SourceEnvironmentModel):
    metadata = _metadata(
        "neutrino.source_environment.tamborra_sgrb_2015", "Tamborra and Ando 2015 short-GRB neutrino flux",
        "tamborra_sgrb_2015.json", "9d7f1a5ff50d95b849d8eb67663e8ad1620626e91d6dff07076fcf4af228b26c", 2015,
        "Diffuse emission of high-energy neutrinos from gamma-ray burst fireballs",
        ("Irene Tamborra", "Shin'ichiro Ando"), "1504.00107", "10.1088/1475-7516/2015/09/036",
        "short-duration GRB",
    )


@register_model
class WinterTDE2023(_SourceEnvironmentModel):
    metadata = _metadata(
        "neutrino.source_environment.winter_tde_2023", "Winter and Lunardini 2023 TDE neutrino flux",
        "winter_tde_2023.json", "f78043324e9bc22979ee00cfa0446580158e14648188f4ea0efd6abc295e404f", 2023,
        "Interpretation of the observed neutrino emission from three Tidal Disruption Events",
        ("Walter Winter", "Cecilia Lunardini"), "2205.11538", "10.3847/1538-4357/acbe9e",
        "tidal disruption events",
    )
