# main.py

import time
from telegram.ext import Updater, CommandHandler
from config import TELEGRAM_BOT_TOKEN
from gmail_utils import get_new_alerts
from telegram_utils import send_alerts_to_telegram
from admin_commands import (
    ping, status, uptime, info, pause, resume,
    setinterval, lastalert, version, help_command,
    is_monitoring_paused, get_interval, set_last_alert_time
)

def main():
    print("✅ Bot ishga tushdi...")

    # Telegram Updater yaratamiz
    updater = Updater(token=TELEGRAM_BOT_TOKEN, use_context=True)
    dispatcher = updater.dispatcher

    # === Admin komandalarni ro'yxatdan o'tkazamiz ===
    dispatcher.add_handler(CommandHandler("ping", ping))
    dispatcher.add_handler(CommandHandler("status", status))
    dispatcher.add_handler(CommandHandler("uptime", uptime))
    dispatcher.add_handler(CommandHandler("info", info))
    dispatcher.add_handler(CommandHandler("pause", pause))
    dispatcher.add_handler(CommandHandler("resume", resume))
    dispatcher.add_handler(CommandHandler("setinterval", setinterval))
    dispatcher.add_handler(CommandHandler("lastalert", lastalert))
    dispatcher.add_handler(CommandHandler("version", version))
    dispatcher.add_handler(CommandHandler("help", help_command))

    # Botni komandalar uchun ishga tushuramiz
    updater.start_polling()

    # === Monitoring sikli (Gmail tekshiradi) ===
    while True:
        try:
            if not is_monitoring_paused():
                alerts = get_new_alerts()
                if alerts:
                    send_alerts_to_telegram(alerts)
                    set_last_alert_time()
                    print(f"📤 {len(alerts)} ta alert yuborildi.")
                else:
                    print("📭 Yangi alert topilmadi.")
            else:
                print("⏸ Monitoring vaqtincha to‘xtatilgan.")

        except Exception as e:
            print(f"❗ Kutilmagan xato: {e}")

        time.sleep(get_interval())

    updater.idle()


if __name__ == '__main__':
    main()
