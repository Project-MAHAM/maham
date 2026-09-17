from pathlib import Path

import astropy.units as u
import matplotlib.pyplot as plt
import numpy as np

from maham.datasets import get_dataset
from maham.plotting import apply_plot_style, bold_tick_labels


OUTPUT_DIR = Path(__file__).resolve().parent / "outputs"
EPHI_UNIT = 1 / (u.cm**2 * u.s * u.sr)
E2PHI_UNIT = u.GeV / (u.cm**2 * u.s * u.sr)


def require(condition, message):
    if not condition:
        raise AssertionError(message)
    print(f"PASS: {message}")


def validate_limit(limit, limit_e2phi):
    require(len(limit) == 7, "combined ANITA I-IV limit contains seven digitized vector vertices")
    require(limit.meta["quantity"] == "Ephi", "native upper-limit quantity is Ephi")
    require(limit.meta["flavor_convention"] == "all_flavor", "combined ANITA I-IV limit is native all flavor")
    require(np.isclose(limit.meta["confidence_level"], 0.90), "combined ANITA I-IV limit is 90% CL")
    require(limit.meta["limit_normalization_convention"] == "anita_bandwidth", "ANITA retains the native Delta=4 bandwidth convention")
    require(np.isclose(limit.meta["limit_bandwidth_factor"], 4.0), "ANITA native bandwidth factor is Delta=4")
    require(limit.meta["limit_normalization_convention"] == "anita_bandwidth", "ANITA retains its native historical bandwidth normalization")
    require(np.isclose(limit.meta["limit_bandwidth_factor"], 4.0), "ANITA native bandwidth factor is Delta=4")
    require(np.all(np.asarray(limit["is_upper_limit"], dtype=bool)), "all combined-limit values are upper limits")
    require(u.allclose(limit["Ephi"][0], 3.0371962350353715e-14 * EPHI_UNIT), "digitized 1 EeV combined-limit value is reproduced")
    require(u.allclose(limit["Ephi"][3], 7.8167335261561550e-18 * EPHI_UNIT), "digitized 31.6 EeV combined-limit value is reproduced")
    require(u.allclose(limit["Ephi"][-1], 2.0057984927391944e-19 * EPHI_UNIT), "digitized 1 ZeV combined-limit value is reproduced")
    require(limit_e2phi.meta["native_quantity"] == "Ephi", "E2phi view retains Ephi as the native quantity")
    require(limit_e2phi.meta["quantity"] == "E2phi", "E2phi comparison view is explicitly constructed")
    require(limit_e2phi.meta["flavor_convention"] == "all_flavor", "E2phi view remains all flavor")
    expected = (limit["Ephi"] * limit["energy"]).to(E2PHI_UNIT)
    require(u.allclose(limit_e2phi["E2phi"], expected), "Ephi-to-E2phi conversion is reproduced")


def validate_acceptance(acceptance):
    expected = np.array([0.0032, 0.033, 0.43, 3.1, 21.0, 68.0, 167.0]) * u.km**2 * u.sr
    require(len(acceptance) == 7, "ANITA-IV acceptance contains the seven values printed in Figure 6")
    require(acceptance.meta["quantity"] == "acceptance", "native detector-response quantity is acceptance")
    require(acceptance.meta["includes_analysis_efficiency"] is False, "published acceptance explicitly excludes analysis efficiency")
    require(acceptance.meta["flight"] == "ANITA-IV", "acceptance is identified as ANITA-IV rather than combined I-IV")
    require(u.allclose(acceptance["acceptance"], expected), "all seven published ANITA-IV acceptance values are reproduced")


def plot_limit(limit):
    energy = limit["energy"].to_value(u.GeV)
    y = limit["Ephi"].to_value(EPHI_UNIT)

    fig, ax = plt.subplots(figsize=(7, 5))
    ax.loglog(energy, y, color="black", linewidth=2.5)
    ax.set_xlim(5e8, 2e12)
    ax.set_ylim(1e-19, 1e-13)
    ax.set_xlabel(r"Neutrino energy, $E_{\nu}$ [GeV]")
    ax.set_ylabel(r"Flux, $E\Phi$ [cm$^{-2}$ s$^{-1}$ sr$^{-1}$]")
    ax.set_title("ANITA I-IV Diffuse Neutrino Upper Limit (2019)")
    ax.grid(True, which="both", alpha=0.25)
    ax.text(0.97, 0.03, "All flavors\n90% CL", transform=ax.transAxes, ha="right", va="bottom", fontweight="bold")
    bold_tick_labels(ax)
    fig.tight_layout()
    fig.savefig(OUTPUT_DIR / "anita_i_iv_diffuse_neutrino_limit_2019.png", dpi=200)
    fig.savefig(OUTPUT_DIR / "anita_i_iv_diffuse_neutrino_limit_2019.pdf")
    plt.close(fig)


def plot_acceptance(acceptance):
    energy = acceptance["energy"].to_value(u.GeV)
    area = acceptance["acceptance"].to_value(u.km**2 * u.sr)

    fig, ax = plt.subplots(figsize=(7, 5))
    ax.loglog(energy, area, color="black", linewidth=2.5)
    ax.set_xlim(5e8, 2e12)
    ax.set_ylim(1e-3, 3e2)
    ax.set_xlabel(r"Neutrino energy, $E_{\nu}$ [GeV]")
    ax.set_ylabel(r"Acceptance, $A$ [km$^{2}$ sr]")
    ax.set_title("ANITA-IV Acceptance (2019)")
    ax.grid(True, which="both", alpha=0.25)
    ax.text(0.97, 0.03, "Excludes analysis efficiency", transform=ax.transAxes, ha="right", va="bottom", fontweight="bold")
    bold_tick_labels(ax)
    fig.tight_layout()
    fig.savefig(OUTPUT_DIR / "anita_iv_acceptance_2019.png", dpi=200)
    fig.savefig(OUTPUT_DIR / "anita_iv_acceptance_2019.pdf")
    plt.close(fig)

def main():
    apply_plot_style()
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    limit_dataset = get_dataset("anita.i_iv_diffuse_neutrino_limit.2019")
    limit = limit_dataset.load_ephi()
    limit_e2phi = limit_dataset.load_e2phi(flavor="all_flavor")
    acceptance = get_dataset("anita.iv.acceptance.2019").load()

    print("ANITA I-IV diffuse neutrino upper limit 2019:")
    validate_limit(limit, limit_e2phi)
    print("\nANITA-IV acceptance 2019:")
    validate_acceptance(acceptance)

    plot_limit(limit)
    plot_acceptance(acceptance)
    print(f"Validation outputs written to {OUTPUT_DIR}")


if __name__ == "__main__":
    main()
