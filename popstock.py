import yfinance as yf
import pandas as pd
import numpy as np
from scipy.signal import argrelextrema

def get_data(ticker, interval="1d"):
    period = "1y" if interval == "1d" else "1mo"
    data = yf.download(ticker, period=period, interval=interval, progress=False)
    return data

def calculate_metrics(ticker, interval="1d"):
    data = get_data(ticker, interval)
    if data.empty: return None
    close = data['Close'][ticker]
    price = float(close.iloc[-1])
    prev_close = float(close.iloc[-2])
    ema21 = float(close.ewm(span=21, adjust=False).mean().iloc[-1])
    sma150 = float(close.rolling(window=150).mean().iloc[-1]) if len(close) > 150 else 0
    rsi = float((100 - (100 / (1 + (close.diff().where(close.diff() > 0, 0).rolling(14).mean() / (-close.diff().where(close.diff() < 0, 0).rolling(14).mean()))))).iloc[-1])
    
    decision = "HOLD"
    if interval == "1d":
        if price > sma150 and rsi < 50: decision = "BUY (Correction Entry)"
        elif rsi > 70: decision = "SELL (Take Profit)"
    else:
        if price > ema21 and rsi < 45: decision = "BUY (Aggressive Crypto)"
        elif rsi > 75: decision = "SELL (Take Profit)"
        
    return {
        "Ticker": ticker, "Price": price, "Pct": ((price-prev_close)/prev_close)*100, 
        "RSI": round(rsi, 1), "Decision": decision, "EMA21": round(ema21, 2),
        "SMA150": round(sma150, 2)
    }
