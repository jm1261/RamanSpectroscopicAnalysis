import tempfile
import unittest
import sys
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from GeneralUtils.FileIO import load_csv
from Logging.cleanup_logs import cleanup_logs
from PlottingUtils.StandardPlots import cm_to_inches


class RamanUtilityTests(unittest.TestCase):
    def test_load_csv_skips_instrument_header_and_footer(self):
        with tempfile.TemporaryDirectory() as directory:
            csv_path = Path(directory) / "spectrum.csv"
            contents = "".join(
                f"instrument-header-{index}\n" for index in range(32)
            )
            contents += "100,1.5\n101,2.5\nfooter\n"
            csv_path.write_text(contents, encoding="utf-8")

            wavelength, intensity = load_csv(csv_path)

        np.testing.assert_array_equal(wavelength, np.array([100, 101]))
        np.testing.assert_array_equal(intensity, np.array([1.5, 2.5]))

    def test_cm_to_inches_converts_and_rounds(self):
        self.assertEqual(cm_to_inches(2.54), 1.0)

    def test_cleanup_logs_removes_clean_logs_and_retains_warnings(self):
        with tempfile.TemporaryDirectory() as directory:
            log_directory = Path(directory)
            clean_log = log_directory / "application_clean.log"
            warning_log = log_directory / "application_warning.log"
            unrelated_file = log_directory / "notes.txt"
            clean_log.write_text("INFO complete", encoding="utf-8")
            warning_log.write_text("WARNING keep", encoding="utf-8")
            unrelated_file.write_text("leave me", encoding="utf-8")

            deleted, retained = cleanup_logs(log_directory)

            self.assertEqual((deleted, retained), (1, 1))
            self.assertFalse(clean_log.exists())
            self.assertTrue(warning_log.exists())
            self.assertTrue(unrelated_file.exists())


if __name__ == "__main__":
    unittest.main()