# admin_commands.py

import os
import datetime
from telegram import Update
from telegram.ext import CallbackContext
from stock_analysis import get_stock_info, calculate_support_resistance_from_range
from utils import get_tradingview_symbol

# Admin ID (shaxsiy chatga ruxsat berish uchun)
ADMIN_CHAT_ID = int(os.getenv("ADMIN_CHAT_ID", "0"))

# Bot ishlash vaqti
start_time = datetime.datetime.now()

# Oxirgi alert vaqti
last_alert_time = None

# Monitoring holati
is_paused = False

# Tekshirish oraliq vaqti (sekundda)
check_interval = 10


# ✅ ADMIN CHECK
def is_admin_private(update: Update):
    return (
        update.effective_user.id == ADMIN_CHAT_ID and
        update.effective_chat.type == "private"
    )


# ✅ /ping — bot tirikligini tekshiradi
def ping(update: Update, context: CallbackContext):
    if is_admin_private(update):
        update.message.reply_text("✅ Bot ishlayapti!")


# ✅ /status — umumiy holat haqida
def status(update: Update, context: CallbackContext):
    if is_admin_private(update):
        msg = "📊 Bot ishlayapti.\n"
        msg += f"⏱ Tekshirish oraliq: {check_interval} soniya\n"
        msg += "⏸ Monitoring: OFF" if is_paused else "▶️ Monitoring: ON"
        update.message.reply_text(msg)


# ✅ /uptime — qancha vaqtdan beri ishlayapti
def uptime(update: Update, context: CallbackContext):
    if is_admin_private(update):
        now = datetime.datetime.now()
        uptime_duration = now - start_time
        hours, rem = divmod(uptime_duration.total_seconds(), 3600)
        minutes, seconds = divmod(rem, 60)
        update.message.reply_text(f"🕒 Uptime: {int(hours)} soat {int(minutes)} daqiqa")


# ✅ /info TICKER — asosiy tahliliy info
def info(update: Update, context: CallbackContext):
    if is_admin_private(update):
        if not context.args:
            update.message.reply_text("❗ Ticker kiritilmadi. Misol: /info AAPL")
            return

        ticker = context.args[0].upper()
        try:
            price, rsi, volume = get_stock_info(ticker)
            support, resistance = calculate_support_resistance_from_range(ticker)

            msg = (
                f"💹 Ticker: #{ticker}\n"
                f"📈 RSI (14): {rsi}\n"
                f"💵 Price: ${price:.2f}\n"
                f"📊 Volume: {volume}k\n"
                f"🔽 Resistance Zone: ${resistance}\n"
                f"🔼 Support Zone: ${support}"
            )
            update.message.reply_text(msg)
        except Exception as e:
            update.message.reply_text(f"❌ Ma'lumot olishda xato: {e}")


# ✅ /pause — monitoringni vaqtincha to‘xtatish
def pause(update: Update, context: CallbackContext):
    global is_paused
    if is_admin_private(update):
        is_paused = True
        update.message.reply_text("⏸️ Monitoring vaqtincha to‘xtatildi.")


# ✅ /resume — qayta ishga tushirish
def resume(update: Update, context: CallbackContext):
    global is_paused
    if is_admin_private(update):
        is_paused = False
        update.message.reply_text("▶️ Monitoring qayta ishga tushdi.")


# ✅ /setinterval 30 — tekshirish oraliq vaqtini o‘zgartirish
def setinterval(update: Update, context: CallbackContext):
    global check_interval
    if is_admin_private(update):
        try:
            new_interval = int(context.args[0])
            check_interval = max(5, new_interval)
            update.message.reply_text(f"⏱️ Interval o‘zgartirildi: {check_interval} soniya")
        except:
            update.message.reply_text("❗ Raqam formatida yozing. Misol: /setinterval 30")


# ✅ /lastalert — oxirgi alert qachon bo‘lganini ko‘rsatadi
def lastalert(update: Update, context: CallbackContext):
    if is_admin_private(update):
        if last_alert_time:
            diff = datetime.datetime.now() - last_alert_time
            minutes = diff.seconds // 60
            update.message.reply_text(f"📤 Oxirgi alert: {minutes} daqiqa oldin")
        else:
            update.message.reply_text("🚫 Hali alert yuborilmagan.")


# ✅ /version — dastur versiyasi haqida
def version(update: Update, context: CallbackContext):
    if is_admin_private(update):
        update.message.reply_text("🔖 Versiya: 1.0.0\n🛠 Yangilangan: 2025-03-31")


# ✅ /help — barcha komandalar ro‘yxati
def help_command(update: Update, context: CallbackContext):
    if is_admin_private(update):
        update.message.reply_text("""
🤖 Barcha komandalar ro‘yxati:
/ping – Bot tirikligini tekshirish
/status – Monitoring holatini ko‘rsatish
/uptime – Ish vaqti
/info TICKER – Ticker haqida tahliliy info
/lastalert – Oxirgi signal vaqti
/pause – Monitoringni vaqtincha to‘xtatish
/resume – Monitoringni qayta ishga tushirish
/setinterval X – Tekshirish intervali (soniyada)
/version – Bot versiyasi
/help – Komandalar ro‘yxati
""")


# =============================
# 👉 Monitoring funksiyalar bilan integratsiya qilish uchun:
# =============================

def is_monitoring_paused():
    return is_paused

def get_interval():
    return check_interval

def set_last_alert_time():
    global last_alert_time
    last_alert_time = datetime.datetime.now()
