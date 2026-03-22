import os
import requests
from dotenv import load_dotenv
from alpaca.trading.client import TradingClient
from alpaca.trading.requests import MarketOrderRequest, LimitOrderRequest
from alpaca.trading.enums import OrderSide, TimeInForce
from popstock import calculate_metrics
import time

# טעינת המפתחות
load_dotenv(".env")
client = TradingClient(os.getenv('ALPACA_KEY'), os.getenv('ALPACA_SECRET'), paper=True)
TELEGRAM_TOKEN = os.getenv('TELEGRAM_BOT_TOKEN')
CHAT_ID = os.getenv('TELEGRAM_CHAT_ID')

def send_telegram(message):
    if TELEGRAM_TOKEN and CHAT_ID:
        url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage?chat_id={CHAT_ID}&text={message}"
        requests.get(url)

def execute_trade(ticker, decision, price, sup):
    side = OrderSide.BUY 
    try:
        # קנייה בתיקון (אגרסיבי ל-5 דקות)
        qty = round(5000 / price, 4)
        order_data = LimitOrderRequest(
            symbol=ticker.replace("-", "/"),
            qty=qty,
            side=side,
            type='limit',
            limit_price=sup, # קונים בתמיכה
            time_in_force=TimeInForce.DAY
        )
        client.submit_order(order_data=order_data)
        
        msg = f"🦞 Scalper Executed: BUY {ticker} @ ${price:,.2f}"
        send_telegram(msg)
        print(msg)
    except Exception as e:
        print(f"Error executing trade for {ticker}: {e}")

def run_crypto_engine():
    # סריקה כל 5 דקות על ה-5 דקות האחרונות
    pairs = ["BTC-USD", "ETH-USD", "SOL-USD", "LINK-USD", "FET-USD"]
    print("🦞 Crypto Hunter [5m Mode] Active...")
    while True:
        for ticker in pairs:
            # משיכת נתונים ב-5 דקות
            metrics = calculate_metrics(ticker, interval="5m")
            if metrics and "BUY" in metrics['Decision']:
                execute_trade(ticker, metrics['Decision'], metrics['Price'], metrics['SUP'], metrics['RSI'])
        time.sleep(300) # סריקה כל 5 דקות

if __name__ == "__main__":
    run_crypto_engine()
