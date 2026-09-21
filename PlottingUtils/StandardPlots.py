###############################################################################
###############################################################################
#                                Standard Plots                               #
#                             Author: Joshua Male                             #
#                              Date: 21/08/2026                               #
#                          Standard Matplotlib Plots                          #
#                         Project: Raman Spectroscopy                         #
#                                                                             #
#                         Script designed for Python 3                        #
#                           © Copyright Joshua Male                           #
#                                                                             #
#                            Software release: 0.1                            #
###############################################################################
###############################################################################

# Imports
import logging
import numpy as np
import matplotlib.pyplot as plt

from pathlib import Path
from matplotlib.ticker import AutoMinorLocator

# Start logging
logger = logging.getLogger(name=Path(__file__).stem)


def cm_to_inches(cm: float) -> float:
    """
    Function Details
    ================
    Returns centimeters as inches.

    Parameters
    ----------
    cm: float
        Dimensions in cm.

    Returns
    -------
    inches: float
        Dimensions in inches.

    Raises
    ------
    None.

    Notes
    -----
    Uses the conversion rate to convert a value given in centimeters to inches.
    Useful for matplotlib plotting.

    ---------------------------------------------------------------------------
    Update History
    ==============

    21/08/2026
    ----------
    - Initial implementation.

    """
    return round(cm * 0.393701, 2)


def scatter_plot(plot_parameters: dict) -> None:
    """
    Function Details
    ================
    Create and save a scatter plot with an optional quadratic fit.

    Parameters
    ----------
    plot_parameters: dict
        Plot configuration containing `figsize` as a two-item centimeter
        dimension, `dpi`, `x-data`, `y-data`, `data-label`, `fit-line`,
        `legend-size`, `x-label`, `y-label`, `axis-fontsize`, `title`,
        `title-fontsize`, `label-size`, and `out-path`. Optional error-bar
        values are supplied with `x-err` and `y-err`; optional styling values
        use `err-color`, `err-capsize`, `err-width`, `fit-color`,
        `fit-linestyle`, `fit-width`, and `fit-label`.

    Returns
    -------
    None

    Raises
    ------
    KeyError
        If a required plotting parameter is missing.

    Notes
    -----
    When `fit-line` is true, a second-degree polynomial is fitted to the
    supplied data. The figure is saved with a tight bounding box and closed
    after saving. NumPy, Matplotlib, and filesystem exceptions propagate to
    the caller.

    Update History
    ==============

    21/08/2026
    ----------
    - Initial implementation.

    """
    fig, ax = plt.subplots(
        nrows=1,
        ncols=1,
        figsize=[
            cm_to_inches(cm=plot_parameters["figsize"][0]),
            cm_to_inches(cm=plot_parameters["figsize"][1])
        ],
        dpi=plot_parameters["dpi"]
    )
    ax.scatter(
        x=plot_parameters["x-data"],
        y=plot_parameters["y-data"],
        s=8,
        c='blue',
        label=plot_parameters["data-label"]
    )
    if "x-err" in plot_parameters or "y-err" in plot_parameters:
        ax.errorbar(
            x=plot_parameters["x-data"],
            y=plot_parameters["y-data"],
            xerr=plot_parameters.get("x-err"),
            yerr=plot_parameters.get("y-err"),
            fmt='none',
            ecolor=plot_parameters.get("err-color", "blue"), 
            capsize=plot_parameters.get("err-capsize", 3),
            elinewidth=plot_parameters.get("err-width", 1),
            alpha=1
        )
    if plot_parameters["fit-line"]:
        coefficients = np.polyfit(
            plot_parameters["x-data"],
            plot_parameters["y-data"],
            3
        )
        poly_func = np.poly1d(coefficients)
        x_fit = np.linspace(
            np.min(plot_parameters["x-data"]),
            np.max(plot_parameters["x-data"]),
            100
        )
        y_fit = poly_func(x_fit)
        ax.plot(
            x_fit,
            y_fit,
            color=plot_parameters.get("fit-color", "red"),
            linestyle=plot_parameters.get("fit-linestyle", "--"),
            linewidth=plot_parameters.get("fit-width", 1.5),
            label=plot_parameters.get("fit-label", "Cubic Fit")
        )
    ax.legend(
        loc=0,
        ncol=1,
        prop={"size": plot_parameters["legend-size"]}
    )
    ax.set_xlabel(
        plot_parameters["x-label"],
        fontsize=plot_parameters["axis-fontsize"],
        fontweight='bold'
    )
    ax.set_ylabel(
        plot_parameters["y-label"],
        fontsize=plot_parameters["axis-fontsize"],
        fontweight='bold'
    )
    ax.set_title(
        plot_parameters["title"],
        fontsize=plot_parameters["title-fontsize"],
        fontweight='bold'
    )
    ax.xaxis.set_minor_locator(AutoMinorLocator())
    ax.yaxis.set_minor_locator(AutoMinorLocator())
    ax.tick_params(
        axis='both',
        which='major',
        labelsize=plot_parameters["label-size"]
    )
    plt.savefig(
        plot_parameters["out-path"],
        bbox_inches='tight'
    )
    fig.clf()
    plt.cla()
    plt.close(fig)


def line_plot(plot_parameters: dict) -> None:
    """
    Function Details
    ================
    Create and save a standard line plot with all series on one axis.

    Parameters
    ----------
    plot_parameters: dict
        Plot configuration containing `figsize` as a two-item centimetre
        dimension, `dpi`, `data`, `legend-size`, `x-label`, `y-label`,
        `axis-fontsize`, `title`, `title-fontsize`, `label-size`, and
        `out-path`. The `data` mapping contains series values as
        ``[x_values, y_values, ...]``; only its first two values are plotted.

    -------
    None

    Raises
    ------
        If Matplotlib cannot create or save the figure from the supplied
        parameters.

    Notes
    -----
    The figure is saved with a tight bounding box and closed after saving.

    Returns
    ------
    None

    ---------------------------------------------------------------------------
    Update History
    ==============

    21/08/2026
    ----------
    - Initial implementation.

    """
    fig, ax = plt.subplots(
        nrows=1,
        ncols=1,
        figsize=[
            cm_to_inches(cm=plot_parameters["figsize"][0]),
            cm_to_inches(cm=plot_parameters["figsize"][1])
        ],
        dpi=plot_parameters["dpi"]
    )
    data_dict = plot_parameters["data"]
    for key, values in data_dict.items():
        ax.plot(
            values[0],
            values[1],
            lw=1,
            label=key
        )
    ax.legend(
        loc=0,
        ncol=1,
        prop={"size": plot_parameters["legend-size"]}
    )
    ax.set_xlabel(
        plot_parameters["x-label"],
        fontsize=plot_parameters["axis-fontsize"],
        fontweight='bold'
    )
    ax.set_ylabel(
        plot_parameters["y-label"],
        fontsize=plot_parameters["axis-fontsize"],
        fontweight='bold'
    )
    ax.set_title(
        plot_parameters["title"],
        fontsize=plot_parameters["title-fontsize"],
        fontweight='bold'
    )
    ax.xaxis.set_minor_locator(AutoMinorLocator())
    ax.yaxis.set_minor_locator(AutoMinorLocator())
    ax.tick_params(
        axis='both',
        which='major',
        labelsize=plot_parameters["label-size"]
    )
    plt.savefig(
        plot_parameters["out-path"],
        bbox_inches='tight'
    )
    fig.clf()
    plt.cla()
    plt.close(fig)
