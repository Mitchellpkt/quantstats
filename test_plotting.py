from datetime import datetime
from typing import Any

import numpy as np
import pandas as pd

import quantstats as qs
import time


def create_quant_stats_series(
    timestamps: Any,
    daily_returns: Any,
) -> pd.Series:
    """Custom helper function for converting usual data format into quantstats format"""

    # Extend pandas if it has not been done already
    if not hasattr(pd.Series, "plot_rolling_volatility"):
        qs.extend_pandas()

    # Convert timestamps to a DatetimeIndex if not already in that format
    if not isinstance(timestamps, pd.DatetimeIndex):
        if isinstance(timestamps, (list, np.ndarray)):
            timestamp_to_spot_check = timestamps[0]
        elif hasattr(timestamps, "tolist"):
            timestamp_to_spot_check = timestamps.tolist()[0]
        else:
            raise ValueError(
                f"Uncertain how to interpret timestamps of type {type(timestamps)}"
            )

        if isinstance(timestamp_to_spot_check, datetime):
            timestamps = pd.DatetimeIndex(timestamps)
        else:
            timestamps = pd.to_datetime(timestamps, unit="s")

    if isinstance(daily_returns, pd.Series):
        daily_returns = daily_returns.values
    if isinstance(timestamps, pd.DatetimeIndex):
        timestamps = timestamps.values

    # Create a pandas Series with the timestamps as the index
    qs_series = pd.Series(daily_returns, index=timestamps, name="Close")

    return qs_series


if __name__ == "__main__":
    returns: pd.Series = create_quant_stats_series(
        [time.time() + 86400 * (2 * i + 365) for i in range(7)],
        [0.1, 0.2, -0.1, 0.3, 0.1, 0.2, -0.1],
    )

    test_text: str = "lorem ipsum epsilon\nfoobar\n>baz\n>bat=5"
    returns.plot_snapshot(overlay_text=test_text, show=True)
