import pandas as pd

def calculate_ema(df: pd.DataFrame, column: str = "Close", periods=(9, 20, 50, 200)) -> pd.DataFrame:
    df = df.copy()

    for period in periods:
        df[f"EMA_{period}"] = df[column].ewm(span=period, adjust=False).mean()

    return df

def calculate_rsi(df: pd.DataFrame, column: str = "Close", period: int = 14) -> pd.DataFrame:
    df = df.copy()
    delta = df[column].diff()

    gain = delta.clip(lower=0)
    loss = -delta.clip(upper=0)

    avg_gain = gain.ewm(alpha=1 / period, min_periods=period, adjust=False).mean()
    avg_loss = loss.ewm(alpha=1 / period, min_periods=period, adjust=False).mean()

    rs = avg_gain / avg_loss
    df["RSI_14"] = 100 - (100 / (1 + rs))

    return df

def get_trend(df: pd.DataFrame) -> str:
    if len(df) < 50:
        return "Neutral"

    last = df.iloc[-1]
    close = last["Close"]
    ema20 = last["EMA_20"]
    ema50 = last["EMA_50"]

    if close > ema20 > ema50:
        return "Bullish"
    if close < ema20 < ema50:
        return "Bearish"
    return "Neutral"

def get_rsi_state(rsi: float) -> str:
    if rsi >= 70:
        return "Overbought"
    if rsi <= 30:
        return "Oversold"
    if rsi > 50:
        return "Bullish momentum"
    if rsi < 50:
        return "Bearish momentum"
    return "Neutral"
