###############################################################################
###############################################################################
#                               Time Experiment                               #
#                             Author: Joshua Male                             #
#                              Date: 19/08/2026                               #
#          Description: Experiment script for time-dependent analysis         #
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
data_path = root_path / 'TPBExperiment' / 'IntegrationTime'
results_path = root_path / 'TPBExperiment'/ 'ProcessedData'