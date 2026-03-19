import streamlit as st
import yfinance as yf
import pandas as pd
import numpy as np
from scipy.signal import argrelextrema

st.set_page_config(page_title="Popstock Watchlist", layout="wide")
st.markdown("<style>.stApp { background-color: #0a0e17; color: #00c9a7; font-family: monospace; }</style>", unsafe_allow_html=True)

st.title("🦞 Popstock Watchlist")

def calculate_metrics(ticker):
    # הורדת נתונים - ניסיון למשוך שנה אחת
    data = yf.download(ticker, period="1y", interval="1d", progress=False)
    if data.empty: return None
    
    # טיפול בנתונים - אם ה-columns הם MultiIndex (במקרה של ריבוי טיקרים) או שטוחים
    close = data['Close']
    if isinstance(close, pd.DataFrame): close = close.iloc[:, 0]
    high = data['High'].iloc[:, 0] if isinstance(data['High'], pd.DataFrame) else data['High']
    low = data['Low'].iloc[:, 0] if isinstance(data['Low'], pd.DataFrame) else data['Low']
    
    price = float(close.iloc[-1])
    prev_close = float(close.iloc[-2])
    ema21 = float(close.ewm(span=21, adjust=False).mean().iloc[-1])
    sma150 = float(close.rolling(window=150).mean().iloc[-1]) if len(close) > 150 else 0
    rsi = float((100 - (100 / (1 + (close.diff().where(close.diff() > 0, 0).rolling(14).mean() / (-close.diff().where(close.diff() < 0, 0).rolling(14).mean()))))).iloc[-1])
    
    recent = data.tail(60)
    highs = recent['High'].iloc[:, 0] if isinstance(recent['High'], pd.DataFrame) else recent['High']
    lows = recent['Low'].iloc[:, 0] if isinstance(recent['Low'], pd.DataFrame) else recent['Low']
    
    peaks = highs.values[argrelextrema(highs.values, np.greater, order=5)[0]]
    valleys = lows.values[argrelextrema(lows, np.less, order=5)[0]]
    
    res = float(peaks[peaks > price].min()) if len(peaks[peaks > price]) > 0 else float(highs.max())
    sup = float(valleys[valleys < price].max()) if len(valleys[valleys < price]) > 0 else float(lows.min())
    
    decision = "HOLD"
    if price > ema21 and price > sma150 and rsi < 65: decision = "BUY"
    elif price < ema21 and rsi > 35: decision = "SELL"
    
    return {
        "Ticker": ticker, "Price": price, "Pct": ((price-prev_close)/prev_close)*100, 
        "RSI": round(rsi, 1), "Decision": decision, "EMA21": round(ema21, 2),
        "SMA150": round(sma150, 2), "SUP": round(sup, 2), "RES": round(res, 2)
    }

tickers_input = st.text_input("Watchlist", "BTC-USD, MU, SWRM, AXTI, WDC, MRVL").upper()
tickers = [t.strip() for t in tickers_input.split(",")]

if st.button("Refresh Watchlist"):
    results = [calculate_metrics(t) for t in tickers]
    cols = st.columns(3)
    for i, res in enumerate(results):
        if res:
            with cols[i % 3]:
                with st.container(border=True):
                    st.subheader(res['Ticker'])
                    st.metric("Price", f"${res['Price']:,.2f}", f"{res['Pct']:.2f}%")
                    st.markdown(f"**RSI:** {res['RSI']} | **EMA21:** ${res['EMA21']}")
                    st.markdown(f"**SUP:** ${res['SUP']} | **RES:** ${res['RES']}")
                    color = "green" if res['Decision'] == "BUY" else "red" if res['Decision'] == "SELL" else "gray"
                    st.markdown(f"Decision: **<span style='color:{color}'>{res['Decision']}</span>**", unsafe_allow_html=True)
