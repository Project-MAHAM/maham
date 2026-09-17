from pathlib import Path

import astropy.units as u
import matplotlib.pyplot as plt
import numpy as np

from maham.datasets import get_dataset
from maham.plotting import apply_plot_style, bold_tick_labels


OUTPUT_DIR = Path(__file__).resolve().parent / "outputs"
E2PHI_UNIT = u.GeV / (u.cm**2 * u.s * u.sr)


def require(condition, message):
    if not condition:
        raise AssertionError(message)
    print(f"PASS: {message}")


def validate_limit(limit):
    require(len(limit) == 10, "five-station diffuse limit contains ten recoverable Figure 13 vector points")
    require(limit.meta["quantity"] == "E2phi", "native upper-limit quantity is E2phi")
    require(limit.meta["flavor_convention"] == "all_flavor", "native upper limit is all flavor")
    require(np.isclose(limit.meta["confidence_level"], 0.90), "diffuse upper limit is 90% CL")
    require(limit.meta["limit_normalization_convention"] == "log10_energy_width", "ARA differential-limit normalization is represented as a logarithmic energy width")
    require(np.isclose(limit.meta["log10_energy_width_decades"], 1.0), "ARA differential upper limit is decade-wide")
    require(np.isclose(limit.meta["array_wide_livetime_years"], 10.6), "10.6 years of array-wide livetime is retained")
    require(np.all(np.asarray(limit["is_upper_limit"], dtype=bool)), "all Figure 13 limit points are upper limits")
    require(u.allclose(limit["energy"][0], 10**7.5 * u.GeV), "first recoverable limit point is 10^16.5 eV")
    require(u.allclose(limit["E2phi"][3], 2.23906122e-7 * E2PHI_UNIT), "digitized 1 EeV upper-limit value is reproduced")
    require(u.allclose(limit["E2phi"][-1], 3.47761864e-7 * E2PHI_UNIT), "digitized 1 ZeV upper-limit value is reproduced")


def validate_acceptance(acceptance):
    require(len(acceptance) == 11, "trigger acceptance contains eleven half-decade Figure 4 points")
    require(acceptance.meta["quantity"] == "acceptance", "native detector-response quantity is acceptance")
    require(acceptance.meta["response_level"] == "trigger", "Figure 4 response is explicitly trigger level")
    require(acceptance.meta["neutrino_type_convention"] == "average_over_six_nu_nubar_types", "acceptance preserves the six-type neutrino average")
    require(acceptance.meta["livetime_averaged"] is True, "acceptance preserves the full-array livetime average")
    require(u.allclose(acceptance["acceptance"][4], 1.09668728e-2 * u.km**2 * u.sr), "digitized 1 EeV trigger acceptance is reproduced")
    expected = (acceptance["acceptance"] / (4 * np.pi * u.sr)).to(u.km**2)
    require(u.allclose(acceptance["sky_averaged_effective_area"], expected), "derived sky-averaged effective area uses acceptance/(4 pi sr)")


def validate_efficiency(efficiency):
    require(len(efficiency) == 11, "signal efficiency contains eleven half-decade Figure 14 points")
    require(efficiency.meta["quantity"] == "efficiency", "native signal-response quantity is efficiency")
    require(efficiency.meta["averaging"] == "exposure_weighted_array_wide", "Figure 14 exposure averaging is retained")
    require(efficiency.meta["response_stage"] == "after_event_selection", "efficiency is identified as post-selection")
    require(np.all((efficiency["efficiency"].value >= 0) & (efficiency["efficiency"].value <= 1)), "all signal efficiencies lie between zero and one")
    require(np.isclose(efficiency["efficiency"][4].value, 0.14344520), "digitized 1 EeV signal efficiency is reproduced")
    require(np.isclose(efficiency["efficiency"][-1].value, 0.32752763), "digitized 1 ZeV signal efficiency is reproduced")


def plot_limit(limit):
    energy = limit["energy"].to_value(u.eV)
    y = limit["E2phi"].to_value(E2PHI_UNIT)

    fig, ax = plt.subplots(figsize=(7, 5))
    ax.loglog(energy, y, color="black", linewidth=2.5)
    ax.set_xlim(2e16, 2e21)
    ax.set_ylim(8e-8, 8e-5)
    ax.set_xlabel(r"Neutrino energy, $E_{\nu}$ [eV]")
    ax.set_ylabel(r"Flux, $E^{2}\Phi$ [GeV cm$^{-2}$ s$^{-1}$ sr$^{-1}$]")
    ax.set_title("ARA Five-Station Diffuse Neutrino Upper Limit (2026)")
    ax.grid(True, which="both", alpha=0.25)
    ax.text(0.97, 0.03, "All flavors\n90% CL", transform=ax.transAxes, ha="right", va="bottom", fontweight="bold")
    bold_tick_labels(ax)
    fig.tight_layout()
    fig.savefig(OUTPUT_DIR / "ara_five_station_diffuse_neutrino_limit_2026.png", dpi=200)
    fig.savefig(OUTPUT_DIR / "ara_five_station_diffuse_neutrino_limit_2026.pdf")
    plt.close(fig)


def plot_acceptance(acceptance):
    energy = acceptance["energy"].to_value(u.eV)
    values = acceptance["acceptance"].to_value(u.km**2 * u.sr)

    fig, ax = plt.subplots(figsize=(7, 5))
    ax.loglog(energy, values, color="black", linewidth=2.5)
    ax.set_xlim(7e15, 2e21)
    ax.set_ylim(1e-7, 1e1)
    ax.set_xlabel(r"Neutrino energy, $E_{\nu}$ [eV]")
    ax.set_ylabel(r"Acceptance, $A$ [km$^{2}$ sr]")
    ax.set_title("ARA Five-Station Trigger-Level Acceptance (2026)")
    ax.grid(True, which="both", alpha=0.25)
    ax.text(0.97, 0.03, r"Average over 6 $\nu/\bar{\nu}$ types", transform=ax.transAxes, ha="right", va="bottom", fontweight="bold")
    bold_tick_labels(ax)
    fig.tight_layout()
    fig.savefig(OUTPUT_DIR / "ara_five_station_trigger_acceptance_2026.png", dpi=200)
    fig.savefig(OUTPUT_DIR / "ara_five_station_trigger_acceptance_2026.pdf")
    plt.close(fig)

def plot_efficiency(efficiency):
    energy = efficiency["energy"].to_value(u.eV)
    values = efficiency["efficiency"].to_value(u.one)

    fig, ax = plt.subplots(figsize=(7, 5))
    ax.semilogx(energy, values, color="black", linewidth=2.5)
    ax.set_xlim(7e15, 2e21)
    ax.set_ylim(0, 0.4)
    ax.set_xlabel(r"Neutrino energy, $E_{\nu}$ [eV]")
    ax.set_ylabel("Efficiency")
    ax.set_title("ARA Five-Station Signal Efficiency (2026)")
    ax.grid(True, which="both", alpha=0.25)
    ax.text(0.97, 0.03, "Exposure-averaged", transform=ax.transAxes, ha="right", va="bottom", fontweight="bold")
    bold_tick_labels(ax)
    fig.tight_layout()
    fig.savefig(OUTPUT_DIR / "ara_five_station_signal_efficiency_2026.png", dpi=200)
    fig.savefig(OUTPUT_DIR / "ara_five_station_signal_efficiency_2026.pdf")
    plt.close(fig)

def main():
    apply_plot_style()
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    limit = get_dataset("ara.five_station.diffuse_neutrino_limit.2026").load_e2phi()
    acceptance = get_dataset("ara.five_station.trigger_acceptance.2026").load()
    efficiency = get_dataset("ara.five_station.signal_efficiency.2026").load()

    print("ARA five-station diffuse neutrino upper limit 2026:")
    validate_limit(limit)
    print("\nARA five-station trigger acceptance 2026:")
    validate_acceptance(acceptance)
    print("\nARA five-station signal efficiency 2026:")
    validate_efficiency(efficiency)

    plot_limit(limit)
    plot_acceptance(acceptance)
    plot_efficiency(efficiency)
    print(f"Validation outputs written to {OUTPUT_DIR}")


if __name__ == "__main__":
    main()
