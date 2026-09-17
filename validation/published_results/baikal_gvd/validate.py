from pathlib import Path

import astropy.units as u
import matplotlib.pyplot as plt
import numpy as np

from maham.datasets import get_dataset
from maham.plotting import apply_plot_style, bold_legend, bold_tick_labels


OUTPUT_DIR = Path(__file__).resolve().parent / "outputs"
E2PHI_UNIT = u.GeV / (u.cm**2 * u.s * u.sr)


def require(condition, message):
    if not condition:
        raise AssertionError(message)
    print(f"[PASS] {message}")


def validate_limit(limit, limit_all):
    require(len(limit) == 8, "diffuse limit contains 8 published decade-wide bins")
    require(np.all(limit["is_upper_limit"]), "all Baikal-GVD flux points are upper limits")
    require(limit.meta["flavor_convention"] == "per_flavor", "native diffuse limit is per-flavor")
    require(limit.meta["particle_convention"] == "nu_plus_nubar", "native diffuse limit sums neutrinos and antineutrinos")
    require(np.isclose(limit.meta["confidence_level"], 0.90), "diffuse limit confidence level is 90%")
    require(limit.meta["limit_normalization_convention"] == "log10_energy_width", "differential-limit normalization is represented as a logarithmic energy width")
    require(np.isclose(limit.meta["log10_energy_width_decades"], 1.0), "published limits use decade-wide energy intervals")
    require(limit.meta["limit_spectral_assumption"] == "E^-1", "published within-interval 1/E spectral assumption is retained")
    require(u.allclose(limit["energy"][0], 1e7 * u.GeV), "first published bin center is reproduced")
    require(u.allclose(limit["E2phi"][0], 0.78e-8 * E2PHI_UNIT), "first published E2phi upper limit is reproduced")
    require(u.allclose(limit["E2phi"][-1], 54e-8 * E2PHI_UNIT), "last published E2phi upper limit is reproduced")
    require(limit_all.meta["flavor_convention"] == "all_flavor", "all-flavor view is explicitly constructed")
    require(limit_all.meta["flavor_assumption"] == "equal", "all-flavor view records the equal-flavor assumption")
    require(u.allclose(limit_all["E2phi"], 3 * limit["E2phi"]), "equal-flavor per-flavor to all-flavor conversion is reproduced")


def validate_effective_area(area):
    energy = area["energy"].to_value(u.GeV)
    nue = area["effective_area_nue"].to_value(u.m**2)
    numu = area["effective_area_numu"].to_value(u.m**2)
    nutau = area["effective_area_nutau"].to_value(u.m**2)
    total = area["effective_area_total"].to_value(u.m**2)
    require(len(area) == 45, "effective area contains 45 official ancillary points")
    require(np.all(np.diff(energy) > 0), "effective-area energy grid is strictly increasing")
    require(np.all(nue > 0) and np.all(numu > 0) and np.all(nutau > 0) and np.all(total > 0), "all effective-area values are positive")
    require(area.meta["solid_angle_convention"] == "upper_hemisphere_2pi_exposure_weighted_average", "upper-hemisphere 2pi averaging convention is explicit")
    require(np.isclose(energy[0], (10**3.55 * u.TeV).to_value(u.GeV)), "first official effective-area energy is reproduced")
    require(np.isclose(total[0], 57.03), "first official total effective area is reproduced")
    require(np.isclose(total[-1], 19026.19), "last official total effective area is reproduced")
    require(np.allclose(total, nue + numu + nutau, atol=0.011), "published total agrees with flavor sum within tabulation rounding")
    peak = np.argmax(nue[:6])
    require(np.isclose(energy[peak], (10**3.85 * u.TeV).to_value(u.GeV)), "electron-neutrino effective-area enhancement near the Glashow resonance is reproduced")


def plot_limit(limit):
    energy = limit["energy"].to_value(u.GeV)
    y = limit["E2phi"].to_value(E2PHI_UNIT)

    fig, ax = plt.subplots(figsize=(7, 5))
    ax.loglog(energy, y, color="black", linewidth=2.5)
    ax.set_xlim(2e6, 2e11)
    ax.set_ylim(1e-9, 2e-6)
    ax.set_xlabel(r"Neutrino energy, $E_{\nu}$ [GeV]")
    ax.set_ylabel(r"Flux, $E^{2}\Phi$ [GeV cm$^{-2}$ s$^{-1}$ sr$^{-1}$]")
    ax.set_title("Baikal-GVD Diffuse Neutrino Upper Limit (2025)")
    ax.grid(True, which="both", alpha=0.25)
    ax.text(0.97, 0.03, r"Per flavor, $\nu+\bar{\nu}$" "\n" r"90% CL", transform=ax.transAxes, ha="right", va="bottom", fontweight="bold")

    bold_tick_labels(ax)
    fig.tight_layout()
    fig.savefig(OUTPUT_DIR / "baikal_gvd_diffuse_limit_2025.png", dpi=200)
    fig.savefig(OUTPUT_DIR / "baikal_gvd_diffuse_limit_2025.pdf")
    plt.close(fig)


def plot_effective_area(area):
    energy = area["energy"].to_value(u.GeV)

    fig, ax = plt.subplots(figsize=(7, 5))
    ax.loglog(energy, area["effective_area_total"].to_value(u.m**2), linewidth=2.5, label="Total")
    ax.loglog(energy, area["effective_area_nue"].to_value(u.m**2), linewidth=1.8, label=r"$\nu_e$")
    ax.loglog(energy, area["effective_area_numu"].to_value(u.m**2), linewidth=1.8, label=r"$\nu_\mu$")
    ax.loglog(energy, area["effective_area_nutau"].to_value(u.m**2), linewidth=1.8, label=r"$\nu_\tau$")
    ax.set_xlabel(r"Neutrino energy, $E_{\nu}$ [GeV]")
    ax.set_ylabel(r"Effective area, $A_{\mathrm{eff}}$ [m$^{2}$]")
    ax.set_title("Baikal-GVD 2025 Effective Area")
    ax.grid(True, which="both", alpha=0.25)
    ax.text(0.97, 0.03, r"2023 configuration" "\n" r"Exposure-weighted upper hemisphere ($2\pi$)", transform=ax.transAxes, ha="right", va="bottom", fontweight="bold")

    bold_tick_labels(ax)
    bold_legend(ax.legend(loc="upper left"))
    fig.tight_layout()
    fig.savefig(OUTPUT_DIR / "baikal_gvd_effective_area_2025.png", dpi=200)
    fig.savefig(OUTPUT_DIR / "baikal_gvd_effective_area_2025.pdf")
    plt.close(fig)


def main():
    apply_plot_style()
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    limit = get_dataset("baikal_gvd.diffuse_neutrino_limit.2025").load_e2phi()
    limit_all = get_dataset("baikal_gvd.diffuse_neutrino_limit.2025").load_e2phi(flavor="all_flavor", flavor_assumption="equal")
    area = get_dataset("baikal_gvd.effective_area.2025").load()

    print("Baikal-GVD 2025 validation\n")
    print("Diffuse upper limit:")
    validate_limit(limit, limit_all)
    print("\nEffective area:")
    validate_effective_area(area)

    plot_limit(limit)
    plot_effective_area(area)

    print("\nAll Baikal-GVD validation checks passed.")
    print(f"Outputs: {OUTPUT_DIR}")


if __name__ == "__main__":
    main()
