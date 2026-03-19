import streamlit as st
import yfinance as yf
import pandas as pd
import numpy as np

st.set_page_config(page_title="Popstock Watchlist", layout="wide")
st.markdown("<style>.stApp { background-color: #0a0e17; color: #00c9a7; font-family: monospace; }</style>", unsafe_allow_html=True)
st.title("🦞 Popstock Watchlist")

def get_data(ticker):
    return yf.download(ticker, period="1mo", interval="1d", progress=False)

def calculate_metrics(ticker):
    data = get_data(ticker)
    if data.empty: return None
    close = data['Close'][ticker]
    price = float(close.iloc[-1])
    ema21 = float(close.ewm(span=21, adjust=False).mean().iloc[-1])
    rsi = float((100 - (100 / (1 + (close.diff().where(close.diff() > 0, 0).rolling(14).mean() / (-close.diff().where(close.diff() < 0, 0).rolling(14).mean()))))).iloc[-1])
    
    decision = "HOLD"
    if price > ema21 and rsi < 65: decision = "BUY"
    elif price < ema21 and rsi > 35: decision = "SELL"
    
    return {"Ticker": ticker, "Price": price, "RSI": round(rsi, 1), "Decision": decision, "EMA21": round(ema21, 2)}

tickers_input = st.text_input("Watchlist (comma separated)", "BTC-USD, MU, SWMR, AXTI, WDC, MRVL").upper()
tickers = [t.strip() for t in tickers_input.split(",")]

if st.button("Analyze Watchlist"):
    results = []
    with st.spinner('Scanning market...'):
        for t in tickers:
            ind = calculate_metrics(t)
            if ind: results.append(ind)
    
    df = pd.DataFrame(results)
    st.table(df)
