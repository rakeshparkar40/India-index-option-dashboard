import numpy as np
import pandas as pd

def find_swing_points(df: pd.DataFrame, lookback: int = 3) -> tuple[float, float]:
    highs = df["High"].values
    lows = df["Low"].values

    swing_high = None
    swing_low = None

    for i in range(lookback, len(df) - lookback):
        window_high = highs[i - lookback:i + lookback + 1]
        window_low = lows[i - lookback:i + lookback + 1]

        if highs[i] == max(window_high):
            swing_high = highs[i]

        if lows[i] == min(window_low):
            swing_low = lows[i]

    if swing_high is None:
        swing_high = float(df["High"].max())

    if swing_low is None:
        swing_low = float(df["Low"].min())

    return float(swing_high), float(swing_low)

def get_support_resistance(
    df: pd.DataFrame,
    current_price: float,
    lookback: int = 100,
) -> tuple[float, float]:
    recent = df.tail(lookback)
    highs = recent["High"].values
    lows = recent["Low"].values

    resistance_candidates = highs[highs > current_price]
    support_candidates = lows[lows < current_price]

    resistance = float(np.min(resistance_candidates)) if len(resistance_candidates) else float(recent["High"].max())
    support = float(np.max(support_candidates)) if len(support_candidates) else float(recent["Low"].min())

    return support, resistance

def get_previous_day_levels(df: pd.DataFrame) -> tuple[float, float]:
    if df.empty:
        return np.nan, np.nan

    dates = df.index.date
    last_date = dates[-1]

    previous_dates = [date for date in dates if date < last_date]

    if not previous_dates:
        return float(df["High"].max()), float(df["Low"].min())

    previous_date = previous_dates[-1]
    previous_day = df[dates == previous_date]

    return float(previous_day["High"].max()), float(previous_day["Low"].min())

def get_session_levels(df: pd.DataFrame) -> tuple[float, float]:
    if df.empty:
        return np.nan, np.nan

    current_date = df.index.date[-1]
    session_df = df[df.index.date == current_date]

    if session_df.empty:
        session_df = df.tail(1)

    return float(session_df["High"].max()), float(session_df["Low"].min())
