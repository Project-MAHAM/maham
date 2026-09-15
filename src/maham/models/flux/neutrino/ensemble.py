import astropy.units as u
import numpy as np

from astropy.table import QTable
from astropy.units import Quantity

from maham.models.flux.neutrino.base import NeutrinoFluxModel
from maham.models.registry import get_models
from maham.physics.neutrino import normalize_flavor_convention
from maham.physics.spectra import normalize_spectral_quantity


def build_envelope(models: tuple[NeutrinoFluxModel, ...], energy: Quantity | None = None, quantity: str = "E2phi", flavor: str | None = None, flavor_assumption: str | None = None, points_per_decade: int = 40, cache: bool = True, show_progress: bool = True) -> QTable:
    if not models:
        raise ValueError("At least one neutrino flux model is required.")
    if points_per_decade < 1:
        raise ValueError("points_per_decade must be at least 1.")

    quantity = normalize_spectral_quantity(quantity)
    if flavor is None:
        native_flavors = {normalize_flavor_convention(model.metadata.flavor_convention) for model in models if model.metadata.flavor_convention is not None}
        if len(native_flavors) != 1:
            raise ValueError("Models with different flavor conventions require an explicit target flavor.")
        target_flavor = native_flavors.pop()
    else:
        target_flavor = normalize_flavor_convention(flavor)

    if energy is None:
        supports = [model.support(cache=cache, show_progress=show_progress) for model in models]
        energy_unit = supports[0][0].unit
        emin = min(lower.to_value(energy_unit) for lower, _ in supports)
        emax = max(upper.to_value(energy_unit) for _, upper in supports)
        n_points = max(2, int(np.ceil(np.log10(emax / emin) * points_per_decade)) + 1)
        energy = np.logspace(np.log10(emin), np.log10(emax), n_points) * energy_unit
    else:
        energy = u.Quantity(energy)

    curves = [model.evaluate(energy, quantity=quantity, flavor=target_flavor, flavor_assumption=flavor_assumption, cache=cache, show_progress=show_progress) for model in models]
    value_unit = curves[0].unit
    values = np.vstack([curve.to_value(value_unit) for curve in curves])
    finite = np.isfinite(values)
    n_models = finite.sum(axis=0)

    lower = np.where(finite, values, np.inf).min(axis=0)
    upper = np.where(finite, values, -np.inf).max(axis=0)
    lower[n_models == 0] = np.nan
    upper[n_models == 0] = np.nan

    table = QTable()
    table["energy"] = energy
    table[f"{quantity}_lower"] = lower * value_unit
    table[f"{quantity}_upper"] = upper * value_unit
    table["n_models"] = n_models
    table.meta["quantity"] = quantity
    table.meta["flavor_convention"] = target_flavor
    table.meta["model_ids"] = tuple(model.id for model in models)
    return table


def family_envelope(family: str, energy: Quantity | None = None, quantity: str = "E2phi", flavor: str | None = None, flavor_assumption: str | None = None, points_per_decade: int = 40, cache: bool = True, show_progress: bool = True) -> QTable:
    models = get_models(messenger="neutrino", model_type="flux", family=family)
    if not models:
        raise KeyError(f"No registered neutrino flux models in family '{family}'.")
    if not all(isinstance(model, NeutrinoFluxModel) for model in models):
        raise TypeError(f"Family '{family}' contains a registered model that is not a NeutrinoFluxModel.")
    table = build_envelope(models, energy=energy, quantity=quantity, flavor=flavor, flavor_assumption=flavor_assumption, points_per_decade=points_per_decade, cache=cache, show_progress=show_progress)
    table.meta["family"] = family
    return table
