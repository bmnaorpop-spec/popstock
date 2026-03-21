import os
from dotenv import load_dotenv
from alpaca.trading.client import TradingClient
from alpaca.trading.requests import MarketOrderRequest
from alpaca.trading.enums import OrderSide, TimeInForce
from popstock import calculate_metrics

# טעינת המפתחות מהקובץ הסודי .env
load_dotenv(".env")
API_KEY = os.getenv('ALPACA_KEY')
SECRET_KEY = os.getenv('ALPACA_SECRET')
# ב-Paper Trading אנחנו משתמשים בכתובת הזו
BASE_URL = 'https://paper-api.alpaca.markets'

client = TradingClient(API_KEY, SECRET_KEY, paper=True)

def execute_trade(ticker, decision):
    side = OrderSide.BUY if 'BUY' in decision else OrderSide.SELL
    try:
        order_data = MarketOrderRequest(
            symbol=ticker,
            qty=1,
            side=side,
            type='market',
            time_in_force=TimeInForce.GTC
        )
        client.submit_order(order_data=order_data)
        print(f"[{ticker}] Successfully executed: {side}")
    except Exception as e:
        print(f"Error executing trade for {ticker}: {e}")

def run_bot(tickers):
    print("Bot started. Scanning...")
    for ticker in tickers:
        metrics = calculate_metrics(ticker)
        if metrics and 'Decision' in metrics:
            print(f"{ticker}: {metrics['Decision']}")
            if "BUY" in metrics['Decision'] or "SELL" in metrics['Decision']:
                execute_trade(ticker, metrics['Decision'])

if __name__ == "__main__":
    # הרשימה החדשה שלך
    tickers = ["EWY", "LITE", "RKLB", "VOYG", "TLA", "LWLG", "ASTS", "MOB", "KTOS", "PLTR"]
    run_bot(tickers)
