import streamlit as st
import yfinance as yf
import pandas as pd
import numpy as np

st.set_page_config(page_title="Popstock Watchlist", layout="wide")
st.markdown("<style>.stApp { background-color: #0a0e17; color: #00c9a7; font-family: monospace; }</style>", unsafe_allow_html=True)

st.title("🦞 Popstock Watchlist")

def get_data(ticker):
    return yf.download(ticker, period="1y", interval="1d", progress=False)

def calculate_metrics(ticker):
    data = get_data(ticker)
    if data.empty: return None
    close = data['Close'][ticker]
    price = float(close.iloc[-1])
    prev_close = float(close.iloc[-2])
    ema21 = float(close.ewm(span=21, adjust=False).mean().iloc[-1])
    rsi = float((100 - (100 / (1 + (close.diff().where(close.diff() > 0, 0).rolling(14).mean() / (-close.diff().where(close.diff() < 0, 0).rolling(14).mean()))))).iloc[-1])
    
    decision = "HOLD"
    if price > ema21 and rsi < 65: decision = "BUY"
    elif price < ema21 and rsi > 35: decision = "SELL"
    
    return {"Ticker": ticker, "Price": price, "Pct": ((price-prev_close)/prev_close)*100, "RSI": round(rsi, 1), "Decision": decision}

tickers_input = st.text_input("Watchlist", "BTC-USD, MU, SWRM, AXTI, WDC, MRVL").upper()
tickers = [t.strip() for t in tickers_input.split(",")]

if st.button("Refresh Watchlist"):
    cols = st.columns(3)
    results = [calculate_metrics(t) for t in tickers]
    
    for i, res in enumerate(results):
        if res:
            with cols[i % 3]:
                with st.container(border=True):
                    st.subheader(res['Ticker'])
                    st.metric("Price", f"${res['Price']:,.2f}", f"{res['Pct']:.2f}%")
                    st.write(f"RSI: {res['RSI']}")
                    color = "green" if res['Decision'] == "BUY" else "red" if res['Decision'] == "SELL" else "gray"
                    st.markdown(f"Decision: **<span style='color:{color}'>{res['Decision']}</span>**", unsafe_allow_html=True)
