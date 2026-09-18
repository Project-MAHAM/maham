"""Physical constants used by MAHAM calculations.

Values are explicit and unit-bearing so calculations remain reproducible across library versions.
"""

import astropy.units as u


# CODATA 2018 proton mass.
PROTON_MASS = 1.67262192369e-24 * u.g

__all__ = ["PROTON_MASS"]
