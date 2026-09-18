from pathlib import Path

import astropy.units as u
import matplotlib.pyplot as plt
import numpy as np

from maham.datasets import get_dataset
from maham.detector import effective_area_from_effective_volume
from maham.models import get_model
from maham.physics.neutrino import interaction_length
from maham.physics.spectra import centered_log_energy_bounds, convert_spectral_quantity, differential_flux_limit
from maham.plotting import apply_plot_style, bold_tick_labels

OUTPUT_DIR = Path(__file__).resolve().parent / "outputs"
FLUX_UNIT = u.GeV / (u.cm**2 * u.s * u.sr)


def derive(energy, veff, width_decades, area_scale):
    sigma = get_model("neutrino.cross_section.ctw_2011").cross_section(energy, particle="nu", current="total", variation="central")
    lint = interaction_length(sigma, 0.917 * u.g / u.cm**3)
    aeff = effective_area_from_effective_volume(veff, lint)
    energy_min, energy_max = centered_log_energy_bounds(energy, width_decades)
    phi = differential_flux_limit(aeff * area_scale, energy_min, energy_max, 2.44, (2.0 / 3.0) * 5.0 * u.yr, 4.0 * np.pi * u.sr)
    return convert_spectral_quantity(energy, phi, "phi", "E2phi").to(FLUX_UNIT)


def main():
    apply_plot_style()
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    veff = get_dataset("rno_g.design.effective_volume.2021").load()
    sensitivity = get_dataset("rno_g.design.diffuse_sensitivity.2021").load(quantity="E2phi")
    spacing = float(np.median(np.diff(np.log10(veff["energy"].to_value(u.eV)))))
    energy, nominal_veff = veff["energy"][8:], veff["effective_volume_2p00sigma"][8:]
    reproduced = derive(energy, nominal_veff, spacing, 5.0)
    np.testing.assert_allclose(sensitivity["E2phi"].to_value(FLUX_UNIT), reproduced.to_value(FLUX_UNIT), rtol=5e-15, atol=0)
    print("PASS: bundled RNO-G sensitivity exactly reproduces the deterministic nominal Figure 24 approximate prescription")

    diagnostic = derive(energy, nominal_veff, 1.0, 1.0)
    ratio = sensitivity["E2phi"].to_value(FLUX_UNIT) / diagnostic.to_value(FLUX_UNIT)
    print(f"Figure 24 approximate / central-Aeff one-decade diagnostic ratio: {np.median(ratio):.6f}")

    fig, ax = plt.subplots(figsize=(8, 5))
    x = sensitivity["energy"].to_value(u.GeV)
    ax.loglog(x, sensitivity["E2phi"].to_value(FLUX_UNIT), color="black", linewidth=2, label="RNO-G Figure 24 nominal approximation")
    ax.loglog(x, diagnostic.to_value(FLUX_UNIT), color="0.5", linestyle="--", linewidth=1.5, label="Central-Aeff one-decade diagnostic")
    ax.set_xlabel("Neutrino energy [GeV]", fontweight="bold")
    ax.set_ylabel(r"$E^2\Phi$ [GeV cm$^{-2}$ s$^{-1}$ sr$^{-1}$]", fontweight="bold")
    ax.set_title("RNO-G 2021 Sensitivity Validation", fontweight="bold")
    ax.grid(True, which="both", alpha=0.2)
    ax.legend(frameon=True)
    bold_tick_labels(ax)
    fig.tight_layout()
    fig.savefig(OUTPUT_DIR / "rno_g_2021_sensitivity_validation.png", dpi=200)
    fig.savefig(OUTPUT_DIR / "rno_g_2021_sensitivity_validation.pdf")
    plt.close(fig)


if __name__ == "__main__":
    main()
