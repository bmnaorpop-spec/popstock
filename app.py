import streamlit as st
import yfinance as yf
import pandas as pd
import numpy as np

st.set_page_config(page_title="Popstock Pro", layout="wide")
st.markdown("<style>.stApp { background-color: #0a0e17; color: #00c9a7; font-family: monospace; }</style>", unsafe_allow_html=True)

st.title("🦞 Popstock Pro: Institutional Analytics")

def calculate_metrics(ticker):
    data = yf.download(ticker, period="1y", interval="1d", progress=False)
    if data.empty: return None
    close = data['Close'][ticker]
    vol = data['Volume'][ticker]
    
    price = float(close.iloc[-1])
    ema21 = float(close.ewm(span=21, adjust=False).mean().iloc[-1])
    
    # MACD
    exp1 = close.ewm(span=12, adjust=False).mean()
    exp2 = close.ewm(span=26, adjust=False).mean()
    macd = float((exp1 - exp2).iloc[-1])
    signal = float((exp1 - exp2).ewm(span=9, adjust=False).mean().iloc[-1])
    
    # Bollinger Bands
    ma20 = close.rolling(20).mean().iloc[-1]
    std20 = close.rolling(20).std().iloc[-1]
    lower_bb = ma20 - (2 * std20)
    
    # Volume Spike
    vol_avg = vol.rolling(20).mean().iloc[-1]
    vol_spike = vol.iloc[-1] > (vol_avg * 1.5)
    
    # Checklist Logic
    checks = {
        "Trend: Price > EMA21": price > ema21,
        "Momentum: MACD > Signal": macd > signal,
        "Volatility: Price > Lower BB": price > lower_bb,
        "Institutional: Volume Spike": vol_spike
    }
    
    return {
        "Ticker": ticker, "Price": price, "EMA21": round(ema21, 2),
        "MACD": round(macd, 2), "Signal": round(signal, 2),
        "VolSpike": vol_spike, "Checks": checks
    }

tickers_input = st.text_input("Watchlist", "BTC-USD, MU, SWRM, AXTI, WDC, MRVL").upper()
tickers = [t.strip() for t in tickers_input.split(",")]

if st.button("Refresh Analysis"):
    cols = st.columns(3)
    results = [calculate_metrics(t) for t in tickers]
    
    for i, res in enumerate(results):
        if res:
            with cols[i % 3]:
                with st.container(border=True):
                    st.subheader(f"{res['Ticker']} {'🔥' if res['VolSpike'] else '⚖️'}")
                    st.metric("Price", f"${res['Price']:,.2f}")
                    st.write(f"MACD: {res['MACD']} | Sig: {res['Signal']}")
                    
                    st.write("### Checklist")
                    c1, c2 = st.columns(2)
                    for idx, (label, passed) in enumerate(res['Checks'].items()):
                        target = c1 if idx < 2 else c2
                        target.markdown(f"{'✅' if passed else '⬜'} {label}")
