import astropy.units as u
import numpy as np

from maham.datasets import get_dataset
from maham.detector import effective_area_from_effective_volume
from maham.models import get_model
from maham.physics.neutrino import interaction_length
from maham.physics.spectra import centered_log_energy_bounds, convert_spectral_quantity, differential_flux_limit


def test_rno_g_effective_volume_source_and_columns():
    dataset = get_dataset("rno_g.design.effective_volume.2021")
    assert dataset.metadata.source.sha256 == "8ec29a23489114d39c9163ed94adce4b0ea04fb4e6c135115e0fdd5e0b0df7c6"
    assert dataset.metadata.source.provenance.value == "official_repository"
    table = dataset.load()
    assert len(table) == 30
    assert table.meta["figure24_nominal_trigger"] == "2.00sigma"
    assert "effective_volume_2p00sigma" in table.colnames
    assert "effective_volume_uncertainty_2p00sigma" in table.colnames
    assert np.isclose(table["energy"][0].to_value(u.eV), 1.2115276586285852e15)


def test_rno_g_sensitivity_metadata_and_support():
    dataset = get_dataset("rno_g.design.diffuse_sensitivity.2021")
    table = dataset.load(quantity="E2phi", flavor="all_flavor")
    assert dataset.metadata.source.provenance.value == "derived"
    assert len(table) == 22
    assert np.isclose(table["energy"][0].to_value(u.GeV), 2.6101572156825224e7)
    assert np.isclose(table["energy"][-1].to_value(u.GeV), 8.25404185268014e10)
    assert table.meta["flavor_convention"] == "all_flavor"
    assert np.isclose(table.meta["confidence_level"], 0.90)
    assert np.isclose(table.meta["figure24_effective_area_scale_factor"], 5.0)
    assert np.isclose(table.meta["fine_grid_log10_width_decades"], 1.0 / 6.0)
    assert np.isclose(table.meta["intended_log10_energy_width_decades"], 1.0)


def test_rno_g_sensitivity_reproduces_nominal_figure24_prescription():
    veff = get_dataset("rno_g.design.effective_volume.2021").load()
    published = get_dataset("rno_g.design.diffuse_sensitivity.2021").load(quantity="E2phi")
    spacing = float(np.median(np.diff(np.log10(veff["energy"].to_value(u.eV)))))
    energy = veff["energy"][8:]
    nominal_veff = veff["effective_volume_2p00sigma"][8:]
    sigma = get_model("neutrino.cross_section.ctw_2011").cross_section(energy, particle="nu", current="total", variation="central")
    lint = interaction_length(sigma, 0.917 * u.g / u.cm**3)
    aeff = effective_area_from_effective_volume(nominal_veff, lint)
    energy_min, energy_max = centered_log_energy_bounds(energy, spacing)
    phi = differential_flux_limit(aeff * 5.0, energy_min, energy_max, 2.44, (2.0 / 3.0) * 5.0 * u.yr, 4.0 * np.pi * u.sr)
    expected = convert_spectral_quantity(energy, phi, "phi", "E2phi").to(u.GeV / (u.cm**2 * u.s * u.sr))
    np.testing.assert_allclose(published["E2phi"].to_value(expected.unit), expected.value, rtol=5e-15, atol=0)
