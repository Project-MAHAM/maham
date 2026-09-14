from pathlib import Path

import astropy.units as u
import matplotlib.pyplot as plt
import numpy as np
from scipy.integrate import trapezoid
from scipy.interpolate import interp1d

from maham.datasets import get_dataset
from maham.plotting.style import apply_plot_style, bold_tick_labels, bold_legend


OUTPUT_DIR = Path(__file__).resolve().parent / "outputs"

ENERGY_MIN_GEV = 7.24e7
ENERGY_MEDIAN_GEV = 2.18e8
ENERGY_MAX_GEV = 2.57e9
LIVETIME_DAYS = 335

FC_INTERVALS = {
    "1sigma": np.array([0.3679, 2.7506]),
    "2sigma": np.array([0.0466, 5.1433]),
    "3sigma": np.array([0.0028, 8.3077]),
}


def require(condition, message):
    if not condition:
        raise AssertionError(message)
    print(f"[PASS] {message}")


def reproduce_flux(area):
    energy = area["energy"].to_value(u.GeV)
    effective_area = area["effective_area_total"].to_value(u.cm**2)

    interpolator = interp1d(energy, effective_area, bounds_error=False, fill_value=0)
    x = np.logspace(np.log10(ENERGY_MIN_GEV), np.log10(ENERGY_MAX_GEV), 200)
    acceptance = trapezoid(y=x**-2 * interpolator(x), x=x)
    livetime = LIVETIME_DAYS * 86400.0
    flux = 1.0 / (4.0 * np.pi * livetime * acceptance)

    return flux * u.GeV / (u.cm**2 * u.s * u.sr), acceptance


def validate_effective_area(area):
    energy = area["energy"].to_value(u.GeV)
    effective_area = area["effective_area_total"].to_value(u.cm**2)

    require(len(area) == 60, "Effective area contains 60 released points")
    require(np.all(np.diff(energy) > 0), "Effective-area energy grid is strictly increasing")
    require(np.all(effective_area >= 0), "Effective area is non-negative")
    require(np.count_nonzero(effective_area[:6]) == 0, "First six released effective-area values are zero")
    require(np.all(effective_area[6:] > 0), "Released effective area is positive above the initial zero region")
    require(np.isclose(energy[0], 112201.845), "First released energy is reproduced")
    require(np.isclose(energy[-1], 89125093800.0), "Last released energy is reproduced")
    require(np.isclose(effective_area[-1], 35343948.1), "Final released effective-area value is reproduced")


def validate_flux_reproduction(area, published):
    unit = u.GeV / (u.cm**2 * u.s * u.sr)
    reproduced, acceptance = reproduce_flux(area)
    published_flux = published["E2phi"][0]

    print("\nFlux reproduction:")
    print(f"  Acceptance integral = {acceptance:.8e} cm2/GeV")
    print(f"  Reproduced E2phi    = {reproduced.to_value(unit):.8e} GeV cm-2 s-1 sr-1")
    print(f"  Published E2phi     = {published_flux.to_value(unit):.8e} GeV cm-2 s-1 sr-1")

    require(np.isclose(reproduced.to_value(unit), 5.80e-8, rtol=0.01), "Official one-event flux normalization is reproduced")
    require(np.isclose(reproduced.to_value(unit), published_flux.to_value(unit), rtol=0.01), "Reproduced flux agrees with MAHAM published-flux dataset")

    for label, factors in FC_INTERVALS.items():
        reproduced_interval = factors * reproduced
        if label == "1sigma":
            lower, upper = published["E2phi_lower"][0], published["E2phi_upper"][0]
        else:
            lower = published[f"E2phi_{label}_lower"][0]
            upper = published[f"E2phi_{label}_upper"][0]

        print(f"  {label}: {reproduced_interval[0].to_value(unit):.8e} -- {reproduced_interval[1].to_value(unit):.8e}")
        require(np.isclose(reproduced_interval[0].to_value(unit), lower.to_value(unit), rtol=0.01), f"{label} lower Feldman-Cousins bound is reproduced")
        require(np.isclose(reproduced_interval[1].to_value(unit), upper.to_value(unit), rtol=0.01), f"{label} upper Feldman-Cousins bound is reproduced")

    require(u.allclose(published["energy_min"][0], ENERGY_MIN_GEV * u.GeV), "5th-percentile neutrino energy is reproduced")
    require(u.allclose(published["energy"][0], ENERGY_MEDIAN_GEV * u.GeV), "Median neutrino energy is reproduced")
    require(u.allclose(published["energy_max"][0], ENERGY_MAX_GEV * u.GeV), "95th-percentile neutrino energy is reproduced")


def plot_effective_area(area):
    apply_plot_style()

    energy = area["energy"].to_value(u.GeV)
    effective_area = area["effective_area_total"].to_value(u.km**2)

    fig, ax = plt.subplots(figsize=(7, 5))
    ax.loglog(energy, effective_area, linewidth=2.5)
    ax.axvspan(ENERGY_MIN_GEV, ENERGY_MAX_GEV, alpha=0.15, label="Central 90% range")
    ax.axvline(ENERGY_MEDIAN_GEV, linestyle="--", linewidth=2, label="Median energy")

    ax.set_xlabel(r"Neutrino energy, $E_\nu$ [GeV]")
    ax.set_ylabel(r"Effective area, $A_{\mathrm{eff}}$ [km$^2$]")
    ax.set_title("KM3NeT KM3-230213A Effective Area", fontweight="bold")

    ax.grid(True, which="major", alpha=0.35)
    ax.grid(True, which="minor", alpha=0.15)

    bold_tick_labels(ax)
    legend = ax.legend(loc="upper left")
    bold_legend(legend)

    fig.tight_layout()
    fig.savefig(OUTPUT_DIR / "km3net_230213a_effective_area.png", dpi=200)
    fig.savefig(OUTPUT_DIR / "km3net_230213a_effective_area.pdf")
    plt.close(fig)


def main():
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    area = get_dataset("km3net.km3_230213a_effective_area.2025").load()
    published = get_dataset("km3net.km3_230213a_flux.2025").load_e2phi()

    print("KM3NeT KM3-230213A validation\n")
    validate_effective_area(area)
    validate_flux_reproduction(area, published)
    plot_effective_area(area)

    print("\nAll KM3NeT validation checks passed.")
    print(f"Outputs: {OUTPUT_DIR}")


if __name__ == "__main__":
    main()
