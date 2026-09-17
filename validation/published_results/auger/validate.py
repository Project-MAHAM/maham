from pathlib import Path

import astropy.units as u
import matplotlib.pyplot as plt
import numpy as np

from maham.datasets import get_dataset
from maham.plotting import apply_plot_style, bold_legend, bold_tick_labels
from maham.physics.spectra import apply_energy_weighting


OUTPUT_DIR = Path(__file__).resolve().parent / "outputs"
E26J_UNIT = u.eV**1.6 / (u.km**2 * u.yr * u.sr)
E2PHI_UNIT = u.GeV / (u.cm**2 * u.s * u.sr)


def require(condition, message):
    if not condition:
        raise AssertionError(message)
    print(f"PASS: {message}")


def validate_auger_spectrum():
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


def validate_diffuse_neutrino_limit(limit, limit_all):
    require(len(limit) == 8, "diffuse neutrino limit contains eight digitized half-decade bins")
    require(limit.meta["flavor_convention"] == "per_flavor", "diffuse neutrino limit is native single flavor")
    require(np.isclose(limit.meta["confidence_level"], 0.90), "diffuse neutrino limit is 90% CL")
    require(limit.meta["limit_normalization_convention"] == "log10_energy_width", "differential-limit normalization is represented as a logarithmic energy width")
    require(np.isclose(limit.meta["log10_energy_width_decades"], 0.5), "native differential limit uses a half-decade energy width")
    require(limit.meta["observation_period"] == "2004-01-01/2021-12-31", "2004-2021 observation period is retained")
    require(np.all(np.asarray(limit["is_upper_limit"], dtype=bool)), "all differential-limit points are upper limits")
    require(u.allclose(limit["E2phi"][0], 7.583e-8 * E2PHI_UNIT), "digitized first differential-limit value is reproduced")
    require(u.allclose(limit["E2phi"][2], 1.151e-8 * E2PHI_UNIT), "digitized minimum-region differential-limit value is reproduced")
    require(u.allclose(limit["E2phi"][-1], 3.468e-7 * E2PHI_UNIT), "digitized highest-energy differential-limit value is reproduced")
    require(limit_all.meta["flavor_convention"] == "all_flavor", "all-flavor view is explicitly constructed")
    require(limit_all.meta["flavor_assumption"] == "equal", "all-flavor view records the equal-flavor assumption")
    require(u.allclose(limit_all["E2phi"], 3 * limit["E2phi"]), "equal-flavor conversion gives a factor of three")


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


def plot_diffuse_neutrino_limit(limit):
    energy = limit["energy"].to_value(u.GeV)
    y = limit["E2phi"].to_value(E2PHI_UNIT)

    fig, ax = plt.subplots(figsize=(7, 5))
    ax.loglog(energy, y, color="black", linewidth=2.5)
    ax.set_xlim(3e7, 3e11)
    ax.set_ylim(3e-9, 3e-7)
    ax.set_xlabel(r"Neutrino energy, $E_{\nu}$ [GeV]")
    ax.set_ylabel(r"Flux, $E^{2}\Phi$ [GeV cm$^{-2}$ s$^{-1}$ sr$^{-1}$]")
    ax.set_title("Pierre Auger Diffuse Neutrino Upper Limit (2023)")
    ax.grid(True, which="both", alpha=0.25)
    ax.text(0.97, 0.03, "Single flavor\n90% CL", transform=ax.transAxes, ha="right", va="bottom", fontweight="bold")
    bold_tick_labels(ax)
    fig.tight_layout()
    fig.savefig(OUTPUT_DIR / "auger_diffuse_neutrino_limit_2023.png", dpi=200)
    fig.savefig(OUTPUT_DIR / "auger_diffuse_neutrino_limit_2023.pdf")
    plt.close(fig)


def main():
    apply_plot_style()
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    spectrum = validate_auger_spectrum()
    limit = get_dataset("auger.diffuse_neutrino_limit.2023").load_e2phi()
    limit_all = get_dataset("auger.diffuse_neutrino_limit.2023").load_e2phi(flavor="all_flavor", flavor_assumption="equal")

    print("\nDiffuse neutrino upper limit 2023:")
    validate_diffuse_neutrino_limit(limit, limit_all)

    plot_auger_spectrum(spectrum)
    plot_diffuse_neutrino_limit(limit)
    print(f"Validation outputs written to {OUTPUT_DIR}")


if __name__ == "__main__":
    main()
