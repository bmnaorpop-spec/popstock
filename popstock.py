import yfinance as yf
import pandas as pd
import numpy as np
import argparse
from scipy.signal import argrelextrema

def get_data(ticker):
    # Fetch 1y data to ensure we have enough for SMA and history
    data = yf.download(ticker, period="1y", interval="1d")
    return data

def calculate_indicators(data, ticker):
    close = data['Close'][ticker]
    high = data['High'][ticker]
    low = data['Low'][ticker]
    
    # EMA 21 & SMA 150
    ema21 = float(close.ewm(span=21, adjust=False).mean().iloc[-1])
    sma150 = float(close.rolling(window=150).mean().iloc[-1])
    
    # RSI 14
    delta = close.diff()
    gain = (delta.where(delta > 0, 0)).rolling(window=14).mean()
    loss = (-delta.where(delta < 0, 0)).rolling(window=14).mean()
    rs = gain / loss
    rsi = float((100 - (100 / (1 + rs))).iloc[-1])
    
    # Market Structure
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
    
    # ATR
    tr1 = high - low
    tr2 = (high - close.shift(1)).abs()
    tr3 = (low - close.shift(1)).abs()
    tr = pd.concat([tr1, tr2, tr3], axis=1).max(axis=1)
    atr = float(tr.rolling(window=14).mean().iloc[-1])
    
    return {
        "price": price, "pct_change": pct_change, "ema21": ema21, "sma150": sma150, "rsi": rsi,
        "sup": sup, "res": res, "stop": price - (2 * atr), "target": price + (4 * atr)
    }

def print_card(ticker, indicators):
    price, pct_change = indicators['price'], indicators['pct_change']
    ema21, sma150 = indicators['ema21'], indicators['sma150']
    rsi, sup, res = indicators['rsi'], indicators['sup'], indicators['res']
    stop, tgt = indicators['stop'], indicators['target']
    
    recommendation = "HOLD"
    if price > ema21 and price > sma150 and rsi < 65: recommendation = "BUY"
    elif price < ema21 and price < sma150 and rsi > 35: recommendation = "SELL"
    elif rsi > 70: recommendation = "HOLD (Overbought)"
    elif rsi < 30: recommendation = "HOLD (Oversold)"
        
    print("--------------------------------------------")
    print(f"PATTERN ALERT: {ticker}")
    print("--------------------------------------------")
    print(f"- Price: ${price:,.2f} ({pct_change:+.2f}%) | RSI: {rsi:.1f}")
    print(f"- EMA21: ${ema21:,.2f} | SMA150: ${sma150:,.2f}")
    print(f"- SUP: ${sup:,.2f} | RES: ${res:,.2f}")
    print("--------------------------------------------")
    print(f"TGT: ${tgt:,.2f} | STOP: ${stop:,.2f}")
    print(f"Decision: {recommendation}")
    print("--------------------------------------------")
    print("Strategy: Market Structure + RSI Risk Control")

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
