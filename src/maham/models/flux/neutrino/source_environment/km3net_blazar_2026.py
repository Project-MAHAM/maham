from maham._core.metadata import DataSource, ModelMetadata, ProvenanceType, Reference, StorageMode
from maham.models.flux.neutrino.base import TabulatedNeutrinoFluxModel
from maham.models.registry import register_model

_ROOT = "data/models/flux/neutrino/source_environment"


@register_model
class KM3NeTBlazarPopulation2026BestFit(TabulatedNeutrinoFluxModel):
    energy_column = "Energy"
    value_column = "FluxE2"
    values_are_log10 = False
    metadata = ModelMetadata(
        id="neutrino.source_environment.km3net_blazar_population_2026_best_fit",
        title="KM3NeT 2026 blazar-population diffuse neutrino flux: joint best fit",
        messenger="neutrino",
        model_type="flux",
        family="source_environment",
        description="Joint KM3NeT/ARCA and IceCube best-fit diffuse neutrino flux from a population of blazars modeled with AM3 and a Fermi-LAT blazar luminosity function.",
        year=2026,
        variant="joint KM3NeT/ARCA + IceCube best fit",
        source=DataSource(
            provenance=ProvenanceType.DIGITIZED,
            storage=StorageMode.BUNDLED,
            path=f"{_ROOT}/km3net_blazar_population_2026_best_fit.csv",
            sha256="de43439542f96e8b7a28aa0599380c20e874287d615e078ebf267b2282ca2719",
        ),
        paper=Reference(
            title="Blazars as a potential origin of the KM3-230213A event",
            authors=("KM3NeT Collaboration",),
            year=2026,
            doi="10.1088/1475-7516/2026/03/033",
            url="https://doi.org/10.1088/1475-7516/2026/03/033",
        ),
        data_reference=Reference(
            title="Figure 4 of Blazars as a potential origin of the KM3-230213A event",
            authors=("KM3NeT Collaboration",),
            year=2026,
            doi="10.1088/1475-7516/2026/03/033",
            url="https://doi.org/10.1088/1475-7516/2026/03/033",
        ),
        quantity="E2phi",
        spectral_kind="differential_intensity",
        energy_unit="GeV",
        value_unit="GeV / (cm2 s sr)",
        flavor_convention="per_flavor",
        solid_angle_convention="diffuse",
        notes=(
            "The bundled table is a raster digitization of the dark-blue best-fit neutrino curve in published Figure 4; the 1-sigma band is not included.",
            "The published JCAP PDF has SHA256 5027c37955289da51e13969aff1b6a4f9d711e42f799b6ec351b9dd79f45b55c.",
            "The embedded Figure 4 raster has SHA256 3463bc218ab0449f7ad23e5f9b70ed4d78f881e008ce59784b129620066bba4c.",
            "Native representation is single-flavor E2phi diffuse intensity, as stated explicitly in the Figure 4 caption.",
            "The joint KM3NeT/ARCA + IceCube best fit has baryonic loading eta approximately 10 and proton spectral index alpha_p approximately 1.8.",
            "The AM3 source template fixes the jet-frame maximum proton energy at 30 PeV and the bulk Lorentz factor at 17.6.",
            "The population calculation uses the Fermi-LAT blazar luminosity function integrated over redshift 1e-3 to 6 and gamma-ray luminosity 1e43 to 1e52 erg/s.",
            "The digitized centerline is sampled every 0.05 dex in energy over the visible plotted support, with the lower-axis clipping intersection excluded.",
            "Values should not be interpreted as more precise than the published raster figure.",
            "MAHAM does not extrapolate beyond the digitized visible support.",
        ),
        tags=("neutrino", "source_environment", "blazar", "AGN", "AM3", "KM3NeT", "KM3-230213A", "digitized"),
    )
