from pathlib import Path
import json
import quantstats as qs
import pandas as pd

qs.extend_pandas()

# Config
config_input_file: Path = Path(__file__).parent / "input_files" / "diagnostic_dict.json"
config_output_dir: Path = Path(__file__).parent / "output_files"
config_periods_pre_year: int = int(365.25 * 24 / 3)

# Load and unpack inputs
with open(config_input_file, "r") as file:
    diagnostic_dict: dict[str, list[float]] = json.load(file)
equity_values: list[float] = diagnostic_dict["equity_values"]
timestamps: list[float] = diagnostic_dict["timestamps"]

# Make output dir
config_output_dir.mkdir(parents=True, exist_ok=True)
quantstats_report_path: Path = config_output_dir / "quantstats_report.html"

# Prepare the returns series
returns_series: pd.Series = pd.Series(
    equity_values, index=pd.to_datetime(timestamps, unit="s", utc=True)
)

# Generate the QuantStats report
qs.reports.html(
    returns=returns_series,
    title=f"TEST",
    output=str(quantstats_report_path.absolute()),
    compounded=True,
    periods_per_year=config_periods_pre_year,
    download_filename=None,
)
print(f"Quantstats report saved to: file://{quantstats_report_path.absolute()}")