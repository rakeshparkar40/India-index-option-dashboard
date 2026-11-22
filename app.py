import streamlit as st
import pandas as pd
import plotly.graph_objects as go

from utils.data import INDEX_SYMBOLS, TIMEFRAMES, get_ohlcv, get_latest_close
from utils.indicators import calculate_ema, calculate_rsi, get_trend, get_rsi_state
from utils.levels import (
    find_swing_points,
    get_support_resistance,
    get_previous_day_levels,
    get_session_levels,
)
from utils.signals import analyze_timeframe, get_option_signal

st.set_page_config(
    page_title="India Index Option Dashboard",
    page_icon="📈",
    layout="wide",
)

st.title("📈 India Index Option Dashboard")
st.caption(
    "Research dashboard for Nifty 50, Bank Nifty, and Sensex. "
    "This tool provides technical analysis only and does not guarantee future market movement."
)

index_name = st.selectbox(
    "Select Index",
    list(INDEX_SYMBOLS.keys()),
    index=0,
)

st.divider()

try:
    timeframe_results = {}
    timeframe_tables = {}

    tabs = st.tabs(list(TIMEFRAMES.keys()))

    for tab, (timeframe_label, _) in zip(tabs, TIMEFRAMES.items()):
        with tab:
            df = get_ohlcv(index_name, timeframe_label)
            df = calculate_ema(df)
            df = calculate_rsi(df)

            result = analyze_timeframe(df)
            timeframe_results[timeframe_label] = result

            latest_close = get_latest_close(df)
            swing_high, swing_low = find_swing_points(df)
            support, resistance = get_support_resistance(df, latest_close)
            previous_high, previous_low = get_previous_day_levels(df)
            session_high, session_low = get_session_levels(df)

            col1, col2, col3, col4 = st.columns(4)

            col1.metric("Latest Close", f"{latest_close:,.2f}")
            col2.metric("Trend", result["Trend"])
            col3.metric("RSI 14", f"{result['RSI 14']:.2f}", get_rsi_state(result["RSI 14"]))
            col4.metric("Timeframe Score", f"{result['Score']:+d}")

            st.subheader("Key Levels")

            levels_df = pd.DataFrame(
                {
                    "Level": [
                        "Nearest Resistance",
                        "Nearest Support",
                        "Last Swing High",
                        "Last Swing Low",
                        "Previous Day High",
                        "Previous Day Low",
                        "Session High",
                        "Session Low",
                    ],
                    "Price": [
                        resistance,
                        support,
                        swing_high,
                        swing_low,
                        previous_high,
                        previous_low,
                        session_high,
                        session_low,
                    ],
                }
            )

            st.dataframe(
                levels_df.style.format({"Price": "{:,.2f}"}),
                use_container_width=True,
                hide_index=True,
            )

            st.subheader("Price and EMAs")

            fig = go.Figure()

            fig.add_trace(
                go.Scatter(
                    x=df.index,
                    y=df["Close"],
                    mode="lines",
                    name="Close",
                    line=dict(color="white", width=2),
                )
            )

            for period, color in [(9, "#00c853"), (20, "#2979ff"), (50, "#ffb300"), (200, "#e0e0e0")]:
                fig.add_trace(
                    go.Scatter(
                        x=df.index,
                        y=df[f"EMA_{period}"],
                        mode="lines",
                        name=f"EMA {period}",
                        line=dict(color=color, width=1.5),
                    )
                )

            fig.update_layout(
                template="plotly_dark",
                height=450,
                margin=dict(l=10, r=10, t=30, b=10),
                legend=dict(orientation="h", yanchor="bottom", y=1.02),
                xaxis_title="Time",
                yaxis_title="Price",
            )

            st.plotly_chart(fig, use_container_width=True)

            timeframe_tables[timeframe_label] = df.tail(10)[
                ["Close", "EMA_9", "EMA_20", "EMA_50", "RSI_14"]
            ]

    st.divider()
    st.header("Intraday Option-Buying Signal")

    option_signal = get_option_signal(timeframe_results)

    col1, col2, col3, col4 = st.columns(4)

    col1.metric("Overall Signal", option_signal["Signal"])
    col2.metric("Option Type", option_signal["Option Type"])
    col3.metric("Signal Strength", option_signal["Strength"])
    col4.metric("Confluence Score", f"{option_signal['Confluence Score']:+d}")

    st.info(
        "A bullish or bearish signal is a research input, not a guaranteed prediction. "
        "Before considering an option trade, check expiry, implied volatility, theta, liquidity, "
        "bid-ask spread, and your maximum acceptable loss."
    )

    st.divider()
    st.header("Recent Data")

    selected_timeframe = st.selectbox(
        "Show recent data for",
        list(TIMEFRAMES.keys()),
        index=0,
    )

    st.dataframe(
        timeframe_tables[selected_timeframe].style.format("{:,.2f}"),
        use_container_width=True,
    )

except Exception as error:
    st.error(f"Unable to load dashboard data: {error}")
    st.warning(
        "Try selecting another timeframe or refresh the page. "
        "Market-data providers can occasionally delay or restrict intraday index data."
    )

st.divider()
st.caption(
    "For research and educational purposes only. Options involve substantial risk, "
    "including the potential loss of the entire premium paid."
)
