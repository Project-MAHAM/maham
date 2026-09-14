import astropy.units as u
import matplotlib.pyplot as plt
import numpy as np

from maham.datasets import get_dataset
from maham.plotting import apply_plot_style, bold_tick_labels


OUTPUT = "validation/published_results/icecube/outputs/icecube_ngc1068_flux_2022"


def require(condition, message):
    if not condition:
        raise AssertionError(message)
    print(f"PASS: {message}")


def main():
    apply_plot_style()

    dataset = get_dataset("icecube.ngc1068_flux.2022")
    table = dataset.load()

    phi0 = table.meta["phi0_TeV_inv_cm2_s"]
    gamma = table.meta["spectral_index"]

    require(phi0 == 5.0e-11, "NGC 1068 normalization matches published best fit")
    require(gamma == 3.2, "NGC 1068 spectral index matches published best fit")
    require(table.meta["signal_events"] == 79, "NGC 1068 best-fit signal count is 79")
    require(table.meta["signal_events_lower"] == 59, "NGC 1068 lower signal-count interval matches publication")
    require(table.meta["signal_events_upper"] == 101, "NGC 1068 upper signal-count interval matches publication")
    require(table.meta["global_significance_sigma"] == 4.2, "NGC 1068 global significance is 4.2 sigma")
    require(table.meta["energy_min_TeV"] == 1.5, "NGC 1068 characteristic energy range starts at 1.5 TeV")
    require(table.meta["energy_max_TeV"] == 15.0, "NGC 1068 characteristic energy range ends at 15 TeV")
    require(table.meta["solid_angle_convention"] == "point_source", "NGC 1068 is represented as a point-source flux")

    energy = table["energy"].to(u.TeV)
    phi = table["phi"].to(1 / (u.TeV * u.cm**2 * u.s))

    reference_energy = 1.0 * u.TeV
    expected = phi0 / (u.TeV * u.cm**2 * u.s) * (energy / reference_energy) ** (-gamma)
    np.testing.assert_allclose(phi.value, expected.value, rtol=1e-12)
    print("PASS: standardized spectrum reproduces the published best-fit power law")

    e2phi = dataset.load(quantity="E2phi")
    expected_e2phi = (table["phi"] * table["energy"] ** 2).to(u.GeV / (u.cm**2 * u.s))
    np.testing.assert_allclose(e2phi["E2phi"].value, expected_e2phi.value, rtol=1e-12)
    print("PASS: E2phi representation is internally consistent")

    fig, ax = plt.subplots(figsize=(7, 5))
    ax.loglog(energy.to_value(u.TeV), phi.to_value(1 / (u.TeV * u.cm**2 * u.s)), color='k', linewidth=2)

    ax.set_xlabel(r"Neutrino energy, $E_\nu$ [TeV]")
    ax.set_ylabel(r"Flux, $\Phi_{\nu_\mu+\bar{\nu}_\mu}$ [TeV$^{-1}$ cm$^{-2}$ s$^{-1}$]")
    ax.set_title("IceCube NGC 1068 Best-Fit Point-Source Flux")
    ax.grid(True, which="both", alpha=0.25)

    ax.text(
        0.04, 0.05,
        r"$\Phi_0 = 5.0\times10^{-11}$ TeV$^{-1}$ cm$^{-2}$ s$^{-1}$"
        "\n" r"$\gamma = 3.2$"
        "\n" r"$E_0 = 1$ TeV"
        "\n" r"79$_{-20}^{+22}$ signal events, 4.2$\sigma$",
        transform=ax.transAxes, fontweight="bold",
    )

    bold_tick_labels(ax)
    fig.tight_layout()
    fig.savefig(f"{OUTPUT}.png", dpi=200)
    fig.savefig(f"{OUTPUT}.pdf")
    plt.close(fig)

    print(f"\nSaved {OUTPUT}.png")
    print(f"Saved {OUTPUT}.pdf")


if __name__ == "__main__":
    main()
