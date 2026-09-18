import json
from functools import cached_property

import astropy.units as u
import numpy as np
from astropy.units import Quantity

from maham._core.metadata import DataSource, ModelMetadata, ProvenanceType, Reference, StorageMode
from maham.models.cross_sections.neutrino.base import NeutrinoCrossSectionModel
from maham.models.registry import register_model


_PAPER = Reference(
    title="Calculation of High Energy Neutrino-Nucleon Cross Sections and Uncertainties Using the MSTW Parton Distribution Functions and Implications for Future Experiments",
    authors=("Amy Connolly", "Robert S. Thorne", "David Waters"),
    year=2011,
    doi="10.1103/PhysRevD.83.113009",
    url="https://arxiv.org/abs/1102.0691v2",
)
_PARAMETERS = Reference(
    title="CTW 2011 Tables III and IV cross-section parametrization coefficients",
    authors=("Amy Connolly", "Robert S. Thorne", "David Waters"),
    year=2011,
    doi="10.1103/PhysRevD.83.113009",
    url="https://arxiv.org/abs/1102.0691v2",
)
_PARTICLES = {"nu", "nubar"}
_CURRENTS = {"cc", "nc", "total"}
_VARIATIONS = {"central", "upper", "lower"}


def _normalize(value: str, allowed: set[str], name: str) -> str:
    try:
        result = value.strip().lower().replace("-", "_").replace(" ", "_")
    except AttributeError as exc:
        raise ValueError(f"{name} must be one of: {', '.join(sorted(allowed))}.") from exc
    if result not in allowed:
        raise ValueError(f"{name} must be one of: {', '.join(sorted(allowed))}.")
    return result


@register_model
class CTW2011CrossSection(NeutrinoCrossSectionModel):
    """Connolly-Thorne-Waters 2011 neutrino-nucleon cross-section parametrization."""

    metadata = ModelMetadata(
        id="neutrino.cross_section.ctw_2011",
        title="CTW 2011 neutrino-nucleon cross section",
        messenger="neutrino",
        model_type="cross_section",
        family="neutrino_nucleon",
        description="Analytic CTW parametrization of charged-current and neutral-current neutrino-nucleon cross sections and PDF uncertainty bounds.",
        year=2011,
        variant="CTW Eq. 7",
        source=DataSource(
            provenance=ProvenanceType.PUBLISHED_TABLE,
            storage=StorageMode.BUNDLED,
            path="data/models/cross_sections/neutrino/ctw_2011.json",
            sha256="248c1e4d5085a2b84dfc04e5e8e19afad549022ba5915ca22d1c077152f20000",
        ),
        paper=_PAPER,
        data_reference=_PARAMETERS,
        quantity="sigma",
        energy_unit="GeV",
        value_unit="cm2",
        notes=(
            "Equation 7 is evaluated using the coefficients published in Tables III and IV of Connolly, Thorne, and Waters (2011).",
            "Blank entries in the published coefficient tables are expanded into complete C0-C4 vectors in the bundled JSON.",
            "The model supports nu and nubar, CC and NC, plus total=CC+NC for central, upper, and lower CTW parametrizations.",
            "MAHAM restricts evaluation to the published CTW energy range 1e4-1e12 GeV.",
        ),
        tags=("neutrino", "cross-section", "CTW", "MSTW2008", "neutrino-nucleon"),
    )

    @cached_property
    def parameters(self) -> dict:
        with self.fetch().open("r", encoding="utf-8") as f:
            return json.load(f)

    @staticmethod
    def _evaluate_eq7(energy_GeV: np.ndarray, coefficients: list[float]) -> Quantity:
        c0, c1, c2, c3, c4 = coefficients
        eps = np.log10(energy_GeV)
        x = np.log(eps - c0)
        log10_sigma = c1 + c2 * x + c3 * x**2 + c4 / x
        return np.power(10.0, log10_sigma) * u.cm**2

    def cross_section(self, energy: Quantity, particle: str = "nu", current: str = "total", variation: str = "central") -> Quantity:
        energy = u.Quantity(energy)
        if energy.unit == u.dimensionless_unscaled:
            raise u.UnitsError("energy must have physical units.")
        energy_GeV = np.asarray(energy.to_value(u.GeV), dtype=float)
        if np.any(~np.isfinite(energy_GeV)) or np.any(energy_GeV <= 0):
            raise ValueError("energy must contain finite positive values.")

        particle = _normalize(particle, _PARTICLES, "particle")
        current = _normalize(current, _CURRENTS, "current")
        variation = _normalize(variation, _VARIATIONS, "variation")
        emin = float(self.parameters["energy_min_GeV"])
        emax = float(self.parameters["energy_max_GeV"])
        if np.any(energy_GeV < emin) or np.any(energy_GeV > emax):
            raise ValueError(f"CTW 2011 is supported only for {emin:g} <= E_nu/GeV <= {emax:g}.")

        coefficients = self.parameters["coefficients"][variation][particle]
        if current == "total":
            return self._evaluate_eq7(energy_GeV, coefficients["cc"]) + self._evaluate_eq7(energy_GeV, coefficients["nc"])
        return self._evaluate_eq7(energy_GeV, coefficients[current])
