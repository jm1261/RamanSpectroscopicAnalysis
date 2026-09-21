###############################################################################
###############################################################################
#                          Lens Alignment Experiment                          #
#                             Author: Joshua Male                             #
#                              Date: 21/08/2026                               #
#             Description: Experiment script for distance analysis            #
#                         Project: Raman Spectroscopy                         #
#                                                                             #
#                         Script designed for Python 3                        #
#                           © Copyright Joshua Male                           #
#                                                                             #
#                            Software release: 0.1                            #
###############################################################################
###############################################################################

# Imports
import InitializeScripts  #noqa

import yaml
import logging
import yaml
import GeneralUtils.FileIO as io
import GeneralUtils.PeakFitting as pf
import PlottingUtils.StandardPlots as plot

from pathlib import Path

# Start logging
logger = logging.getLogger(name=Path(__file__).stem)

# Configuration
project_root = Path(__file__).resolve().parents[1]
config_path = project_root / 'local_config.yml'
with config_path.open(mode='r', encoding='utf-8') as config_file:
    local_config = yaml.safe_load(config_file)
plot_config_path = (
    project_root / 'standard_plot_parameters.yml'
)
with plot_config_path.open(mode='r', encoding='utf-8') as plot_config_file:
    plot_parameters = yaml.safe_load(plot_config_file)
root_path = Path(local_config['RAMAN_DATA_ROOT'])
data_path = root_path / 'SetupAlignment' / 'ExcitationLensDistance' / '31degrees17mm'
results_path = root_path / 'SetupAlignment' / 'ProcessedData'

# Load raw data
distance_offset = -17

# Data arrays
lens_separation = []
signal_amplitude = []
signal_error = []
signal_quality = []

for measurement in data_path.iterdir():
    logger.info(f'Processing: {measurement}')
    digits = "".join(filter(str.isdigit, measurement.stem))
    distance = int(digits) - distance_offset
    lens_separation.append(distance)
    wavelength, intensity = io.load_csv(file_path=measurement)
    gaussian_fit = pf.gaussian(xdata=wavelength, ydata=intensity)
    if gaussian_fit:
        q_stat = pf.calculate_q_factor(
            mu=gaussian_fit["mu"],
            sigma=gaussian_fit["sigma"]
        )
        signal_quality.append(q_stat)
        signal_amplitude.append(gaussian_fit["amplitude"])
        signal_error.append(gaussian_fit["error"])
    else:
        signal_quality.append(None)
        signal_amplitude.append(None)

# Stack data for plotting
out_name = f'{data_path.stem}_Intensity.png'
out_path = results_path / out_name
plot_parameters.update({"out-path": out_path})
plot_parameters.update({
    "title": "Excitation Lens Alignment",
    "x-label": "Separation [cm]",
    "y-label": "Intensity [au]",
    "data-label": "31 degrees 17 mm",
    "x-data": lens_separation,
    "y-data": signal_amplitude,
    "x-err": 1,
    "y-err": signal_error,
    "fit-line": False
})
plot.scatter_plot(plot_parameters=plot_parameters)

out_name = f'{data_path.stem}_QFactor.png'
out_path = results_path / out_name
plot_parameters.update({"out-path": out_path})
plot_parameters.update({
    "title": "Excitation Lens Alignment",
    "x-label": "Separation [cm]",
    "y-label": "Quality Factor [au]",
    "data-label": "31 degrees 17 mm",
    "x-data": lens_separation,
    "y-data": signal_quality,
    "x-err": 1,
    "y-err": signal_error,
    "fit-line": False
})
plot.scatter_plot(plot_parameters=plot_parameters)
