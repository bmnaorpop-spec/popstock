import sys
import yfinance as yf
import pandas as pd
import numpy as np
import json

def analyze_stock(symbol):
    try:
        ticker = yf.Ticker(symbol)
        # Fetch 2 years to ensure we have enough data for 200-day averages and trend analysis
        df = ticker.history(period="2y")
        
        if df.empty:
            return {"error": f"No data found for {symbol}"}

        # --- Indicator Calculations ---
        
        # Exponential Moving Averages (EMAs) - Focus on Shardi/Minervini favorites
        df['EMA10'] = df['Close'].ewm(span=10, adjust=False).mean()
        df['EMA21'] = df['Close'].ewm(span=21, adjust=False).mean() # Shardi's favored short-term
        df['EMA50'] = df['Close'].ewm(span=50, adjust=False).mean()
        
        # Simple Moving Averages (SMAs) - Weinstein/Minervini Stages
        df['SMA150'] = df['Close'].rolling(window=150).mean() # Weinstein Stage
        df['SMA200'] = df['Close'].rolling(window=200).mean()
        
        # RSI (14)
        delta = df['Close'].diff()
        gain = (delta.where(delta > 0, 0)).rolling(window=14).mean()
        loss = (-delta.where(delta < 0, 0)).rolling(window=14).mean()
        rs = gain / loss
        df['RSI'] = 100 - (100 / (1 + rs))
        
        # ATR (Average True Range) - for volatility and Supertrend-like analysis
        high_low = df['High'] - df['Low']
        high_close = np.abs(df['High'] - df['Close'].shift())
        low_close = np.abs(df['Low'] - df['Close'].shift())
        ranges = pd.concat([high_low, high_close, low_close], axis=1)
        true_range = np.max(ranges, axis=1)
        df['ATR'] = true_range.rolling(14).mean()

        latest = df.iloc[-1]
        prev = df.iloc[-2]
        
        # --- Shardi/Weinstein/Minervini Logic ---
        
        # Stage Analysis (Stan Weinstein)
        stage = "Unknown"
        if latest['Close'] > latest['SMA150'] and latest['SMA150'] > latest['SMA200']:
            if latest['SMA200'] > prev['SMA200']:
                stage = "Stage 2 (Advancing)"
            else:
                stage = "Entering Stage 2 / Transitioning"
        elif latest['Close'] < latest['SMA150'] and latest['SMA150'] < latest['SMA200']:
            stage = "Stage 4 (Declining)"
        elif latest['SMA150'] > latest['Close'] and latest['SMA150'] > latest['SMA200']:
            stage = "Stage 3 (Topping)"
        else:
            stage = "Stage 1 (Base/Consolidation)"

        # Mark Minervini's Trend Template (simplified 5/8 criteria)
        minervini_trend = "Failing"
        if (latest['Close'] > latest['EMA50'] and 
            latest['EMA50'] > latest['SMA150'] and 
            latest['SMA150'] > latest['SMA200'] and
            latest['Close'] > latest['SMA200']):
            minervini_trend = "Bullish (Trend Template Active)"

        # Signal Logic
        signals = []
        if latest['Close'] > latest['EMA21'] and prev['Close'] <= prev['EMA21']:
            signals.append("Price crossed above EMA21 (Aggressive Entry)")
        if latest['RSI'] < 30:
            signals.append("Oversold (RSI < 30)")
        if latest['RSI'] > 70:
            signals.append("Overbought (RSI > 70)")
            
        analysis = {
            "symbol": symbol,
            "current_price": round(latest['Close'], 2),
            "change_pct": round(((latest['Close'] - prev['Close']) / prev['Close']) * 100, 2),
            "indicators": {
                "EMA10": round(latest['EMA10'], 2),
                "EMA21": round(latest['EMA21'], 2),
                "EMA50": round(latest['EMA50'], 2),
                "SMA150": round(latest['SMA150'], 2) if not pd.isna(latest['SMA150']) else "N/A",
                "SMA200": round(latest['SMA200'], 2) if not pd.isna(latest['SMA200']) else "N/A",
                "RSI": round(latest['RSI'], 2) if not pd.isna(latest['RSI']) else "N/A",
                "ATR": round(latest['ATR'], 2) if not pd.isna(latest['ATR']) else "N/A"
            },
            "market_structure": {
                "weinstein_stage": stage,
                "minervini_trend": minervini_trend
            },
            "signals": signals,
            "stats": {
                "high_52w": round(df['High'].max(), 2),
                "low_52w": round(df['Low'].min(), 2),
                "dist_from_52w_high": round(((df['High'].max() - latest['Close']) / df['High'].max()) * 100, 2)
            }
        }
        return analysis
    except Exception as e:
        return {"error": str(e)}

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print(json.dumps({"error": "No symbol provided"}))
    else:
        symbol = sys.argv[1].upper()
        result = analyze_stock(symbol)
        print(json.dumps(result))
