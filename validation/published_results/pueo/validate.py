from pathlib import Path

import astropy.units as u
import matplotlib.pyplot as plt
import numpy as np

from maham.datasets import get_dataset
from maham.physics.spectra import convert_sensitivity_normalization_to_decade_width, convert_single_event_sensitivity_to_confidence_level
from maham.plotting import apply_plot_style, bold_tick_labels


OUTPUT_DIR = Path(__file__).resolve().parent / "outputs"
UNIT = u.GeV / (u.cm**2 * u.s * u.sr)


def main():
    apply_plot_style()
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    native = get_dataset("pueo.diffuse_sensitivity.2025").load(quantity="E2phi", flavor="all_flavor")
    decade = convert_sensitivity_normalization_to_decade_width(native, target_width_decades=1.0)
    fc90 = convert_single_event_sensitivity_to_confidence_level(decade, confidence_level=0.90, method="feldman_cousins")

    bandwidth_factor = decade.meta["sensitivity_normalization_scale_factor"]
    count_factor = fc90.meta["expected_signal_count_scale_factor"]
    total_factor = bandwidth_factor * count_factor
    print(f"Native Delta=4 -> one-decade factor: {bandwidth_factor:.9f}")
    print(f"Feldman-Cousins 90% count factor (n=0, b=0): {count_factor:.9f}")
    print(f"Total native SES -> one-decade FC90 factor: {total_factor:.9f}")

    x = native["energy"].to_value(u.GeV)
    fig, ax = plt.subplots(figsize=(8, 5))
    ax.loglog(x, native["E2phi"].to_value(UNIT), linewidth=1.8, label="Native PUEO 30d SES, Delta=4")
    ax.loglog(x, decade["E2phi"].to_value(UNIT), linestyle=":", linewidth=1.8, label="One-decade SES")
    ax.loglog(x, fc90["E2phi"].to_value(UNIT), color="indigo", linestyle="--", linewidth=2.0, label="One-decade 90% FC sensitivity")
    ax.set_xlabel("Neutrino energy [GeV]", fontweight="bold")
    ax.set_ylabel(r"$E^2\Phi$ [GeV cm$^{-2}$ s$^{-1}$ sr$^{-1}$]", fontweight="bold")
    ax.set_title("PUEO ICRC2025 Sensitivity Validation", fontweight="bold")
    ax.grid(True, which="both", alpha=0.2)
    ax.legend(frameon=True)
    bold_tick_labels(ax)
    fig.tight_layout()
    fig.savefig(OUTPUT_DIR / "pueo_2025_sensitivity_validation.png", dpi=200)
    fig.savefig(OUTPUT_DIR / "pueo_2025_sensitivity_validation.pdf")
    plt.close(fig)


if __name__ == "__main__":
    main()
