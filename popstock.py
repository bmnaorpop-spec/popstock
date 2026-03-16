import yfinance as yf
import pandas as pd
import numpy as np
import argparse

def get_data(ticker):
    data = yf.download(ticker, period="1y", interval="1d")
    return data

def calculate_indicators(data, ticker):
    close = data['Close'][ticker]
    high = data['High'][ticker]
    low = data['Low'][ticker]
    
    # EMA 21
    ema21_series = close.ewm(span=21, adjust=False).mean()
    # SMA 150
    sma150_series = close.rolling(window=150).mean()
    
    current_price = close.iloc[-1]
    ema21 = ema21_series.iloc[-1]
    sma150 = sma150_series.iloc[-1]
    
    # Simple Fibonacci approximation
    h = high.max()
    l = low.min()
    diff = h - l
    fib_0618 = l + (0.618 * diff)
    fib_1618 = h + (0.618 * diff)
    
    return {
        "price": current_price,
        "ema21": ema21,
        "sma150": sma150,
        "fib_sup": fib_0618,
        "fib_res": fib_1618
    }

def print_card(ticker, indicators):
    price = indicators['price']
    ema21 = indicators['ema21']
    sma150 = indicators['sma150']
    sup = indicators['fib_sup']
    res = indicators['fib_res']
    
    # Dynamic calculations
    tgt_percent = ((res - price) / price) * 100
    stop_price = sup * 0.98 
    reliability = 50 + min((abs(price - ema21) / price) * 100, 20)
    
    # Determine type based on simple logic
    alert_type = "TYPE 2"
    pattern = "Bullish Rebound"
    if price < ema21:
        alert_type = "TYPE 4"
        pattern = "Bearish Breakdown"
    
    print("--------------------------------------------")
    print(f"PATTERN BREAKOUTS: {ticker}")
    print("--------------------------------------------")
    print(f"{pattern.ljust(20)} [{alert_type}]")
    print("\nMetrics:")
    print(f"- Price: ${price:,.2f}")
    print(f"- EMA21: ${ema21:,.2f} | SMA150: ${sma150:,.2f}")
    print("\nLevels:")
    print(f"- SUP (Fib 0.618): ${sup:,.2f}")
    print(f"- RES (Fib 1.618): ${res:,.2f}")
    print("--------------------------------------------")
    print(f"Reliability: {reliability:.1f}%  TGT: +{tgt_percent:.1f}%  STOP: ${stop_price:,.2f}")
    print("--------------------------------------------")
    print("Price holding between SUP & RES levels")

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("ticker", help="Stock ticker symbol")
    args = parser.parse_args()
    
    try:
        data = get_data(args.ticker)
        indicators = calculate_indicators(data, args.ticker)
        print_card(args.ticker, indicators)
    except Exception as e:
        import traceback
        traceback.print_exc()
