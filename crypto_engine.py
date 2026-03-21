import os
import time
import requests
from dotenv import load_dotenv
from alpaca.trading.client import TradingClient
from alpaca.trading.requests import MarketOrderRequest
from alpaca.trading.enums import OrderSide, TimeInForce
from popstock import calculate_metrics

# טעינת המפתחות מהקובץ הסודי .env
load_dotenv(".env")
API_KEY = os.getenv('ALPACA_KEY')
SECRET_KEY = os.getenv('ALPACA_SECRET')
TELEGRAM_TOKEN = os.getenv('TELEGRAM_BOT_TOKEN')
CHAT_ID = os.getenv('TELEGRAM_CHAT_ID')

# לקוח Alpaca
client = TradingClient(API_KEY, SECRET_KEY, paper=True)

def send_telegram(message):
    if TELEGRAM_TOKEN and CHAT_ID:
        url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage?chat_id={CHAT_ID}&text={message}"
        requests.get(url)

def execute_trade(ticker, decision, price):
    side = OrderSide.BUY if 'BUY' in decision else OrderSide.SELL
    try:
        order_data = MarketOrderRequest(
            symbol=ticker,
            qty=0.01,
            side=side,
            type='market',
            time_in_force=TimeInForce.GTC
        )
        client.submit_order(order_data=order_data)
        
        # שליחת התראה מפורטת לטלגרם
        msg = f"🦞 Popbot Executed: {side.value.upper()} {ticker} @ ${price:,.2f}"
        send_telegram(msg)
        print(msg)
    except Exception as e:
        err_msg = f"Error executing trade for {ticker}: {e}"
        send_telegram(err_msg)
        print(err_msg)

def run_crypto_engine():
    pairs = ["BTC/USD", "ETH/USD", "SOL/USD"]
    print("🦞 Crypto Hunter Active (24/7) ...")
    while True:
        for ticker in pairs:
            metrics = calculate_metrics(ticker, interval="15m")
            if metrics and "BUY" in metrics['Decision']:
                execute_trade(ticker, metrics['Decision'], metrics['Price'])
                print(f"🦞 Scalping BUY: {ticker}")
        time.sleep(900) # סריקה כל 15 דקות

if __name__ == "__main__":
    run_crypto_engine()
