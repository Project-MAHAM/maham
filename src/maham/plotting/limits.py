import numpy as np


def plot_upper_limits(ax, x, y, xerr=None, arrow_factor=2.5, color="black", linewidth=1.5, capsize=3, mutation_scale=12, **kwargs):
    """Plot upper limits with the horizontal error bar at the limit value and a downward arrow."""
    x = np.atleast_1d(np.asarray(x, dtype=float))
    y = np.atleast_1d(np.asarray(y, dtype=float))

    if xerr is not None:
        ax.errorbar(x, y, xerr=xerr, fmt="none", ecolor=color, elinewidth=linewidth, capsize=capsize, zorder=4)

    for xi, yi in zip(x, y):
        ax.annotate("", xy=(xi, yi / arrow_factor), xytext=(xi, yi), arrowprops={"arrowstyle": "-|>", "color": color, "lw": linewidth, "mutation_scale": mutation_scale, "shrinkA": 0, "shrinkB": 0}, zorder=5)


def plot_lower_limits(ax, x, y, xerr=None, arrow_factor=2.5, color="black", linewidth=1.5, capsize=3, mutation_scale=12, **kwargs):
    """Plot lower limits with the horizontal error bar at the limit value and an upward arrow."""
    x = np.atleast_1d(np.asarray(x, dtype=float))
    y = np.atleast_1d(np.asarray(y, dtype=float))

    if xerr is not None:
        ax.errorbar(x, y, xerr=xerr, fmt="none", ecolor=color, elinewidth=linewidth, capsize=capsize, zorder=4)

    for xi, yi in zip(x, y):
        ax.annotate("", xy=(xi, yi * arrow_factor), xytext=(xi, yi), arrowprops={"arrowstyle": "-|>", "color": color, "lw": linewidth, "mutation_scale": mutation_scale, "shrinkA": 0, "shrinkB": 0}, zorder=5)
