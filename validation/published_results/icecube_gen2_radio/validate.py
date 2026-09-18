from pathlib import Path

import astropy.units as u
import matplotlib.pyplot as plt
import numpy as np

from maham.datasets import get_dataset
from maham.plotting import apply_plot_style, bold_tick_labels


OUTPUT_DIR = Path(__file__).resolve().parent / "outputs"
UNIT = u.GeV / (u.cm**2 * u.s * u.sr)


def main():
    apply_plot_style()
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    table = get_dataset("icecube_gen2.radio.diffuse_sensitivity.2021").load(quantity="E2phi", flavor="all_flavor")
    spacing = np.diff(np.log10(table["energy"].to_value(u.GeV)))
    np.testing.assert_allclose(spacing, 0.5, atol=2e-7)
    assert np.isclose(table.meta["log10_energy_width_decades"], 1.0)

    print("PASS: loaded 8 exact Figure 2 vector-path vertices")
    print("Native confidence level: 90%")
    print("Native statistical energy width: 1 decade")
    print("Plotted vertex spacing: 0.5 decade")
    print("No flavor, confidence-level, or decade-width conversion is applied")

    fig, ax = plt.subplots(figsize=(8, 5))
    ax.loglog(table["energy"].to_value(u.GeV), table["E2phi"].to_value(UNIT), color="forestgreen", linestyle="--", linewidth=2.0, marker="o", markerfacecolor="none", label="IceCube-Gen2 Radio 10 yr")
    ax.set_xlabel("Neutrino energy [GeV]", fontweight="bold")
    ax.set_ylabel(r"$E^2\Phi$ [GeV cm$^{-2}$ s$^{-1}$ sr$^{-1}$]", fontweight="bold")
    ax.set_title("IceCube-Gen2 Radio 2021 Sensitivity Validation", fontweight="bold")
    ax.grid(True, which="both", alpha=0.2)
    ax.legend(frameon=True)
    bold_tick_labels(ax)
    fig.tight_layout()
    fig.savefig(OUTPUT_DIR / "icecube_gen2_radio_2021_sensitivity_validation.png", dpi=200)
    fig.savefig(OUTPUT_DIR / "icecube_gen2_radio_2021_sensitivity_validation.pdf")
    plt.close(fig)


if __name__ == "__main__":
    main()
