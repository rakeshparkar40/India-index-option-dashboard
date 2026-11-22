import pandas as pd

def analyze_timeframe(df: pd.DataFrame) -> dict:
    if df.empty:
        return {}

    last = df.iloc[-1]
    close = float(last["Close"])
    rsi = float(last["RSI_14"])
    ema9 = float(last["EMA_9"])
    ema20 = float(last["EMA_20"])
    ema50 = float(last["EMA_50"])

    trend = "Bullish" if close > ema20 > ema50 else "Bearish" if close < ema20 < ema50 else "Neutral"

    score = 0
    if trend == "Bullish":
        score += 1
    elif trend == "Bearish":
        score -= 1

    if rsi > 50:
        score += 1
    elif rsi < 50:
        score -= 1

    return {
        "Close": close,
        "EMA 9": ema9,
        "EMA 20": ema20,
        "EMA 50": ema50,
        "RSI 14": rsi,
        "Trend": trend,
        "Score": score,
    }

def get_option_signal(timeframe_results: dict) -> dict:
    total_score = sum(result["Score"] for result in timeframe_results.values())

    if total_score >= 3:
        signal = "Bullish Call Setup"
        option_type = "Call"
        strength = "Strong"
    elif total_score >= 1:
        signal = "Moderate Bullish Bias"
        option_type = "Call"
        strength = "Moderate"
    elif total_score <= -3:
        signal = "Bearish Put Setup"
        option_type = "Put"
        strength = "Strong"
    elif total_score <= -1:
        signal = "Moderate Bearish Bias"
        option_type = "Put"
        strength = "Moderate"
    else:
        signal = "No Clear Edge"
        option_type = "Avoid"
        strength = "Weak"

    return {
        "Signal": signal,
        "Option Type": option_type,
        "Strength": strength,
        "Confluence Score": total_score,
    }
