from pathlib import Path

import astropy.units as u
import matplotlib.pyplot as plt
import numpy as np

from maham.datasets import get_dataset
from maham.plotting import apply_plot_style, bold_legend, bold_tick_labels, plot_upper_limits

OUTPUT_DIR = Path(__file__).resolve().parent / "outputs"
E2PHI_UNIT = u.GeV / (u.cm**2 * u.s * u.sr)


def require(condition, message):
    if not condition:
        raise AssertionError(message)
    print(f"PASS: {message}")


def validate_fermi_lat():
    igrb_dataset = get_dataset("fermi_lat.igrb.2015")
    egb_dataset = get_dataset("fermi_lat.egb.2015")
    sources_dataset = get_dataset("fermi_lat.resolved_sources.2015")
    igrb_raw = igrb_dataset.load_raw()
    egb_raw = egb_dataset.load_raw()
    sources_raw = sources_dataset.load_raw()
    igrb = igrb_dataset.load_e2phi()
    egb = egb_dataset.load_e2phi()
    sources = sources_dataset.load_e2phi()

    for name, raw in (("IGRB", igrb_raw), ("EGB", egb_raw), ("resolved sources", sources_raw)):
        require(len(raw) == 26, f"{name} contains 26 Model-A energy bins")
        require(np.all(np.asarray(raw["model"]) == "A"), f"{name} uses the Model-A table rows")
    require(np.isclose(igrb_raw["energy_min"][0], 100.0), "spectrum starts at 100 MeV")
    require(np.isclose(igrb_raw["energy_max"][-1], 819200.0), "spectrum ends at 819.2 GeV")
    require(np.count_nonzero(igrb["is_upper_limit"]) == 1, "IGRB contains one upper limit")
    require(bool(igrb["is_upper_limit"][-1]), "IGRB upper limit is the final energy bin")
    require(np.count_nonzero(egb["is_upper_limit"]) == 0, "EGB contains no upper-limit bins")
    require(np.count_nonzero(sources["is_upper_limit"]) == 0, "resolved-source spectrum contains no upper-limit bins")
    require(np.isclose(igrb["integrated_flux"][-1].value, 2.3e-12), "final IGRB bin uses the published upper limit")
    require(np.isclose(sources["integrated_flux"][0].value, 8.977e-7), "first resolved-source integrated flux is reproduced")
    expected_first_bin = igrb_raw["igrb"][0] + sources_raw["resolved_sources"][0]
    require(np.isclose(egb_raw["egb"][0], expected_first_bin, rtol=0.01), "EGB first bin is consistent with IGRB plus resolved sources")

    for name, table in (("IGRB", igrb), ("EGB", egb), ("resolved sources", sources)):
        require(table.meta["native_quantity"] == "phi", f"{name} native MAHAM spectral quantity is phi")
        require(table.meta["quantity"] == "E2phi", f"{name} converts to E2phi")
        energy = table["energy"].to_value(u.MeV)
        energy_min = table["energy_min"].to_value(u.MeV)
        energy_max = table["energy_max"].to_value(u.MeV)
        require(np.all(np.diff(energy) > 0), f"{name} energy grid is strictly increasing")
        require(np.all(energy_min < energy), f"{name} bin minima lie below representative energies")
        require(np.all(energy < energy_max), f"{name} bin maxima lie above representative energies")

    require(igrb.meta["foreground_model"] == "A", "IGRB foreground-model metadata is retained")
    require(egb.meta["foreground_model"] == "A", "EGB foreground-model metadata is retained")
    require(sources.meta["has_foreground_model_uncertainty"] is False, "resolved sources correctly omit foreground-model uncertainty")
    return igrb, egb, sources


def spectrum_arrays(table):
    energy = table["energy"].to_value(u.GeV)
    energy_min = table["energy_min"].to_value(u.GeV)
    energy_max = table["energy_max"].to_value(u.GeV)
    xerr = np.vstack((energy - energy_min, energy_max - energy))
    y = table["E2phi"].to_value(E2PHI_UNIT)
    y_lower = table["E2phi_lower"].to_value(E2PHI_UNIT)
    y_upper = table["E2phi_upper"].to_value(E2PHI_UNIT)
    fg_lower = table["E2phi_foreground_err_lower"].to_value(E2PHI_UNIT)
    fg_upper = table["E2phi_foreground_err_upper"].to_value(E2PHI_UNIT)
    return energy, xerr, y, y_lower, y_upper, fg_lower, fg_upper


def plot_fermi_lat(igrb, egb, sources):
    fig, ax = plt.subplots(figsize=(8, 5))
    igrb_energy, igrb_xerr, igrb_y, igrb_lower, igrb_upper, igrb_fg_lower, igrb_fg_upper = spectrum_arrays(igrb)
    egb_energy, egb_xerr, egb_y, egb_lower, egb_upper, egb_fg_lower, egb_fg_upper = spectrum_arrays(egb)
    src_energy, src_xerr, src_y, src_lower, src_upper, _, _ = spectrum_arrays(sources)

    igrb_ul = np.asarray(igrb["is_upper_limit"], dtype=bool)
    igrb_det = ~igrb_ul
    igrb_handle = ax.errorbar(
        igrb_energy[igrb_det], igrb_y[igrb_det], xerr=igrb_xerr[:, igrb_det],
        yerr=np.vstack((igrb_y[igrb_det] - igrb_lower[igrb_det], igrb_upper[igrb_det] - igrb_y[igrb_det])),
        fmt="o", linestyle="none", markersize=5.5, markerfacecolor="white", markeredgewidth=1.3,
        elinewidth=1.2, capsize=2.5, label="Fermi-LAT IGRB",
    )
    igrb_color = igrb_handle[0].get_color()
    ax.fill_between(
        igrb_energy[igrb_det], igrb_y[igrb_det] - igrb_fg_lower[igrb_det],
        igrb_y[igrb_det] + igrb_fg_upper[igrb_det], color=igrb_color, alpha=0.15, linewidth=0,
    )
    plot_upper_limits(
        ax, igrb_energy[igrb_ul], igrb_y[igrb_ul], xerr=igrb_xerr[:, igrb_ul],
        arrow_factor=2.5, color=igrb_color, linewidth=1.5, capsize=3, mutation_scale=12,
    )

    egb_handle = ax.errorbar(
        egb_energy, egb_y, xerr=egb_xerr, yerr=np.vstack((egb_y - egb_lower, egb_upper - egb_y)),
        fmt="s", linestyle="none", markersize=5.5, markerfacecolor="white", markeredgewidth=1.3,
        elinewidth=1.2, capsize=2.5, label="Fermi-LAT EGB",
    )
    egb_color = egb_handle[0].get_color()
    ax.fill_between(egb_energy, egb_y - egb_fg_lower, egb_y + egb_fg_upper, color=egb_color, alpha=0.15, linewidth=0)

    ax.errorbar(
        src_energy, src_y, xerr=src_xerr, yerr=np.vstack((src_y - src_lower, src_upper - src_y)),
        fmt="^", linestyle="none", markersize=5.5, markerfacecolor="white", markeredgewidth=1.3,
        elinewidth=1.2, capsize=2.5, label=r"Resolved sources ($|b|>20^\circ$)",
    )

    ax.set_xscale("log")
    ax.set_yscale("log")
    ax.set_xlim(0.08, 1000)
    ax.set_ylim(1e-9, 2e-6)
    ax.set_xlabel(r"Gamma-ray energy, $E_\gamma$ [GeV]")
    ax.set_ylabel(r"Flux, $E^2\Phi_\gamma$ [GeV cm$^{-2}$ s$^{-1}$ sr$^{-1}$]")
    ax.set_title("Fermi-LAT IGRB, EGB, and Resolved Sources (2015)")
    ax.grid(True, which="both", alpha=0.25)
    ax.text(
        0.03, 0.04, "Galactic foreground model A\nShaded bands: IGRB/EGB foreground-model uncertainty",
        transform=ax.transAxes, ha="left", va="bottom", fontweight="bold",
    )
    bold_tick_labels(ax)
    bold_legend(ax.legend(loc="best"))
    fig.tight_layout()
    fig.savefig(OUTPUT_DIR / "fermi_lat_igrb_egb_2015.png", dpi=200)
    fig.savefig(OUTPUT_DIR / "fermi_lat_igrb_egb_2015.pdf")
    plt.close(fig)


def main():
    apply_plot_style()
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    igrb, egb, sources = validate_fermi_lat()
    plot_fermi_lat(igrb, egb, sources)
    print(f"Validation outputs written to {OUTPUT_DIR}")


if __name__ == "__main__":
    main()
