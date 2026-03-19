import streamlit as st
import yfinance as yf
import pandas as pd
import numpy as np

st.set_page_config(page_title="Popstock Watchlist", layout="wide")
st.markdown("""
<style>
.stApp { background-color: #0a0e17; color: #00c9a7; font-family: monospace; }
</style>
""", unsafe_allow_html=True)

st.title("🦞 Popstock Watchlist")

# הגדרת ה-Watchlist הקבוע שלך
DEFAULT_TICKERS = "MU, WDC, MRVL, AXTI, BTC-USD"
tickers_input = st.text_input("Watchlist (comma separated)", DEFAULT_TICKERS).upper()
tickers = [t.strip() for t in tickers_input.split(",")]

def calculate_metrics(ticker):
data = yf.download(ticker, period="1mo", interval="1d", progress=False)
if data.empty: return None
close = data['Close'][ticker]
price = float(close.iloc[-1])
ema21 = float(close.ewm(span=21, adjust=False).mean().iloc[-1])
rsi = float((100 - (100 / (1 + (close.diff().where(close.diff() > 0, 0).rolling(14).mean() / (-close.diff().where(close.diff() < 0, 0).rolling(14).mean()))))).iloc[-1])

# Check Logic
decision = "HOLD"
if price > ema21 and rsi < 65: decision = "BUY"
elif price < ema21 and rsi > 35: decision = "SELL"

return {"Ticker": ticker, "Price": price, "RSI": round(rsi, 1), "Decision": decision, "EMA21": round(ema21, 2)}

# בניית הטבלה
if st.button("Refresh Watchlist"):
results = [calculate_metrics(t) for t in tickers]
df = pd.DataFrame([r for r in results if r])
st.table(df)

# ניתוח מורחב למניה נבחרת
selected = st.selectbox("Select ticker for full checklist", tickers)
if st.button("Show Checklist"):
data = yf.download(selected, period="1mo", interval="1d", progress=False)
# כאן נכנס ה-Checklist הוויזואלי שביקשת
st.write(f"### Confirmation Checklist: {selected}")
ind = calculate_metrics(selected)

# הצגת תנאים עם V
cols = st.columns(2)
cols[0].markdown(f"{'✅' if ind['Price'] > ind['EMA21'] else '⬜'} Trend: Above EMA21")
cols[0].markdown(f"{'✅' if ind['RSI'] < 65 else '⬜'} Momentum: RSI OK")
cols[1].metric("Current Price", f"${ind['Price']:,.2f}")
