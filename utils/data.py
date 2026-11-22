import yfinance as yf
import pandas as pd
import streamlit as st

INDEX_SYMBOLS = {
    "Nifty 50": "^NSEI",
    "Bank Nifty": "^NSEBANK",
    "Sensex": "^BSESN",
}

TIMEFRAMES = {
    "5 Minutes": "5m",
    "15 Minutes": "15m",
    "1 Hour": "1h",
    "4 Hours": "4h",
}

# Yahoo Finance limits intraday history.
HISTORY_PERIODS = {
    "5m": "5d",
    "15m": "1mo",
    "1h": "3mo",
    "4h": "6mo",
}

@st.cache_data(ttl=300, show_spinner="Loading market data...")
def get_ohlcv(index_name: str, timeframe: str) -> pd.DataFrame:
    symbol = INDEX_SYMBOLS[index_name]
    interval = TIMEFRAMES[timeframe]
    period = HISTORY_PERIODS[interval]

    df = yf.download(
        tickers=symbol,
        period=period,
        interval=interval,
        auto_adjust=False,
        progress=False,
    )

    if df.empty:
        raise ValueError(f"No data returned for {index_name} on {timeframe} timeframe.")

    if isinstance(df.columns, pd.MultiIndex):
        df.columns = [col[0] for col in df.columns]

    required = ["Open", "High", "Low", "Close", "Volume"]
    missing = [col for col in required if col not in df.columns]
    if missing:
        raise ValueError(f"Missing columns: {missing}")

    df = df[required].copy()
    df = df.dropna(subset=["Open", "High", "Low", "Close"])
    df.index = pd.to_datetime(df.index)
    df = df.sort_index()
    return df

def get_latest_close(df: pd.DataFrame) -> float:
    return float(df["Close"].iloc[-1])
