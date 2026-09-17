import numpy as np

from maham.datasets import get_dataset


def test_native_upper_limit_normalization_metadata():
    icecube = get_dataset("icecube.ehe.differential_limit.2025").load_e2phi()
    baikal = get_dataset("baikal_gvd.diffuse_neutrino_limit.2025").load_e2phi()
    auger = get_dataset("auger.diffuse_neutrino_limit.2023").load_e2phi()
    ara = get_dataset("ara.five_station.diffuse_neutrino_limit.2026").load_e2phi()
    anita = get_dataset("anita.i_iv_diffuse_neutrino_limit.2019").load_ephi()

    for table in (icecube, baikal, auger, ara):
        assert table.meta["limit_normalization_convention"] == "log10_energy_width"
    assert np.isclose(icecube.meta["log10_energy_width_decades"], 1.0)
    assert np.isclose(baikal.meta["log10_energy_width_decades"], 1.0)
    assert np.isclose(auger.meta["log10_energy_width_decades"], 0.5)
    assert np.isclose(ara.meta["log10_energy_width_decades"], 1.0)
    assert anita.meta["limit_normalization_convention"] == "anita_bandwidth"
    assert np.isclose(anita.meta["limit_bandwidth_factor"], 4.0)
