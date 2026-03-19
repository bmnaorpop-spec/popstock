import streamlit as st
import yfinance as yf
import pandas as pd
import numpy as np
from scipy.signal import argrelextrema

st.set_page_config(page_title="Popstock Watchlist", layout="wide")
st.markdown("<style>.stApp { background-color: #0a0e17; color: #00c9a7; font-family: monospace; }</style>", unsafe_allow_html=True)
st.title("🦞 Popstock Watchlist")

def calculate_indicators(data, ticker):
if data.empty or ticker not in data['Close'].columns: return None
close = data['Close'][ticker]
# ... (אותה לוגיקה בדיוק מהסקריפט הקודם) ...
ema21 = float(close.ewm(span=21, adjust=False).mean().iloc[-1])
rsi = float((100 - (100 / (1 + (close.diff().where(close.diff() > 0, 0).rolling(14).mean() / (-close.diff().where(close.diff() < 0, 0).rolling(14).mean()))) )).iloc[-1])
price = float(close.iloc[-1])
prev_close = float(close.iloc[-2])
return {"ticker": ticker, "price": price, "pct": ((price-prev_close)/prev_close)*100, "ema21": ema21, "rsi": rsi}

tickers_input = st.text_area("Enter tickers separated by commas", "BTC-USD, MU, SWMR, AXTI, WDC, MRVL")
tickers = [t.strip().upper() for t in tickers_input.split(",")]

if st.button("Analyze Watchlist"):
results = []
with st.spinner('Scanning market...'):
data = yf.download(tickers, period="1y", interval="1d")
for t in tickers:
ind = calculate_indicators(data, t)
if ind: results.append(ind)

# הצגת טבלה מסכמת
df = pd.DataFrame(results)
st.table(df[['ticker', 'price', 'pct', 'rsi', 'ema21']])

# פירוט לכל מניה
for res in results:
with st.expander(f"Details: {res['ticker']}"):
st.metric("Price", f"${res['price']:,.2f}", f"{res['pct']:.2f}%")
st.write(f"RSI: {res['rsi']:.1f} | EMA21: ${res['ema21']:,.2f}")
