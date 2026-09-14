import astropy.units as u
from astropy.units import Quantity


_SINGLE_FLAVOR_CONVENTIONS = {"per_flavor", "numu_nubar"}


def normalize_flavor_convention(flavor: str) -> str:
    """Return the canonical MAHAM name for a neutrino flavor convention."""
    aliases = {
        "per_flavor": "per_flavor",
        "all_flavor": "all_flavor",
        "numu_nubar": "numu_nubar",
        "numu_plus_numubar": "numu_nubar",
        "nu_mu_nubar_mu": "numu_nubar",
    }
    try:
        key = flavor.strip().lower().replace("-", "_").replace(" ", "_")
        return aliases[key]
    except (AttributeError, KeyError) as exc:
        raise ValueError("Flavor convention must be 'per_flavor', 'all_flavor', or 'numu_nubar'.") from exc


def normalize_flavor_assumption(assumption: str | None) -> str | None:
    """Return the canonical MAHAM name for a flavor assumption."""
    if assumption is None:
        return None
    key = assumption.strip().lower().replace("-", "_").replace(" ", "_")
    if key == "equal":
        return "equal"
    raise ValueError("Currently supported flavor assumption: 'equal'.")


def convert_flavor_convention(values: Quantity, from_flavor: str, to_flavor: str, assumption: str | None = None) -> Quantity:
    """Convert neutrino quantities between supported flavor conventions."""
    values = u.Quantity(values)
    source = normalize_flavor_convention(from_flavor)
    target = normalize_flavor_convention(to_flavor)

    if source == target:
        return values

    assumption = normalize_flavor_assumption(assumption)
    if assumption != "equal":
        raise ValueError("Converting between different flavor conventions requires flavor_assumption='equal'.")

    if source in _SINGLE_FLAVOR_CONVENTIONS and target == "all_flavor":
        return values * 3.0
    if source == "all_flavor" and target in _SINGLE_FLAVOR_CONVENTIONS:
        return values / 3.0
    if source in _SINGLE_FLAVOR_CONVENTIONS and target in _SINGLE_FLAVOR_CONVENTIONS:
        return values

    raise ValueError(f"Unsupported flavor conversion from '{source}' to '{target}'.")
