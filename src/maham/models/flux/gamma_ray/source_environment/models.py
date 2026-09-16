from maham._core.metadata import DataSource, ModelMetadata, ProvenanceType, Reference, StorageMode
from maham.models.flux.gamma_ray.base import TabulatedGammaRayFluxModel
from maham.models.registry import register_model

_ROOT = "data/models/flux/gamma_ray/source_environment"

@register_model
class KM3NeTBlazarPopulation2026GammaBestFit(TabulatedGammaRayFluxModel):
    metadata = ModelMetadata(
        id="gamma_ray.source_environment.km3net_blazar_population_2026_best_fit",
        title="KM3NeT 2026 blazar-population diffuse gamma-ray flux: joint best fit",
        messenger="gamma_ray", model_type="flux", family="source_environment",
        description="Diffuse gamma-ray best-fit prediction from the joint KM3NeT/ARCA and IceCube blazar-population model.",
        year=2026, variant="joint KM3NeT/ARCA + IceCube best fit",
        source=DataSource(provenance=ProvenanceType.DIGITIZED, storage=StorageMode.BUNDLED, path=f"{_ROOT}/km3net_blazar_population_2026_gamma_best_fit.csv", sha256="a696833bc7a67cfd54655f54c30ea3f2d454d314af5ebf55300a7b466b4c1b71"),
        paper=Reference(title="Blazars as a potential origin of the KM3-230213A event", authors=("KM3NeT Collaboration",), year=2026, doi="10.1088/1475-7516/2026/03/033", url="https://doi.org/10.1088/1475-7516/2026/03/033"),
        data_reference=Reference(title="Figure 5 of Blazars as a potential origin of the KM3-230213A event", authors=("KM3NeT Collaboration",), year=2026, doi="10.1088/1475-7516/2026/03/033", url="https://doi.org/10.1088/1475-7516/2026/03/033"),
        quantity="E2phi", spectral_kind="differential_intensity", energy_unit="GeV", value_unit="GeV / (cm2 s sr)", solid_angle_convention="diffuse",
        notes=("Digitized solid best-fit curve from published Figure 5; the 1-sigma band is not included.", "Joint best fit: eta approximately 10 and alpha_p approximately 1.8.", "The paper reports that this model contributes approximately 42% of the EGB.", "MAHAM does not extrapolate beyond the digitized support."),
        tags=("gamma_ray", "source_environment", "blazar", "AGN", "AM3", "KM3NeT", "digitized"),
    )

@register_model
class AjelloBlazarPopulation2015(TabulatedGammaRayFluxModel):
    lower_column = "FluxE2Lower"
    upper_column = "FluxE2Upper"
    metadata = ModelMetadata(
        id="gamma_ray.source_environment.ajello_blazar_population_2015",
        title="Ajello et al. 2015 integrated blazar gamma-ray emission",
        messenger="gamma_ray", model_type="flux", family="source_environment",
        description="Integrated gamma-ray emission predicted for the full blazar population using Fermi-LAT-constrained luminosity-function and SED models.",
        year=2015, variant="all-blazar PLE/PDE/LDDE model band",
        source=DataSource(provenance=ProvenanceType.DIGITIZED, storage=StorageMode.BUNDLED, path=f"{_ROOT}/ajello_blazar_population_2015.csv", sha256="d224b067030ad53ae6accb890afa7da735ed66697187d284a0e69f850d170b2b"),
        paper=Reference(title="The Origin of the Extragalactic Gamma-Ray Background and Implications for Dark-Matter Annihilation", authors=("M. Ajello", "D. Gasparrini", "M. Sanchez-Conde", "G. Zaharijas", "M. Gustafsson", "J. Cohen-Tanugi", "C. D. Dermer", "Y. Inoue", "D. Hartmann", "M. Ackermann", "K. Bechtol", "A. Franckowiak", "A. Reimer", "R. W. Romani", "A. W. Strong"), year=2015, doi="10.1088/2041-8205/800/2/L27", url="https://arxiv.org/abs/1501.05301"),
        data_reference=Reference(title="Figure 3 of Ajello et al. 2015", authors=("M. Ajello et al.",), year=2015, doi="10.1088/2041-8205/800/2/L27", url="https://arxiv.org/abs/1501.05301"),
        quantity="E2phi", spectral_kind="differential_intensity", energy_unit="GeV", value_unit="GeV / (cm2 s sr)", solid_angle_convention="diffuse",
        notes=("Figure 3 is a band spanning the PLE, PDE and LDDE luminosity-function models.", "MAHAM preserves digitized lower and upper envelopes; E2phi is a representative centerline for plotting.", "The paper reports 50(+12/-11)% of EGB photons above 0.1 GeV from blazars and about 70% of that blazar emission already resolved.", "The model includes EBL attenuation and omits secondary electromagnetic-cascade emission.", "The digitization is intentionally sparse and should not be treated as precision numerical data."),
        tags=("gamma_ray", "source_environment", "blazar", "Fermi-LAT", "EGB", "digitized"),
    )
