from pathlib import Path

import astropy.units as u
import matplotlib.pyplot as plt
import numpy as np

from maham.datasets import get_dataset
from maham.plotting import apply_plot_style, bold_legend, bold_tick_labels, validation_curve_style


OUTPUT_DIR = Path(__file__).resolve().parent / "outputs"
UNIT = u.GeV / (u.cm**2 * u.s * u.sr)


def main():
    apply_plot_style()
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    table = get_dataset("ret_n.diffuse_sensitivity.2022").load(quantity="E2phi", flavor="all_flavor")

    assert len(table) == 55
    assert np.isclose(table.meta["confidence_level"], 0.90)
    assert np.isclose(table.meta["log10_energy_width_decades"], 1.0)
    assert np.isclose(table.meta["projection_years"], 10.0)
    assert table.meta["benchmark_stations"] == 10
    assert np.isclose(table.meta["transmitter_power_kw_per_station"], 100.0)
    assert table.meta["response_level"] == "trigger_level"
    assert table.meta["statistical_method"] == "not_specified_in_source"

    print("PASS: loaded 55 vector-derived RET-N Figure 18 dash-center samples")
    print("Native confidence level: 90%")
    print("Native statistical energy width: 1 decade")
    print("Projection: 10 stations, 10 yr, 100 kW transmitter per station")
    print("Trigger assumption: 0 dB relative to thermal noise over 50 MHz")
    print("Statistical construction: not specified in the source")
    print("No flavor, confidence-level, decade-width, or exposure conversion is applied")

    fig, ax = plt.subplots(figsize=(8, 5))
    ax.loglog(table["energy"].to_value(u.GeV), table["E2phi"].to_value(UNIT), label="RET-N 10 stn, 10 yr", **validation_curve_style("sensitivity"))
    ax.set_xlabel("Neutrino energy [GeV]", fontweight="bold")
    ax.set_ylabel(r"$E^2\Phi$ [GeV cm$^{-2}$ s$^{-1}$ sr$^{-1}$]", fontweight="bold")
    ax.set_title("RET-N Diffuse Neutrino Sensitivity (2022)", fontweight="bold")
    ax.grid(True, which="both", alpha=0.2)
    ax.text(0.97, 0.03, "All flavors\n90% CL\n10 stations, 10 yr\n100 kW/stn", transform=ax.transAxes, ha="right", va="bottom", fontweight="bold")
    bold_tick_labels(ax)
    legend = ax.legend(frameon=True)
    bold_legend(legend)
    fig.tight_layout()
    fig.savefig(OUTPUT_DIR / "ret_n_diffuse_neutrino_sensitivity_2022.png", dpi=200)
    fig.savefig(OUTPUT_DIR / "ret_n_diffuse_neutrino_sensitivity_2022.pdf")
    plt.close(fig)


if __name__ == "__main__":
    main()
