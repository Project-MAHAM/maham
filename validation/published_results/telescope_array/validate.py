from pathlib import Path

import astropy.units as u
import matplotlib.pyplot as plt
import numpy as np

from maham.datasets import get_dataset
from maham.plotting import apply_plot_style, bold_legend, bold_tick_labels, plot_upper_limits


OUTPUT_DIR = Path(__file__).resolve().parent / "outputs"
E3J_UNIT = u.eV**2 / (u.m**2 * u.s * u.sr)


def require(condition, message):
    if not condition:
        raise AssertionError(message)
    print(f"PASS: {message}")


def validate_telescope_array():
    dataset = get_dataset("telescope_array.combined_spectrum.2023")
    raw = dataset.load_raw()
    table = dataset.load()

    upper = np.asarray(table["is_upper_limit"], dtype=bool)
    resolved = np.asarray(table["has_resolved_vertical_error"], dtype=bool)
    energy = table["energy"].to_value(u.eV)

    require(len(raw) == 21, "digitized source contains 21 points")
    require(len(table) == 21, "standardized spectrum contains 21 points")
    require(np.count_nonzero(~upper) == 20, "spectrum contains 20 measurements")
    require(np.count_nonzero(upper) == 1, "spectrum contains one upper limit")
    require(bool(upper[-1]), "final spectrum point is the upper limit")
    require(np.count_nonzero(resolved) == 11, "11 measurement uncertainties are visually resolved")
    require(np.all(~resolved[upper]), "upper-limit point has no measurement error assigned")
    require(np.all(np.diff(energy) > 0), "energy grid is strictly increasing")
    require(dataset.metadata.quantity == "E3J", "native spectral quantity is E3J")
    require(dataset.metadata.spectral_kind == "differential_intensity", "spectral kind is differential intensity")
    require(dataset.metadata.source.provenance.value == "digitized", "dataset provenance is digitized")
    require(table.meta["source_figure"] == "Figure 7, right panel", "source figure metadata is retained")

    log_energy = np.log10(energy)
    log_min = np.log10(table["energy_min"].to_value(u.eV))
    log_max = np.log10(table["energy_max"].to_value(u.eV))
    require(np.allclose(log_energy - log_min, 0.05, atol=5e-3), "lower energy-bin half-widths reproduce the digitization")
    require(np.allclose(log_max - log_energy, 0.05, atol=5e-3), "upper energy-bin half-widths reproduce the digitization")

    return table


def plot_telescope_array(table):
    log_energy = np.log10(table["energy"].to_value(u.eV))
    log_min = np.log10(table["energy_min"].to_value(u.eV))
    log_max = np.log10(table["energy_max"].to_value(u.eV))
    xerr = np.vstack((log_energy - log_min, log_max - log_energy))

    upper = np.asarray(table["is_upper_limit"], dtype=bool)
    measured = ~upper

    y = table["E3J"].to_value(E3J_UNIT) / 1e24
    y_lower = table["E3J_lower"].to_value(E3J_UNIT) / 1e24
    y_upper = table["E3J_upper"].to_value(E3J_UNIT) / 1e24
    yerr = np.vstack((y[measured] - y_lower[measured], y_upper[measured] - y[measured]))

    fig, ax = plt.subplots(figsize=(7, 5))
    ax.set_yscale("log")
    ax.set_xlim(18.35, 20.55)
    ax.set_ylim(8e-2, 1.2e1)

    ax.errorbar(log_energy[measured], y[measured], xerr=xerr[:, measured], yerr=yerr, fmt="o", linestyle="none",
                markersize=6, markerfacecolor="white", markeredgecolor="black", markeredgewidth=1.4,
                ecolor="black", elinewidth=1.4, capsize=3, label="TA + TAx4")

    plot_upper_limits(ax, log_energy[upper], y[upper], xerr=xerr[:, upper], arrow_factor=2.5, color="black",
                      linewidth=1.5, capsize=3, mutation_scale=12)

    ax.set_xlabel(r"Cosmic-ray energy, $\log_{10}(E/\mathrm{eV})$")
    ax.set_ylabel(r"Scaled flux, $E^3J(E)\times10^{-24}$ [m$^{-2}$ s$^{-1}$ sr$^{-1}$ eV$^2$]")
    ax.set_title("Telescope Array Combined Energy Spectrum (2023)")
    ax.grid(True, which="both", alpha=0.25)

    bold_tick_labels(ax)
    bold_legend(ax.legend(loc="best"))
    fig.tight_layout()
    fig.savefig(OUTPUT_DIR / "telescope_array_combined_spectrum_2023.png", dpi=200)
    fig.savefig(OUTPUT_DIR / "telescope_array_combined_spectrum_2023.pdf")
    plt.close(fig)


def main():
    apply_plot_style()
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    table = validate_telescope_array()
    plot_telescope_array(table)
    print(f"Validation outputs written to {OUTPUT_DIR}")


if __name__ == "__main__":
    main()
