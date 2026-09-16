from pathlib import Path

import astropy.units as u
import matplotlib.pyplot as plt
import numpy as np

from maham.models import get_model, list_models
from maham.models.flux.neutrino import family_envelope
from maham.plotting import apply_plot_style, bold_tick_labels
from maham.physics.spectra import normalize_spectral_quantity, spectral_quantity_info

PLOT_QUANTITY = "E2phi"
OUTPUT_DIR = Path(__file__).resolve().parent / "outputs"
NEUTRINO_TEXT = r"Neutrino fluxes shown as all flavor" "\n" r"$\nu_e:\nu_\mu:\nu_\tau=1:1:1$, $\nu:\bar{\nu}=1:1$"

MODEL_LABELS = {
    "gamma_ray.source_environment.ajello_blazar_population_2015": "Ajello et al. 2015",
    "gamma_ray.source_environment.km3net_blazar_population_2026_best_fit": "KM3NeT 2026",
    "neutrino.source_environment.boncioli_llgrb_2019": "Boncioli et al. 2019 (LLGRB)",
    "neutrino.source_environment.fang_pulsar_2014": "Fang et al. 2014 (pulsar)",
    "neutrino.source_environment.km3net_blazar_population_2026_best_fit": "KM3NeT 2026 (blazars)",
    "neutrino.source_environment.rodrigues_agn_2021": "Rodrigues et al. 2021 (AGN)",
    "neutrino.source_environment.rodrigues_bllac_2024": "Rodrigues et al. 2024 (BL Lac)",
    "neutrino.source_environment.rodrigues_fsrq_2024": "Rodrigues et al. 2024 (FSRQ)",
    "neutrino.source_environment.tamborra_llgrb_2015": "Tamborra et al. 2015 (LLGRB)",
    "neutrino.source_environment.tamborra_sgrb_2015": "Tamborra et al. 2015 (sGRB)",
    "neutrino.source_environment.winter_tde_2023": "Winter et al. 2023 (TDE)",
    "neutrino.cosmogenic.allard_2026_frii_model1": "Allard et al. 2026 (1)",
    "neutrino.cosmogenic.allard_2026_frii_model2": "Allard et al. 2026 (2)",
    "neutrino.cosmogenic.allard_2026_frii_model3": "Allard et al. 2026 (3)",
    "neutrino.cosmogenic.aloisio_2015": "Aloisio et al. 2015",
    "neutrino.cosmogenic.auger_2023": "Auger 2023",
    "neutrino.cosmogenic.berat_2024": "Berat et al. 2024",
    "neutrino.cosmogenic.boncioli_2019": "Boncioli et al. 2019",
    "neutrino.cosmogenic.condorelli_2023": "Condorelli et al. 2023",
    "neutrino.cosmogenic.ehlert_2024": "Ehlert et al. 2024",
    "neutrino.cosmogenic.heinze_2019": "Heinze et al. 2019",
    "neutrino.cosmogenic.kuznetsov_petrov_savchenko_2026_best_fit": "KPS 2026 (best fit)",
    "neutrino.cosmogenic.kuznetsov_petrov_savchenko_2026_local_min": "KPS 2026 (local min.)",
    "neutrino.cosmogenic.muzio_farrar_2023": "Muzio et al. 2023",
    "neutrino.cosmogenic.muzio_unger_wissel_2023": "Muzio et al. 2023",
    "neutrino.cosmogenic.yoshida_meier_2026_no_evolution": "Yoshida et al. 2026 (no evo.)",
    "neutrino.cosmogenic.yoshida_meier_2026_log_normal": "Yoshida et al. 2026 (log-norm.)",
    "neutrino.cosmogenic.zhang_murase_2019": "Zhang et al. 2019",
}


def common_unit(quantity):
    _, power = spectral_quantity_info(quantity)
    return u.GeV ** (power - 1) / (u.cm**2 * u.s * u.sr)


def quantity_label(quantity):
    family, power = spectral_quantity_info(quantity)
    symbol = r"\Phi" if family == "phi" else "J"
    prefix = "" if power == 0 else "E" if power == 1 else rf"E^{{{power}}}"
    return rf"${prefix}{symbol}(E)$"


def short_label(metadata):
    return MODEL_LABELS.get(metadata.id, metadata.title)


def load_metadata_group(messenger, family):
    return sorted(list_models(messenger=messenger, model_type="flux", family=family), key=short_label)


def load_model_table(metadata, quantity, neutrino=False):
    model = get_model(metadata.id)
    return model.load(quantity=quantity, flavor="all_flavor", flavor_assumption="equal") if neutrino else model.load(quantity=quantity)


def gamma_envelope(metadata_group, quantity, unit, points_per_decade=80):
    tables = [load_model_table(metadata, quantity) for metadata in metadata_group]
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


def neutrino_envelope(family, quantity, unit):
    table = family_envelope(family, quantity=quantity, flavor="all_flavor", flavor_assumption="equal")
    return table["energy"].to_value(u.GeV), table[f"{quantity}_lower"].to_value(unit), table[f"{quantity}_upper"].to_value(unit), np.asarray(table["n_models"], dtype=int)


def class_colors(cmap_name, n, vmin=0.42, vmax=0.92):
    if n == 1:
        return [plt.get_cmap(cmap_name)(0.72)]
    return [plt.get_cmap(cmap_name)(value) for value in np.linspace(vmin, vmax, n)]


def plot_group_lines(ax, metadata_group, quantity, unit, cmap_name, neutrino, vmin=0.42, vmax=0.92):
    handles = []
    for metadata, color in zip(metadata_group, class_colors(cmap_name, len(metadata_group), vmin, vmax)):
        table = load_model_table(metadata, quantity, neutrino)
        handles.append(ax.plot(table["energy"].to_value(u.GeV), table[quantity].to_value(unit), color=color, linewidth=1.45, alpha=0.98, label=short_label(metadata), zorder=4)[0])
    return handles


def compact_legend(ax, handles, ncol):
    legend = ax.legend(handles=handles, loc="lower left", ncol=ncol, fontsize=6.2, frameon=True, framealpha=0.90, fancybox=True, borderpad=0.45, labelspacing=0.28, handlelength=2.0, handletextpad=0.45, columnspacing=0.75)
    for text in legend.get_texts():
        text.set_fontweight("bold")
    return legend


def plot_models():
    quantity = normalize_spectral_quantity(PLOT_QUANTITY)
    unit = common_unit(quantity)
    gamma_source = load_metadata_group("gamma_ray", "source_environment")
    nu_source = load_metadata_group("neutrino", "source_environment")
    nu_cosmogenic = load_metadata_group("neutrino", "cosmogenic")

    fig, axs = plt.subplots(1, 3, figsize=(15, 5), sharey=True)
    for ax in axs:
        ax.set_xscale("log")
        ax.set_yscale("log")
        ax.set_ylim(1e-17, 5e-5)
        ax.grid(True, which="both", alpha=0.22)

    axs[0].set_xlim(8e-2, 2e3)
    axs[1].set_xlim(5e3, 2e10)
    axs[2].set_xlim(5e3, 4e11)

    gamma_handles = plot_group_lines(axs[0], gamma_source, quantity, unit, "Blues", False, 0.42, 0.88)
    source_handles = plot_group_lines(axs[1], nu_source, quantity, unit, "Greens", True, 0.42, 0.90)
    cosmo_handles = plot_group_lines(axs[2], nu_cosmogenic, quantity, unit, "Greys", True, 0.55, 0.95)

    gamma_energy, gamma_lower, gamma_upper, gamma_n = gamma_envelope(gamma_source, quantity, unit)
    source_energy, source_lower, source_upper, source_n = neutrino_envelope("source_environment", quantity, unit)
    cosmo_energy, cosmo_lower, cosmo_upper, cosmo_n = neutrino_envelope("cosmogenic", quantity, unit)

    gamma_fill = axs[0].fill_between(gamma_energy, gamma_lower, gamma_upper, where=gamma_n > 0, color=plt.get_cmap("Blues")(0.58), alpha=0.20, linewidth=0, label="Envelope", zorder=1)
    source_fill = axs[1].fill_between(source_energy, source_lower, source_upper, where=source_n > 0, color=plt.get_cmap("Greens")(0.56), alpha=0.18, linewidth=0, label="Envelope", zorder=1)
    cosmo_fill = axs[2].fill_between(cosmo_energy, cosmo_lower, cosmo_upper, where=cosmo_n > 0, color=plt.get_cmap("Greys")(0.55), alpha=0.18, linewidth=0, label="Envelope", zorder=1)

    compact_legend(axs[0], [*gamma_handles, gamma_fill], 1)
    compact_legend(axs[1], [*source_handles, source_fill], 2)
    compact_legend(axs[2], [*cosmo_handles, cosmo_fill], 3)

    _, power = spectral_quantity_info(quantity)
    units = {
        0: r"GeV$^{-1}$ cm$^{-2}$ s$^{-1}$ sr$^{-1}$",
        1: r"cm$^{-2}$ s$^{-1}$ sr$^{-1}$",
        2: r"GeV cm$^{-2}$ s$^{-1}$ sr$^{-1}$",
        3: r"GeV$^{2}$ cm$^{-2}$ s$^{-1}$ sr$^{-1}$",
    }

    axs[0].set_title(r"$\gamma$: source environment", fontweight="bold", pad=5)
    axs[1].set_title(r"$\nu$: source environment", fontweight="bold", pad=5)
    axs[2].set_title(r"$\nu$: cosmogenic", fontweight="bold", pad=5)

    fig.suptitle("Multimessenger Diffuse Flux Models", fontsize=14, fontweight="bold", y=0.975)
    fig.supxlabel(r"Particle energy, $E$ [GeV]", fontweight="bold", y=0.035)
    fig.supylabel(rf"Differential intensity, {quantity_label(quantity)} [{units[power]}]", fontweight="bold", x=0.012)
    fig.text(0.97, 0.02, NEUTRINO_TEXT, ha="right", va="bottom", fontsize=8.5, fontweight="bold")

    for ax in axs:
        bold_tick_labels(ax)

    fig.subplots_adjust(left=0.075, right=0.995, bottom=0.14, top=0.86, wspace=0.04)
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    stem = f"model_spectra_{quantity.lower()}"
    fig.savefig(OUTPUT_DIR / f"{stem}.png", dpi=200, bbox_inches="tight")
    fig.savefig(OUTPUT_DIR / f"{stem}.pdf", bbox_inches="tight")
    plt.close(fig)
    print(f"Model comparison outputs written to {OUTPUT_DIR}")


def main():
    apply_plot_style()
    plot_models()


if __name__ == "__main__":
    main()
