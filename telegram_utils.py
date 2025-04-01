# telegram_utils.py

import os
import datetime
from telegram import Bot
from stock_analysis import get_stock_info, calculate_support_resistance_from_range
from chart_utils import tradingview_chart_only_screenshot
from utils import get_tradingview_symbol
from config import TELEGRAM_BOT_TOKEN, TELEGRAM_CHAT_ID
from fundamental_analysis import get_fundamental_analysis


def send_alerts_to_telegram(alerts):
    bot = Bot(token=TELEGRAM_BOT_TOKEN)

    for alert in alerts:
        algo_name = alert['algo']

        for ticker in alert['tickers']:
            image_path = None
            now = datetime.datetime.now().strftime('%H:%M, %d-%b, %Y')
            tv_symbol = get_tradingview_symbol(ticker)

            try:
                # Asosiy ma'lumotlar
                price, rsi, volume = get_stock_info(ticker)
                support, resistance = calculate_support_resistance_from_range(ticker)
                image_path = tradingview_chart_only_screenshot(ticker)
                # Fundamental tahlil
                fundamental_evals, fundamental_summary = get_fundamental_analysis(ticker)
                # Baholarni Telegram formatda tayyorlash
                details = "\n".join(fundamental_evals.values())

                caption = (
                    f"💹 <b>Ticker:</b> #{ticker}\n"
                    f"🧠 <b>Algorithm:</b> {algo_name}\n"
                    f"--------------------------------\n"
                    f"📈 <b>RSI (14):</b> {rsi}\n"
                    f"📊 <b>Volume:</b> {volume}k\n"
                    f"--------------------------------\n"
                    f"🔽 <b>Resistance Zone:</b> ${resistance}\n"
                    f"💵 <b>Price:</b> ${price:.2f}\n"
                    f"🔼 <b>Support Zone:</b> ${support}\n"
                    f"--------------------------------\n"
                    f"{fundamental_summary}\n"
                    f"{details}\n\n"
                    f"🕒 <b>Time:</b> {now}\n\n"
                    f"<a href='https://www.tradingview.com/chart/?symbol={tv_symbol}'>TradingView</a>"
                )

                if image_path:
                    with open(image_path, 'rb') as photo:
                        bot.send_photo(
                            chat_id=TELEGRAM_CHAT_ID,
                            photo=photo,
                            caption=caption,
                            parse_mode='HTML',
                            timeout=120
                        )
                else:
                    raise Exception("Grafik yuklanmadi")

                print(f"✅ {ticker} haqida grafik bilan xabar yuborildi.")

            except Exception as e:
                print(f"❌ {ticker} xabar yuborishda xato: {e}")

                # Fallback qiymatlar
                try:
                    price_display = f"${float(price):.2f}"
                except:
                    price_display = "?"

                rsi_display = rsi if 'rsi' in locals() else "?"
                vol_display = f"{volume}k" if 'volume' in locals() else "?"
                support_display = support if 'support' in locals() else "?"
                resist_display = resistance if 'resistance' in locals() else "?"

                fallback_message = (
                    f"💹 <b>Ticker:</b> #{ticker}\n"
                    f"🧠 <b>Algorithm:</b> {algo_name}\n"
                    f"--------------------------------\n"
                    f"📈 <b>RSI (14):</b> {rsi}\n"
                    f"📊 <b>Volume:</b> {volume}k\n"
                    f"--------------------------------\n"
                    f"🔽 <b>Resistance Zone:</b> ${resistance}\n"
                    f"💵 <b>Price:</b> ${price:.2f}\n"
                    f"🔼 <b>Support Zone:</b> ${support}\n"
                    f"--------------------------------\n"
                    f"{fundamental_summary}\n"
                    f"{details}\n\n"
                    f"🕒 <b>Time:</b> {now}\n\n"
                    f"⚠️ Grafik mavjud emas, <a href='https://www.tradingview.com/chart/?symbol={tv_symbol}'>TradingView</a>"
                )

                bot.send_message(chat_id=TELEGRAM_CHAT_ID, text=fallback_message, parse_mode='HTML')

            finally:
                if image_path and os.path.exists(image_path):
                    os.remove(image_path)
