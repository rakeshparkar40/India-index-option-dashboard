# India Index Option Dashboard

A Streamlit research dashboard for Nifty 50, Bank Nifty, and Sensex.

It analyzes 5-minute, 15-minute, 1-hour, and 4-hour charts using:

- EMA 9, 20, 50, and 200
- RSI 14
- Swing highs and lows
- Support and resistance
- Previous-day high and low
- Session high and low
- Multi-timeframe confluence score
- Intraday Call / Put / Avoid research signal

## Run locally

```bash
python -m venv venv
source venv/bin/activate  # macOS/Linux
# venv\Scripts\activate   # Windows

pip install -r requirements.txt
streamlit run app.py
```

## Deploy on Streamlit Community Cloud

1. Push this repository to GitHub.
2. Create a free Streamlit Community Cloud account.
3. Click **Create app**.
4. Connect your GitHub repository.
5. Select the main branch.
6. Set the main file path to `app.py`.
7. Click **Deploy**.

## Important

This dashboard is for research and educational purposes only. It does not provide guaranteed trading signals. Options can lose value quickly because of directional movement, time decay, volatility changes, liquidity, and spreads.
