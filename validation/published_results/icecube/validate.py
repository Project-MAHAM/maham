from pathlib import Path

import astropy.units as u
import matplotlib.pyplot as plt
import numpy as np

from maham.datasets import get_dataset
from maham.plotting import apply_plot_style, bold_legend, bold_tick_labels, validation_curve_style, plot_upper_limits


apply_plot_style()

OUTPUT_DIR = Path(__file__).parent / "outputs"
E2PHI_UNIT = u.GeV / (u.cm**2 * u.s * u.sr)
E2PHI_POINT_SOURCE_UNIT = u.GeV / (u.cm**2 * u.s)


def require(condition, message):
    if not condition:
        print(f"[FAIL] {message}")
        raise AssertionError(message)
    print(f"[PASS] {message}")


def validate_ehe(limit, sensitivity):
    require(len(limit) == 10, "EHE differential limit contains 10 published points")
    require(len(sensitivity) == 10, "EHE sensitivity contains 10 published points")
    require(u.allclose(limit["energy"], sensitivity["energy"]), "EHE limit and sensitivity energy grids agree")
    require(np.all(limit["is_upper_limit"]), "All EHE differential-limit points are marked as upper limits")
    require(limit.meta["flavor_convention"] == "all_flavor", "EHE differential limit is all-flavor")
    require(sensitivity.meta["flavor_convention"] == "all_flavor", "EHE sensitivity is all-flavor")
    require(np.isclose(limit.meta["confidence_level"], 0.90), "EHE differential limit confidence level is 90%")
    require(limit.meta["limit_normalization_convention"] == "log10_energy_width", "EHE differential-limit normalization is represented as a logarithmic energy width")
    require(np.isclose(limit.meta["log10_energy_width_decades"], 1.0), "EHE differential limit is decade-wide")
    require(np.isclose(sensitivity.meta["confidence_level"], 0.90), "EHE sensitivity confidence level is 90%")
    require(u.allclose(limit["energy"][3], 1e8 * u.GeV), "Published EHE 1e8 GeV reference energy is reproduced")
    require(u.allclose(limit["E2phi"][3], 5.743e-9 * E2PHI_UNIT), "Published EHE 1e8 GeV differential limit is reproduced")
    require(u.allclose(sensitivity["E2phi"][3], 5.142e-9 * E2PHI_UNIT), "Published EHE 1e8 GeV sensitivity is reproduced")


def validate_glashow(glashow, glashow_all):
    require(len(glashow) == 3, "Glashow spectrum contains 3 published energy bins")
    require(glashow.meta["flavor_convention"] == "per_flavor", "Glashow native flux is per-flavor")
    require(np.isclose(glashow.meta["confidence_level"], 0.683), "Glashow confidence level is 68.3%")
    require(glashow["is_upper_limit"].tolist() == [True, False, True], "Glashow upper-limit bins are correctly identified")
    require(u.allclose(glashow["E2phi"][1], 1.9e-9 * E2PHI_UNIT), "Published Glashow middle-bin E2phi is reproduced")
    require(u.allclose(glashow["E2phi_lower"][1], 8e-10 * E2PHI_UNIT), "Published Glashow middle-bin lower bound is reproduced")
    require(u.allclose(glashow["E2phi_upper"][1], 1.13e-8 * E2PHI_UNIT), "Published Glashow middle-bin upper bound is reproduced")
    require(glashow_all.meta["flavor_convention"] == "all_flavor", "Glashow all-flavor view is explicitly constructed")
    require(glashow_all.meta["flavor_assumption"] == "equal", "Glashow all-flavor view records the equal-flavor assumption")
    require(u.allclose(glashow_all["E2phi"][1], 5.7e-9 * E2PHI_UNIT), "Glashow equal-flavor all-flavor conversion is reproduced")


def validate_170922a(event):
    require(len(event) == 1, "IceCube-170922A dataset contains one event")
    require(event.meta["dataset_id"] == "icecube.170922a.2017", "IceCube-170922A dataset ID is correct")
    require(event["event_name"][0] == "IceCube-170922A", "IceCube-170922A event name is reproduced")
    require(event["instrument"][0] == "IceCube", "IceCube-170922A instrument is IceCube")
    require(event["topology"][0] == "track", "IceCube-170922A topology is track-like")
    require(event["selection"][0] == "EHE", "IceCube-170922A belongs to the EHE alert selection")
    require(u.allclose(event["ra"][0], 77.43 * u.deg), "Published IceCube-170922A right ascension is reproduced")
    require(u.allclose(event["dec"][0], 5.72 * u.deg), "Published IceCube-170922A declination is reproduced")
    require(u.allclose(event["energy"][0], 290.0 * u.TeV), "Published most-probable parent-neutrino energy is reproduced")
    require(u.allclose(event["energy_lower"][0], 183.0 * u.TeV), "Published 90% neutrino-energy lower bound is reproduced")
    require(u.allclose(event["energy_upper"][0], 4.3 * u.PeV), "Published 90% neutrino-energy upper bound is reproduced")
    require(u.allclose(event["deposited_muon_energy"][0], 23.7 * u.TeV), "Published deposited muon energy is reproduced")
    require(np.isclose(event["signalness"][0], 0.565), "Published IceCube-170922A signalness is reproduced")
    require(event["associated_source"][0] == "TXS 0506+056", "TXS 0506+056 association is retained")
    require(event.meta["energy_spectral_assumption"] == "E^-2.13", "Parent-neutrino energy assumption is explicitly retained")


def validate_combined(combined):
    require(len(combined) == 9, "Combined astrophysical spectrum contains 9 published energy bins")
    require(combined.meta["flavor_convention"] == "all_flavor", "Combined astrophysical spectrum is all-flavor")
    require(np.isclose(combined.meta["confidence_level"], 0.6827), "Combined default confidence level is 68.27%")
    require(combined.meta["interval_method"] == "profile_likelihood", "Combined intervals use released profile likelihoods")
    require(u.allclose(combined["energy_min"][0], 1e4 * u.GeV), "Combined spectrum begins at 1e4 GeV")
    require(u.allclose(combined["energy_max"][-1], 1e7 * u.GeV), "Combined spectrum ends at 1e7 GeV")
    require(np.array_equal(np.flatnonzero(combined["is_upper_limit"]), [5, 7, 8]), "Combined zero-best-fit bins 6, 8, and 9 are identified as upper limits")

    scale = 1e-8 * E2PHI_UNIT
    bestfit = np.array([9.31407260358, 22.5643864183, 5.63201177622, 3.20115983712, 4.25417119386, 0.0, 6.85816864131, 0.0, 0.0])
    lower68 = np.array([1.7, 17.0, 2.4, 0.8, 2.0, 0.0, 4.5, 0.0, 0.0])
    upper68 = np.array([17.3, 28.5, 9.2, 5.9, 7.0, 1.5, 9.7, 1.5, 0.6])
    lower90 = np.array([0.0, 13.5, 0.5, 0.0, 0.8, 0.0, 3.1, 0.0, 0.0])
    upper90 = np.array([22.7, 32.5, 11.6, 7.9, 9.0, 3.5, 11.9, 3.8, 1.5])

    require(u.allclose(combined["E2phi"], bestfit * scale), "All 9 released combined-spectrum best-fit values are reproduced")
    require(np.allclose(np.round(combined["E2phi_lower"].to_value(scale.unit) / 1e-8, 1), lower68), "Published 68% profile-likelihood lower bounds are reproduced")
    require(np.allclose(np.round(combined["E2phi_upper"].to_value(scale.unit) / 1e-8, 1), upper68), "Published 68% profile-likelihood upper bounds are reproduced")
    require(np.allclose(np.round(combined["E2phi_90_lower"].to_value(scale.unit) / 1e-8, 1), lower90), "Published 90% profile-likelihood lower bounds are reproduced")
    require(np.allclose(np.round(combined["E2phi_90_upper"].to_value(scale.unit) / 1e-8, 1), upper90), "Published 90% profile-likelihood upper bounds are reproduced")



def validate_cascade_2020(cascade, cascade_all):
    require(len(cascade) == 13, "Six-year cascade spectrum contains 13 digitized Figure 3 bins")
    require(cascade.meta["flavor_convention"] == "per_flavor", "Cascade native flux is per-flavor")
    require(np.isclose(cascade.meta["confidence_level"], 0.68), "Cascade confidence level is 68% simultaneous coverage")
    require(cascade.meta["interval_method"] == "digitized_68_percent_simultaneous_coverage", "Cascade interval provenance is explicit")
    require(np.allclose(cascade.meta["sensitive_energy_range_GeV"], [1.6e4, 2.6e6]), "Published 16 TeV to 2.6 PeV sensitive range is retained")
    upper = np.asarray(cascade["is_upper_limit"], dtype=bool)
    require(np.array_equal(np.flatnonzero(upper), [5, 8, 9, 10, 11, 12]), "Cascade Figure 3 upper-limit bins are correctly identified")
    require(u.allclose(cascade["E2phi"][2], 4.42099e-8 * E2PHI_UNIT), "Digitized 31.6 TeV cascade best-fit point is reproduced")
    require(u.allclose(cascade["E2phi_upper"][5], 1.72801e-9 * E2PHI_UNIT), "Digitized first cascade upper limit is reproduced")
    require(cascade_all.meta["flavor_convention"] == "all_flavor", "Cascade all-flavor view is explicitly constructed")
    require(cascade_all.meta["flavor_assumption"] == "equal", "Cascade all-flavor view records the equal-flavor assumption")
    require(u.allclose(cascade_all["E2phi"], 3 * cascade["E2phi"]), "Cascade equal-flavor all-flavor conversion is reproduced")


def validate_throughgoing_muon(piecewise, piecewise_all):
    require(len(piecewise) == 5, "9.5-year through-going muon spectrum contains 5 published pieces")
    require(piecewise.meta["flavor_convention"] == "numu_nubar", "Native through-going muon flux is nu_mu + nubar_mu")
    require(piecewise.meta["confidence_level"] is None, "Mixed confidence levels are represented per row")
    require(np.allclose(piecewise["confidence_level"], [0.90, 0.6827, 0.6827, 0.6827, 0.90]), "Published mixed confidence levels are reproduced")
    require(piecewise["is_upper_limit"].tolist() == [True, False, False, False, True], "Pieces 1 and 5 are identified as 90% upper limits")

    scale = 1e-8 * E2PHI_UNIT
    require(u.allclose(piecewise["E2phi"], np.array([0.0, 2.22, 1.21, 0.33, 0.0]) * scale), "Published piece-wise best-fit normalizations are reproduced")
    require(u.allclose(piecewise["E2phi_lower"], np.array([0.0, 1.42, 0.90, 0.15, 0.0]) * scale), "Published piece-wise lower bounds are reproduced")
    require(u.allclose(piecewise["E2phi_upper"], np.array([3.10, 3.02, 1.53, 0.55, 0.41]) * scale), "Published piece-wise upper bounds are reproduced")
    require(u.allclose(piecewise["energy_min"], [100, 15000, 104000, 721000, 5000000] * u.GeV), "Published piece-wise lower energy edges are reproduced")
    require(u.allclose(piecewise["energy_max"], [15000, 104000, 721000, 5000000, 100000000] * u.GeV), "Published piece-wise upper energy edges are reproduced")
    require(piecewise_all.meta["flavor_convention"] == "all_flavor", "Equal-flavor all-flavor view is explicitly constructed")
    require(piecewise_all.meta["flavor_assumption"] == "equal", "All-flavor view records the equal-flavor assumption")
    require(u.allclose(piecewise_all["E2phi"], 3 * piecewise["E2phi"]), "Equal-flavor all-flavor conversion is reproduced")


def validate_ngc1068(ngc):
    require(len(ngc) == 64, "NGC 1068 spectrum contains 64 generated best-fit points")
    require(ngc.meta["quantity"] == "E2phi", "NGC 1068 validation uses E2phi")
    require(ngc.meta["flavor_convention"] == "numu_nubar", "NGC 1068 native flux is nu_mu + nubar_mu")
    require(ngc.meta["solid_angle_convention"] == "point_source", "NGC 1068 is represented as a point-source flux")
    require(ngc.meta["spectral_model"] == "unbroken_power_law", "NGC 1068 spectral model is an unbroken power law")
    require(np.isclose(ngc.meta["phi0_TeV_inv_cm2_s"], 5.0e-11), "Published NGC 1068 normalization is reproduced")
    require(np.isclose(ngc.meta["spectral_index"], 3.2), "Published NGC 1068 spectral index is reproduced")
    require(np.isclose(ngc.meta["energy_min_TeV"], 1.5), "NGC 1068 characteristic energy range begins at 1.5 TeV")
    require(np.isclose(ngc.meta["energy_max_TeV"], 15.0), "NGC 1068 characteristic energy range ends at 15 TeV")
    require(ngc.meta["signal_events"] == 79, "Published NGC 1068 best-fit signal count is reproduced")
    require(ngc.meta["signal_events_lower"] == 59, "Published NGC 1068 lower signal-count bound is reproduced")
    require(ngc.meta["signal_events_upper"] == 101, "Published NGC 1068 upper signal-count bound is reproduced")
    require(np.isclose(ngc.meta["global_significance_sigma"], 4.2), "Published NGC 1068 global significance is reproduced")
    require(np.all(np.diff(ngc["energy"].to_value(u.GeV)) > 0), "NGC 1068 energy grid is strictly increasing")
    require(np.all(ngc["E2phi"].to_value(E2PHI_POINT_SOURCE_UNIT) > 0), "NGC 1068 E2phi values are positive")

    energy = ngc["energy"]
    phi0 = ngc.meta["phi0_TeV_inv_cm2_s"] / (u.TeV * u.cm**2 * u.s)
    gamma = ngc.meta["spectral_index"]
    expected = (phi0 * (energy / (1.0 * u.TeV)) ** (-gamma) * energy**2).to(E2PHI_POINT_SOURCE_UNIT)
    require(u.allclose(ngc["E2phi"], expected, rtol=1e-12), "NGC 1068 E2phi curve reproduces the published best-fit power law")


def validate_txs0506(txs):
    require(len(txs) == 64, "TXS 0506+056 flare spectrum contains 64 generated best-fit points")
    require(txs.meta["quantity"] == "E2phi", "TXS 0506+056 validation uses E2phi")
    require(txs.meta["flavor_convention"] == "numu_nubar", "TXS 0506+056 native flux is nu_mu + nubar_mu")
    require(txs.meta["solid_angle_convention"] == "point_source", "TXS 0506+056 is represented as a point-source flux")
    require(txs.meta["spectral_model"] == "unbroken_power_law", "TXS 0506+056 spectral model is an unbroken power law")
    require(np.isclose(txs.meta["phi100_TeV_inv_cm2_s"], 1.6e-15), "Published TXS normalization is reproduced")
    require(np.isclose(txs.meta["phi100_lower_TeV_inv_cm2_s"], 1.0e-15), "Published TXS lower normalization bound is reproduced")
    require(np.isclose(txs.meta["phi100_upper_TeV_inv_cm2_s"], 2.3e-15), "Published TXS upper normalization bound is reproduced")
    require(np.isclose(txs.meta["spectral_index"], 2.2), "Published TXS spectral index is reproduced")
    require(np.isclose(txs.meta["spectral_index_err"], 0.2), "Published TXS spectral-index uncertainty is reproduced")
    require(np.isclose(txs.meta["window_start_mjd"], 56937.81), "Published TXS flare start MJD is reproduced")
    require(np.isclose(txs.meta["window_end_mjd"], 57096.21), "Published TXS flare end MJD is reproduced")
    require(np.isclose(txs.meta["window_duration_days"], 158.0), "Published TXS flare duration is reproduced")
    require(txs.meta["signal_events"] == 13, "Published TXS signal-event count is reproduced")
    require(txs.meta["signal_events_err"] == 5, "Published TXS signal-event uncertainty is reproduced")
    require(np.isclose(txs.meta["global_significance_sigma"], 3.5), "Published TXS global significance is reproduced")
    require(np.all(np.diff(txs["energy"].to_value(u.GeV)) > 0), "TXS energy grid is strictly increasing")
    require(np.all(txs["E2phi"].to_value(E2PHI_POINT_SOURCE_UNIT) > 0), "TXS E2phi values are positive")

    energy = txs["energy"]
    phi100 = txs.meta["phi100_TeV_inv_cm2_s"] / (u.TeV * u.cm**2 * u.s)
    gamma = txs.meta["spectral_index"]
    expected = (phi100 * (energy / (100.0 * u.TeV)) ** (-gamma) * energy**2).to(E2PHI_POINT_SOURCE_UNIT)
    require(u.allclose(txs["E2phi"], expected, rtol=1e-12), "TXS E2phi curve reproduces the published best-fit power law")

    fluence = ((100.0 * u.TeV) ** 2 * phi100 * (txs.meta["window_duration_days"] * u.day)).to(u.TeV / u.cm**2)
    require(np.isclose(fluence.value, 2.18e-4, rtol=0.02), "TXS average flux reproduces the published box-window fluence")


def validate_effective_area(area):
    require(len(area) == 100, "Effective area contains 100 published points")
    energy = area["energy"].to_value(u.GeV)
    require(np.all(np.diff(energy) > 0), "Effective-area energy grid is strictly increasing")

    flavor_sum = area["effective_area_nue"] + area["effective_area_numu"] + area["effective_area_nutau"]
    relative_difference = np.abs(((area["effective_area_total"] - flavor_sum) / area["effective_area_total"]).to_value(u.dimensionless_unscaled))
    max_relative_difference = float(np.max(relative_difference))
    require(max_relative_difference < 0.01, "Total effective area agrees with flavor sum within 1% published precision")
    require(u.allclose(area["energy"][15], 5.97e6 * u.GeV), "Published 5.97 PeV effective-area reference energy is reproduced")
    require(u.allclose(area["effective_area_total"][15], 512.0 * u.m**2), "Published 5.97 PeV total effective area is reproduced")

    window = (energy >= 5e6) & (energy <= 8e6)
    window_indices = np.where(window)[0]
    peak_index = window_indices[np.argmax(area["effective_area_nue"][window])]
    peak_energy = area["energy"][peak_index]
    peak_area = area["effective_area_nue"][peak_index]

    require(5.5e6 * u.GeV < peak_energy < 6.5e6 * u.GeV, "Local nue effective-area enhancement occurs near the Glashow-resonance energy")
    require(u.allclose(peak_energy, 5.97e6 * u.GeV), "Published nue Glashow-region peak energy is reproduced")
    require(u.allclose(peak_area, 471.0 * u.m**2), "Published nue Glashow-region effective-area peak is reproduced")

    print(f"       Maximum total-vs-flavor-sum difference: {100 * max_relative_difference:.3f}%")
    print(f"       Local nue effective-area peak: {peak_energy.to_value(u.PeV):.3f} PeV, {peak_area.to_value(u.m**2):.1f} m2")


def plot_flux_results(limit, sensitivity, glashow):
    fig, ax = plt.subplots(figsize=(7, 5))
    ax.set_xlim(2e6, 2e11)
    ax.set_ylim(1e-9, 1.2e-6)

    ax.loglog(limit["energy"].to_value(u.GeV), limit["E2phi"].to_value(E2PHI_UNIT), marker="o", markerfacecolor="white", markeredgecolor="black", markeredgewidth=1.5, markersize=6, label="EHE upper limit", **validation_curve_style("upper_limit"))
    ax.loglog(sensitivity["energy"].to_value(u.GeV), sensitivity["E2phi"].to_value(E2PHI_UNIT), marker="s", markerfacecolor="white", markeredgecolor="black", markeredgewidth=1.5, markersize=5.5, label="EHE sensitivity", **validation_curve_style("sensitivity"))

    energy = glashow["energy"].to_value(u.GeV)
    energy_min = glashow["energy_min"].to_value(u.GeV)
    energy_max = glashow["energy_max"].to_value(u.GeV)
    xerr = np.vstack((energy - energy_min, energy_max - energy))
    upper = np.asarray(glashow["is_upper_limit"], dtype=bool)
    measured = ~upper
    y = glashow["E2phi"].to_value(E2PHI_UNIT)
    y_lower = glashow["E2phi_lower"].to_value(E2PHI_UNIT)
    y_upper = glashow["E2phi_upper"].to_value(E2PHI_UNIT)
    yerr = np.vstack((y[measured] - y_lower[measured], y_upper[measured] - y[measured]))

    ax.errorbar(energy[measured], y[measured], xerr=xerr[:, measured], yerr=yerr, fmt="*", markersize=10, capsize=3, elinewidth=1.5, markeredgecolor="black", ecolor="black", markerfacecolor="white", markeredgewidth=1.5, linestyle="none", label="Glashow")
    plot_upper_limits(ax, energy[upper], y_upper[upper], xerr=xerr[:, upper], arrow_factor=2.5, color="black", linewidth=1.5, capsize=3, mutation_scale=12)

    ax.set_xlabel(r"Neutrino energy, $E_{\nu}$ [GeV]")
    ax.set_ylabel(r"Flux, $E^{2}\Phi$ [GeV cm$^{-2}$ s$^{-1}$ sr$^{-1}$]")
    ax.set_title("IceCube EHE Upper Limit and Sensitivity (2025)")
    ax.grid(True, which="both", alpha=0.25)
    ax.text(0.97, 0.02, r"All flavors" "\n" r"90% CL" "\n" r"$\nu_e:\nu_\mu:\nu_\tau=1:1:1$, $\nu:\bar{\nu}=1:1$", transform=ax.transAxes, ha="right", va="bottom", fontweight="bold")

    bold_tick_labels(ax)
    bold_legend(ax.legend(loc="upper right"))
    fig.tight_layout()
    fig.savefig(OUTPUT_DIR / "icecube_flux_results.png", dpi=200)
    fig.savefig(OUTPUT_DIR / "icecube_flux_results.pdf")
    plt.close(fig)


def plot_combined_spectrum(combined):
    energy = combined["energy"].to_value(u.GeV)
    energy_min = combined["energy_min"].to_value(u.GeV)
    energy_max = combined["energy_max"].to_value(u.GeV)
    xerr = np.vstack((energy - energy_min, energy_max - energy))
    upper = np.asarray(combined["is_upper_limit"], dtype=bool)
    measured = ~upper
    y = combined["E2phi"].to_value(E2PHI_UNIT)
    y_lower = combined["E2phi_lower"].to_value(E2PHI_UNIT)
    y_upper = combined["E2phi_upper"].to_value(E2PHI_UNIT)
    yerr = np.vstack((y[measured] - y_lower[measured], y_upper[measured] - y[measured]))

    fig, ax = plt.subplots(figsize=(7, 5))
    ax.set_xlim(8e3, 1.2e7)
    ax.set_ylim(1.5e-9, 5e-7)

    ax.errorbar(energy[measured], y[measured], xerr=xerr[:, measured], yerr=yerr, fmt="o", markersize=7, capsize=3, elinewidth=1.5, markeredgecolor="black", ecolor="black", markerfacecolor="white", markeredgewidth=1.5, linestyle="none", label="Combined spectrum")
    plot_upper_limits(ax, energy[upper], y_upper[upper], xerr=xerr[:, upper], arrow_factor=2.5, color="black", linewidth=1.5, capsize=3, mutation_scale=12)

    ax.set_xscale("log")
    ax.set_yscale("log")
    ax.set_xlabel(r"Neutrino energy, $E_{\nu}$ [GeV]")
    ax.set_ylabel(r"Flux, $E^{2}\Phi$ [GeV cm$^{-2}$ s$^{-1}$ sr$^{-1}$]")
    ax.set_title("IceCube Combined Astrophysical Spectrum (2015)")
    ax.grid(True, which="both", alpha=0.25)
    ax.text(0.97, 0.03, r"All flavors" "\n" r"68% profile intervals", transform=ax.transAxes, ha="right", va="bottom", fontweight="bold")

    bold_tick_labels(ax)
    bold_legend(ax.legend(loc="upper right"))
    fig.tight_layout()
    fig.savefig(OUTPUT_DIR / "icecube_combined_2015_spectrum.png", dpi=200)
    fig.savefig(OUTPUT_DIR / "icecube_combined_2015_spectrum.pdf")
    plt.close(fig)



def plot_cascade_2020(cascade):
    energy = cascade["energy"].to_value(u.GeV)
    energy_min = cascade["energy_min"].to_value(u.GeV)
    energy_max = cascade["energy_max"].to_value(u.GeV)
    xerr = np.vstack((energy - energy_min, energy_max - energy))
    upper = np.asarray(cascade["is_upper_limit"], dtype=bool)
    measured = ~upper
    y = cascade["E2phi"].to_value(E2PHI_UNIT)
    y_lower = cascade["E2phi_lower"].to_value(E2PHI_UNIT)
    y_upper = cascade["E2phi_upper"].to_value(E2PHI_UNIT)
    yerr = np.vstack((y[measured] - y_lower[measured], y_upper[measured] - y[measured]))

    fig, ax = plt.subplots(figsize=(7, 5))
    ax.set_xlim(3e3, 1.2e8)
    ax.set_ylim(3e-10, 1.2e-7)
    ax.errorbar(energy[measured], y[measured], xerr=xerr[:, measured], yerr=yerr, fmt="o", markersize=7, capsize=3, elinewidth=1.5, markeredgecolor="black", ecolor="black", markerfacecolor="white", markeredgewidth=1.5, linestyle="none", label="Differential flux")
    plot_upper_limits(ax, energy[upper], y_upper[upper], xerr=xerr[:, upper], arrow_factor=2.5, color="black", linewidth=1.5, capsize=3, mutation_scale=12)
    ax.set_xscale("log")
    ax.set_yscale("log")
    ax.set_xlabel(r"Neutrino energy, $E_{\nu}$ [GeV]")
    ax.set_ylabel(r"Flux, $E^{2}\Phi$ [GeV cm$^{-2}$ s$^{-1}$ sr$^{-1}$]")
    ax.set_title("IceCube Six-Year Cascade Differential Flux (2020)")
    ax.grid(True, which="both", alpha=0.25)
    ax.text(0.97, 0.03, "Per flavor" "\n" "68% simultaneous coverage" "\n" "Sensitive range: 16 TeV-2.6 PeV", transform=ax.transAxes, ha="right", va="bottom", fontweight="bold")
    bold_tick_labels(ax)
    bold_legend(ax.legend(loc="upper right"))
    fig.tight_layout()
    fig.savefig(OUTPUT_DIR / "icecube_cascade_2020_piecewise.png", dpi=200)
    fig.savefig(OUTPUT_DIR / "icecube_cascade_2020_piecewise.pdf")
    plt.close(fig)


def plot_throughgoing_muon(piecewise):
    energy = piecewise["energy"].to_value(u.GeV)
    energy_min = piecewise["energy_min"].to_value(u.GeV)
    energy_max = piecewise["energy_max"].to_value(u.GeV)
    xerr = np.vstack((energy - energy_min, energy_max - energy))
    upper = np.asarray(piecewise["is_upper_limit"], dtype=bool)
    measured = ~upper
    y = piecewise["E2phi"].to_value(E2PHI_UNIT)
    y_lower = piecewise["E2phi_lower"].to_value(E2PHI_UNIT)
    y_upper = piecewise["E2phi_upper"].to_value(E2PHI_UNIT)
    yerr = np.vstack((y[measured] - y_lower[measured], y_upper[measured] - y[measured]))

    fig, ax = plt.subplots(figsize=(7, 5))
    ax.set_xlim(7e1, 1.4e8)
    ax.set_ylim(8e-10, 8e-8)

    ax.errorbar(energy[measured], y[measured], xerr=xerr[:, measured], yerr=yerr, fmt="o", markersize=7, capsize=3, elinewidth=1.5, markeredgecolor="black", ecolor="black", markerfacecolor="white", markeredgewidth=1.5, linestyle="none", label="Piece-wise flux")
    plot_upper_limits(ax, energy[upper], y_upper[upper], xerr=xerr[:, upper], arrow_factor=2.5, color="black", linewidth=1.5, capsize=3, mutation_scale=12)

    ax.set_xscale("log")
    ax.set_yscale("log")
    ax.set_xlabel(r"Neutrino energy, $E_{\nu}$ [GeV]")
    ax.set_ylabel(r"Flux, $E^{2}\Phi$ [GeV cm$^{-2}$ s$^{-1}$ sr$^{-1}$]")
    ax.set_title("IceCube 9.5-Year Through-Going Muon Flux")
    ax.grid(True, which="both", alpha=0.25)
    ax.text(0.97, 0.03, r"$\nu_\mu+\bar{\nu}_\mu$" "\n" r"68.27% measurements, 90% limits", transform=ax.transAxes, ha="right", va="bottom", fontweight="bold")

    bold_tick_labels(ax)
    bold_legend(ax.legend(loc="upper right"))
    fig.tight_layout()
    fig.savefig(OUTPUT_DIR / "icecube_throughgoing_muon_2022_piecewise.png", dpi=200)
    fig.savefig(OUTPUT_DIR / "icecube_throughgoing_muon_2022_piecewise.pdf")
    plt.close(fig)


def plot_ngc1068(ngc):
    energy = ngc["energy"].to_value(u.GeV)
    y = ngc["E2phi"].to_value(E2PHI_POINT_SOURCE_UNIT)

    fig, ax = plt.subplots(figsize=(7, 5))
    ax.loglog(energy, y, color="black", linewidth=2.2, label="NGC 1068 (steady)")
    ax.set_xlabel(r"Neutrino energy, $E_{\nu}$ [GeV]")
    ax.set_ylabel(r"Flux, $E^{2}\Phi$ [GeV cm$^{-2}$ s$^{-1}$]")
    ax.set_title("IceCube NGC 1068 Point-Source Flux")
    ax.grid(True, which="both", alpha=0.25)
    ax.text(0.04, 0.05, r"$\Phi_0=5.0\times10^{-11}$ TeV$^{-1}$ cm$^{-2}$ s$^{-1}$" "\n" r"$\gamma=3.2$" "\n" r"$E_0=1$ TeV" "\n" r"79$_{-20}^{+22}$ signal events, 4.2$\sigma$", transform=ax.transAxes, fontweight="bold")

    bold_tick_labels(ax)
    bold_legend(ax.legend(loc="upper right"))
    fig.tight_layout()
    fig.savefig(OUTPUT_DIR / "icecube_ngc1068_flux_2022.png", dpi=200)
    fig.savefig(OUTPUT_DIR / "icecube_ngc1068_flux_2022.pdf")
    plt.close(fig)


def plot_txs0506(txs):
    energy = txs["energy"].to_value(u.GeV)
    y = txs["E2phi"].to_value(E2PHI_POINT_SOURCE_UNIT)

    fig, ax = plt.subplots(figsize=(7, 5))
    ax.loglog(energy, y, color="black", linewidth=2.2, label="TXS 0506+056 (158-day flare)")
    ax.set_xlabel(r"Neutrino energy, $E_{\nu}$ [GeV]")
    ax.set_ylabel(r"Flux, $E^{2}\Phi$ [GeV cm$^{-2}$ s$^{-1}$]")
    ax.set_title("IceCube TXS 0506+056 2014-2015 Flare Flux")
    ax.grid(True, which="both", alpha=0.25)
    ax.text(0.04, 0.05, "158-day box flare" "\n" r"$\Phi_{100}=1.6\times10^{-15}$ TeV$^{-1}$ cm$^{-2}$ s$^{-1}$" "\n" r"$\gamma=2.2$" "\n" r"13$\pm5$ signal events, 3.5$\sigma$", transform=ax.transAxes, fontweight="bold")

    bold_tick_labels(ax)
    bold_legend(ax.legend(loc="upper right"))
    fig.tight_layout()
    fig.savefig(OUTPUT_DIR / "icecube_txs0506_flare_2018.png", dpi=200)
    fig.savefig(OUTPUT_DIR / "icecube_txs0506_flare_2018.pdf")
    plt.close(fig)


def plot_effective_area(area):
    energy = area["energy"].to_value(u.GeV)

    fig, ax = plt.subplots(figsize=(7, 5))
    ax.set_xlim(8e5, 2e11)
    ax.loglog(energy, area["effective_area_total"].to_value(u.km**2), label="Total", linewidth=2)
    ax.loglog(energy, area["effective_area_nue"].to_value(u.km**2), label=r"$(\nu_e+\bar{\nu}_e)/2$")
    ax.loglog(energy, area["effective_area_numu"].to_value(u.km**2), label=r"$(\nu_\mu+\bar{\nu}_\mu)/2$")
    ax.loglog(energy, area["effective_area_nutau"].to_value(u.km**2), label=r"$(\nu_\tau+\bar{\nu}_\tau)/2$")

    ax.set_xlabel(r"Neutrino energy, $E_{\nu}$ [GeV]")
    ax.set_ylabel(r"Effective area, $A_{\mathrm{eff}}$ [km$^{2}$]")
    ax.set_title("IceCube EHE 2025 Effective Area")
    ax.grid(True, which="both", alpha=0.25)

    bold_tick_labels(ax)
    bold_legend(ax.legend(loc="upper left"))
    fig.tight_layout()
    fig.savefig(OUTPUT_DIR / "icecube_ehe_2025_effective_area.png", dpi=200)
    fig.savefig(OUTPUT_DIR / "icecube_ehe_2025_effective_area.pdf")
    plt.close(fig)


def main():
    OUTPUT_DIR.mkdir(exist_ok=True)
    print("IceCube scientific validation\n")

    limit = get_dataset("icecube.ehe.differential_limit.2025").load_e2phi()
    sensitivity = get_dataset("icecube.ehe.sensitivity.2025").load_e2phi()
    area = get_dataset("icecube.ehe.effective_area.2025").load()
    glashow = get_dataset("icecube.glashow.flux.2021").load_e2phi()
    glashow_all = get_dataset("icecube.glashow.flux.2021").load_e2phi(flavor="all_flavor", flavor_assumption="equal")
    combined = get_dataset("icecube.combined_astrophysical_flux.2015").load_e2phi()
    cascade = get_dataset("icecube.cascade_piecewise_flux.2020").load_e2phi()
    cascade_all = get_dataset("icecube.cascade_piecewise_flux.2020").load_e2phi(flavor="all_flavor", flavor_assumption="equal")
    piecewise = get_dataset("icecube.throughgoing_muon_piecewise_flux.2022").load_e2phi()
    piecewise_all = get_dataset("icecube.throughgoing_muon_piecewise_flux.2022").load_e2phi(flavor="all_flavor", flavor_assumption="equal")
    ngc1068 = get_dataset("icecube.ngc1068_flux.2022").load_e2phi()
    txs0506 = get_dataset("icecube.txs0506_flare_flux.2018").load_e2phi()
    icecube_170922a = get_dataset("icecube.170922a.2017").load()

    print("EHE 2025 limit and sensitivity:")
    validate_ehe(limit, sensitivity)

    print("\nGlashow 2021:")
    validate_glashow(glashow, glashow_all)

    print("\nCombined astrophysical spectrum 2015:")
    validate_combined(combined)

    print("\nSix-year cascade spectrum 2020:")
    validate_cascade_2020(cascade, cascade_all)

    print("\nThrough-going muon spectrum 2022:")
    validate_throughgoing_muon(piecewise, piecewise_all)

    print("\nNGC 1068 point-source flux 2022:")
    validate_ngc1068(ngc1068)

    print("\nTXS 0506+056 flare flux 2018:")
    validate_txs0506(txs0506)

    print("\nIceCube-170922A event 2017:")
    validate_170922a(icecube_170922a)

    print("\nEHE 2025 effective area:")
    validate_effective_area(area)

    print("\nGenerating validation figures...")
    plot_flux_results(limit, sensitivity, glashow_all)
    plot_combined_spectrum(combined)
    plot_cascade_2020(cascade)
    plot_throughgoing_muon(piecewise)
    plot_ngc1068(ngc1068)
    plot_txs0506(txs0506)
    plot_effective_area(area)

    print(f"[PASS] Validation figures written to {OUTPUT_DIR}")
    print("\nValidation passed.")


if __name__ == "__main__":
    main()
