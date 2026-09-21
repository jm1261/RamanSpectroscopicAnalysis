###############################################################################
###############################################################################
#                                 Peak Fitting                                #
#                             Author: Joshua Male                             #
#                              Date: 21/08/2026                               #
#                          Peak Fitting Functionality                         #
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

from pathlib import Path
from scipy.optimize import curve_fit

from typing import Dict

# Start logging
logger = logging.getLogger(name=Path(__file__).stem)


def gaussian(xdata: np.ndarray, ydata: np.ndarray) -> Dict:
    """
    Function Details
    ================
    Fit a Gaussian curve to one-dimensional intensity data.

    Parameters
    ----------
    data: np.ndarray
        Array containing intensity values sampled at uniform positions.

    Returns
    -------
    fit: Dict
        Dictionary containing the fitted amplitude, mean, standard deviation,
        offset, and root mean square error. Returns an empty dictionary when
        the fit cannot be calculated.

    Raises
    ------
    ValueError: If data is empty or cannot be used to initialise the fit
        before curve fitting begins.
    TypeError: If data contains fewer points than the Gaussian has parameters.

    Notes
    -----
    - RuntimeError and ValueError from the fitting procedure are logged and
            return an empty dictionary.

    ---------------------------------------------------------------------------
    Update History
    ==============

    19/08/2026
    ----------
    - Initial implementation.

    """
    def gaussian_function(
        x: np.ndarray,
        a: float,
        mu: float,
        sigma: float,
        offset: float,
    ) -> np.ndarray:
        """
        Return Gaussian values for the supplied parameters.

        Parameters
        ----------
        x: np.ndarray
            Positions at which to evaluate the Gaussian.
        a: float
            Gaussian amplitude.
        mu: float
            Gaussian centre position.
        sigma: float
            Gaussian standard deviation.
        offset: float
            Constant vertical offset.

        Returns
        -------
        values: np.ndarray
            Gaussian values evaluated at each position.

        """
        return a * np.exp(-((x - mu) ** 2) / (2 * sigma ** 2)) + offset
    if len(ydata) == 0:
        return {}
        
    # Find the wavelength where intensity is at its maximum for the initial guess
    peak_index = np.argmax(ydata)
    initial_mu = xdata[peak_index]
    
    # Estimate an initial sigma based on the span of your xdata
    initial_sigma = (np.max(xdata) - np.min(xdata)) / 10 
    
    p0 = [
        np.max(ydata) - np.min(ydata), # Amplitude guess
        initial_mu,                    # Center (mu) guess in wavelength units
        initial_sigma,                 # Width (sigma) guess
        np.mean(ydata)                 # Offset guess
    ]
    
    try:
        popt, _ = curve_fit(gaussian_function, xdata, ydata, p0=p0)
    except (RuntimeError, ValueError) as e:
        print(f'[ERROR] Curve fitting failed {e}')
        return {}

    error = RMSE(ydata, gaussian_function(xdata, *popt))
    return {
        'amplitude': popt[0],
        'mu':        popt[1],
        'sigma':     popt[2],
        'offset':    popt[3],
        'error':     error,
    }


def RMSE(
        data1: np.ndarray,
        data2: np.ndarray
) -> float:
    """
    Calculate the root mean square error between two arrays.

    Parameters
    ----------
    data1: np.ndarray
        First array of values to compare.
    data2: np.ndarray
        Second array of values to compare. It must be broadcast-compatible
        with `data1`.

    Returns
    -------
    error: float
        Square root of the mean squared element-wise difference.

    Raises
    ------
    ValueError
        If the arrays cannot be broadcast together.

    Notes
    -----
    NumPy broadcasting is applied before the mean is calculated.
    Empty arrays return `nan` and emit a NumPy runtime warning.

    ---------------------------------------------------------------------------
    Update History
    ==============

    19/08/2026
    ----------
    - Initial implementation.

    """
    squared_difference = (data1 - data2) ** 2
    mean_squared_error = np.mean(squared_difference)
    return np.sqrt(mean_squared_error)


def calculate_q_factor(mu: float, sigma: float) -> float:
    """
    Calculate the quality factor of a fitted Gaussian peak.

    Parameters
    ----------
    mu: float
        Fitted Gaussian centre position.
    sigma: float
        Fitted Gaussian standard deviation. Its absolute value is used when
        calculating the full width at half maximum.

    Returns
    -------
    q_factor: float
        Ratio of `mu` to the Gaussian full width at half maximum. Returns
        ``0.0`` when `sigma` is zero.

    Notes
    -----
    The full width at half maximum is calculated as
    ``2 * sqrt(2 * ln(2)) * abs(sigma)``.
    """
    # Prevent DivisionByZero if sigma is 0
    if sigma == 0:
        return 0.0
        
    # FWHM = 2 * sqrt(2 * ln(2)) * sigma
    fwhm = 2 * np.sqrt(2 * np.log(2)) * np.abs(sigma)
    
    q_factor = mu / fwhm
    return q_factor