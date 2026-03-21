import os
import requests
from datetime import datetime
from dotenv import load_dotenv
from alpaca.trading.client import TradingClient
from alpaca.trading.requests import MarketOrderRequest, LimitOrderRequest
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

def send_daily_summary():
    today = datetime.now().strftime('%Y-%m-%d')
    orders = client.get_orders(status='closed', after=today)
    
    msg = "🦞 Popbot Daily Summary:\n"
    if not orders:
        msg += "No trades executed today."
    else:
        for o in orders:
            msg += f"- {o.side.value.upper()} {o.symbol} @ ${o.filled_avg_price}\n"
    
    send_telegram(msg)
    print(msg)

def execute_trade(ticker, decision, price, sup, rsi):
    side = OrderSide.BUY if 'BUY' in decision else OrderSide.SELL
    try:
        if side == OrderSide.BUY:
            is_near_sup = abs(price - sup) / price < 0.05
            limit_price = sup if is_near_sup else price
            qty = round(5000 / price, 4)
            
            order_data = LimitOrderRequest(
                symbol=ticker,
                qty=qty,
                side=side,
                type='limit',
                limit_price=limit_price,
                time_in_force=TimeInForce.DAY
            )
        else:
            qty = 1
            order_data = MarketOrderRequest(
                symbol=ticker,
                qty=qty,
                side=side,
                type='market',
                time_in_force=TimeInForce.DAY
            )
            
        client.submit_order(order_data=order_data)
        msg = f"🦞 Popbot Executed: {side.value.upper()} {ticker} @ ${price:,.2f}"
        send_telegram(msg)
        print(msg)
    except Exception as e:
        err_msg = f"Error executing trade for {ticker}: {e}"
        send_telegram(err_msg)
        print(err_msg)

def run_bot(tickers):
    print("Bot started. Scanning...")
    clock = client.get_clock()
    
    # אם השוק סגור, נשלח סיכום יומי
    if not clock.is_open:
        print("Market closed. Sending summary...")
        send_daily_summary()
        return

    for ticker in tickers:
        metrics = calculate_metrics(ticker)
        if metrics and 'Decision' in metrics:
            print(f"{ticker}: {metrics['Decision']}")
            if "BUY" in metrics['Decision'] or "SELL" in metrics['Decision']:
                execute_trade(ticker, metrics['Decision'], metrics['Price'], metrics['SUP'], metrics['RSI'])

if __name__ == "__main__":
    tickers = ["EWY", "LITE", "RKLB", "VOYG", "TLA", "LWLG", "ASTS", "MOB", "KTOS", "PLTR"]
    run_bot(tickers)
