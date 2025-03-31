# main.py

import time
from gmail_utils import get_new_alerts
from telegram_utils import send_alerts_to_telegram

if __name__ == '__main__':
    print("🔄 Dastur ishga tushdi.")
    while True:
        try:
            alerts = get_new_alerts()
            if alerts:
                send_alerts_to_telegram(alerts)
                print(f"📬 {len(alerts)} ta alert yuborildi.")
            else:
                print("📭 Yangi alert topilmadi.")
        except Exception as e:
            print(f"❗ Kutilmagan xato: {e}")
        time.sleep(10)
