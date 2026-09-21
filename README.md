# RamanSpectroscopy

`RamanSpectroscopy` loads Raman CSV spectra, fits Gaussian peaks, calculates
quality factors, creates standard plots, and provides experiment-specific
scripts with rotating application logs.

See the detailed [RamanSpectroscopy architecture](architecture.md) for
component ownership and data flow.

The repository pins Python with `.python-version`, installs dependencies from
`requirements.txt`, and runs its tests through `.github/workflows/ci.yml`.

## Setup

From the repository root, create or activate a Python environment and install
the project dependencies:

```powershell
python -m pip install -r requirements.txt
```

Copy `local_config.example.yml` to the ignored `local_config.yml` file and set
the Raman data root:

```yaml
RAMAN_DATA_ROOT: D:/data/raman
```

`standard_plot_parameters.yml` supplies shared figure, font, and label defaults
used by the experiment scripts.

## Components

- `GeneralUtils/FileIO.py` loads CSV files after the instrument header and
  before the footer row.
- `GeneralUtils/PeakFitting.py` fits Gaussian peaks and calculates Q factors.
- `PlottingUtils/StandardPlots.py` creates line and scatter plots.
- `ExperimentScripts/` contains integration-time, lens-alignment, and
  process-specific workflows.
- `Logging/` contains the logging configuration and log cleanup command.

## Running workflows

Initialize the general utility logging configuration from the repository root:

```powershell
python GeneralUtils/InitializeGeneralUtils.py
```

Run an experiment script after setting `RAMAN_DATA_ROOT` and confirming that
the expected input files exist:

```powershell
python ExperimentScripts/IntegrationTime.py
python ExperimentScripts/LensAlignment.py
python ExperimentScripts/ProcessSpecific.py
```

Preview application-log cleanup before deleting clean log files:

```powershell
python Logging/cleanup_logs.py --dry-run
```

Run the focused tests from the repository root:

```powershell
python -m unittest discover --start-directory tests --pattern "test_*.py" --verbose
```

`IntegrationTime.py` currently derives its data path without processing files.
The other workflows depend on experiment-specific CSV names and directory
layouts supplied by the local data environment. This repository is
self-contained when cloned independently.
