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


def validate_combined(combined):
    require(len(combined) == 9, "Combined astrophysical spectrum contains 9 published energy bins")
    require(combined.meta["flavor_convention"] == "all_flavor", "Combined astrophysical spectrum is all-flavor")
    require(np.isclose(combined.meta["confidence_level"], 0.6827), "Combined default confidence level is 68.27%")
    require(combined.meta["interval_method"] == "profile_likelihood", "Combined intervals use released profile likelihoods")
    require(u.allclose(combined["energy_min"][0], 1e4 * u.GeV), "Combined spectrum begins at 1e4 GeV")
    require(u.allclose(combined["energy_max"][-1], 1e7 * u.GeV), "Combined spectrum ends at 1e7 GeV")
    require(np.array_equal(np.flatnonzero(combined["is_upper_limit"]), [5, 7, 8]), "Combined zero-best-fit bins 6, 8, and 9 are identified as upper limits")

    scale = 1e-8 * E2PHI_UNIT
    bestfit = np.array([9.31407260358, 22.5643864183, 5.63201177622, 3.20115983712, 4.25417119386, 0.0, 6.85816864131, 0.0, 0.0])
    lower68 = np.array([1.7, 17.0, 2.4, 0.8, 2.0, 0.0, 4.5, 0.0, 0.0])
    upper68 = np.array([17.3, 28.5, 9.2, 5.9, 7.0, 1.5, 9.7, 1.5, 0.6])
    lower90 = np.array([0.0, 13.5, 0.5, 0.0, 0.8, 0.0, 3.1, 0.0, 0.0])
    upper90 = np.array([22.7, 32.5, 11.6, 7.9, 9.0, 3.5, 11.9, 3.8, 1.5])

    require(u.allclose(combined["E2phi"], bestfit * scale), "All 9 released combined-spectrum best-fit values are reproduced")
    require(np.allclose(np.round(combined["E2phi_lower"].to_value(scale.unit) / 1e-8, 1), lower68), "Published 68% profile-likelihood lower bounds are reproduced")
    require(np.allclose(np.round(combined["E2phi_upper"].to_value(scale.unit) / 1e-8, 1), upper68), "Published 68% profile-likelihood upper bounds are reproduced")
    require(np.allclose(np.round(combined["E2phi_90_lower"].to_value(scale.unit) / 1e-8, 1), lower90), "Published 90% profile-likelihood lower bounds are reproduced")
    require(np.allclose(np.round(combined["E2phi_90_upper"].to_value(scale.unit) / 1e-8, 1), upper90), "Published 90% profile-likelihood upper bounds are reproduced")


def validate_throughgoing_muon(piecewise, piecewise_all):
    require(len(piecewise) == 5, "9.5-year through-going muon spectrum contains 5 published pieces")
    require(piecewise.meta["flavor_convention"] == "numu_nubar", "Native through-going muon flux is nu_mu + nubar_mu")
    require(piecewise.meta["confidence_level"] is None, "Mixed confidence levels are represented per row")
    require(np.allclose(piecewise["confidence_level"], [0.90, 0.6827, 0.6827, 0.6827, 0.90]), "Published mixed confidence levels are reproduced")
    require(piecewise["is_upper_limit"].tolist() == [True, False, False, False, True], "Pieces 1 and 5 are identified as 90% upper limits")

    scale = 1e-8 * E2PHI_UNIT
    require(u.allclose(piecewise["E2phi"], np.array([0.0, 2.22, 1.21, 0.33, 0.0]) * scale), "Published piece-wise best-fit normalizations are reproduced")
    require(u.allclose(piecewise["E2phi_lower"], np.array([0.0, 1.42, 0.90, 0.15, 0.0]) * scale), "Published piece-wise lower bounds are reproduced")
    require(u.allclose(piecewise["E2phi_upper"], np.array([3.10, 3.02, 1.53, 0.55, 0.41]) * scale), "Published piece-wise upper bounds are reproduced")
    require(u.allclose(piecewise["energy_min"], [100, 15000, 104000, 721000, 5000000] * u.GeV), "Published piece-wise lower energy edges are reproduced")
    require(u.allclose(piecewise["energy_max"], [15000, 104000, 721000, 5000000, 100000000] * u.GeV), "Published piece-wise upper energy edges are reproduced")

    require(piecewise_all.meta["flavor_convention"] == "all_flavor", "Equal-flavor all-flavor view is explicitly constructed")
    require(piecewise_all.meta["flavor_assumption"] == "equal", "All-flavor view records the equal-flavor assumption")
    require(u.allclose(piecewise_all["E2phi"], 3 * piecewise["E2phi"]), "Equal-flavor all-flavor conversion is reproduced")


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

    ax.text(0.97, 0.02, r"All flavors" "\n" r"$\nu_e:\nu_\mu:\nu_\tau=1:1:1$, $\nu:\bar{\nu}=1:1$", transform=ax.transAxes, ha="right", va="bottom", fontweight="bold")

    bold_tick_labels(ax)
    bold_legend(ax.legend(loc="upper right"))
    fig.tight_layout()
    fig.savefig(OUTPUT_DIR / "icecube_flux_results.png", dpi=200)
    fig.savefig(OUTPUT_DIR / "icecube_flux_results.pdf")
    plt.close(fig)


def plot_combined_spectrum(combined):
    energy = combined["energy"].to_value(u.GeV)
    energy_min = combined["energy_min"].to_value(u.GeV)
    energy_max = combined["energy_max"].to_value(u.GeV)
    xerr = np.vstack((energy - energy_min, energy_max - energy))

    upper = np.asarray(combined["is_upper_limit"], dtype=bool)
    measured = ~upper
    y = combined["E2phi"].to_value(E2PHI_UNIT)
    y_lower = combined["E2phi_lower"].to_value(E2PHI_UNIT)
    y_upper = combined["E2phi_upper"].to_value(E2PHI_UNIT)
    yerr = np.vstack((y[measured] - y_lower[measured], y_upper[measured] - y[measured]))

    fig, ax = plt.subplots(figsize=(7, 5))
    ax.set_xlim(8e3, 1.2e7)
    ax.set_ylim(1.5e-9, 5e-7)

    ax.errorbar(energy[measured], y[measured], xerr=xerr[:, measured], yerr=yerr, fmt="o", markersize=7, capsize=3, elinewidth=1.5, markeredgecolor="black", ecolor="black", markerfacecolor="white", markeredgewidth=1.5, linestyle="none", label="Combined spectrum")
    plot_upper_limits(ax, energy[upper], y_upper[upper], xerr=xerr[:, upper], arrow_factor=2.5, color="black", linewidth=1.5, capsize=3, mutation_scale=12)

    ax.set_xscale("log")
    ax.set_yscale("log")
    ax.set_xlabel(r"Neutrino energy, $E_{\nu}$ [GeV]")
    ax.set_ylabel(r"Flux, $E^{2}\Phi$ [GeV cm$^{-2}$ s$^{-1}$ sr$^{-1}$]")
    ax.set_title("IceCube Combined Astrophysical Spectrum (2015)")
    ax.grid(True, which="both", alpha=0.25)
    ax.text(0.97, 0.03, r"All flavors" "\n" r"68% profile intervals", transform=ax.transAxes, ha="right", va="bottom", fontweight="bold")
    bold_tick_labels(ax)
    bold_legend(ax.legend(loc="upper right"))
    fig.tight_layout()
    fig.savefig(OUTPUT_DIR / "icecube_combined_2015_spectrum.png", dpi=200)
    fig.savefig(OUTPUT_DIR / "icecube_combined_2015_spectrum.pdf")
    plt.close(fig)


def plot_throughgoing_muon(piecewise):
    energy = piecewise["energy"].to_value(u.GeV)
    energy_min = piecewise["energy_min"].to_value(u.GeV)
    energy_max = piecewise["energy_max"].to_value(u.GeV)
    xerr = np.vstack((energy - energy_min, energy_max - energy))

    upper = np.asarray(piecewise["is_upper_limit"], dtype=bool)
    measured = ~upper
    y = piecewise["E2phi"].to_value(E2PHI_UNIT)
    y_lower = piecewise["E2phi_lower"].to_value(E2PHI_UNIT)
    y_upper = piecewise["E2phi_upper"].to_value(E2PHI_UNIT)
    yerr = np.vstack((y[measured] - y_lower[measured], y_upper[measured] - y[measured]))

    fig, ax = plt.subplots(figsize=(7, 5))
    ax.set_xlim(7e1, 1.4e8)
    ax.set_ylim(8e-10, 8e-8)

    ax.errorbar(energy[measured], y[measured], xerr=xerr[:, measured], yerr=yerr, fmt="o", markersize=7, capsize=3, elinewidth=1.5, markeredgecolor="black", ecolor="black", markerfacecolor="white", markeredgewidth=1.5, linestyle="none", label="Piece-wise flux")
    plot_upper_limits(ax, energy[upper], y_upper[upper], xerr=xerr[:, upper], arrow_factor=2.5, color="black", linewidth=1.5, capsize=3, mutation_scale=12)

    ax.set_xscale("log")
    ax.set_yscale("log")
    ax.set_xlabel(r"Neutrino energy, $E_{\nu}$ [GeV]")
    ax.set_ylabel(r"Flux, $E^{2}\Phi$ [GeV cm$^{-2}$ s$^{-1}$ sr$^{-1}$]")
    ax.set_title("IceCube 9.5-Year Through-Going Muon Flux")
    ax.grid(True, which="both", alpha=0.25)
    ax.text(0.97, 0.03, r"$\nu_\mu+\bar{\nu}_\mu$" "\n" r"68.27% measurements, 90% limits", transform=ax.transAxes, ha="right", va="bottom", fontweight="bold")
    bold_tick_labels(ax)
    bold_legend(ax.legend(loc="upper right"))
    fig.tight_layout()
    fig.savefig(OUTPUT_DIR / "icecube_throughgoing_muon_2022_piecewise.png", dpi=200)
    fig.savefig(OUTPUT_DIR / "icecube_throughgoing_muon_2022_piecewise.pdf")
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
    combined = get_dataset("icecube.combined_astrophysical_flux.2015").load_e2phi()
    piecewise = get_dataset("icecube.throughgoing_muon_piecewise_flux.2022").load_e2phi()
    piecewise_all = get_dataset("icecube.throughgoing_muon_piecewise_flux.2022").load_e2phi(flavor="all_flavor", flavor_assumption="equal")

    print("EHE 2025 limit and sensitivity:")
    validate_ehe(limit, sensitivity)

    print("\nGlashow 2021:")
    validate_glashow(glashow, glashow_all)

    print("\nCombined astrophysical spectrum 2015:")
    validate_combined(combined)

    print("\nThrough-going muon spectrum 2022:")
    validate_throughgoing_muon(piecewise, piecewise_all)

    print("\nEHE 2025 effective area:")
    validate_effective_area(area)

    print("\nGenerating validation figures...")
    plot_flux_results(limit, sensitivity, glashow_all)
    plot_effective_area(area)
    plot_combined_spectrum(combined)
    plot_throughgoing_muon(piecewise)

    print(f"[PASS] Validation figures written to {OUTPUT_DIR}")
    print("\nValidation passed.")


if __name__ == "__main__":
    main()
