from pathlib import Path

import astropy.units as u
import matplotlib.pyplot as plt
import numpy as np

from maham.datasets import get_dataset
from maham.physics.spectra import normalize_spectral_quantity
from maham.plotting import apply_plot_style, bold_legend, bold_tick_labels


apply_plot_style()

OUTPUT_DIR = Path(__file__).parent / "outputs"
PLOT_QUANTITY = "E2phi"  # Options: phi, Ephi, E2phi, E3phi.

QUANTITY_UNITS = {
    "phi": 1 / (u.GeV * u.cm**2 * u.s),
    "Ephi": 1 / (u.cm**2 * u.s),
    "E2phi": u.GeV / (u.cm**2 * u.s),
    "E3phi": u.GeV**2 / (u.cm**2 * u.s),
}

QUANTITY_LABELS = {
    "phi": r"Flux, $\Phi$ [GeV$^{-1}$ cm$^{-2}$ s$^{-1}$]",
    "Ephi": r"Flux, $E\Phi$ [cm$^{-2}$ s$^{-1}$]",
    "E2phi": r"Flux, $E^{2}\Phi$ [GeV cm$^{-2}$ s$^{-1}$]",
    "E3phi": r"Flux, $E^{3}\Phi$ [GeV$^{2}$ cm$^{-2}$ s$^{-1}$]",
}

STYLE = {
    "ngc1068": {"color": "blue", "linestyle": "-", "linewidth": 2.2},
    "txs0506": {"color": "orange", "linestyle": "--", "linewidth": 2.2},
}


def require(condition, message):
    if not condition:
        print(f"[FAIL] {message}")
        raise AssertionError(message)
    print(f"[PASS] {message}")


def validate_dataset(table, dataset_id, source_name, quantity):
    require(table.meta["dataset_id"] == dataset_id, f"{source_name} dataset ID is correct")
    require(table.meta["quantity"] == quantity, f"{source_name} is represented as {quantity}")
    require(table.meta["flavor_convention"] == "numu_nubar", f"{source_name} uses nu_mu + nubar_mu")
    require(table.meta["solid_angle_convention"] == "point_source", f"{source_name} is a point-source flux")
    require(table.meta["spectral_kind"] == "differential_flux", f"{source_name} is a differential flux")
    require(np.all(np.diff(table["energy"].to_value(u.GeV)) > 0), f"{source_name} energy grid is strictly increasing")
    require(np.all(table[quantity].to_value(QUANTITY_UNITS[quantity]) > 0), f"{source_name} {quantity} values are positive")


def plot_comparison(ngc1068, txs0506, quantity):
    unit = QUANTITY_UNITS[quantity]
    fig, ax = plt.subplots(figsize=(7, 5))

    ax.loglog(ngc1068["energy"].to_value(u.GeV), ngc1068[quantity].to_value(unit), color=STYLE["ngc1068"]["color"], linestyle=STYLE["ngc1068"]["linestyle"], linewidth=STYLE["ngc1068"]["linewidth"], label="NGC 1068 (steady)")
    ax.loglog(txs0506["energy"].to_value(u.GeV), txs0506[quantity].to_value(unit), color=STYLE["txs0506"]["color"], linestyle=STYLE["txs0506"]["linestyle"], linewidth=STYLE["txs0506"]["linewidth"], label="TXS 0506+056 (158-day flare)")

    ax.set_xlabel(r"Neutrino energy, $E_{\nu}$ [GeV]")
    ax.set_ylabel(QUANTITY_LABELS[quantity])
    ax.set_title("IceCube Point-Source Neutrino Fluxes")
    ax.grid(True, which="both", alpha=0.25)
    ax.text(0.97, 0.02, r"$\nu_\mu+\bar{\nu}_\mu$" "\n" "Best-fit source fluxes", transform=ax.transAxes, ha="right", va="bottom", fontweight="bold")

    bold_tick_labels(ax)
    bold_legend(ax.legend(loc="upper right"))
    fig.tight_layout()
    fig.savefig(OUTPUT_DIR / f"icecube_point_source_neutrinos_{quantity}.png", dpi=200)
    fig.savefig(OUTPUT_DIR / f"icecube_point_source_neutrinos_{quantity}.pdf")
    plt.close(fig)


def main():
    OUTPUT_DIR.mkdir(exist_ok=True)
    quantity = normalize_spectral_quantity(PLOT_QUANTITY)
    if quantity not in QUANTITY_UNITS:
        raise ValueError("Point-source comparison supports phi, Ephi, E2phi, and E3phi.")

    ngc1068 = get_dataset("icecube.ngc1068_flux.2022").load(quantity=quantity)
    txs0506 = get_dataset("icecube.txs0506_flare_flux.2018").load(quantity=quantity)

    print(f"IceCube point-source neutrino comparison: {quantity}\n")
    validate_dataset(ngc1068, "icecube.ngc1068_flux.2022", "NGC 1068", quantity)
    validate_dataset(txs0506, "icecube.txs0506_flare_flux.2018", "TXS 0506+056", quantity)

    plot_comparison(ngc1068, txs0506, quantity)
    print(f"\n[PASS] Comparison outputs written to {OUTPUT_DIR}")


if __name__ == "__main__":
    main()
