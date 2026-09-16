from dataclasses import asdict
from pathlib import Path
from pprint import pprint

import astropy.units as u
import matplotlib.pyplot as plt
import numpy as np

from maham.datasets import get_dataset
from maham.models import get_model, list_models
from maham.models.flux.neutrino import family_envelope
from maham.plotting import apply_plot_style, bold_legend, bold_tick_labels, plot_upper_limits
from maham.physics.spectra import normalize_spectral_quantity, spectral_quantity_info

PLOT_QUANTITY = "E2phi"
OUTPUT_DIR = Path(__file__).resolve().parent / "outputs"
NEUTRINO_ENVELOPE_FLOOR_E2PHI = 1e-11
NEUTRINO_TEXT = r"Neutrino fluxes shown as all flavor" "\n" r"$\nu_e:\nu_\mu:\nu_\tau=1:1:1$, $\nu:\bar{\nu}=1:1$"

UNIT_LABELS = {
    0: r"GeV$^{-1}$ cm$^{-2}$ s$^{-1}$ sr$^{-1}$",
    1: r"cm$^{-2}$ s$^{-1}$ sr$^{-1}$",
    2: r"GeV cm$^{-2}$ s$^{-1}$ sr$^{-1}$",
    3: r"GeV$^{2}$ cm$^{-2}$ s$^{-1}$ sr$^{-1}$",
}

STYLE = {
    "fermi": {"color": "blue", "marker": "h", "mfc": "cyan", "ms": 6},
    "auger": {"color": "deepskyblue", "marker": "o", "mfc": "lightskyblue", "ms": 6},
    "ta": {"color": "orange", "marker": "h", "mfc": "gold", "ms": 6},
    "icecube": {"color": "green", "marker": "s", "mfc": "limegreen", "ms": 6},
    "km3net": {"color": "red", "marker": "*", "mfc": "white", "ms": 12},
    "glashow": {"color": "black", "marker": "*", "mfc": "white", "ms": 11},
    "ehe": {"color": "black"},
}


def require(condition, message):
    if not condition:
        raise AssertionError(message)
    print(f"PASS: {message}")


def common_unit(quantity):
    _, power = spectral_quantity_info(quantity)
    return u.GeV ** (power - 1) / (u.cm**2 * u.s * u.sr)


def quantity_label(quantity):
    family, power = spectral_quantity_info(quantity)
    symbol = r"\Phi" if family == "phi" else "J"
    prefix = "" if power == 0 else "E" if power == 1 else rf"E^{{{power}}}"
    return rf"${prefix}{symbol}(E)$"


def print_dataset_metadata(dataset, table, label):
    print("\n" + "=" * 100)
    print(label)
    print("=" * 100)
    print("\nRegistered DatasetMetadata:")
    pprint(asdict(dataset.metadata), sort_dicts=False)
    print("\nPlotted table metadata:")
    pprint(dict(table.meta), sort_dicts=False)
    print(f"\nRows: {len(table)}")


def bin_xerr(table):
    energy = table["energy"].to_value(u.GeV)
    energy_min = table["energy_min"].to_value(u.GeV)
    energy_max = table["energy_max"].to_value(u.GeV)
    return energy, np.vstack((energy - energy_min, energy_max - energy))


def gamma_source_envelope(quantity, unit, points_per_decade=80):
    metadata_group = list_models(messenger="gamma_ray", model_type="flux", family="source_environment")
    models = [get_model(metadata.id) for metadata in metadata_group]
    require(len(models) > 0, "gamma-ray source-environment model family is available")
    tables = [model.load(quantity=quantity) for model in models]
    emin = min(table["energy"][0].to_value(u.GeV) for table in tables)
    emax = max(table["energy"][-1].to_value(u.GeV) for table in tables)
    n_points = max(2, int(np.ceil((np.log10(emax) - np.log10(emin)) * points_per_decade)) + 1)
    energy = np.logspace(np.log10(emin), np.log10(emax), n_points)
    lower_stack = np.full((len(tables), n_points), np.nan)
    upper_stack = np.full((len(tables), n_points), np.nan)

    for i, table in enumerate(tables):
        x = table["energy"].to_value(u.GeV)
        center = table[quantity].to_value(unit)
        lower_column, upper_column = f"{quantity}_lower", f"{quantity}_upper"
        lower = table[lower_column].to_value(unit) if lower_column in table.colnames else center
        upper = table[upper_column].to_value(unit) if upper_column in table.colnames else center
        mask = (energy >= x[0]) & (energy <= x[-1])
        lower_stack[i, mask] = 10 ** np.interp(np.log10(energy[mask]), np.log10(x), np.log10(lower))
        upper_stack[i, mask] = 10 ** np.interp(np.log10(energy[mask]), np.log10(x), np.log10(upper))

    n_models = np.sum(np.isfinite(lower_stack) & np.isfinite(upper_stack), axis=0)
    lower, upper = np.full(n_points, np.nan), np.full(n_points, np.nan)
    valid = n_models > 0
    lower[valid] = np.nanmin(lower_stack[:, valid], axis=0)
    upper[valid] = np.nanmax(upper_stack[:, valid], axis=0)
    return energy, lower, upper, n_models


def neutrino_family_envelope(family, quantity, unit):
    table = family_envelope(family, quantity=quantity, flavor="all_flavor", flavor_assumption="equal")
    return table["energy"].to_value(u.GeV), table[f"{quantity}_lower"].to_value(unit), table[f"{quantity}_upper"].to_value(unit), np.asarray(table["n_models"], dtype=int)


def load_model_envelopes(quantity):
    unit = common_unit(quantity)
    return {
        "gamma_source": gamma_source_envelope(quantity, unit),
        "nu_source": neutrino_family_envelope("source_environment", quantity, unit),
        "nu_cosmogenic": neutrino_family_envelope("cosmogenic", quantity, unit),
    }


def plot_model_envelopes(ax, envelopes, quantity):
    gamma_energy, gamma_lower, gamma_upper, gamma_n = envelopes["gamma_source"]
    source_energy, source_lower, source_upper, source_n = envelopes["nu_source"]
    cosmo_energy, cosmo_lower, cosmo_upper, cosmo_n = envelopes["nu_cosmogenic"]

    gamma_handle = ax.fill_between(gamma_energy, gamma_lower, gamma_upper, where=gamma_n > 0, color=plt.get_cmap("Blues")(0.58), alpha=0.22, linewidth=0, label=r"$\gamma$: source environment", zorder=1)

    if quantity == "E2phi":
        floor = NEUTRINO_ENVELOPE_FLOOR_E2PHI
        source_mask = (source_n > 0) & np.isfinite(source_upper) & (source_upper >= floor)
        cosmo_mask = (cosmo_n > 0) & np.isfinite(cosmo_upper) & (cosmo_upper >= floor)
        source_bottom = np.full_like(source_upper, floor)
        cosmo_bottom = np.full_like(cosmo_upper, floor)
        ax.axhline(floor, color="0.45", linestyle=":", linewidth=0.9, alpha=0.55, zorder=0)
    else:
        source_mask = (source_n > 0) & np.isfinite(source_lower) & np.isfinite(source_upper)
        cosmo_mask = (cosmo_n > 0) & np.isfinite(cosmo_lower) & np.isfinite(cosmo_upper)
        source_bottom, cosmo_bottom = source_lower, cosmo_lower

    source_handle = ax.fill_between(source_energy, source_bottom, source_upper, where=source_mask, interpolate=True, color=plt.get_cmap("Greens")(0.56), alpha=0.20, linewidth=0, label=r"$\nu$: source environment", zorder=1)
    cosmo_handle = ax.fill_between(cosmo_energy, cosmo_bottom, cosmo_upper, where=cosmo_mask, interpolate=True, color=plt.get_cmap("Greys")(0.55), alpha=0.20, linewidth=0, label=r"$\nu$: cosmogenic", zorder=1)
    return [gamma_handle, source_handle, cosmo_handle]


def load_datasets():
    quantity = normalize_spectral_quantity(PLOT_QUANTITY)
    datasets = {
        "auger": get_dataset("auger.combined_spectrum.2021"),
        "ta": get_dataset("telescope_array.combined_spectrum.2023"),
        "fermi": get_dataset("fermi_lat.egb.2015"),
        "icecube_2020": get_dataset("icecube.cascade_piecewise_flux.2020"),
        "icecube_2022": get_dataset("icecube.throughgoing_muon_piecewise_flux.2022"),
        "glashow": get_dataset("icecube.glashow.flux.2021"),
        "ehe": get_dataset("icecube.ehe.differential_limit.2025"),
        "km3net": get_dataset("km3net.km3_230213a_flux.2025"),
    }

    tables = {
        "auger": datasets["auger"].load(quantity=quantity),
        "ta": datasets["ta"].load(quantity=quantity),
        "fermi": datasets["fermi"].load(quantity=quantity),
        "icecube_2020": datasets["icecube_2020"].load(quantity=quantity, flavor="all_flavor", flavor_assumption="equal"),
        "icecube_2022": datasets["icecube_2022"].load(quantity=quantity, flavor="all_flavor", flavor_assumption="equal"),
        "glashow": datasets["glashow"].load(quantity=quantity, flavor="all_flavor", flavor_assumption="equal"),
        "ehe": datasets["ehe"].load(quantity=quantity),
        "km3net": datasets["km3net"].load(quantity=quantity, flavor="all_flavor", flavor_assumption="equal"),
    }

    labels = {
        "auger": "Pierre Auger Combined Spectrum 2021",
        "ta": "Telescope Array Combined Spectrum 2023",
        "fermi": "Fermi-LAT EGB 2015",
        "icecube_2020": "IceCube Six-Year Cascade Spectrum 2020",
        "icecube_2022": "IceCube 9.5-Year Through-Going Muon Flux 2022",
        "glashow": "IceCube Glashow Flux 2021",
        "ehe": "IceCube EHE Differential Upper Limit 2025",
        "km3net": "KM3NeT KM3-230213A Flux 2025",
    }

    for key in datasets:
        print_dataset_metadata(datasets[key], tables[key], labels[key])
    return tables


def validate_comparison(tables):
    quantity = normalize_spectral_quantity(PLOT_QUANTITY)
    unit = common_unit(quantity)

    names = {
        "auger": "Auger",
        "ta": "Telescope Array",
        "fermi": "Fermi-LAT EGB",
        "icecube_2020": "IceCube 2020",
        "icecube_2022": "IceCube 2022",
        "glashow": "IceCube Glashow",
        "ehe": "IceCube EHE limit",
        "km3net": "KM3NeT KM3-230213A",
    }

    for key, table in tables.items():
        require(table.meta["quantity"] == quantity, f"{names[key]} is represented as {quantity}")
        table[quantity].to(unit)
        require(True, f"{names[key]} is convertible to the common physical unit")

    require(np.count_nonzero(tables["ta"]["is_upper_limit"]) == 1, "Telescope Array contributes one upper limit")
    require(bool(tables["ta"]["is_upper_limit"][-1]), "Telescope Array upper limit is the final point")
    require(np.count_nonzero(tables["fermi"]["is_upper_limit"]) == 0, "Fermi-LAT EGB contributes no upper limits")
    require(tables["icecube_2020"].meta["flavor_convention"] == "all_flavor", "IceCube 2020 is converted to all-flavor")
    require(tables["icecube_2022"].meta["flavor_convention"] == "all_flavor", "IceCube 2022 is converted to all-flavor")
    require(tables["glashow"].meta["flavor_convention"] == "all_flavor", "Glashow is converted to all-flavor")
    require(tables["km3net"].meta["flavor_convention"] == "all_flavor", "KM3NeT is converted to all-flavor")
    require(np.all(tables["ehe"]["is_upper_limit"]), "All IceCube EHE points are upper limits")


def plot_fermi(ax, table, quantity, unit):
    s = STYLE["fermi"]
    energy, xerr = bin_xerr(table)
    upper = np.asarray(table["is_upper_limit"], dtype=bool)
    measured = ~upper
    y = table[quantity].to_value(unit)
    y_lower = table[f"{quantity}_lower"].to_value(unit)
    y_upper = table[f"{quantity}_upper"].to_value(unit)
    handle = ax.errorbar(energy[measured], y[measured], xerr=xerr[:, measured], yerr=np.vstack((y[measured] - y_lower[measured], y_upper[measured] - y[measured])), fmt=s["marker"], linestyle="none", color=s["color"], markerfacecolor=s["mfc"], markeredgecolor=s["color"], markersize=s["ms"], markeredgewidth=1.3, elinewidth=1.2, capsize=2.5, label=r"Total EGB $\gamma$ (Fermi-LAT)", zorder=10)
    if np.any(upper):
        plot_upper_limits(ax, energy[upper], y[upper], xerr=xerr[:, upper], arrow_factor=2.5, color=s["color"], linewidth=1.5, capsize=3, mutation_scale=12)
    return handle


def plot_auger(ax, table, quantity, unit):
    s = STYLE["auger"]
    energy = table["energy"].to_value(u.GeV)
    y = table[quantity].to_value(unit)
    lower = table[f"{quantity}_stat_err_lower"].to_value(unit)
    upper = table[f"{quantity}_stat_err_upper"].to_value(unit)
    return ax.errorbar(energy, y, yerr=np.vstack((lower, upper)), fmt=s["marker"], linestyle="none", color=s["color"], markerfacecolor=s["mfc"], markeredgecolor=s["color"], markersize=s["ms"], markeredgewidth=1.3, elinewidth=1.2, capsize=2.5, label="Cosmic Rays (Auger)", zorder=10)


def plot_ta(ax, table, quantity, unit):
    s = STYLE["ta"]
    energy, xerr = bin_xerr(table)
    upper = np.asarray(table["is_upper_limit"], dtype=bool)
    measured = ~upper
    resolved = np.asarray(table["has_resolved_vertical_error"], dtype=bool) & measured
    unresolved = measured & ~resolved
    y = table[quantity].to_value(unit)
    y_lower = table[f"{quantity}_lower"].to_value(unit)
    y_upper = table[f"{quantity}_upper"].to_value(unit)

    handle = ax.errorbar(energy[resolved], y[resolved], xerr=xerr[:, resolved], yerr=np.vstack((y[resolved] - y_lower[resolved], y_upper[resolved] - y[resolved])), fmt=s["marker"], linestyle="none", color=s["color"], markerfacecolor=s["mfc"], markeredgecolor=s["color"], markersize=s["ms"], markeredgewidth=1.3, elinewidth=1.2, capsize=2.5, label="Cosmic Rays (TA)", zorder=10)
    ax.errorbar(energy[unresolved], y[unresolved], xerr=xerr[:, unresolved], fmt=s["marker"], linestyle="none", color=s["color"], markerfacecolor=s["mfc"], markeredgecolor=s["color"], markersize=s["ms"], markeredgewidth=1.3, elinewidth=1.2, capsize=2.5, zorder=10)
    plot_upper_limits(ax, energy[upper], y[upper], xerr=xerr[:, upper], arrow_factor=2.5, color=s["color"], linewidth=1.5, capsize=3, mutation_scale=12)
    return handle


def plot_icecube_spectrum(ax, table, quantity, unit, label="_nolegend_"):
    s = STYLE["icecube"]
    energy, xerr = bin_xerr(table)
    upper = np.asarray(table["is_upper_limit"], dtype=bool)
    measured = ~upper
    y = table[quantity].to_value(unit)
    y_lower = table[f"{quantity}_lower"].to_value(unit)
    y_upper = table[f"{quantity}_upper"].to_value(unit)

    handle = ax.errorbar(energy[measured], y[measured], xerr=xerr[:, measured], yerr=np.vstack((y[measured] - y_lower[measured], y_upper[measured] - y[measured])), fmt=s["marker"], linestyle="none", color=s["color"], markerfacecolor=s["mfc"], markeredgecolor=s["color"], markersize=s["ms"], markeredgewidth=1.3, elinewidth=1.3, capsize=2.5, label=label, zorder=12)
    plot_upper_limits(ax, energy[upper], y_upper[upper], xerr=xerr[:, upper], arrow_factor=2.5, color=s["color"], linewidth=1.5, capsize=3, mutation_scale=12)
    return handle


def plot_ehe_limit(ax, table, quantity, unit):
    return ax.plot(table["energy"].to_value(u.GeV), table[quantity].to_value(unit), linestyle="-", linewidth=2.2, color=STYLE["ehe"]["color"], label="IceCube EHE", zorder=8)[0]


def plot_km3net(ax, table, quantity, unit):
    s = STYLE["km3net"]
    energy, xerr = bin_xerr(table)
    y = table[quantity].to_value(unit)
    y_lower = table[f"{quantity}_lower"].to_value(unit)
    y_upper = table[f"{quantity}_upper"].to_value(unit)
    return ax.errorbar(energy, y, xerr=xerr, yerr=np.vstack((y - y_lower, y_upper - y)), fmt=s["marker"], linestyle="none", color=s["color"], markerfacecolor=s["mfc"], markeredgecolor=s["color"], markersize=s["ms"], markeredgewidth=1.6, elinewidth=1.5, capsize=3, label="KM3-230213A (KM3NeT)", zorder=30)


def plot_glashow(ax, table, quantity, unit):
    s = STYLE["glashow"]
    energy, xerr = bin_xerr(table)
    upper = np.asarray(table["is_upper_limit"], dtype=bool)
    measured = ~upper
    y = table[quantity].to_value(unit)
    y_lower = table[f"{quantity}_lower"].to_value(unit)
    y_upper = table[f"{quantity}_upper"].to_value(unit)

    handle = ax.errorbar(energy[measured], y[measured], xerr=xerr[:, measured], yerr=np.vstack((y[measured] - y_lower[measured], y_upper[measured] - y[measured])), fmt=s["marker"], linestyle="none", color=s["color"], markerfacecolor=s["mfc"], markeredgecolor=s["color"], markersize=s["ms"], markeredgewidth=1.5, elinewidth=1.5, capsize=3, label="Glashow (IceCube)", zorder=31)
    plot_upper_limits(ax, energy[upper], y_upper[upper], xerr=xerr[:, upper], arrow_factor=2.5, color=s["color"], linewidth=1.5, capsize=3, mutation_scale=12)
    return handle


def plot_comparison(tables):
    quantity = normalize_spectral_quantity(PLOT_QUANTITY)
    unit = common_unit(quantity)
    _, power = spectral_quantity_info(quantity)

    fig, ax = plt.subplots(figsize=(12, 6))
    ax.set_xscale("log")
    ax.set_yscale("log")
    ax.set_xlim(8e-2, 4e11)
    ax.set_ylim(1e-11, 1e-5)

    model_handles = plot_model_envelopes(ax, load_model_envelopes(quantity), quantity)

    h_fermi = plot_fermi(ax, tables["fermi"], quantity, unit)
    h_auger = plot_auger(ax, tables["auger"], quantity, unit)
    h_ta = plot_ta(ax, tables["ta"], quantity, unit)
    h_ic = plot_icecube_spectrum(ax, tables["icecube_2020"], quantity, unit, r"Astrophysical $\nu$ (IceCube)")
    plot_icecube_spectrum(ax, tables["icecube_2022"], quantity, unit)
    h_ehe = plot_ehe_limit(ax, tables["ehe"], quantity, unit)
    h_km3net = plot_km3net(ax, tables["km3net"], quantity, unit)
    h_glashow = plot_glashow(ax, tables["glashow"], quantity, unit)

    ax.set_xlabel(r"Particle energy, $E$ [GeV]", fontweight="bold")
    ax.set_ylabel(rf"Differential intensity, {quantity_label(quantity)} [{UNIT_LABELS[power]}]", fontweight="bold")
    ax.set_title("Multimessenger Diffuse Spectra", fontweight="bold")
    ax.grid(True, which="both", alpha=0.25)
    ax.text(0.97, 0.02, NEUTRINO_TEXT, transform=ax.transAxes, ha="right", va="bottom", fontweight="bold")

    observation_handles = [h_fermi, h_auger, h_ta, h_ic, h_km3net, h_glashow]
    observation_legend = ax.legend(handles=observation_handles, loc="upper left", ncol=3, frameon=True)
    bold_legend(observation_legend)
    ax.add_artist(observation_legend)

    limit_legend = ax.legend(handles=[h_ehe], title="90% CL UL", loc="lower center", bbox_to_anchor=(0.5, 0.02), ncol=1, frameon=True)
    limit_legend.get_title().set_fontweight("bold")
    bold_legend(limit_legend)
    ax.add_artist(limit_legend)

    model_legend = ax.legend(handles=model_handles, title="Model envelopes", loc="center left", bbox_to_anchor=(0.01, 0.50), ncol=1, frameon=True)
    model_legend.get_title().set_fontweight("bold")
    bold_legend(model_legend)
    ax.add_artist(model_legend)

    bold_tick_labels(ax)
    fig.tight_layout()
    stem = f"diffuse_spectra_{quantity.lower()}"
    fig.savefig(OUTPUT_DIR / f"{stem}.png", dpi=200)
    fig.savefig(OUTPUT_DIR / f"{stem}.pdf")
    plt.close(fig)


def main():
    apply_plot_style()
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    tables = load_datasets()
    validate_comparison(tables)
    plot_comparison(tables)
    print(f"\nComparison outputs written to {OUTPUT_DIR}")


if __name__ == "__main__":
    main()
