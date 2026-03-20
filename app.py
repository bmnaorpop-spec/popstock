import streamlit as st
import yfinance as yf
import pandas as pd
import numpy as np

st.set_page_config(page_title="Popstock Watchlist", layout="wide")
st.markdown("<style>.stApp { background-color: #0a0e17; color: #00c9a7; font-family: monospace; }</style>", unsafe_allow_html=True)

st.title("🦞 Popstock Watchlist")

# אתחול זיכרון - שים לב ששינינו את שם המשתנה כדי להפריד אותו מהווידג'ט עצמו
if 'saved_tickers' not in st.session_state:
    st.session_state['saved_tickers'] = "BTC-USD, MU, SWRM, AXTI, WDC, MRVL"

def calculate_metrics(ticker):
    data = yf.download(ticker, period="1y", interval="1d", progress=False)
    if data.empty: return None
    # התאמת פורמט הנתונים בצורה בטוחה
    close = data['Close'][ticker] if isinstance(data['Close'], pd.DataFrame) else data['Close']
    price = float(close.iloc[-1])
    prev_close = float(close.iloc[-2])
    ema21 = float(close.ewm(span=21, adjust=False).mean().iloc[-1])
    sma150 = float(close.rolling(window=150).mean().iloc[-1]) if len(close) > 150 else 0
    rsi = float((100 - (100 / (1 + (close.diff().where(close.diff() > 0, 0).rolling(14).mean() / (-close.diff().where(close.diff() < 0, 0).rolling(14).mean()))))).iloc[-1])
    
    decision = "HOLD"
    if price > sma150 and rsi < 50: decision = "BUY (Correction Entry)"
    elif rsi > 70: decision = "SELL (Take Profit)"
        
    return {
        "Ticker": ticker, "Price": price, "Pct": ((price-prev_close)/prev_close)*100, 
        "RSI": round(rsi, 1), "Decision": decision, "EMA21": round(ema21, 2),
        "SMA150": round(sma150, 2)
    }

# עוטפים את ה-Input והכפתור בתוך Form
with st.form("watchlist_form"):
    tickers_input = st.text_input("Watchlist", value=st.session_state['saved_tickers']).upper()
    submit_button = st.form_submit_button("Refresh Analysis")

if submit_button:
    # מעדכנים את הזיכרון *רק* כשהמשתמש לחץ על כפתור הרענון
    st.session_state['saved_tickers'] = tickers_input
    
    tickers = [t.strip() for t in tickers_input.split(",") if t.strip()]
    cols = st.columns(3)
    results = [calculate_metrics(t) for t in tickers]
    
    for i, res in enumerate(results):
        if res:
            with cols[i % 3]:
                with st.container(border=True):
                    st.subheader(res['Ticker'])
                    st.metric("Price", f"${res['Price']:,.2f}", f"{res['Pct']:.2f}%")
                    st.write(f"**EMA21:** ${res['EMA21']} | **SMA150:** ${res['SMA150']}")
                    st.write(f"**RSI:** {res['RSI']}")
                    color = "green" if "BUY" in res['Decision'] else "red" if "SELL" in res['Decision'] else "gray"
                    st.markdown(f"Decision: **<span style='color:{color}'>{res['Decision']}</span>**", unsafe_allow_html=True)
