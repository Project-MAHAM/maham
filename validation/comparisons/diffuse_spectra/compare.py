from pathlib import Path

import astropy.units as u
import matplotlib.pyplot as plt
import numpy as np

from maham.datasets import get_dataset
from maham.plotting import apply_plot_style, bold_legend, bold_tick_labels, plot_upper_limits
from maham.spectra import normalize_spectral_quantity, spectral_quantity_info


PLOT_QUANTITY = "E2phi"  # Try "E3J" or "E2phi" for the alternate common representation.

OUTPUT_DIR = Path(__file__).resolve().parent / "outputs"

UNIT_LABELS = {
    0: r"GeV$^{-1}$ cm$^{-2}$ s$^{-1}$ sr$^{-1}$",
    1: r"cm$^{-2}$ s$^{-1}$ sr$^{-1}$",
    2: r"GeV cm$^{-2}$ s$^{-1}$ sr$^{-1}$",
    3: r"GeV$^{2}$ cm$^{-2}$ s$^{-1}$ sr$^{-1}$",
}


def require(condition, message):
    if not condition:
        raise AssertionError(message)
    print(f"PASS: {message}")


def common_unit(quantity):
    _, power = spectral_quantity_info(quantity)
    return u.GeV ** (power - 1) / (u.cm**2 * u.s * u.sr)


def quantity_label(quantity):
    family, power = spectral_quantity_info(quantity)
    symbol = r"\Phi" if family == "phi" else "J"
    prefix = "" if power == 0 else "E" if power == 1 else rf"E^{{{power}}}"
    return rf"${prefix}{symbol}(E)$"


def load_datasets():
    quantity = normalize_spectral_quantity(PLOT_QUANTITY)

    auger = get_dataset("auger.combined_spectrum.2021").load(quantity=quantity)
    glashow = get_dataset("icecube.glashow.flux.2021").load(quantity=quantity, flavor="all_flavor", flavor_assumption="equal")
    ehe_limit = get_dataset("icecube.ehe.differential_limit.2025").load(quantity=quantity)
    ehe_sensitivity = get_dataset("icecube.ehe.sensitivity.2025").load(quantity=quantity)

    return auger, glashow, ehe_limit, ehe_sensitivity


def validate_comparison(auger, glashow, ehe_limit, ehe_sensitivity):
    quantity = normalize_spectral_quantity(PLOT_QUANTITY)
    unit = common_unit(quantity)

    for name, table in (
        ("Auger", auger),
        ("IceCube Glashow", glashow),
        ("IceCube EHE limit", ehe_limit),
        ("IceCube EHE sensitivity", ehe_sensitivity),
    ):
        require(table.meta["quantity"] == quantity, f"{name} is represented as {quantity}")
        table[quantity].to(unit)
        require(True, f"{name} is convertible to the common physical unit")

    require(glashow.meta["flavor_convention"] == "all_flavor", "Glashow spectrum uses the all-flavor comparison convention")


def plot_comparison(auger, glashow, ehe_limit, ehe_sensitivity):
    quantity = normalize_spectral_quantity(PLOT_QUANTITY)
    unit = common_unit(quantity)
    _, power = spectral_quantity_info(quantity)

    fig, ax = plt.subplots(figsize=(10, 5))
    ax.set_xscale("log")
    ax.set_yscale("log")
    ax.set_xlim(2e6, 2e11)

    energy = auger["energy"].to_value(u.GeV)
    y = auger[quantity].to_value(unit)
    stat_lower = auger[f"{quantity}_stat_err_lower"].to_value(unit)
    stat_upper = auger[f"{quantity}_stat_err_upper"].to_value(unit)
    ax.errorbar(energy, y, yerr=np.vstack((stat_lower, stat_upper)), fmt="o", linestyle="none", markersize=5, markerfacecolor="white", markeredgewidth=1.2, elinewidth=1.2, capsize=2, label="Auger 2021")

    energy = ehe_limit["energy"].to_value(u.GeV)
    y = ehe_limit[quantity].to_value(unit)
    ax.plot(energy, y, marker="o", markerfacecolor="white", markeredgewidth=1.5, linewidth=2, markersize=6, label="IceCube EHE limit")

    energy = ehe_sensitivity["energy"].to_value(u.GeV)
    y = ehe_sensitivity[quantity].to_value(unit)
    ax.plot(energy, y, marker="s", markerfacecolor="white", markeredgewidth=1.5, linestyle="--", linewidth=2, markersize=5.5, label="IceCube EHE sensitivity")

    energy = glashow["energy"].to_value(u.GeV)
    energy_min = glashow["energy_min"].to_value(u.GeV)
    energy_max = glashow["energy_max"].to_value(u.GeV)
    xerr = np.vstack((energy - energy_min, energy_max - energy))
    upper = np.asarray(glashow["is_upper_limit"], dtype=bool)
    measured = ~upper

    y = glashow[quantity].to_value(unit)
    y_lower = glashow[f"{quantity}_lower"].to_value(unit)
    y_upper = glashow[f"{quantity}_upper"].to_value(unit)
    yerr = np.vstack((y[measured] - y_lower[measured], y_upper[measured] - y[measured]))

    ax.errorbar(energy[measured], y[measured], xerr=xerr[:, measured], yerr=yerr, fmt="*", markersize=10, capsize=3, elinewidth=1.5, markeredgecolor="black", ecolor="black", markerfacecolor="white", markeredgewidth=1.5, linestyle="none", label="IceCube Glashow")
    plot_upper_limits(ax, energy[upper], y_upper[upper], xerr=xerr[:, upper], arrow_factor=2.5, color="black", linewidth=1.5, capsize=3, mutation_scale=12)

    ax.set_xlabel(r"Particle energy, $E$ [GeV]")
    ax.set_ylabel(rf"Scaled differential intensity, {quantity_label(quantity)} [{UNIT_LABELS[power]}]")
    ax.set_title("Diffuse Spectrum Comparison")
    ax.grid(True, which="both", alpha=0.25)
    ax.text(0.97, 0.02, r"All flavors neutrino" "\n" r"$\nu_e:\nu_\mu:\nu_\tau=1:1:1$, $\nu:\bar{\nu}=1:1$", transform=ax.transAxes, ha="right", va="bottom", fontweight="bold")

    bold_tick_labels(ax)
    bold_legend(ax.legend(loc="best"))
    fig.tight_layout()

    stem = f"diffuse_spectra_{quantity.lower()}"
    fig.savefig(OUTPUT_DIR / f"{stem}.png", dpi=200)
    fig.savefig(OUTPUT_DIR / f"{stem}.pdf")
    plt.close(fig)


def main():
    apply_plot_style()
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    auger, glashow, ehe_limit, ehe_sensitivity = load_datasets()
    validate_comparison(auger, glashow, ehe_limit, ehe_sensitivity)
    plot_comparison(auger, glashow, ehe_limit, ehe_sensitivity)

    print(f"Comparison outputs written to {OUTPUT_DIR}")


if __name__ == "__main__":
    main()
