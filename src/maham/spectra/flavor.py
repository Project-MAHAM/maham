import astropy.units as u
from astropy.units import Quantity


def normalize_flavor_convention(flavor: str) -> str:
    """Return the canonical MAHAM name for a neutrino flavor convention."""
    aliases = {"per_flavor": "per_flavor", "all_flavor": "all_flavor"}
    try:
        key = flavor.strip().lower().replace("-", "_").replace(" ", "_")
        return aliases[key]
    except (AttributeError, KeyError) as exc:
        raise ValueError("Flavor convention must be 'per_flavor' or 'all_flavor'.") from exc


def normalize_flavor_assumption(assumption: str | None) -> str | None:
    """Return the canonical MAHAM name for a flavor assumption."""
    if assumption is None:
        return None
    key = assumption.strip().lower().replace("-", "_").replace(" ", "_")
    if key == "equal":
        return "equal"
    raise ValueError("Currently supported flavor assumption: 'equal'.")


def convert_flavor_convention(values: Quantity, from_flavor: str, to_flavor: str, assumption: str | None = None) -> Quantity:
    """Convert between per-flavor and all-flavor neutrino quantities."""
    values = u.Quantity(values)
    source = normalize_flavor_convention(from_flavor)
    target = normalize_flavor_convention(to_flavor)
    if source == target:
        return values
    assumption = normalize_flavor_assumption(assumption)
    if assumption != "equal":
        raise ValueError("Converting between per_flavor and all_flavor requires flavor_assumption='equal'.")
    factor = 3.0 if source == "per_flavor" and target == "all_flavor" else 1.0 / 3.0
    return values * factor
