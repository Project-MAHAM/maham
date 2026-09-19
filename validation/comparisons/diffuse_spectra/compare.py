from dataclasses import asdict
from pathlib import Path
from pprint import pprint
import astropy.units as u
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.ticker import LogLocator, NullFormatter
from maham.datasets import get_dataset
from maham.models import get_model, list_models
from maham.models.flux.neutrino import family_envelope
from maham.physics.spectra import convert_limit_normalization_to_decade_width, convert_sensitivity_normalization_to_decade_width, convert_single_event_sensitivity_to_confidence_level, normalize_spectral_quantity, spectral_quantity_info
from maham.plotting import apply_plot_style, bold_legend, bold_tick_labels, plot_upper_limits

PLOT_QUANTITY = "E2phi"
OUTPUT_DIR = Path(__file__).resolve().parent / "outputs"
NEUTRINO_ENVELOPE_FLOOR_E2PHI = 1e-11
NEUTRINO_TEXT = r"All flavors neutrino data" "\n" r"$\nu_e:\nu_\mu:\nu_\tau=1:1:1$, $\nu:\bar{\nu}=1:1$"
UNIT_LABELS = {
    0: r"GeV$^{-1}$ cm$^{-2}$ s$^{-1}$ sr$^{-1}$",
    1: r"cm$^{-2}$ s$^{-1}$ sr$^{-1}$",
    2: r"GeV cm$^{-2}$ s$^{-1}$ sr$^{-1}$",
    3: r"GeV$^{2}$ cm$^{-2}$ s$^{-1}$ sr$^{-1}$",
}
STYLE = {
    "fermi": {"color": "blue", "marker": "h", "mfc": "cyan", "ms": 6},
    "auger_cr": {"color": "deepskyblue", "marker": "o", "mfc": "lightskyblue", "ms": 6},
    "ta": {"color": "orange", "marker": "h", "mfc": "gold", "ms": 6},
    "icecube": {"color": "green", "marker": "s", "mfc": "limegreen", "ms": 6},
    "km3net": {"color": "red", "marker": "*", "mfc": "white", "ms": 12},
    "glashow": {"color": "black", "marker": "*", "mfc": "white", "ms": 11},
}
LIMIT_STYLE = {
    "icecube_ehe": {"color": "limegreen", "lw": 2.2},
    "auger_nu": {"color": "lightskyblue", "lw": 2.0},
    "ara": {"color": "deeppink", "lw": 2.1},
    "anita": {"color": "mediumpurple", "lw": 2.0},
}
LIMIT_LABELS = {
    "icecube_ehe": "IceCube EHE 2025",
    "auger_nu": "Auger 2022",
    "ara": "ARA 10.6 yr",
    "anita": "ANITA I-IV",
}
LIMIT_KEYS = ("ara", "icecube_ehe", "anita", "auger_nu")
SENSITIVITY_STYLE = {"rno_g": {"color": "mediumvioletred", "lw": 2.0, "ls": "--"}, "icecube_gen2_radio": {"color": "forestgreen", "lw": 2.0, "ls": "--"}, "pueo": {"color": "indigo", "lw": 2.0, "ls": "--"}, "grand200k": {"color": "saddlebrown", "lw": 2.0, "ls": "--"}, "trinity": {"color": "darkcyan", "lw": 2.0, "ls": "--"}, "ret_n": {"color": "crimson", "lw": 2.0, "ls": "--"}}
SENSITIVITY_LABELS = {"rno_g": "RNO-G 35 stn, 5 yr", "icecube_gen2_radio": "IceCube-Gen2 Radio 10 yr", "pueo": "PUEO 30 d", "grand200k": "GRAND200k 10 yr", "trinity": "Trinity 10 yr", "ret_n": "RET-N 10 stn, 10 yr"}
SENSITIVITY_KEYS = ("rno_g", "icecube_gen2_radio", "pueo", "grand200k", "trinity", "ret_n")

ZORDER_MODELS = 0
ZORDER_SENSITIVITIES = 8
ZORDER_LIMITS = 15
ZORDER_SPECTRA = 30
ZORDER_SPECTRUM_UL = 34
ZORDER_EVENTS = 36
LEGEND_FONTSIZE = 9.5
LEGEND_TITLE_FONTSIZE = 9.5


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

def plot_spectrum_upper_limits(ax, x, y, xerr, **kwargs):
    existing = {id(artist) for artist in ax.get_children()}
    plot_upper_limits(ax, x, y, xerr=xerr, **kwargs)
    for artist in ax.get_children():
        if id(artist) not in existing:
            artist.set_zorder(ZORDER_SPECTRUM_UL)

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
    gamma_handle = ax.fill_between(gamma_energy, gamma_lower, gamma_upper, where=gamma_n > 0, color=plt.get_cmap("Blues")(0.58), alpha=0.20, linewidth=0, label=r"$\gamma$: source environment", zorder=ZORDER_MODELS)
    if quantity == "E2phi":
        floor = NEUTRINO_ENVELOPE_FLOOR_E2PHI
        source_mask = (source_n > 0) & np.isfinite(source_upper) & (source_upper >= floor)
        cosmo_mask = (cosmo_n > 0) & np.isfinite(cosmo_upper) & (cosmo_upper >= floor)
        source_bottom = np.full_like(source_upper, floor)
        cosmo_bottom = np.full_like(cosmo_upper, floor)
        ax.axhline(floor, color="0.45", linestyle=":", linewidth=0.9, alpha=0.5, zorder=ZORDER_MODELS)
    else:
        source_mask = (source_n > 0) & np.isfinite(source_lower) & np.isfinite(source_upper)
        cosmo_mask = (cosmo_n > 0) & np.isfinite(cosmo_lower) & np.isfinite(cosmo_upper)
        source_bottom, cosmo_bottom = source_lower, cosmo_lower
    source_handle = ax.fill_between(source_energy, source_bottom, source_upper, where=source_mask, interpolate=True, color=plt.get_cmap("Greens")(0.56), alpha=0.18, linewidth=0, label=r"$\nu$: source environment", zorder=ZORDER_MODELS)
    cosmo_handle = ax.fill_between(cosmo_energy, cosmo_bottom, cosmo_upper, where=cosmo_mask, interpolate=True, color=plt.get_cmap("Greys")(0.55), alpha=0.18, linewidth=0, label=r"$\nu$: cosmogenic", zorder=ZORDER_MODELS)
    return [gamma_handle, source_handle, cosmo_handle]

def load_datasets():
    quantity = normalize_spectral_quantity(PLOT_QUANTITY)
    datasets = {
        "auger_cr": get_dataset("auger.combined_spectrum.2021"),
        "ta": get_dataset("telescope_array.combined_spectrum.2023"),
        "fermi": get_dataset("fermi_lat.egb.2015"),
        "icecube_2020": get_dataset("icecube.cascade_piecewise_flux.2020"),
        "icecube_2022": get_dataset("icecube.throughgoing_muon_piecewise_flux.2022"),
        "glashow": get_dataset("icecube.glashow.flux.2021"),
        "km3net": get_dataset("km3net.km3_230213a_flux.2025"),
        "icecube_ehe": get_dataset("icecube.ehe.differential_limit.2025"),
        "auger_nu": get_dataset("auger.diffuse_neutrino_limit.2023"),
        "ara": get_dataset("ara.five_station.diffuse_neutrino_limit.2026"),
        "anita": get_dataset("anita.i_iv_diffuse_neutrino_limit.2019"),
        "rno_g": get_dataset("rno_g.design.diffuse_sensitivity.2021"),
        "pueo": get_dataset("pueo.diffuse_sensitivity.2025"),
        "icecube_gen2_radio": get_dataset("icecube_gen2.radio.diffuse_sensitivity.2021"),
        "grand200k": get_dataset("grand200k.diffuse_sensitivity.2021"),
        "trinity": get_dataset("trinity.diffuse_sensitivity.2025"),
        "ret_n": get_dataset("ret_n.diffuse_sensitivity.2022"),
    }
    tables = {
        "auger_cr": datasets["auger_cr"].load(quantity=quantity),
        "ta": datasets["ta"].load(quantity=quantity),
        "fermi": datasets["fermi"].load(quantity=quantity),
        "icecube_2020": datasets["icecube_2020"].load(quantity=quantity, flavor="all_flavor", flavor_assumption="equal"),
        "icecube_2022": datasets["icecube_2022"].load(quantity=quantity, flavor="all_flavor", flavor_assumption="equal"),
        "glashow": datasets["glashow"].load(quantity=quantity, flavor="all_flavor", flavor_assumption="equal"),
        "km3net": datasets["km3net"].load(quantity=quantity, flavor="all_flavor", flavor_assumption="equal"),
        "icecube_ehe": datasets["icecube_ehe"].load(quantity=quantity, flavor="all_flavor"),
        "auger_nu": datasets["auger_nu"].load(quantity=quantity, flavor="all_flavor", flavor_assumption="equal"),
        "ara": datasets["ara"].load(quantity=quantity, flavor="all_flavor"),
        "anita": datasets["anita"].load(quantity=quantity, flavor="all_flavor"),
        "rno_g": datasets["rno_g"].load(quantity=quantity, flavor="all_flavor"),
        "pueo": datasets["pueo"].load(quantity=quantity, flavor="all_flavor"),
        "icecube_gen2_radio": datasets["icecube_gen2_radio"].load(quantity=quantity, flavor="all_flavor"),
        "grand200k": datasets["grand200k"].load(quantity=quantity, flavor="all_flavor"),
        "trinity": datasets["trinity"].load(quantity=quantity, flavor="all_flavor"),
        "ret_n": datasets["ret_n"].load(quantity=quantity, flavor="all_flavor"),
    }
    for key in LIMIT_KEYS:
        tables[key] = convert_limit_normalization_to_decade_width(tables[key], target_width_decades=1.0)
    tables["pueo"] = convert_sensitivity_normalization_to_decade_width(tables["pueo"], target_width_decades=1.0)
    tables["pueo"] = convert_single_event_sensitivity_to_confidence_level(tables["pueo"], confidence_level=0.90, method="feldman_cousins", n_observed=0, expected_background=0.0)
    labels = {
        "auger_cr": "Pierre Auger Combined Spectrum 2021",
        "ta": "Telescope Array Combined Spectrum 2023",
        "fermi": "Fermi-LAT EGB 2015",
        "icecube_2020": "IceCube Six-Year Cascade Spectrum 2020",
        "icecube_2022": "IceCube 9.5-Year Through-Going Muon Flux 2022",
        "glashow": "IceCube Glashow Flux 2021",
        "km3net": "KM3NeT KM3-230213A Flux 2025",
        "icecube_ehe": "IceCube EHE Differential Upper Limit 2025",
        "auger_nu": "Pierre Auger Diffuse Neutrino Upper Limit 2023",
        "ara": "ARA Five-Station Diffuse Neutrino Upper Limit 2026",
        "anita": "ANITA I-IV Diffuse Neutrino Upper Limit 2019",
        "rno_g": "RNO-G 35-Station Five-Year Diffuse Neutrino Sensitivity 2021",
        "pueo": "PUEO 30-Day Diffuse Neutrino Sensitivity 2025",
        "icecube_gen2_radio": "IceCube-Gen2 Radio Ten-Year Diffuse Neutrino Sensitivity 2021",
        "grand200k": "GRAND200k Ten-Year Diffuse Neutrino Sensitivity 2021",
        "trinity": "Trinity Observatory Ten-Year Diffuse Neutrino Sensitivity 2025",
        "ret_n": "RET-N Ten-Station Ten-Year Diffuse Neutrino Sensitivity 2022",
    }
    for key in datasets:
        print_dataset_metadata(datasets[key], tables[key], labels[key])
    return tables

def validate_comparison(tables):
    quantity = normalize_spectral_quantity(PLOT_QUANTITY)
    unit = common_unit(quantity)
    names = {
        "auger_cr": "Auger cosmic-ray spectrum",
        "ta": "Telescope Array",
        "fermi": "Fermi-LAT EGB",
        "icecube_2020": "IceCube 2020",
        "icecube_2022": "IceCube 2022",
        "glashow": "IceCube Glashow",
        "km3net": "KM3NeT KM3-230213A",
        "icecube_ehe": "IceCube EHE",
        "auger_nu": "Auger neutrino limit",
        "ara": "ARA",
        "anita": "ANITA",
        "rno_g": "RNO-G projected sensitivity",
        "pueo": "PUEO projected sensitivity",
        "icecube_gen2_radio": "IceCube-Gen2 Radio projected sensitivity",
        "grand200k": "GRAND200k projected sensitivity",
        "trinity": "Trinity projected sensitivity",
        "ret_n": "RET-N projected sensitivity",
    }
    for key, table in tables.items():
        require(table.meta["quantity"] == quantity, f"{names[key]} is represented as {quantity}")
        table[quantity].to(unit)
        require(True, f"{names[key]} is convertible to the common physical unit")
    require(np.count_nonzero(tables["ta"]["is_upper_limit"]) == 1, "Telescope Array contributes one upper limit")
    require(bool(tables["ta"]["is_upper_limit"][-1]), "Telescope Array upper limit is the final point")
    require(np.count_nonzero(tables["fermi"]["is_upper_limit"]) == 0, "Fermi-LAT EGB contributes no upper limits")
    require(tables["icecube_2020"].meta["flavor_convention"] == "all_flavor", "IceCube 2020 is converted to all flavor")
    require(tables["icecube_2022"].meta["flavor_convention"] == "all_flavor", "IceCube 2022 is converted to all flavor")
    require(tables["glashow"].meta["flavor_convention"] == "all_flavor", "Glashow is converted to all flavor")
    require(tables["km3net"].meta["flavor_convention"] == "all_flavor", "KM3NeT is converted to all flavor")
    for key in LIMIT_KEYS:
        table = tables[key]
        require(np.all(np.asarray(table["is_upper_limit"], dtype=bool)), f"{names[key]} contains only upper-limit values")
        require(np.isclose(table.meta["confidence_level"], 0.90), f"{names[key]} is represented at 90% CL")
        require(table.meta["flavor_convention"] == "all_flavor", f"{names[key]} is represented as all flavor")
        require(table.meta["limit_normalization_convention"] == "log10_energy_width", f"{names[key]} uses logarithmic decade-width normalization")
        require(np.isclose(table.meta["log10_energy_width_decades"], 1.0), f"{names[key]} is represented with a one-decade differential-limit normalization")
    require(tables["auger_nu"].meta.get("native_flavor_convention") == "per_flavor", "Auger retains single flavor as its native convention")
    require(tables["auger_nu"].meta.get("flavor_assumption") == "equal", "Auger all-flavor conversion records the equal-flavor assumption")
    require(tables["ara"].meta.get("native_flavor_convention") == "all_flavor", "ARA is native all flavor")
    require(tables["icecube_ehe"].meta.get("native_flavor_convention") == "all_flavor", "IceCube EHE is native all flavor")
    require(tables["anita"].meta.get("native_flavor_convention") == "all_flavor", "ANITA is native all flavor")
    require(tables["anita"].meta.get("native_quantity") == "Ephi", "ANITA retains Ephi as its native spectral quantity")
    require(tables["anita"].meta["quantity"] == "E2phi", "ANITA is explicitly converted from Ephi to E2phi for the comparison")
    require(np.isclose(tables["icecube_ehe"].meta["limit_normalization_scale_factor"], 1.0), "IceCube EHE is already decade-wide")
    require(tables["auger_nu"].meta["native_limit_normalization_convention"] == "log10_energy_width", "Auger native normalization is an explicit logarithmic energy width")
    require(np.isclose(tables["auger_nu"].meta["native_log10_energy_width_decades"], 0.5), "Auger native differential limit uses half-decade energy intervals")
    require(np.isclose(tables["auger_nu"].meta["limit_normalization_scale_factor"], 0.5), "Auger half-decade limit is rescaled by 0.5 to one decade")
    require(np.isclose(tables["ara"].meta["limit_normalization_scale_factor"], 1.0), "ARA five-station limit is already decade-wide")
    require(tables["anita"].meta["native_limit_normalization_convention"] == "anita_bandwidth", "ANITA retains its native bandwidth normalization provenance")
    require(np.isclose(tables["anita"].meta["native_limit_bandwidth_factor"], 4.0), "ANITA native bandwidth factor is Delta=4")
    require(np.isclose(tables["anita"].meta["limit_normalization_scale_factor"], 4.0 / np.log(10.0)), "ANITA bandwidth normalization is converted by 4/ln(10) to one decade")
    require(tables["rno_g"].meta["sensitivity_type"] == "projected_differential_upper_limit", "RNO-G is explicitly represented as a projected differential sensitivity")
    require(np.isclose(tables["rno_g"].meta["confidence_level"], 0.90), "RNO-G projected sensitivity is represented at 90% CL")
    require(tables["rno_g"].meta["flavor_convention"] == "all_flavor", "RNO-G projected sensitivity is native all flavor")
    require(tables["rno_g"].meta["figure24_mode"] == "approximate", "RNO-G retains the official Figure 24 approximate-mode provenance")
    require(np.isclose(tables["rno_g"].meta["figure24_effective_area_scale_factor"], 5.0), "RNO-G retains the official Figure 24 decade_factor=5 approximation")
    require(tables["pueo"].meta.get("native_sensitivity_type") == "single_event_sensitivity", "PUEO retains single-event sensitivity as its native statistical convention")
    require(tables["pueo"].meta["sensitivity_type"] == "projected_confidence_level_sensitivity", "PUEO is explicitly converted to a confidence-level projected sensitivity")
    require(np.isclose(tables["pueo"].meta["confidence_level"], 0.90), "PUEO is converted to 90% CL")
    require(tables["pueo"].meta["statistical_method"] == "feldman_cousins", "PUEO uses Feldman-Cousins statistics")
    require(np.isclose(tables["pueo"].meta["native_sensitivity_bandwidth_factor"], 4.0), "PUEO retains native Delta=4 bandwidth provenance")
    require(np.isclose(tables["pueo"].meta["log10_energy_width_decades"], 1.0), "PUEO is represented with one-decade normalization")
    require(np.isclose(tables["icecube_gen2_radio"].meta["confidence_level"], 0.90), "IceCube-Gen2 Radio is native 90% CL")
    require(tables["icecube_gen2_radio"].meta["flavor_convention"] == "all_flavor", "IceCube-Gen2 Radio is native all flavor")
    require(tables["icecube_gen2_radio"].meta["response_level"] == "trigger_level", "IceCube-Gen2 Radio sensitivity is trigger level")
    require(np.isclose(tables["icecube_gen2_radio"].meta["log10_energy_width_decades"], 1.0), "IceCube-Gen2 Radio uses native decade-wide bins")
    require(np.isclose(tables["icecube_gen2_radio"].meta["plot_point_spacing_decades"], 0.5), "IceCube-Gen2 Radio plotting points are half-decade spaced")
    require(np.isclose(tables["grand200k"].meta["confidence_level"], 0.90), "GRAND200k is native 90% CL")
    require(tables["grand200k"].meta["flavor_convention"] == "all_flavor", "GRAND200k is native all flavor")
    require(tables["grand200k"].meta["response_level"] == "trigger_level", "GRAND200k sensitivity is trigger level")
    require(tables["grand200k"].meta["statistical_method"] == "feldman_cousins", "GRAND200k uses Feldman-Cousins statistics")
    require(np.isclose(tables["grand200k"].meta["feldman_cousins_upper_count"], 2.44), "GRAND200k preserves the published FC upper count 2.44")
    require(np.isclose(tables["grand200k"].meta["log10_energy_width_decades"], 1.0), "GRAND200k uses native decade-wide normalization")
    require(np.isclose(tables["trinity"].meta["confidence_level"], 0.90), "Trinity is native 90% CL")
    require(tables["trinity"].meta["flavor_convention"] == "all_flavor", "Trinity is native all flavor")
    require(np.isclose(tables["trinity"].meta["duty_cycle"], 0.20), "Trinity preserves the published 20% duty cycle")
    require(np.isclose(tables["trinity"].meta["log10_energy_width_decades"], 1.0), "Trinity uses native decade-wide normalization")
    require(tables["trinity"].meta["statistical_method"] == "not_specified_in_source", "Trinity statistical method is not inferred beyond the published 90% CL")

    require(np.isclose(tables["ret_n"].meta["confidence_level"], 0.90), "RET-N is native 90% CL")
    require(tables["ret_n"].meta["flavor_convention"] == "all_flavor", "RET-N is native all flavor")
    require(np.isclose(tables["ret_n"].meta["projection_years"], 10.0), "RET-N preserves the ten-year projection")
    require(tables["ret_n"].meta["benchmark_stations"] == 10, "RET-N preserves the ten-station benchmark")
    require(np.isclose(tables["ret_n"].meta["transmitter_power_kw_per_station"], 100.0), "RET-N preserves the 100 kW transmitter power per station")
    require(tables["ret_n"].meta["response_level"] == "trigger_level", "RET-N sensitivity preserves its trigger-level design assumption")
    require(np.isclose(tables["ret_n"].meta["trigger_snr_db"], 0.0), "RET-N preserves the 0 dB trigger assumption")
    require(np.isclose(tables["ret_n"].meta["trigger_noise_bandwidth_mhz"], 50.0), "RET-N preserves the 50 MHz trigger-noise bandwidth")
    require(np.isclose(tables["ret_n"].meta["log10_energy_width_decades"], 1.0), "RET-N uses native decade-wide normalization")
    require(tables["ret_n"].meta["statistical_method"] == "not_specified_in_source", "RET-N statistical method is not inferred beyond the published 90% CL")

def plot_fermi(ax, table, quantity, unit):
    s = STYLE["fermi"]
    energy, xerr = bin_xerr(table)
    upper = np.asarray(table["is_upper_limit"], dtype=bool)
    measured = ~upper
    y = table[quantity].to_value(unit)
    y_lower = table[f"{quantity}_lower"].to_value(unit)
    y_upper = table[f"{quantity}_upper"].to_value(unit)
    handle = ax.errorbar(energy[measured], y[measured], xerr=xerr[:, measured], yerr=np.vstack((y[measured] - y_lower[measured], y_upper[measured] - y[measured])), fmt=s["marker"], linestyle="none", color=s["color"], markerfacecolor=s["mfc"], markeredgecolor=s["color"], markersize=s["ms"], markeredgewidth=1.3, elinewidth=1.2, capsize=2.5, label=r"Total EGB $\gamma$ (Fermi-LAT)", zorder=ZORDER_SPECTRA)
    if np.any(upper):
        plot_spectrum_upper_limits(ax, energy[upper], y[upper], xerr=xerr[:, upper], arrow_factor=2.5, color=s["color"], linewidth=1.5, capsize=3, mutation_scale=12)
    return handle

def plot_auger_cr(ax, table, quantity, unit):
    s = STYLE["auger_cr"]
    energy = table["energy"].to_value(u.GeV)
    y = table[quantity].to_value(unit)
    lower = table[f"{quantity}_stat_err_lower"].to_value(unit)
    upper = table[f"{quantity}_stat_err_upper"].to_value(unit)
    return ax.errorbar(energy, y, yerr=np.vstack((lower, upper)), fmt=s["marker"], linestyle="none", color=s["color"], markerfacecolor=s["mfc"], markeredgecolor=s["color"], markersize=s["ms"], markeredgewidth=1.3, elinewidth=1.2, capsize=2.5, label="Cosmic Rays (Auger)", zorder=ZORDER_SPECTRA)

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
    handle = ax.errorbar(energy[resolved], y[resolved], xerr=xerr[:, resolved], yerr=np.vstack((y[resolved] - y_lower[resolved], y_upper[resolved] - y[resolved])), fmt=s["marker"], linestyle="none", color=s["color"], markerfacecolor=s["mfc"], markeredgecolor=s["color"], markersize=s["ms"], markeredgewidth=1.3, elinewidth=1.2, capsize=2.5, label="Cosmic Rays (TA)", zorder=ZORDER_SPECTRA)
    ax.errorbar(energy[unresolved], y[unresolved], xerr=xerr[:, unresolved], fmt=s["marker"], linestyle="none", color=s["color"], markerfacecolor=s["mfc"], markeredgecolor=s["color"], markersize=s["ms"], markeredgewidth=1.3, elinewidth=1.2, capsize=2.5, zorder=ZORDER_SPECTRA)
    plot_spectrum_upper_limits(ax, energy[upper], y[upper], xerr=xerr[:, upper], arrow_factor=2.5, color=s["color"], linewidth=1.5, capsize=3, mutation_scale=12)
    return handle

def plot_icecube_spectrum(ax, table, quantity, unit, label="_nolegend_"):
    s = STYLE["icecube"]
    energy, xerr = bin_xerr(table)
    upper = np.asarray(table["is_upper_limit"], dtype=bool)
    measured = ~upper
    y = table[quantity].to_value(unit)
    y_lower = table[f"{quantity}_lower"].to_value(unit)
    y_upper = table[f"{quantity}_upper"].to_value(unit)
    handle = ax.errorbar(energy[measured], y[measured], xerr=xerr[:, measured], yerr=np.vstack((y[measured] - y_lower[measured], y_upper[measured] - y[measured])), fmt=s["marker"], linestyle="none", color=s["color"], markerfacecolor=s["mfc"], markeredgecolor=s["color"], markersize=s["ms"], markeredgewidth=1.3, elinewidth=1.3, capsize=2.5, label=label, zorder=ZORDER_SPECTRA + 2)
    plot_spectrum_upper_limits(ax, energy[upper], y_upper[upper], xerr=xerr[:, upper], arrow_factor=2.5, color=s["color"], linewidth=1.5, capsize=3, mutation_scale=12)
    return handle

def plot_km3net(ax, table, quantity, unit):
    s = STYLE["km3net"]
    energy, xerr = bin_xerr(table)
    y = table[quantity].to_value(unit)
    y_lower = table[f"{quantity}_lower"].to_value(unit)
    y_upper = table[f"{quantity}_upper"].to_value(unit)
    return ax.errorbar(energy, y, xerr=xerr, yerr=np.vstack((y - y_lower, y_upper - y)), fmt=s["marker"], linestyle="none", color=s["color"], markerfacecolor=s["mfc"], markeredgecolor=s["color"], markersize=s["ms"], markeredgewidth=1.6, elinewidth=1.5, capsize=3, label="KM3-230213A (KM3NeT)", zorder=ZORDER_EVENTS)

def plot_glashow(ax, table, quantity, unit):
    s = STYLE["glashow"]
    energy, xerr = bin_xerr(table)
    upper = np.asarray(table["is_upper_limit"], dtype=bool)
    measured = ~upper
    y = table[quantity].to_value(unit)
    y_lower = table[f"{quantity}_lower"].to_value(unit)
    y_upper = table[f"{quantity}_upper"].to_value(unit)
    handle = ax.errorbar(energy[measured], y[measured], xerr=xerr[:, measured], yerr=np.vstack((y[measured] - y_lower[measured], y_upper[measured] - y[measured])), fmt=s["marker"], linestyle="none", color=s["color"], markerfacecolor=s["mfc"], markeredgecolor=s["color"], markersize=s["ms"], markeredgewidth=1.5, elinewidth=1.5, capsize=3, label="Glashow (IceCube)", zorder=ZORDER_EVENTS)
    plot_spectrum_upper_limits(ax, energy[upper], y_upper[upper], xerr=xerr[:, upper], arrow_factor=2.5, color=s["color"], linewidth=1.5, capsize=3, mutation_scale=12)
    return handle

def plot_limit_curve(ax, table, quantity, unit, key):
    style = LIMIT_STYLE[key]
    return ax.plot(table["energy"].to_value(u.GeV), table[quantity].to_value(unit), color=style["color"], linestyle="-", linewidth=style["lw"], label=LIMIT_LABELS[key], zorder=ZORDER_LIMITS)[0]

def plot_sensitivity_curve(ax, table, quantity, unit, key):
    style = SENSITIVITY_STYLE[key]
    return ax.plot(table["energy"].to_value(u.GeV), table[quantity].to_value(unit), color=style["color"], linestyle=style["ls"], linewidth=style["lw"], label=SENSITIVITY_LABELS[key], zorder=ZORDER_SENSITIVITIES)[0]

def determine_axis_limits(tables, quantity, unit):
    all_x = []
    for table in tables.values():
        all_x.extend(table["energy"].to_value(u.GeV))
    xmin, xmax = np.nanmin(all_x), np.nanmax(all_x)
    if quantity == "E2phi":
        return xmin, xmax, 1e-11, 1e-5
    ymax = max(np.nanmax(tables[key][quantity].to_value(unit)) for key in LIMIT_KEYS)
    return xmin, xmax, 1e-11, ymax

def configure_log_x_ticks(ax):
    ax.xaxis.set_major_locator(LogLocator(base=10.0, subs=(1.0,), numticks=100))
    ax.xaxis.set_minor_locator(LogLocator(base=10.0, subs=np.arange(2, 10) * 0.1, numticks=1000))
    ax.xaxis.set_minor_formatter(NullFormatter())

def plot_comparison(tables):
    quantity = normalize_spectral_quantity(PLOT_QUANTITY)
    unit = common_unit(quantity)
    _, power = spectral_quantity_info(quantity)
    fig, ax = plt.subplots(figsize=(12, 6))
    ax.set_xscale("log")
    ax.set_yscale("log")
    xmin, xmax, ymin, ymax = determine_axis_limits(tables, quantity, unit)
    ax.set_xlim(xmin, xmax)
    ax.set_ylim(ymin, ymax)
    configure_log_x_ticks(ax)
    model_handles = plot_model_envelopes(ax, load_model_envelopes(quantity), quantity)
    sensitivity_handles = [plot_sensitivity_curve(ax, tables[key], quantity, unit, key) for key in SENSITIVITY_KEYS]
    limit_handles = [plot_limit_curve(ax, tables[key], quantity, unit, key) for key in LIMIT_KEYS]
    h_fermi = plot_fermi(ax, tables["fermi"], quantity, unit)
    h_auger_cr = plot_auger_cr(ax, tables["auger_cr"], quantity, unit)
    h_ta = plot_ta(ax, tables["ta"], quantity, unit)
    h_ic = plot_icecube_spectrum(ax, tables["icecube_2020"], quantity, unit, r"Astrophysical $\nu$ (IceCube)")
    plot_icecube_spectrum(ax, tables["icecube_2022"], quantity, unit)
    h_km3net = plot_km3net(ax, tables["km3net"], quantity, unit)
    h_glashow = plot_glashow(ax, tables["glashow"], quantity, unit)
    ax.set_xlabel(r"Particle energy, $E$ [GeV]", fontweight="bold")
    ax.set_ylabel(rf"Differential intensity, {quantity_label(quantity)} [{UNIT_LABELS[power]}]", fontweight="bold")
    ax.set_title("Multimessenger Diffuse Flux Landscape", fontweight="bold")
    ax.grid(True, which="major", alpha=0.25)
    ax.grid(True, which="minor", alpha=0.15)
    ax.text(0.985, 0.005, NEUTRINO_TEXT, transform=ax.transAxes, ha="right", va="bottom", fontweight="bold", fontsize=LEGEND_FONTSIZE)
    observation_handles = [h_fermi, h_auger_cr, h_ta, h_ic, h_km3net, h_glashow]
    observation_legend = ax.legend(handles=observation_handles, loc="upper left", ncol=3, frameon=True, fontsize=LEGEND_FONTSIZE, title_fontsize=LEGEND_TITLE_FONTSIZE)
    bold_legend(observation_legend)
    ax.add_artist(observation_legend)
    limit_legend = ax.legend(handles=limit_handles, title="Current 90% CL upper limits", loc="lower left", ncol=4, frameon=True, fontsize=LEGEND_FONTSIZE, title_fontsize=LEGEND_TITLE_FONTSIZE)
    limit_legend.get_title().set_fontweight("bold")
    bold_legend(limit_legend)
    ax.add_artist(limit_legend)
    sensitivity_legend = ax.legend(handles=sensitivity_handles, title="Projected 90% CL sensitivities", loc="center left", bbox_to_anchor=(0.01, 0.28), ncol=2, frameon=True, fontsize=LEGEND_FONTSIZE, title_fontsize=LEGEND_TITLE_FONTSIZE)
    sensitivity_legend.get_title().set_fontweight("bold")
    bold_legend(sensitivity_legend)
    ax.add_artist(sensitivity_legend)
    model_legend = ax.legend(handles=model_handles, title="Model envelopes", loc="center left", bbox_to_anchor=(0.01, 0.50), ncol=1, frameon=True, fontsize=LEGEND_FONTSIZE, title_fontsize=LEGEND_TITLE_FONTSIZE)
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
