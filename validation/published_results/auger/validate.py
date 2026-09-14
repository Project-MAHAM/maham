from pathlib import Path

import astropy.units as u
import matplotlib.pyplot as plt
import numpy as np

from maham.datasets import get_dataset
from maham.plotting import apply_plot_style, bold_legend, bold_tick_labels
from maham.physics.spectra import apply_energy_weighting


OUTPUT_DIR = Path(__file__).resolve().parent / "outputs"
E26J_UNIT = u.eV**1.6 / (u.km**2 * u.yr * u.sr)


def require(condition, message):
    if not condition:
        raise AssertionError(message)
    print(f"PASS: {message}")


def validate_auger():
    dataset = get_dataset("auger.combined_spectrum.2021")
    raw = dataset.load_raw()
    table = dataset.load_j()

    require(len(raw) == 32, "combined spectrum contains 32 points")
    require(len(table) == 32, "standardized spectrum contains 32 points")
    require(dataset.metadata.quantity == "J", "native quantity is J")
    require(dataset.metadata.spectral_kind == "differential_intensity", "spectral kind is differential intensity")
    require(np.isclose(raw["lgE_eV"][0], 17.05), "first lg(E/eV) is 17.05")
    require(np.isclose(raw["lgE_eV"][-1], 20.15), "last lg(E/eV) is 20.15")
    require(np.isclose(raw["J"][0], 6.341e-14), "first J matches the published release")
    require(np.isclose(raw["J"][-1], 2.9e-24), "last J matches the published release")
    require(np.all(np.diff(table["energy"].to_value(u.eV)) > 0), "energy grid is strictly increasing")
    require(np.all(raw["J_stat_err_lower"] >= 0) and np.all(raw["J_stat_err_upper"] >= 0), "statistical uncertainties are non-negative")
    require(np.all(raw["J_sys_err_lower"] >= 0) and np.all(raw["J_sys_err_upper"] >= 0), "systematic uncertainties are non-negative")

    expected_energy = 10 ** np.asarray(raw["lgE_eV"], dtype=float) * u.eV
    expected_min = 10 ** (np.asarray(raw["lgE_eV"], dtype=float) - np.asarray(raw["lgE_halfwidth"], dtype=float)) * u.eV
    expected_max = 10 ** (np.asarray(raw["lgE_eV"], dtype=float) + np.asarray(raw["lgE_halfwidth"], dtype=float)) * u.eV
    require(u.allclose(table["energy"], expected_energy), "energies reproduce the published logarithmic bin centers")
    require(u.allclose(table["energy_min"], expected_min), "lower bin edges reproduce the published bins")
    require(u.allclose(table["energy_max"], expected_max), "upper bin edges reproduce the published bins")

    return table


def plot_auger_spectrum(table):
    energy = table["energy"].to_value(u.eV)
    weighted = apply_energy_weighting(table["energy"], table["J"], 2.6).to_value(E26J_UNIT)
    stat_lower = apply_energy_weighting(table["energy"], table["J_stat_err_lower"], 2.6).to_value(E26J_UNIT)
    stat_upper = apply_energy_weighting(table["energy"], table["J_stat_err_upper"], 2.6).to_value(E26J_UNIT)

    fig, ax = plt.subplots(figsize=(7, 5))
    ax.set_xscale("log")
    ax.set_yscale("log")
    ax.set_xlim(8e16, 2e20)
    ax.set_ylim(4e28, 2e31)

    ax.errorbar(energy, weighted, yerr=np.vstack((stat_lower, stat_upper)), fmt="o", linestyle="none", markersize=5.5, markerfacecolor="white", markeredgecolor="black", markeredgewidth=1.2, ecolor="black", elinewidth=1.3, capsize=2.5, label="Auger 2021")

    ax.set_xlabel(r"Cosmic-ray energy, $E$ [eV]")
    ax.set_ylabel(r"Scaled flux, $E^{2.6}J(E)$ [km$^{-2}$ yr$^{-1}$ sr$^{-1}$ eV$^{1.6}$]")
    ax.set_title("Pierre Auger Combined Cosmic-Ray Spectrum (2021)")
    ax.grid(True, which="both", alpha=0.25)

    bold_tick_labels(ax)
    bold_legend(ax.legend(loc="best"))
    fig.tight_layout()
    fig.savefig(OUTPUT_DIR / "auger_combined_spectrum_2021.png", dpi=200)
    fig.savefig(OUTPUT_DIR / "auger_combined_spectrum_2021.pdf")
    plt.close(fig)


def main():
    apply_plot_style()
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    table = validate_auger()
    plot_auger_spectrum(table)
    print(f"Validation outputs written to {OUTPUT_DIR}")


if __name__ == "__main__":
    main()
