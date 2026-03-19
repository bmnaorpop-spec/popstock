import streamlit as st
import yfinance as yf
import pandas as pd
import numpy as np

st.set_page_config(page_title="Popstock Watchlist", layout="wide")
st.markdown("""
<style>
.stApp { background-color: #0a0e17; color: #00c9a7; font-family: 'Courier New', monospace; }
.metric-label { color: #8892a4; font-size: 14px; font-weight: normal; }
.metric-value { color: #ffffff; font-size: 16px; font-weight: bold; }
</style>
""", unsafe_allow_html=True)

st.title("🦞 Popstock Watchlist")

def render_metric(label, value):
return f'<div style="margin: 4px 0;"><span class="metric-label">{label}:</span> <span class="metric-value">{value}</span></div>'

def calculate_metrics(ticker):
data = yf.download(ticker, period="1mo", interval="1d", progress=False)
if data.empty: return None
close = data['Close'][ticker]
price = float(close.iloc[-1])
prev_close = float(close.iloc[-2])
ema21 = float(close.ewm(span=21, adjust=False).mean().iloc[-1])
sma150 = float(close.rolling(window=150).mean().iloc[-1])
rsi = float((100 - (100 / (1 + (close.diff().where(close.diff() > 0, 0).rolling(14).mean() / (-close.diff().where(close.diff() < 0, 0).rolling(14).mean()))))).iloc[-1])

recent = data.tail(60)
highs, lows = recent['High'][ticker].values, recent['Low'][ticker].values
res = float(highs[highs > price].min()) if len(highs[highs > price]) > 0 else float(recent['High'][ticker].max())
sup = float(lows[lows < price].max()) if len(lows[lows < price]) > 0 else float(recent['Low'][ticker].min())

decision = "HOLD"
if price > ema21 and rsi < 65: decision = "BUY"
elif price < ema21 and rsi > 35: decision = "SELL"

return {
"Ticker": ticker, "Price": price, "Pct": ((price-prev_close)/prev_close)*100,
"RSI": round(rsi, 1), "Decision": decision, "EMA21": round(ema21, 2),
"SMA150": round(sma150, 2), "SUP": round(sup, 2), "RES": round(res, 2)
}

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
st.markdown(render_metric("RSI", res['RSI']), unsafe_allow_html=True)
st.markdown(render_metric("EMA21", f"${res['EMA21']}"), unsafe_allow_html=True)
st.markdown(render_metric("SMA150", f"${res['SMA150']}"), unsafe_allow_html=True)
st.markdown(render_metric("SUP", f"${res['SUP']}"), unsafe_allow_html=True)
st.markdown(render_metric("RES", f"${res['RES']}"), unsafe_allow_html=True)

color = "green" if res['Decision'] == "BUY" else "red" if res['Decision'] == "SELL" else "gray"
st.markdown(f"Decision: **<span style='color:{color}'>{res['Decision']}</span>**", unsafe_allow_html=True)
