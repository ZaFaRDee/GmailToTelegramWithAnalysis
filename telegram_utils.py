# telegram_utils.py

import datetime
from telegram import Bot
from config import TELEGRAM_BOT_TOKEN, TELEGRAM_CHAT_ID
from stock_analysis import get_stock_info, calculate_support_resistance_from_range
from utils import get_tradingview_symbol

def send_alerts_to_telegram(alerts):
    bot = Bot(token=TELEGRAM_BOT_TOKEN)
    for alert in alerts:
        algo_name = alert['algo']
        for ticker in alert['tickers']:
            now = datetime.datetime.now().strftime('%H:%M, %d-%b, %Y')
            tv_symbol = get_tradingview_symbol(ticker)

            try:
                price, rsi, volume = get_stock_info(ticker)
                support, resistance = calculate_support_resistance_from_range(ticker)

                caption = (
                    f"💹 <b>Ticker:</b> #{ticker}\n"
                    f"🧠 <b>Algorithm:</b> #{algo_name}\n"
                    f"--------------------------------\n"
                    f"📈 <b>RSI (14):</b> {rsi}\n"
                    f"📊 <b>Volume:</b> {volume}k\n"
                    f"--------------------------------\n"
                    f"🔽 <b>Resistance Zone:</b> ${resistance}\n"
                    f"💵 <b>Price:</b> ${price:.2f}\n"
                    f"🔼 <b>Support Zone:</b> ${support}\n\n"
                    f"🕒 <b>Time:</b> {now}"
                )

                bot.send_message(chat_id=TELEGRAM_CHAT_ID, text=caption, parse_mode='HTML')
                print(f"✅ {ticker} uchun xabar yuborildi.")

            except Exception as e:
                print(f"❌ {ticker} xatolik: {e}")
                fallback_msg = (
                    f"💹 <b>Ticker:</b> #{ticker}\n"
                    f"🧠 <b>Algorithm:</b> #{algo_name}\n"
                    f"⚠️ Ma’lumot olishda xatolik yuz berdi.\n"
                    f"<a href='https://www.tradingview.com/chart/?symbol={tv_symbol}'>TradingView</a>"
                )
                bot.send_message(chat_id=TELEGRAM_CHAT_ID, text=fallback_msg, parse_mode='HTML')
