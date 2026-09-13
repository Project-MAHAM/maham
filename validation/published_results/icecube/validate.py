from pathlib import Path

import astropy.units as u
import matplotlib.pyplot as plt
import numpy as np

from maham.datasets import get_dataset
from maham.plotting import apply_plot_style, bold_legend, bold_tick_labels, plot_upper_limits


apply_plot_style()

OUTPUT_DIR = Path(__file__).parent / "outputs"
E2PHI_UNIT = u.GeV / (u.cm**2 * u.s * u.sr)


def require(condition, message):
    if not condition:
        print(f"[FAIL] {message}")
        raise AssertionError(message)
    print(f"[PASS] {message}")


def validate_ehe(limit, sensitivity):
    require(len(limit) == 10, "EHE differential limit contains 10 published points")
    require(len(sensitivity) == 10, "EHE sensitivity contains 10 published points")
    require(u.allclose(limit["energy"], sensitivity["energy"]), "EHE limit and sensitivity energy grids agree")
    require(np.all(limit["is_upper_limit"]), "All EHE differential-limit points are marked as upper limits")
    require(limit.meta["flavor_convention"] == "all_flavor", "EHE differential limit is all-flavor")
    require(sensitivity.meta["flavor_convention"] == "all_flavor", "EHE sensitivity is all-flavor")
    require(np.isclose(limit.meta["confidence_level"], 0.90), "EHE differential limit confidence level is 90%")
    require(np.isclose(sensitivity.meta["confidence_level"], 0.90), "EHE sensitivity confidence level is 90%")
    require(u.allclose(limit["energy"][3], 1e8 * u.GeV), "Published EHE 1e8 GeV reference energy is reproduced")
    require(u.allclose(limit["E2phi"][3], 5.743e-9 * E2PHI_UNIT), "Published EHE 1e8 GeV differential limit is reproduced")
    require(u.allclose(sensitivity["E2phi"][3], 5.142e-9 * E2PHI_UNIT), "Published EHE 1e8 GeV sensitivity is reproduced")


def validate_glashow(glashow, glashow_all):
    require(len(glashow) == 3, "Glashow spectrum contains 3 published energy bins")
    require(glashow.meta["flavor_convention"] == "per_flavor", "Glashow native flux is per-flavor")
    require(np.isclose(glashow.meta["confidence_level"], 0.683), "Glashow confidence level is 68.3%")
    require(glashow["is_upper_limit"].tolist() == [True, False, True], "Glashow upper-limit bins are correctly identified")
    require(u.allclose(glashow["E2phi"][1], 1.9e-9 * E2PHI_UNIT), "Published Glashow middle-bin E2phi is reproduced")
    require(u.allclose(glashow["E2phi_lower"][1], 8e-10 * E2PHI_UNIT), "Published Glashow middle-bin lower bound is reproduced")
    require(u.allclose(glashow["E2phi_upper"][1], 1.13e-8 * E2PHI_UNIT), "Published Glashow middle-bin upper bound is reproduced")
    require(glashow_all.meta["flavor_convention"] == "all_flavor", "Glashow all-flavor view is explicitly constructed")
    require(glashow_all.meta["flavor_assumption"] == "equal", "Glashow all-flavor view records the equal-flavor assumption")
    require(u.allclose(glashow_all["E2phi"][1], 5.7e-9 * E2PHI_UNIT), "Glashow equal-flavor all-flavor conversion is reproduced")


def validate_effective_area(area):
    require(len(area) == 100, "Effective area contains 100 published points")
    energy = area["energy"].to_value(u.GeV)
    require(np.all(np.diff(energy) > 0), "Effective-area energy grid is strictly increasing")

    flavor_sum = area["effective_area_nue"] + area["effective_area_numu"] + area["effective_area_nutau"]
    relative_difference = np.abs((area["effective_area_total"] - flavor_sum) / area["effective_area_total"]).to_value(u.dimensionless_unscaled)
    max_relative_difference = float(np.max(relative_difference))

    require(max_relative_difference < 0.01, "Total effective area agrees with flavor sum within 1% published precision")
    require(u.allclose(area["energy"][15], 5.97e6 * u.GeV), "Published 5.97 PeV effective-area reference energy is reproduced")
    require(u.allclose(area["effective_area_total"][15], 512.0 * u.m**2), "Published 5.97 PeV total effective area is reproduced")

    window = (energy >= 5e6) & (energy <= 8e6)
    window_indices = np.where(window)[0]
    peak_index = window_indices[np.argmax(area["effective_area_nue"][window])]
    peak_energy = area["energy"][peak_index]
    peak_area = area["effective_area_nue"][peak_index]

    require(5.5e6 * u.GeV < peak_energy < 6.5e6 * u.GeV, "Local nue effective-area enhancement occurs near the Glashow-resonance energy")
    require(u.allclose(peak_energy, 5.97e6 * u.GeV), "Published nue Glashow-region peak energy is reproduced")
    require(u.allclose(peak_area, 471.0 * u.m**2), "Published nue Glashow-region effective-area peak is reproduced")

    print(f"       Maximum total-vs-flavor-sum difference: {100 * max_relative_difference:.3f}%")
    print(f"       Local nue effective-area peak: {peak_energy.to_value(u.PeV):.3f} PeV, {peak_area.to_value(u.m**2):.1f} m2")


def plot_flux_results(limit, sensitivity, glashow):
    fig, ax = plt.subplots(figsize=(7, 5))
    ax.set_xlim(2e6, 2e11)
    ax.set_ylim(1e-9, 1.2e-6)

    ax.loglog(limit["energy"].to_value(u.GeV), limit["E2phi"].to_value(E2PHI_UNIT), marker="o", markerfacecolor="white", markeredgewidth=1.5, linewidth=2, markersize=6, label="EHE limit")
    ax.loglog(sensitivity["energy"].to_value(u.GeV), sensitivity["E2phi"].to_value(E2PHI_UNIT), marker="s", markerfacecolor="white", markeredgewidth=1.5, linestyle="--", linewidth=2, markersize=5.5, label="EHE sensitivity")

    energy = glashow["energy"].to_value(u.GeV)
    energy_min = glashow["energy_min"].to_value(u.GeV)
    energy_max = glashow["energy_max"].to_value(u.GeV)
    xerr = np.vstack((energy - energy_min, energy_max - energy))
    upper = np.asarray(glashow["is_upper_limit"], dtype=bool)
    measured = ~upper

    y = glashow["E2phi"].to_value(E2PHI_UNIT)
    y_lower = glashow["E2phi_lower"].to_value(E2PHI_UNIT)
    y_upper = glashow["E2phi_upper"].to_value(E2PHI_UNIT)
    yerr = np.vstack((y[measured] - y_lower[measured], y_upper[measured] - y[measured]))

    ax.errorbar(energy[measured], y[measured], xerr=xerr[:, measured], yerr=yerr, fmt="*", markersize=10, capsize=3, elinewidth=1.5, markeredgecolor="black", ecolor="black", markerfacecolor="white", markeredgewidth=1.5, linestyle="none", label="Glashow")
    plot_upper_limits(ax, energy[upper], y_upper[upper], xerr=xerr[:, upper], arrow_factor=2.5, color="black", linewidth=1.5, capsize=3, mutation_scale=12)

    ax.set_xlabel(r"Neutrino energy, $E_{\nu}$ [GeV]")
    ax.set_ylabel(r"Flux, $E^{2}\Phi$ [GeV cm$^{-2}$ s$^{-1}$ sr$^{-1}$]")
    ax.set_title("IceCube Neutrino Flux Results")
    ax.grid(True, which="both", alpha=0.25)

    ax.text(0.97, 0.06, r"All flavors" "\n" r"$\nu_e:\nu_\mu:\nu_\tau=1:1:1$" "\n" r"$\nu:\bar{\nu}=1:1$", transform=ax.transAxes, ha="right", va="bottom", fontweight="bold")

    bold_tick_labels(ax)
    bold_legend(ax.legend(loc="upper right"))
    fig.tight_layout()
    fig.savefig(OUTPUT_DIR / "icecube_flux_results.png", dpi=200)
    fig.savefig(OUTPUT_DIR / "icecube_flux_results.pdf")
    plt.close(fig)


def plot_effective_area(area):
    energy = area["energy"].to_value(u.GeV)
    fig, ax = plt.subplots(figsize=(7, 5))
    ax.set_xlim(8e5, 2e11)

    ax.loglog(energy, area["effective_area_total"].to_value(u.km**2), label="Total", linewidth=2)
    ax.loglog(energy, area["effective_area_nue"].to_value(u.km**2), label=r"$(\nu_e+\bar{\nu}_e)/2$")
    ax.loglog(energy, area["effective_area_numu"].to_value(u.km**2), label=r"$(\nu_\mu+\bar{\nu}_\mu)/2$")
    ax.loglog(energy, area["effective_area_nutau"].to_value(u.km**2), label=r"$(\nu_\tau+\bar{\nu}_\tau)/2$")

    ax.set_xlabel(r"Neutrino energy, $E_{\nu}$ [GeV]")
    ax.set_ylabel(r"Effective area, $A_{\mathrm{eff}}$ [km$^{2}$]")
    ax.set_title("IceCube EHE 2025 Effective Area")
    ax.grid(True, which="both", alpha=0.25)

    bold_tick_labels(ax)
    bold_legend(ax.legend(loc="upper left"))
    fig.tight_layout()
    fig.savefig(OUTPUT_DIR / "icecube_ehe_2025_effective_area.png", dpi=200)
    fig.savefig(OUTPUT_DIR / "icecube_ehe_2025_effective_area.pdf")
    plt.close(fig)


def main():
    OUTPUT_DIR.mkdir(exist_ok=True)

    print("IceCube scientific validation\n")

    limit = get_dataset("icecube.ehe.differential_limit.2025").load_e2phi()
    sensitivity = get_dataset("icecube.ehe.sensitivity.2025").load_e2phi()
    area = get_dataset("icecube.ehe.effective_area.2025").load()
    glashow = get_dataset("icecube.glashow.flux.2021").load_e2phi()
    glashow_all = get_dataset("icecube.glashow.flux.2021").load_e2phi(flavor="all_flavor", flavor_assumption="equal")

    print("EHE 2025 limit and sensitivity:")
    validate_ehe(limit, sensitivity)

    print("\nGlashow 2021:")
    validate_glashow(glashow, glashow_all)

    print("\nEHE 2025 effective area:")
    validate_effective_area(area)

    print("\nGenerating validation figures...")
    plot_flux_results(limit, sensitivity, glashow_all)
    plot_effective_area(area)

    print(f"[PASS] Validation figures written to {OUTPUT_DIR}")
    print("\nValidation passed.")


if __name__ == "__main__":
    main()
