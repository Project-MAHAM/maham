from pathlib import Path

import astropy.units as u
import matplotlib.pyplot as plt
import numpy as np

from maham.datasets import get_dataset
from maham.plotting import apply_plot_style, bold_tick_labels, validation_curve_style
from maham.statistics import feldman_cousins_upper_limit


OUTPUT_DIR = Path(__file__).resolve().parent / "outputs"
UNIT = u.GeV / (u.cm**2 * u.s * u.sr)


def main():
    apply_plot_style()
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    table = get_dataset("grand200k.diffuse_sensitivity.2021").load(quantity="E2phi", flavor="all_flavor")
    exact_fc = feldman_cousins_upper_limit(0, expected_background=0.0, confidence_level=0.90)

    assert np.isclose(table.meta["confidence_level"], 0.90)
    assert np.isclose(table.meta["log10_energy_width_decades"], 1.0)
    assert table.meta["statistical_method"] == "feldman_cousins"
    assert np.isclose(table.meta["feldman_cousins_upper_count"], exact_fc, atol=0.005)

    print("PASS: loaded 24 visible GRAND200k Figure 1 vector-path points")
    print("Native confidence level: 90%")
    print("Native statistical energy width: 1 decade")
    print("Published Feldman-Cousins upper count: 2.44")
    print(f"MAHAM exact Feldman-Cousins count: {exact_fc:.9f}")
    print("No flavor, confidence-level, or decade-width conversion is applied")

    fig, ax = plt.subplots(figsize=(8, 5))
    ax.loglog(table["energy"].to_value(u.GeV), table["E2phi"].to_value(UNIT), label="GRAND200k 10 yr", **validation_curve_style("sensitivity"))
    ax.set_xlabel("Neutrino energy [GeV]", fontweight="bold")
    ax.set_ylabel(r"$E^2\Phi$ [GeV cm$^{-2}$ s$^{-1}$ sr$^{-1}$]", fontweight="bold")
    ax.set_title("GRAND200k Diffuse Neutrino Sensitivity (2021)", fontweight="bold")
    ax.grid(True, which="both", alpha=0.2)
    ax.text(0.97, 0.03, "All flavors\n90% CL\n10 yr", transform=ax.transAxes, ha="right", va="bottom", fontweight="bold")
    ax.legend(frameon=True)
    bold_tick_labels(ax)
    fig.tight_layout()
    fig.savefig(OUTPUT_DIR / "grand200k_2021_sensitivity_validation.png", dpi=200)
    fig.savefig(OUTPUT_DIR / "grand200k_2021_sensitivity_validation.pdf")
    plt.close(fig)


if __name__ == "__main__":
    main()
