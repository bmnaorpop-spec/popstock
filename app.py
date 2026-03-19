import streamlit as st
import yfinance as yf
import pandas as pd
import numpy as np
from scipy.signal import argrelextrema

st.set_page_config(page_title="Popstock Terminal", layout="centered")
st.markdown("""
    <style>
    .stApp { background-color: #0a0e17; color: #00c9a7; font-family: monospace; }
    pre { background-color: #0d1421; color: #00c9a7; padding: 20px; border: 1px solid #00c9a7; }
    </style>
""", unsafe_allow_html=True)

st.title("🦞 Popstock Terminal")

def get_data(ticker):
    return yf.download(ticker, period="1y", interval="1d")

def calculate_indicators(data, ticker):
    if data.empty or ticker not in data['Close'].columns: return None
    close = data['Close'][ticker]
    high = data['High'][ticker]
    low = data['Low'][ticker]
    
    ema21 = float(close.ewm(span=21, adjust=False).mean().iloc[-1])
    sma150 = float(close.rolling(window=150).mean().iloc[-1])
    
    delta = close.diff()
    gain = (delta.where(delta > 0, 0)).rolling(window=14).mean()
    loss = (-delta.where(delta < 0, 0)).rolling(window=14).mean()
    rs = gain / loss
    rsi = float((100 - (100 / (1 + rs))).iloc[-1])
    
    recent = data.tail(60)
    highs = recent['High'][ticker].values
    lows = recent['Low'][ticker].values
    peaks = highs[argrelextrema(highs, np.greater, order=5)[0]]
    valleys = lows[argrelextrema(lows, np.less, order=5)[0]]
    
    price = float(close.iloc[-1])
    prev_close = float(close.iloc[-2])
    pct_change = ((price - prev_close) / prev_close) * 100
    
    res = float(peaks[peaks > price].min()) if len(peaks[peaks > price]) > 0 else float(high.max())
    sup = float(valleys[valleys < price].max()) if len(valleys[valleys < price]) > 0 else float(low.min())
    
    return {"price": price, "pct_change": pct_change, "ema21": ema21, "sma150": sma150, "rsi": rsi, "sup": sup, "res": res}

ticker = st.text_input("Enter Ticker (e.g. BTC-USD, MU)", "BTC-USD").upper()

if st.button("Analyze"):
    data = get_data(ticker)
    ind = calculate_indicators(data, ticker)
    if ind is None: st.error("Error fetching data.")
    else:
        st.metric("Price", f"${ind['price']:,.2f}", f"{ind['pct_change']:.2f}%")
        st.write(f"**RSI:** {ind['rsi']:.1f} | **EMA21:** ${ind['ema21']:,.2f}")
        st.write(f"**SUP:** ${ind['sup']:,.2f} | **RES:** ${ind['res']:,.2f}")
        st.line_chart(data['Close'][ticker].tail(30))
