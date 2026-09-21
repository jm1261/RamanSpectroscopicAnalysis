###############################################################################
###############################################################################
#                              Process Specific                               #
#                             Author: Joshua Male                             #
#                              Date: 21/08/2026                               #
#             Description: Process experiment with specific files             #
#                         Project: Raman Spectroscopy                         #
#                                                                             #
#                         Script designed for Python 3                        #
#                           © Copyright Joshua Male                           #
#                                                                             #
#                            Software release: 0.1                            #
###############################################################################
###############################################################################

"""
Comment sections out as appropriate
"""

# Imports
import InitializeScripts  #noqa

import yaml
import logging
import GeneralUtils.FileIO as io
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
data_path = root_path / 'Lightpipes' / '420mAGaAsTest'
results_path = root_path / 'Lightpipes' / 'ProcessedData'

# Experiment files
experiment = {
    "1726": "1726_420mA_2000ms_260910.csv",
    "1742": "1742_420mA_15ms_260910.csv"
}

# Load and fit raw data
data = {}
for sample, file in experiment.items():
    path = data_path / file
    wavelength, intensity = io.load_csv(file_path=path)
    data.update({sample: [wavelength, intensity]})

    # Plot raw intensity
out_name = f'{data_path.stem}_RawIntensity.png'
out_path = results_path / out_name
plot_parameters.update({"out-path": out_path})
plot_parameters.update({
    "title": "GaAs Proxy",
    "x-label": "Wavelength [nm]",
    "y-label": "Intensity [au]"
})
plot_parameters.update({"data": data})
plot.line_plot(plot_parameters=plot_parameters)

# Normalize intensity and subtract background
normalized_data = {}
for sample, file in experiment.items():
    path = data_path / file
    wavelength, intensity = io.load_csv(file_path=path)
    string =  file.replace('-', '.')
    integration_time = float((string.split('_')[2])[0:-2])
    normalized_intensity = intensity / integration_time
    normalized_data.update({sample: [wavelength, normalized_intensity]})

# Plot normalized intensity
out_name = f'{data_path.stem}_NormalizedIntensity.png'
out_path = results_path / out_name
plot_parameters.update({"out-path": out_path})
plot_parameters.update({
    "title": "GaAs Proxy",
    "x-label": "Wavelength [nm]",
    "y-label": "Intensity [au]"
})
plot_parameters.update({"data": normalized_data})
plot.line_plot(plot_parameters=plot_parameters)

# Plot background data
# data = {}
# for sample, values in normalized_data.items():
#     if sample == 'Background':
#         pass
#     else:
#         background_intensity = normalized_data["Background"][1]
#         background_subtracted = values[1] - background_intensity
#         data.update(
#             {sample: [values[0], background_subtracted]}
#         )
# out_name = f'{data_path.stem}_NormalizedBackground.png'
# out_path = results_path / out_name
# plot_parameters.update({"out-path": out_path})
# plot_parameters.update({
#     "title": "Initial LFD Test",
#     "x-label": "Wavelength [nm]",
#     "y-label": "Intensity [au]"
# })
# plot_parameters.update({"data": data})
# plot.line_plot(plot_parameters=plot_parameters)
