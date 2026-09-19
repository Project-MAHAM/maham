import matplotlib


def apply_plot_style():
    matplotlib.rcParams.update({"font.size": 10})
    font = {"weight": "bold", "size": 10}
    matplotlib.rc("font", **font)
    matplotlib.rcParams["axes.labelweight"] = "bold"
    matplotlib.rcParams["axes.titleweight"] = "bold"
    matplotlib.rcParams["xtick.labelsize"] = 10
    matplotlib.rcParams["ytick.labelsize"] = 10
    matplotlib.rcParams["xtick.direction"] = "out"
    matplotlib.rcParams["ytick.direction"] = "out"
    matplotlib.rcParams["legend.fontsize"] = 10
    matplotlib.rcParams["legend.title_fontsize"] = 10
    matplotlib.rcParams["mathtext.default"] = "bf"


def bold_tick_labels(ax):
    for label in ax.get_xticklabels() + ax.get_yticklabels():
        label.set_fontweight("bold")


def bold_legend(legend):
    for text in legend.get_texts():
        text.set_fontweight("bold")
    if legend.get_title() is not None:
        legend.get_title().set_fontweight("bold")


def validation_curve_style(product):
    """Return the standard monochrome curve style for validation plots."""
    styles = {
        "upper_limit": {"color": "black", "linestyle": "-", "linewidth": 2.5},
        "sensitivity": {"color": "black", "linestyle": "--", "linewidth": 2.5},
    }
    try:
        return styles[product].copy()
    except KeyError as exc:
        raise ValueError(f"Unknown validation product: {product!r}") from exc
